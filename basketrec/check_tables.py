import pandas as pd
from sqlalchemy import text
from database_config import DatabaseConfig

def check_tables():
    """Check what tables exist in the database"""
    db_config = DatabaseConfig()
    
    if not db_config.test_connection():
        print("❌ Database connection failed!")
        return
    
    try:
        engine = db_config.get_engine()
        
        # Get all tables
        query = "SHOW TABLES"
        df = pd.read_sql(text(query), engine)
        
        print(f"📊 Tables in database '{db_config.database}':")
        for table in df.iloc[:, 0]:
            print(f"   - {table}")
        
        # Check if products table exists
        if 'products' in df.iloc[:, 0].values:
            print("\n✅ Products table exists!")
            
            # Check products table structure
            structure_query = "DESCRIBE products"
            structure_df = pd.read_sql(text(structure_query), engine)
            print("\n📋 Products table structure:")
            print(structure_df.to_string(index=False))
            
        else:
            print("\n❌ Products table does not exist!")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_tables() 