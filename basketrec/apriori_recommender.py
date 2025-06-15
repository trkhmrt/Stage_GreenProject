import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

class AprioriRecommender:
    def __init__(self, min_support=0.01, min_confidence=0.5):
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.frequent_itemsets = None
        self.rules = None
        self.product_mapping = {}
        
    def prepare_data(self, df):
        """
        Prepare basket data for Apriori algorithm
        """
        # Group products by basket_id
        basket_products = df.groupby('basket_id')['product_name'].apply(list).reset_index()
        
        # Create product mapping for easier reference
        unique_products = df['product_name'].unique()
        self.product_mapping = {i: product for i, product in enumerate(unique_products)}
        
        # Convert to transaction format
        transactions = basket_products['product_name'].tolist()
        
        # Encode transactions
        te = TransactionEncoder()
        te_ary = te.fit(transactions).transform(transactions)
        df_encoded = pd.DataFrame(te_ary, columns=te.columns_)
        
        return df_encoded, transactions
    
    def fit(self, df):
        """
        Train the Apriori model
        """
        print("Preparing data...")
        df_encoded, self.transactions = self.prepare_data(df)
        
        print("Running Apriori algorithm...")
        self.frequent_itemsets = apriori(df_encoded, 
                                       min_support=self.min_support, 
                                       use_colnames=True)
        
        print("Generating association rules...")
        self.rules = association_rules(self.frequent_itemsets, 
                                     metric="confidence", 
                                     min_threshold=self.min_confidence)
        
        print(f"Found {len(self.frequent_itemsets)} frequent itemsets")
        print(f"Generated {len(self.rules)} association rules")
        
        return self
    
    def get_recommendations(self, products, top_n=10):
        """
        Get product recommendations based on input products
        """
        if self.rules is None:
            return []
        
        recommendations = []
        
        # Strategy 1: Direct association rules
        for _, rule in self.rules.iterrows():
            antecedents = list(rule['antecedents'])
            consequents = list(rule['consequents'])
            
            # Check if any of our products are in antecedents
            if any(product in antecedents for product in products):
                # Get products in consequents that are not in our input
                new_products = [p for p in consequents if p not in products]
                for product in new_products:
                    recommendations.append({
                        'product': product,
                        'confidence': rule['confidence'],
                        'support': rule['support'],
                        'lift': rule['lift'],
                        'antecedents': list(antecedents),
                        'consequents': list(consequents),
                        'type': 'direct_rule'
                    })
        
        # Strategy 2: Partial matches (if we have many products, try subsets)
        if len(products) > 3:
            # Try with subsets of products
            for i in range(len(products) - 1, 0, -1):
                for subset in self._get_subsets(products, i):
                    for _, rule in self.rules.iterrows():
                        antecedents = list(rule['antecedents'])
                        consequents = list(rule['consequents'])
                        
                        if any(product in antecedents for product in subset):
                            new_products = [p for p in consequents if p not in products]
                            for product in new_products:
                                recommendations.append({
                                    'product': product,
                                    'confidence': rule['confidence'] * 0.8,  # Slightly lower confidence for partial matches
                                    'support': rule['support'],
                                    'lift': rule['lift'],
                                    'antecedents': list(antecedents),
                                    'consequents': list(consequents),
                                    'type': 'partial_match'
                                })
        
        # Strategy 3: Category-based recommendations
        category_recommendations = self._get_category_recommendations(products)
        recommendations.extend(category_recommendations)
        
        # Strategy 4: Popular products in same baskets
        popular_recommendations = self._get_popular_in_same_baskets(products)
        recommendations.extend(popular_recommendations)
        
        # Sort by confidence and lift
        recommendations.sort(key=lambda x: (x['confidence'], x['lift']), reverse=True)
        
        # Remove duplicates and return top_n
        seen = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec['product'] not in seen:
                seen.add(rec['product'])
                unique_recommendations.append(rec)
                if len(unique_recommendations) >= top_n:
                    break
        
        return unique_recommendations
    
    def _get_subsets(self, products, size):
        """Get all subsets of given size from products list"""
        from itertools import combinations
        return list(combinations(products, size))
    
    def _get_category_recommendations(self, products, top_n=5):
        """Get recommendations based on product categories"""
        recommendations = []
        
        # Extract categories from product names
        categories = set()
        for product in products:
            if ' - ' in product:
                category = product.split(' - ')[1] if len(product.split(' - ')) > 1 else 'Unknown'
                categories.add(category)
        
        # Find products in same categories
        if self.frequent_itemsets is not None:
            for _, itemset in self.frequent_itemsets.iterrows():
                itemset_products = list(itemset['itemsets'])
                if len(itemset_products) == 1:  # Single products
                    product = itemset_products[0]
                    if ' - ' in product:
                        product_category = product.split(' - ')[1] if len(product.split(' - ')) > 1 else 'Unknown'
                        if product_category in categories and product not in products:
                            recommendations.append({
                                'product': product,
                                'confidence': itemset['support'] * 0.6,  # Lower confidence for category-based
                                'support': itemset['support'],
                                'lift': 1.0,
                                'antecedents': [f"Category: {product_category}"],
                                'consequents': [product],
                                'type': 'category_based'
                            })
        
        return recommendations[:top_n]
    
    def _get_popular_in_same_baskets(self, products, top_n=5):
        """Get popular products that appear in same baskets"""
        recommendations = []
        
        # Find baskets containing our products
        product_baskets = set()
        for product in products:
            # This would need access to original data, so we'll use a simplified approach
            # In a real implementation, you'd query the database
            pass
        
        # For now, return popular single products
        if self.frequent_itemsets is not None:
            single_products = self.frequent_itemsets[self.frequent_itemsets['itemsets'].apply(len) == 1]
            for _, itemset in single_products.head(top_n).iterrows():
                product = list(itemset['itemsets'])[0]
                if product not in products:
                    recommendations.append({
                        'product': product,
                        'confidence': itemset['support'] * 0.5,  # Lower confidence for popular items
                        'support': itemset['support'],
                        'lift': 1.0,
                        'antecedents': ['Popular Product'],
                        'consequents': [product],
                        'type': 'popular_product'
                    })
        
        return recommendations
    
    def get_popular_combinations(self, top_n=10):
        """
        Get most popular product combinations
        """
        if self.frequent_itemsets is None:
            return []
        
        # Sort by support
        popular = self.frequent_itemsets.sort_values('support', ascending=False)
        
        combinations = []
        for _, row in popular.head(top_n).iterrows():
            combinations.append({
                'products': list(row['itemsets']),
                'support': row['support'],
                'frequency': int(row['support'] * len(self.transactions))
            })
        
        return combinations
    
    def get_product_stats(self, df):
        """
        Get basic statistics about products
        """
        stats = df.groupby('product_name').agg({
            'basket_id': 'count',
            'product_quantity': 'sum',
            'product_total_price': 'sum'
        }).rename(columns={
            'basket_id': 'basket_count',
            'product_quantity': 'total_quantity',
            'product_total_price': 'total_revenue'
        })
        
        stats['avg_quantity'] = stats['total_quantity'] / stats['basket_count']
        stats = stats.sort_values('basket_count', ascending=False)
        
        return stats 