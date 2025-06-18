#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from mlxtend.preprocessing import TransactionEncoder
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database configurations
PRODUCT_DB_CONFIG = {
    'host': 'localhost',
    'port': 3301,
    'user': 'root',
    'password': 'root',
    'database': 'productservicedb'
}

BASKET_DB_CONFIG = {
    'host': 'localhost',
    'port': 3309,
    'user': 'root',
    'password': 'root',
    'database': 'basketservicedb'
}

class BasketRecommender:
    def __init__(self):
        self.rules = None
        self.product_mapping = {}
        self.is_fitted = False
    
    def load_data(self):
        """Load basket data from database"""
        try:
            # Connect to basket database
            basket_conn = mysql.connector.connect(**BASKET_DB_CONFIG)
            basket_cursor = basket_conn.cursor()
            
            # Connect to product database
            product_conn = mysql.connector.connect(**PRODUCT_DB_CONFIG)
            product_cursor = product_conn.cursor()
            
            # Get basket product units
            basket_query = """
                SELECT basket_id, product_id, product_quantity, product_unit_price
                FROM basket_product_units
                ORDER BY basket_id
            """
            
            basket_cursor.execute(basket_query)
            basket_data = basket_cursor.fetchall()
            
            if not basket_data:
                logger.warning("No basket data found!")
                return None
            
            # Get product details
            product_ids = [row[1] for row in basket_data if row[1] is not None]
            if not product_ids:
                logger.warning("No product IDs found!")
                return None
            
            # Create placeholders for IN clause
            placeholders = ','.join(['%s'] * len(product_ids))
            product_query = f"""
                SELECT product_id, product_name, product_price, product_model
                FROM products
                WHERE product_id IN ({placeholders})
                AND product_name IS NOT NULL AND product_name != ''
            """
            
            product_cursor.execute(product_query, product_ids)
            product_data = product_cursor.fetchall()
            
            # Create product mapping
            product_map = {row[0]: {'name': row[1], 'price': row[2], 'model': row[3]} for row in product_data}
            
            # Combine data
            combined_data = []
            for basket_row in basket_data:
                basket_id, product_id, quantity, unit_price = basket_row
                if product_id in product_map:
                    product_info = product_map[product_id]
                    combined_data.append({
                        'basket_id': basket_id,
                        'product_name': product_info['name'],
                        'product_price': product_info['price'],
                        'product_model': product_info['model']
                    })
            
            if not combined_data:
                logger.warning("No combined data found!")
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame(combined_data)
            
            logger.info(f"✅ {len(df)} adet sepet ürünü yüklendi")
            logger.info(f"✅ {df['basket_id'].nunique()} adet sepet bulundu")
            logger.info(f"✅ {df['product_name'].nunique()} adet farklı ürün bulundu")
            
            basket_cursor.close()
            basket_conn.close()
            product_cursor.close()
            product_conn.close()
            
            return df
            
        except Exception as e:
            logger.error(f"Veri yükleme hatası: {e}")
            return None
    
    def prepare_data(self, df):
        """Prepare data for Apriori algorithm"""
        try:
            # Group products by basket_id (same basket = bought together)
            basket_products = df.groupby('basket_id')['product_name'].apply(list).reset_index()
            
            # Remove or replace None product names in each basket - more robust cleaning
            def clean_product_names(product_list):
                cleaned = []
                for p in product_list:
                    if p is not None and str(p).strip() != '' and str(p).lower() != 'nan':
                        cleaned.append(str(p).strip())
                return cleaned if cleaned else ['Unknown Product']
            
            basket_products['product_name'] = basket_products['product_name'].apply(clean_product_names)
            
            # Filter out empty baskets
            basket_products = basket_products[basket_products['product_name'].apply(len) > 0]
            
            # Create product mapping for easier reference
            unique_products = df['product_name'].dropna().unique()
            self.product_mapping = {i: product for i, product in enumerate(unique_products)}
            
            # Convert to transaction format (each basket is a transaction)
            transactions = basket_products['product_name'].tolist()
            
            logger.info(f"📦 {len(transactions)} adet sepet/transaction hazırlandı")
            
            return transactions
            
        except Exception as e:
            logger.error(f"Veri hazırlama hatası: {e}")
            return None
    
    def fit(self, min_support=0.02, min_confidence=0.3, min_lift=1.2):
        """Fit the Apriori model"""
        try:
            logger.info("🔄 Veriler hazırlanıyor...")
            
            # Load data
            df = self.load_data()
            if df is None:
                return False
            
            # Prepare transactions
            transactions = self.prepare_data(df)
            if transactions is None:
                return False
            
            logger.info("🔄 Sepet verileri Apriori algoritması için hazırlanıyor...")
            
            # Use TransactionEncoder
            te = TransactionEncoder()
            te_ary = te.fit(transactions).transform(transactions)
            df_encoded = pd.DataFrame(te_ary, columns=te.columns_)
            
            logger.info("🎯 Apriori algoritması çalıştırılıyor...")
            logger.info(f"   - Minimum Support: {min_support} ({min_support*100:.1f}%)")
            logger.info(f"   - Minimum Confidence: {min_confidence} ({min_confidence*100:.1f}%)")
            logger.info(f"   - Minimum Lift: {min_lift}")
            
            # Generate frequent itemsets
            frequent_itemsets = apriori(df_encoded, min_support=min_support, use_colnames=True)
            
            if frequent_itemsets.empty:
                logger.warning("❌ Frequent itemsets bulunamadı!")
                return False
            
            logger.info(f"📊 Frequent Itemsets bulundu: {len(frequent_itemsets)}")
            
            # Generate association rules
            self.rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
            
            # Filter by lift
            self.rules = self.rules[self.rules['lift'] >= min_lift]
            
            if self.rules.empty:
                logger.warning("❌ Association rules bulunamadı!")
                return False
            
            logger.info(f"🔗 Association Rules oluşturuldu: {len(self.rules)}")
            
            self.is_fitted = True
            return True
            
        except Exception as e:
            logger.error(f"Apriori fit hatası: {e}")
            return False
    
    def get_recommendations(self, product_list, top_n=5):
        """Get recommendations for given product list"""
        if not self.is_fitted or self.rules is None:
            logger.error("Model henüz fit edilmemiş!")
            return []
        
        try:
            # Convert product list to frozenset for matching
            input_set = frozenset(product_list)
            
            # Find rules where antecedents match input products
            matching_rules = []
            
            for idx, rule in self.rules.iterrows():
                antecedents = rule['antecedents']
                consequents = rule['consequents']
                
                # Check if input products are subset of antecedents or match exactly
                if input_set.issubset(antecedents) or input_set == antecedents:
                    # Get products that are not in input list
                    new_products = list(consequents - input_set)
                    
                    if new_products:
                        for product in new_products:
                            matching_rules.append({
                                'product': product,
                                'confidence': rule['confidence'],
                                'lift': rule['lift'],
                                'support': rule['support'],
                                'antecedents': list(antecedents),
                                'consequents': list(consequents)
                            })
            
            # Sort by confidence and lift
            matching_rules.sort(key=lambda x: (x['confidence'], x['lift']), reverse=True)
            
            # Remove duplicates and get top N
            seen_products = set()
            unique_recommendations = []
            
            for rule in matching_rules:
                if rule['product'] not in seen_products:
                    seen_products.add(rule['product'])
                    unique_recommendations.append(rule)
                    
                    if len(unique_recommendations) >= top_n:
                        break
            
            return unique_recommendations
            
        except Exception as e:
            logger.error(f"Öneri alma hatası: {e}")
            return []

# Global recommender instance
recommender = BasketRecommender()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'model_fitted': recommender.is_fitted
    })

@app.route('/fit', methods=['POST'])
def fit_model():
    """Fit the Apriori model with custom parameters"""
    try:
        data = request.get_json() or {}
        
        min_support = data.get('min_support', 0.02)
        min_confidence = data.get('min_confidence', 0.3)
        min_lift = data.get('min_lift', 1.2)
        
        success = recommender.fit(min_support, min_confidence, min_lift)
        
        return jsonify({
            'success': success,
            'message': 'Model başarıyla fit edildi' if success else 'Model fit edilemedi',
            'parameters': {
                'min_support': min_support,
                'min_confidence': min_confidence,
                'min_lift': min_lift
            }
        })
        
    except Exception as e:
        logger.error(f"Model fit hatası: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def get_product_details(product_names):
    """Get product details from productservicedb for given product names"""
    conn = mysql.connector.connect(**PRODUCT_DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    if not product_names:
        return []
    format_strings = ','.join(['%s'] * len(product_names))
    query = f"""
        SELECT
            product_id,
            product_description,
            product_image_url,
            product_model,
            product_model_year,
            product_name,
            product_price,
            product_quantity,
            product_sub_category_id
        FROM products
        WHERE product_name IN ({format_strings})
    """
    cursor.execute(query, tuple(product_names))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        products = data.get('products', [])
        top_n = data.get('top_n', 5)
        
        if not recommender.is_fitted:
            return jsonify({'error': 'Model not fitted. Please call /fit endpoint first.'}), 400
        if not products:
            return jsonify({'error': 'No products provided'}), 400
        
        # Get recommendations (list of dicts with 'product', 'confidence', 'lift' keys)
        recommendations = recommender.get_recommendations(products, top_n)
        
        if not recommendations:
            return jsonify({'recommendations': [], 'message': 'No recommendations found for the given products'})
        
        # Create a mapping of product names to recommendation data
        recommendation_map = {}
        for rec in recommendations:
            product_name = rec['product']
            recommendation_map[product_name] = {
                'confidence': rec['confidence'],
                'lift': rec['lift'],
                'support': rec['support'],
                'antecedents': rec['antecedents'],
                'consequents': rec['consequents']
            }
        
        # Get product details
        product_names = list(recommendation_map.keys())
        product_details = get_product_details(product_names)
        
        # Combine product details with recommendation metrics
        enhanced_recommendations = []
        for product in product_details:
            product_name = product['product_name']
            if product_name in recommendation_map:
                rec_data = recommendation_map[product_name]
                enhanced_product = {
                    'product_id': product['product_id'],
                    'product_name': product['product_name'],
                    'product_description': product['product_description'],
                    'product_image_url': product['product_image_url'],
                    'product_model': product['product_model'],
                    'product_model_year': product['product_model_year'],
                    'product_price': product['product_price'],
                    'product_quantity': product['product_quantity'],
                    'product_sub_category_id': product['product_sub_category_id'],
                    'confidence': rec_data['confidence'],
                    'lift': rec_data['lift'],
                    'support': rec_data['support'],
                    'antecedents': rec_data['antecedents'],
                    'consequents': rec_data['consequents']
                }
                enhanced_recommendations.append(enhanced_product)
        
        return jsonify({'recommendations': enhanced_recommendations})
        
    except Exception as e:
        logger.error(f'Recommendation error: {e}')
        return jsonify({'error': str(e)}), 500

@app.route('/products', methods=['GET'])
def get_products():
    """Get all products from productservicedb"""
    try:
        # Connect to product database
        product_conn = mysql.connector.connect(**PRODUCT_DB_CONFIG)
        product_cursor = product_conn.cursor(dictionary=True)
        
        # Get all products with category and subcategory info
        query = """
            SELECT 
                p.product_id,
                p.product_name,
                p.product_price,
                p.product_model,
                c.category_name,
                sc.sub_category_name
            FROM products p
            LEFT JOIN sub_categories sc ON p.product_sub_category_id = sc.sub_category_id
            LEFT JOIN categories c ON sc.category_id = c.category_id
            WHERE p.product_name IS NOT NULL AND p.product_name != ''
            ORDER BY p.product_name
        """
        
        product_cursor.execute(query)
        products = product_cursor.fetchall()
        
        # Convert to list of dictionaries
        product_list = []
        for product in products:
            product_list.append({
                'id': product['product_id'],
                'name': product['product_name'],
                'price': float(product['product_price']) if product['product_price'] else 0.0,
                'model': product['product_model'] or '',
                'category': product['category_name'] or '',
                'subcategory': product['sub_category_name'] or ''
            })
        
        product_cursor.close()
        product_conn.close()
        
        return jsonify({
            'products': product_list,
            'total_count': len(product_list)
        })
        
    except Exception as e:
        logger.error(f"Ürün listesi alma hatası: {e}")
        return jsonify({
            'error': f'Ürün listesi alınamadı: {str(e)}'
        }), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get database statistics"""
    try:
        # Basket stats
        basket_conn = mysql.connector.connect(**BASKET_DB_CONFIG)
        basket_cursor = basket_conn.cursor()
        
        basket_cursor.execute("SELECT COUNT(*) FROM baskets")
        total_baskets = basket_cursor.fetchone()[0]
        
        basket_cursor.execute("SELECT COUNT(*) FROM basket_product_units")
        total_basket_products = basket_cursor.fetchone()[0]
        
        basket_cursor.close()
        basket_conn.close()
        
        # Product stats
        prod_conn = mysql.connector.connect(**PRODUCT_DB_CONFIG)
        prod_cursor = prod_conn.cursor()
        
        prod_cursor.execute("SELECT COUNT(*) FROM products")
        total_products = prod_cursor.fetchone()[0]
        
        prod_cursor.close()
        prod_conn.close()
        
        return jsonify({
            'success': True,
            'statistics': {
                'total_baskets': total_baskets,
                'total_basket_products': total_basket_products,
                'total_products': total_products,
                'model_fitted': recommender.is_fitted,
                'association_rules': len(recommender.rules) if recommender.rules is not None else 0
            }
        })
        
    except Exception as e:
        logger.error(f"İstatistik alma hatası: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Auto-fit model on startup
    logger.info("🚀 Flask API başlatılıyor...")
    logger.info("🔄 Model otomatik olarak fit ediliyor...")
    
    success = recommender.fit()
    if success:
        logger.info("✅ Model başarıyla fit edildi")
    else:
        logger.warning("⚠️ Model fit edilemedi, manuel fit gerekli")
    
    logger.info("🌐 API http://localhost:5000 adresinde çalışıyor")
    app.run(host='0.0.0.0', port=5000, debug=True) 