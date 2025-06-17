import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
from collections import defaultdict
import warnings
from sqlalchemy import text, create_engine
warnings.filterwarnings('ignore')

class AprioriRecommender:
    def __init__(self, min_support=0.01, min_confidence=0.3, min_lift=1.0):
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.min_lift = min_lift
        self.frequent_itemsets = None
        self.rules = None
        self.product_mapping = {}
        self.basket_data = None
        
        # Database configuration
        self.basket_host = "localhost"
        self.basket_port = 3309
        self.basket_database = "basketservicedb"
        self.product_host = "localhost"
        self.product_port = 3301
        self.product_database = "productservicedb"
        self.username = "root"
        self.password = "root"
        
    def load_basket_data(self):
        """
        Load basket data from database
        """
        try:
            # Connect to basket database
            basket_connection_string = f"mysql+mysqlconnector://{self.username}:{self.password}@{self.basket_host}:{self.basket_port}/{self.basket_database}"
            basket_engine = create_engine(basket_connection_string)
            
            # Connect to product database
            product_connection_string = f"mysql+mysqlconnector://{self.username}:{self.password}@{self.product_host}:{self.product_port}/{self.product_database}"
            product_engine = create_engine(product_connection_string)
            
            print("📊 Veritabanından sepet verileri yükleniyor...")
            
            # Load basket_product_units data
            basket_query = """
            SELECT 
                bpu.basket_id,
                bpu.product_id,
                bpu.product_name,
                bpu.product_model,
                bpu.product_model_year,
                bpu.product_quantity,
                bpu.product_total_price,
                bpu.product_unit_price,
                b.customer_id,
                b.basket_status_id,
                b.create_date
            FROM basket_product_units bpu
            JOIN baskets b ON bpu.basket_id = b.basket_id
            WHERE b.basket_status_id = 4  -- Only paid baskets
            ORDER BY bpu.basket_id, bpu.product_id
            """
            
            self.basket_data = pd.read_sql(text(basket_query), basket_engine)
            
            print(f"✅ {len(self.basket_data)} adet sepet ürünü yüklendi")
            print(f"✅ {self.basket_data['basket_id'].nunique()} adet sepet bulundu")
            print(f"✅ {self.basket_data['product_name'].nunique()} adet farklı ürün bulundu")
            
            return self.basket_data
            
        except Exception as e:
            print(f"❌ Veri yükleme hatası: {e}")
            return None
        
    def prepare_data(self, df=None):
        """
        Prepare basket data for Apriori algorithm
        Focus on "products bought together in the same basket"
        """
        if df is None:
            df = self.basket_data
            
        if df is None:
            print("❌ Veri bulunamadı! Önce load_basket_data() çağırın.")
            return None, None
        
        print("🔄 Sepet verileri Apriori algoritması için hazırlanıyor...")
        
        # Group products by basket_id (same basket = bought together)
        basket_products = df.groupby('basket_id')['product_name'].apply(list).reset_index()
        
        # Create product mapping for easier reference
        unique_products = df['product_name'].unique()
        self.product_mapping = {i: product for i, product in enumerate(unique_products)}
        
        # Convert to transaction format (each basket is a transaction)
        transactions = basket_products['product_name'].tolist()
        
        print(f"📦 {len(transactions)} adet sepet/transaction hazırlandı")
        
        # Encode transactions
        te = TransactionEncoder()
        te_ary = te.fit(transactions).transform(transactions)
        df_encoded = pd.DataFrame(te_ary, columns=te.columns_)
        
        return df_encoded, transactions
    
    def fit(self, df=None):
        """
        Train the Apriori model based on "products bought together in same basket"
        """
        if df is None:
            df = self.basket_data
            
        if df is None:
            print("❌ Veri bulunamadı! Önce load_basket_data() çağırın.")
            return self
        
        print("🔄 Veriler hazırlanıyor...")
        df_encoded, self.transactions = self.prepare_data(df)
        
        print(f"🎯 Apriori algoritması çalıştırılıyor...")
        print(f"   - Minimum Support: {self.min_support} ({self.min_support*100}%)")
        print(f"   - Minimum Confidence: {self.min_confidence} ({self.min_confidence*100}%)")
        print(f"   - Minimum Lift: {self.min_lift}")
        
        # Run Apriori algorithm
        self.frequent_itemsets = apriori(df_encoded, 
                                       min_support=self.min_support, 
                                       use_colnames=True)
        
        print(f"📊 Frequent Itemsets bulundu: {len(self.frequent_itemsets)}")
        
        # Generate association rules
        self.rules = association_rules(self.frequent_itemsets, 
                                     metric="confidence", 
                                     min_threshold=self.min_confidence)
        
        # Filter by lift
        self.rules = self.rules[self.rules['lift'] >= self.min_lift]
        
        print(f"🔗 Association Rules oluşturuldu: {len(self.rules)}")
        
        # Sort rules by confidence and lift
        self.rules = self.rules.sort_values(['confidence', 'lift'], ascending=[False, False])
        
        return self
    
    def get_recommendations(self, selected_products, top_n=10):
        """
        Get product recommendations based on selected products
        """
        if self.rules is None or len(self.rules) == 0:
            return []
        
        recommendations = []
        
        # Find rules where selected products are in antecedents
        for _, rule in self.rules.iterrows():
            antecedents = list(rule['antecedents'])
            consequents = list(rule['consequents'])
            
            # Check if any selected product is in antecedents
            if any(product in antecedents for product in selected_products):
                # Get products from consequents that are not in selected products
                new_products = [p for p in consequents if p not in selected_products]
                
                for product in new_products:
                    # Check if this product is already recommended
                    existing_rec = next((r for r in recommendations if r['product'] == product), None)
                    
                    if existing_rec is None:
                        # Create new recommendation
                        recommendations.append({
                            'product': product,
                            'confidence': rule['confidence'],
                            'lift': rule['lift'],
                            'support': rule['support'],
                            'antecedents': antecedents,
                            'consequents': consequents,
                            'explanation': f"Bu ürün {', '.join(antecedents)} ile birlikte {rule['confidence']:.1%} olasılıkla satın alınıyor."
                        })
                    else:
                        # Update existing recommendation with higher confidence
                        if rule['confidence'] > existing_rec['confidence']:
                            existing_rec.update({
                                'confidence': rule['confidence'],
                                'lift': rule['lift'],
                                'support': rule['support'],
                                'antecedents': antecedents,
                                'consequents': consequents,
                                'explanation': f"Bu ürün {', '.join(antecedents)} ile birlikte {rule['confidence']:.1%} olasılıkla satın alınıyor."
                            })
        
        # Sort by confidence and return top N
        recommendations.sort(key=lambda x: x['confidence'], reverse=True)
        return recommendations[:top_n]
    
    def get_basket_insights(self):
        """
        Get insights about basket data
        """
        if self.basket_data is None:
            return {}
        
        # Basic statistics
        total_baskets = self.basket_data['basket_id'].nunique()
        total_products = self.basket_data['product_name'].nunique()
        total_transactions = len(self.basket_data)
        
        # Average products per basket
        avg_products_per_basket = total_transactions / total_baskets if total_baskets > 0 else 0
        
        # Basket size distribution
        basket_sizes = self.basket_data.groupby('basket_id').size()
        basket_size_distribution = basket_sizes.value_counts().sort_index().to_dict()
        
        # Most common products
        most_common_products = self.basket_data['product_name'].value_counts().head(10).to_dict()
        
        return {
            'total_baskets': total_baskets,
            'total_products': total_products,
            'total_transactions': total_transactions,
            'avg_products_per_basket': avg_products_per_basket,
            'basket_size_distribution': basket_size_distribution,
            'most_common_products': most_common_products
        }

    def get_popular_combinations(self, top_n=10):
        """
        Get popular product combinations
        """
        if self.frequent_itemsets is None:
            return []
        
        combinations = []
        
        for itemset in self.frequent_itemsets:
            if len(itemset) >= 2:  # Only combinations with 2+ products
                products = list(itemset)
                
                # Calculate support for this itemset
                support = self._calculate_support(itemset)
                frequency = int(support * len(self.basket_data['basket_id'].unique()))
                
                combinations.append({
                    'products': products,
                    'support': support,
                    'frequency': frequency,
                    'explanation': f"Bu {len(products)} ürün {frequency} sepette birlikte bulunuyor."
                })
        
        # Sort by support and return top N
        combinations.sort(key=lambda x: x['support'], reverse=True)
        return combinations[:top_n]

    def get_product_stats(self):
        """
        Get detailed product statistics
        """
        if self.basket_data is None:
            return None
        
        # Group by product and calculate statistics
        product_stats = self.basket_data.groupby('product_name').agg({
            'basket_id': 'nunique',  # Number of baskets containing this product
            'product_quantity': 'sum',  # Total quantity sold
            'product_total_price': 'sum'  # Total revenue
        }).rename(columns={
            'basket_id': 'basket_count',
            'product_quantity': 'total_quantity',
            'product_total_price': 'total_revenue'
        })
        
        # Calculate additional metrics
        total_baskets = self.basket_data['basket_id'].nunique()
        product_stats['basket_percentage'] = (product_stats['basket_count'] / total_baskets) * 100
        product_stats['avg_quantity_per_basket'] = product_stats['total_quantity'] / product_stats['basket_count']
        product_stats['avg_price_per_unit'] = product_stats['total_revenue'] / product_stats['total_quantity']
        
        # Sort by basket count
        product_stats = product_stats.sort_values('basket_count', ascending=False)
        
        return product_stats

    def _calculate_support(self, itemset):
        """
        Calculate support for a given itemset
        """
        if self.basket_data is None:
            return 0
        
        total_baskets = self.basket_data['basket_id'].nunique()
        
        # Count baskets containing all items in the itemset
        baskets_with_itemset = set()
        first_item = True
        
        for item in itemset:
            item_baskets = set(self.basket_data[self.basket_data['product_name'] == item]['basket_id'])
            
            if first_item:
                baskets_with_itemset = item_baskets
                first_item = False
            else:
                baskets_with_itemset = baskets_with_itemset.intersection(item_baskets)
        
        return len(baskets_with_itemset) / total_baskets if total_baskets > 0 else 0

    def _get_subsets(self, products, size):
        """Get all subsets of given size from products list"""
        from itertools import combinations
        return list(combinations(products, size)) 