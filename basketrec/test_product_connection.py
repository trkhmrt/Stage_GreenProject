import pandas as pd
from sqlalchemy import text, create_engine

def test_connection():
    """Test database connection and get basic product info"""
    
    # Database configuration
    product_host = "localhost"
    product_port = 3301
    product_database = "productservicedb"
    username = "root"
    password = "root"
    
    try:
        # Connect to product database
        product_connection_string = f"mysql+mysqlconnector://{username}:{password}@{product_host}:{product_port}/{product_database}"
        product_engine = create_engine(product_connection_string)
        
        # Test connection
        with product_engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Product database connection successful!")
        
        # Get basic product info
        products_query = """
        SELECT 
            p.product_id,
            p.product_name,
            p.product_price,
            c.category_id,
            c.category_name
        FROM products p
        LEFT JOIN sub_categories sc ON p.product_sub_category_id = sc.sub_category_id
        LEFT JOIN categories c ON sc.category_id = c.category_id
        ORDER BY c.category_id, p.product_id
        LIMIT 20
        """
        
        products_df = pd.read_sql(text(products_query), product_engine)
        
        print(f"\n📦 İlk 20 Ürün:")
        print("=" * 80)
        for _, product in products_df.iterrows():
            print(f"{product['product_id']:3d}. {product['product_name']:<40} | Kategori {product['category_id']}: {product['category_name']}")
        
        # Get category counts
        category_counts = products_df.groupby(['category_id', 'category_name']).size()
        print(f"\n📊 Kategori Dağılımı:")
        print("=" * 40)
        for (cat_id, cat_name), count in category_counts.items():
            print(f"Kategori {cat_id}: {cat_name} - {count} ürün")
        
        return products_df
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return None

if __name__ == "__main__":
    test_connection() 