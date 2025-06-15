import pandas as pd
from sqlalchemy import text, create_engine

def check_products():
    """Check products table for duplicate descriptions"""
    
    # Products database configuration
    host = "localhost"
    port = 3301  # Products database port
    database = "productservicedb"  # Products database
    username = "root"
    password = "root"
    
    try:
        # Connect to products database
        connection_string = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}"
        engine = create_engine(connection_string)
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Products database connection successful!")
        
        # Get all products
        query = """
        SELECT 
            product_id,
            product_name,
            product_description,
            product_price,
            product_sub_category_id
        FROM products 
        ORDER BY product_id
        """
        
        df = pd.read_sql(text(query), engine)
        
        print(f"📊 Total products: {len(df)}")
        print(f"📊 Unique product names: {df['product_name'].nunique()}")
        print(f"📊 Unique descriptions: {df['product_description'].nunique()}")
        
        # Check for duplicate descriptions
        duplicate_descriptions = df[df.duplicated(['product_description'], keep=False)]
        
        if len(duplicate_descriptions) > 0:
            print(f"\n⚠️  Found {len(duplicate_descriptions)} products with duplicate descriptions:")
            print("\nDuplicate descriptions:")
            for desc in duplicate_descriptions['product_description'].unique():
                products_with_desc = df[df['product_description'] == desc]
                print(f"\n📝 Description: '{desc}'")
                print(f"   Products with this description:")
                for _, product in products_with_desc.iterrows():
                    print(f"   - ID: {product['product_id']}, Name: {product['product_name']}")
        else:
            print("\n✅ No duplicate descriptions found!")
        
        # Show sample of products
        print(f"\n📋 Sample of products:")
        print(df.head(10).to_string(index=False))
        
        return df
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    check_products() 