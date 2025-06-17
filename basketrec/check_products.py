import pandas as pd
from sqlalchemy import text, create_engine

def check_products():
    """Check existing products and identify potential combinations"""
    
    # Database configuration
    product_host = "localhost"
    product_port = 3301
    product_database = "productservicedb"
    username = "root"
    password = "root"
    
    # Connect to product database
    product_connection_string = f"mysql+mysqlconnector://{username}:{password}@{product_host}:{product_port}/{product_database}"
    product_engine = create_engine(product_connection_string)
    
    # Get all products with category info
    products_query = """
    SELECT 
        p.product_id,
        p.product_name,
        p.product_description,
        p.product_price,
        sc.sub_category_name,
        c.category_name
    FROM products p
    LEFT JOIN sub_categories sc ON p.product_sub_category_id = sc.sub_category_id
    LEFT JOIN categories c ON sc.category_id = c.category_id
    ORDER BY p.product_id
    """
    
    products_df = pd.read_sql(text(products_query), product_engine)
    
    print("📱 Mevcut Ürünler:")
    print("=" * 80)
    for _, product in products_df.iterrows():
        print(f"{product['product_id']:2d}. {product['product_name']:<40} | {product['category_name']:<15} | {product['sub_category_name']}")
    
    print("\n🔍 Potansiyel Ürün Kombinasyonları:")
    print("=" * 80)
    
    # Find potential combinations
    combinations = []
    
    # Apple products
    apple_products = products_df[products_df['product_name'].str.contains('iPhone|iPad|MacBook|iMac|Apple', case=False, na=False)]
    apple_accessories = products_df[products_df['product_name'].str.contains('kılıf|kablo|şarj|mouse|pencil|magsafe', case=False, na=False)]
    
    print("🍎 Apple Ürün + Aksesuar Kombinasyonları:")
    for _, main_product in apple_products.iterrows():
        for _, accessory in apple_accessories.iterrows():
            if any(keyword in accessory['product_name'].lower() for keyword in ['iphone', 'ipad', 'macbook', 'apple']):
                combinations.append({
                    'main_product': main_product['product_name'],
                    'accessory': accessory['product_name'],
                    'category': 'Apple'
                })
    
    # Samsung products
    samsung_products = products_df[products_df['product_name'].str.contains('Samsung|Galaxy', case=False, na=False)]
    samsung_accessories = products_df[products_df['product_name'].str.contains('kılıf|kablo|şarj|samsung', case=False, na=False)]
    
    print("\n📱 Samsung Ürün + Aksesuar Kombinasyonları:")
    for _, main_product in samsung_products.iterrows():
        for _, accessory in samsung_accessories.iterrows():
            if any(keyword in accessory['product_name'].lower() for keyword in ['samsung', 'galaxy']):
                combinations.append({
                    'main_product': main_product['product_name'],
                    'accessory': accessory['product_name'],
                    'category': 'Samsung'
                })
    
    # Gaming combinations
    gaming_products = products_df[products_df['product_name'].str.contains('gaming|tuf|rog|victus', case=False, na=False)]
    gaming_accessories = products_df[products_df['product_name'].str.contains('mouse|klavye|kulaklık|monitör', case=False, na=False)]
    
    print("\n🎮 Gaming Ürün + Aksesuar Kombinasyonları:")
    for _, main_product in gaming_products.iterrows():
        for _, accessory in gaming_accessories.iterrows():
            if any(keyword in accessory['product_name'].lower() for keyword in ['gaming', 'tuf', 'rog']):
                combinations.append({
                    'main_product': main_product['product_name'],
                    'accessory': accessory['product_name'],
                    'category': 'Gaming'
                })
    
    # Print combinations
    for combo in combinations[:20]:  # Show first 20 combinations
        print(f"   {combo['main_product']} + {combo['accessory']}")
    
    return products_df, combinations

if __name__ == "__main__":
    check_products() 