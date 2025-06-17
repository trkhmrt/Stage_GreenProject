import pandas as pd
from sqlalchemy import text, create_engine

def check_product_database():
    """Check what's in the product database"""
    
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
        
        print("🔍 Product veritabanına bağlanılıyor...")
        
        # Test connection
        with product_engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Bağlantı başarılı!")
        
        # Check if products table exists
        tables_query = "SHOW TABLES"
        tables_df = pd.read_sql(text(tables_query), product_engine)
        print(f"\n📋 Veritabanındaki tablolar:")
        for _, table in tables_df.iterrows():
            print(f"   - {table.iloc[0]}")
        
        # Check products table
        if 'products' in tables_df.values:
            print("\n📦 Products tablosu kontrol ediliyor...")
            
            # Count products
            count_query = "SELECT COUNT(*) as count FROM products"
            count_result = pd.read_sql(text(count_query), product_engine)
            product_count = count_result.iloc[0]['count']
            print(f"   Toplam ürün sayısı: {product_count}")
            
            if product_count > 0:
                # Get sample products
                sample_query = "SELECT * FROM products LIMIT 10"
                sample_df = pd.read_sql(text(sample_query), product_engine)
                print(f"\n📱 Örnek ürünler:")
                for _, product in sample_df.iterrows():
                    print(f"   {product['product_id']}. {product['product_name']} - {product['product_price']} TL")
            else:
                print("   ❌ Products tablosunda ürün bulunamadı!")
                
                # Check if we need to insert sample data
                print("\n🔧 Örnek ürün verileri eklenmeli mi?")
                
        else:
            print("❌ Products tablosu bulunamadı!")
        
        # Check categories
        if 'categories' in tables_df.values:
            print("\n📂 Categories tablosu kontrol ediliyor...")
            categories_query = "SELECT * FROM categories"
            categories_df = pd.read_sql(text(categories_query), product_engine)
            print(f"   Toplam kategori sayısı: {len(categories_df)}")
            
            if len(categories_df) > 0:
                print("   Kategoriler:")
                for _, category in categories_df.iterrows():
                    print(f"     - {category['category_id']}: {category['category_name']}")
        
        # Check sub_categories
        if 'sub_categories' in tables_df.values:
            print("\n📂 Sub_categories tablosu kontrol ediliyor...")
            sub_categories_query = "SELECT * FROM sub_categories LIMIT 10"
            sub_categories_df = pd.read_sql(text(sub_categories_query), product_engine)
            print(f"   Toplam alt kategori sayısı: {len(sub_categories_df)}")
            
            if len(sub_categories_df) > 0:
                print("   Örnek alt kategoriler:")
                for _, sub_category in sub_categories_df.iterrows():
                    print(f"     - {sub_category['sub_category_id']}: {sub_category['sub_category_name']}")
        
        return product_engine
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        return None

if __name__ == "__main__":
    check_product_database() 