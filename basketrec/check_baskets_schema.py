import pandas as pd
from sqlalchemy import text, create_engine

def check_baskets_schema():
    """Check the baskets table schema and sample data"""
    basket_host = "localhost"
    basket_port = 3309
    basket_database = "basketservicedb"
    username = "root"
    password = "root"
    try:
        basket_conn_str = f"mysql+mysqlconnector://{username}:{password}@{basket_host}:{basket_port}/{basket_database}"
        basket_engine = create_engine(basket_conn_str)
        print("🔍 baskets tablosu şeması kontrol ediliyor...")
        schema_query = '''
        SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT, COLUMN_KEY, EXTRA
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = 'basketservicedb' AND TABLE_NAME = 'baskets'
        ORDER BY ORDINAL_POSITION
        '''
        schema_df = pd.read_sql(text(schema_query), basket_engine)
        print(schema_df)
        sample_query = "SELECT * FROM baskets LIMIT 5"
        sample_df = pd.read_sql(text(sample_query), basket_engine)
        print(sample_df)
        return schema_df, sample_df
    except Exception as e:
        print(f"❌ Error: {e}")
        return None, None

if __name__ == "__main__":
    check_baskets_schema() 