import pandas as pd
from sqlalchemy import text, create_engine

def check_products_table_schema():
    """Check the products table schema and see all columns"""
    
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
        
        print("🔍 Products tablosu şeması kontrol ediliyor...")
        
        # Get table schema information
        schema_query = """
        SELECT 
            COLUMN_NAME,
            DATA_TYPE,
            IS_NULLABLE,
            COLUMN_DEFAULT,
            COLUMN_KEY,
            EXTRA
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = 'productservicedb' 
        AND TABLE_NAME = 'products'
        ORDER BY ORDINAL_POSITION
        """
        
        schema_df = pd.read_sql(text(schema_query), product_engine)
        
        print(f"📊 Products tablosu sütunları ({len(schema_df)} sütun):")
        print("=" * 80)
        print(f"{'Sütun Adı':<25} {'Veri Tipi':<15} {'Null':<8} {'Varsayılan':<12} {'Key':<8} {'Extra':<10}")
        print("-" * 80)
        
        for _, column in schema_df.iterrows():
            print(f"{column['COLUMN_NAME']:<25} {column['DATA_TYPE']:<15} {column['IS_NULLABLE']:<8} {str(column['COLUMN_DEFAULT']):<12} {column['COLUMN_KEY']:<8} {column['EXTRA']:<10}")
        
        # Get sample data to see actual values
        print(f"\n📦 Örnek ürün verileri (ilk 5 kayıt):")
        print("=" * 80)
        
        sample_query = """
        SELECT * FROM products LIMIT 5
        """
        
        sample_df = pd.read_sql(text(sample_query), product_engine)
        
        # Display column names
        print("Sütunlar:", list(sample_df.columns))
        print()
        
        # Display sample data
        for idx, row in sample_df.iterrows():
            print(f"Ürün {idx + 1}:")
            for col in sample_df.columns:
                print(f"  {col}: {row[col]}")
            print()
        
        # Check for specific columns that might be null
        print("🔍 Null değer kontrolü:")
        print("=" * 40)
        
        null_check_query = """
        SELECT 
            COUNT(*) as total_products,
            SUM(CASE WHEN product_name IS NULL THEN 1 ELSE 0 END) as null_product_name,
            SUM(CASE WHEN product_description IS NULL THEN 1 ELSE 0 END) as null_description,
            SUM(CASE WHEN product_price IS NULL THEN 1 ELSE 0 END) as null_price,
            SUM(CASE WHEN product_quantity IS NULL THEN 1 ELSE 0 END) as null_quantity
        FROM products
        """
        
        null_stats = pd.read_sql(text(null_check_query), product_engine)
        print(f"Toplam ürün: {null_stats.iloc[0]['total_products']}")
        print(f"Null product_name: {null_stats.iloc[0]['null_product_name']}")
        print(f"Null description: {null_stats.iloc[0]['null_description']}")
        print(f"Null price: {null_stats.iloc[0]['null_price']}")
        print(f"Null quantity: {null_stats.iloc[0]['null_quantity']}")
        
        return schema_df, sample_df
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None, None

if __name__ == "__main__":
    check_products_table_schema() 