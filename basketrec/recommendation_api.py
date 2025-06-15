from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sqlalchemy import text, create_engine
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from mlxtend.preprocessing import TransactionEncoder
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database configurations
product_host = "localhost"
product_port = 3301
product_database = "productservicedb"

basket_host = "localhost"
basket_port = 3309
basket_database = "basketservicedb"

username = "root"
password = "root"

def get_recommendations(selected_products, min_support=0.01, min_confidence=0.1):
    """Get recommendations based on selected products"""
    try:
        # Connect to basket database
        basket_engine = create_engine(f"mysql+mysqlconnector://{username}:{password}@{basket_host}:{basket_port}/{basket_database}")
        
        # Connect to product database
        product_engine = create_engine(f"mysql+mysqlconnector://{username}:{password}@{product_host}:{product_port}/{product_database}")
        
        # Get basket data
        query = """
        SELECT bpu.basket_id, bpu.product_name, bpu.product_quantity
        FROM basket_product_units bpu
        JOIN baskets b ON bpu.basket_id = b.basket_id
        WHERE b.basket_status_id = 4
        """
        
        basket_data = pd.read_sql(text(query), basket_engine)
        
        print(f"DEBUG: Found {len(basket_data)} basket records")
        print(f"DEBUG: Selected products: {selected_products}")
        
        if basket_data.empty:
            return {"recommendations": [], "debug": "No basket data found"}
        
        # Use TransactionEncoder like in Streamlit
        basket_products = basket_data.groupby('basket_id')['product_name'].apply(list).reset_index()
        transactions = basket_products['product_name'].tolist()
        
        print(f"DEBUG: Number of transactions: {len(transactions)}")
        print(f"DEBUG: Sample transactions: {transactions[:3]}")
        
        # Encode transactions
        te = TransactionEncoder()
        te_ary = te.fit(transactions).transform(transactions)
        df_encoded = pd.DataFrame(te_ary, columns=te.columns_)
        
        print(f"DEBUG: Encoded dataframe shape: {df_encoded.shape}")
        print(f"DEBUG: Available products: {list(te.columns_)[:10]}")
        
        # Run Apriori algorithm
        frequent_itemsets = apriori(df_encoded, min_support=min_support, use_colnames=True)
        
        print(f"DEBUG: Found {len(frequent_itemsets)} frequent itemsets")
        
        if frequent_itemsets.empty:
            return {"recommendations": [], "debug": "No frequent itemsets found"}
        
        # Generate association rules
        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
        
        print(f"DEBUG: Generated {len(rules)} association rules")
        
        if rules.empty:
            return {"recommendations": [], "debug": "No association rules found"}
        
        # Get all available product names
        all_products = list(te.columns_)
        
        # Collect all recommended product names
        recommended_products = set()
        
        for selected_product in selected_products:
            print(f"DEBUG: Processing selected product: {selected_product}")
            
            # Try exact match first
            product_rules = rules[rules['antecedents'].apply(lambda x: selected_product in x)]
            
            print(f"DEBUG: Found {len(product_rules)} exact match rules")
            
            # If no exact match, try partial matching
            if product_rules.empty:
                # Find products that contain the selected product name
                matching_products = [p for p in all_products if selected_product.lower() in p.lower()]
                print(f"DEBUG: Found {len(matching_products)} partial matches: {matching_products[:5]}")
                
                for matching_product in matching_products:
                    product_rules = rules[rules['antecedents'].apply(lambda x: matching_product in x)]
                    if not product_rules.empty:
                        print(f"DEBUG: Found rules for partial match: {matching_product}")
                        break
            
            for _, rule in product_rules.iterrows():
                consequents = list(rule['consequents'])
                # Remove selected products from recommendations
                consequents = [item for item in consequents if item not in selected_products]
                recommended_products.update(consequents)
        
        print(f"DEBUG: Total recommended products found: {len(recommended_products)}")
        print(f"DEBUG: Recommended products: {list(recommended_products)[:10]}")
        
        # Convert to list and limit to top 20
        recommendations_list = list(recommended_products)[:20]
        
        # If no recommendations, add popular products as fallback
        if not recommendations_list:
            print("DEBUG: No recommendations found, using popular products as fallback")
            product_counts = basket_data['product_name'].value_counts()
            popular_products = product_counts.head(10).index.tolist()
            popular_products = [item for item in popular_products if item not in selected_products]
            recommendations_list = popular_products[:5]
            print(f"DEBUG: Popular products: {recommendations_list}")
        
        # Get detailed product information for recommended products
        if recommendations_list:
            # Use named parameters for SQLAlchemy text IN clause
            placeholders = ','.join([f":name{i}" for i in range(len(recommendations_list))])
            product_query = f"""
            SELECT p.product_id, p.product_name, p.product_price, p.product_description,
                   sc.sub_category_name, c.category_name
            FROM products p
            JOIN sub_categories sc ON p.product_sub_category_id = sc.sub_category_id
            JOIN categories c ON sc.category_id = c.category_id
            WHERE p.product_name IN ({placeholders})
            ORDER BY p.product_name
            """
            params = {f"name{i}": name for i, name in enumerate(recommendations_list)}
            with product_engine.connect() as conn:
                result = conn.execute(text(product_query), params)
                detailed_products = pd.DataFrame(result.fetchall(), columns=result.keys())
            recommendations_with_details = []
            for _, product in detailed_products.iterrows():
                recommendations_with_details.append({
                    'product_id': int(product['product_id']),
                    'product_name': product['product_name'],
                    'product_price': float(product['product_price']),
                    'product_description': product['product_description'],
                    'sub_category_name': product['sub_category_name'],
                    'category_name': product['category_name']
                })
            return {
                'recommendations': recommendations_with_details
            }
        else:
            return {
                'recommendations': []
            }
        
    except Exception as e:
        print(f"DEBUG: Exception occurred: {str(e)}")
        return {"recommendations": [], "debug": f"Error: {str(e)}"}

@app.route('/recommend', methods=['POST'])
def recommend():
    """API endpoint for product recommendations"""
    try:
        data = request.get_json()
        
        if not data or 'products' not in data:
            return jsonify({"error": "No products provided"}), 400
        
        selected_products = data['products']
        
        if not isinstance(selected_products, list) or len(selected_products) == 0:
            return jsonify({"error": "Products must be a non-empty list"}), 400
        
        # Optional parameters
        min_support = data.get('min_support', 0.003)  # Same as Streamlit default
        min_confidence = data.get('min_confidence', 0.03)  # Same as Streamlit default
        
        # Get recommendations
        result = get_recommendations(selected_products, min_support, min_confidence)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Recommendation API is running"})

@app.route('/products', methods=['GET'])
def get_products():
    """Get all available products"""
    try:
        product_engine = create_engine(f"mysql+mysqlconnector://{username}:{password}@{product_host}:{product_port}/{product_database}")
        
        query = """
        SELECT p.product_id, p.product_name, p.product_price, p.product_description,
               sc.sub_category_name, c.category_name
        FROM products p
        JOIN sub_categories sc ON p.product_sub_category_id = sc.sub_category_id
        JOIN categories c ON sc.category_id = c.category_id
        ORDER BY c.category_name, sc.sub_category_name, p.product_name
        """
        
        products = pd.read_sql(text(query), product_engine)
        
        return jsonify({
            'products': products.to_dict('records'),
            'total_products': len(products)
        })
        
    except Exception as e:
        return jsonify({"error": f"Error fetching products: {str(e)}"}), 500

@app.route('/popular-products', methods=['GET'])
def get_popular_products():
    """Get most popular products based on purchase frequency"""
    try:
        # Connect to basket database
        basket_engine = create_engine(f"mysql+mysqlconnector://{username}:{password}@{basket_host}:{basket_port}/{basket_database}")
        
        # Connect to product database
        product_engine = create_engine(f"mysql+mysqlconnector://{username}:{password}@{product_host}:{product_port}/{product_database}")
        
        # Get basket data
        query = """
        SELECT bpu.basket_id, bpu.product_name, bpu.product_quantity
        FROM basket_product_units bpu
        JOIN baskets b ON bpu.basket_id = b.basket_id
        WHERE b.basket_status_id = 4
        """
        
        basket_data = pd.read_sql(text(query), basket_engine)
        
        if basket_data.empty:
            return jsonify({"popular_products": [], "total_products": 0, "message": "No basket data found"})
        
        # Calculate product popularity (purchase frequency)
        product_counts = basket_data['product_name'].value_counts()
        
        # Get top 20 popular products
        top_products = product_counts.head(20).index.tolist()
        
        # Get detailed product information for popular products
        if top_products:
            placeholders = ','.join([f":name{i}" for i in range(len(top_products))])
            product_query = f"""
            SELECT p.product_id, p.product_name, p.product_price, p.product_description,
                   sc.sub_category_name, c.category_name
            FROM products p
            JOIN sub_categories sc ON p.product_sub_category_id = sc.sub_category_id
            JOIN categories c ON sc.category_id = c.category_id
            WHERE p.product_name IN ({placeholders})
            ORDER BY p.product_name
            """
            params = {f"name{i}": name for i, name in enumerate(top_products)}
            
            with product_engine.connect() as conn:
                result = conn.execute(text(product_query), params)
                detailed_products = pd.DataFrame(result.fetchall(), columns=result.keys())
            
            # Add purchase count to each product
            popular_products_with_details = []
            for _, product in detailed_products.iterrows():
                purchase_count = product_counts.get(product['product_name'], 0)
                popular_products_with_details.append({
                    'product_id': int(product['product_id']),
                    'product_name': product['product_name'],
                    'product_price': float(product['product_price']),
                    'product_description': product['product_description'],
                    'sub_category_name': product['sub_category_name'],
                    'category_name': product['category_name'],
                    'purchase_count': int(purchase_count),
                    'popularity_rank': int(product_counts.rank(ascending=False).get(product['product_name'], 0))
                })
            
            # Sort by purchase count (descending)
            popular_products_with_details.sort(key=lambda x: x['purchase_count'], reverse=True)
            
            return jsonify({
                'popular_products': popular_products_with_details,
                'total_products': len(popular_products_with_details),
                'total_baskets': len(basket_data['basket_id'].unique()),
                'total_purchases': len(basket_data)
            })
        else:
            return jsonify({
                'popular_products': [],
                'total_products': 0,
                'message': 'No popular products found'
            })
        
    except Exception as e:
        return jsonify({"error": f"Error fetching popular products: {str(e)}"}), 500

if __name__ == '__main__':
    print("🚀 Starting Recommendation API...")
    print("📊 Available endpoints:")
    print("   - POST /recommend - Get product recommendations")
    print("   - GET /health - Health check")
    print("   - GET /products - Get all products")
    print("   - GET /popular-products - Get most popular products")
    print("🌐 API will be available at: http://localhost:5000")
    
    app.run(host='0.0.0.0', port=5000, debug=True) 