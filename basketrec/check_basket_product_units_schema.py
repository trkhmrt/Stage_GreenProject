import pandas as pd
from sqlalchemy import text, create_engine

def check_basket_product_units_schema():
    """Check the basket_product_units table schema and sample data"""
    
    # Database configuration
    basket_host = "localhost"
    basket_port = 3309
    basket_database = "basketservicedb"
    username = "root"
    password = "root"
    
    try:
        # Connect to basket database
        basket_connection_string = f"mysql+mysqlconnector://{username}:{password}@{basket_host}:{basket_port}/{basket_database}"
        basket_engine = create_engine(basket_connection_string)
        
        print("🔍 basket_product_units tablosu şeması kontrol ediliyor...")
        
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
        WHERE TABLE_SCHEMA = 'basketservicedb' 
        AND TABLE_NAME = 'basket_product_units'
        ORDER BY ORDINAL_POSITION
        """
        
        schema_df = pd.read_sql(text(schema_query), basket_engine)
        print(schema_df)
        
        # Get sample data
        sample_query = "SELECT * FROM basket_product_units LIMIT 5"
        sample_df = pd.read_sql(text(sample_query), basket_engine)
        print(sample_df)
        
        return schema_df, sample_df
    except Exception as e:
        print(f"❌ Error: {e}")
        return None, None

if __name__ == "__main__":
    check_basket_product_units_schema() 