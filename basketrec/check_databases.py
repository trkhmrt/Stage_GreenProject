import pandas as pd
from sqlalchemy import text, create_engine

def check_databases():
    """Check what databases exist and find products table"""
    
    # Database configuration
    host = "localhost"
    port = 3309
    username = "root"
    password = "root"
    
    try:
        # Connect without specifying database
        connection_string = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}"
        engine = create_engine(connection_string)
        
        with engine.connect() as conn:
            # Get all databases
            result = conn.execute(text("SHOW DATABASES"))
            databases = [row[0] for row in result.fetchall()]
            
            print("📊 Available databases:")
            for db in databases:
                print(f"   - {db}")
            
            # Check each database for products table
            print("\n🔍 Searching for products table...")
            for db in databases:
                if db in ['information_schema', 'mysql', 'performance_schema', 'sys']:
                    continue  # Skip system databases
                    
                try:
                    conn.execute(text(f"USE {db}"))
                    result = conn.execute(text("SHOW TABLES"))
                    tables = [row[0] for row in result.fetchall()]
                    
                    if 'products' in tables:
                        print(f"\n✅ Found products table in database: {db}")
                        print(f"   Tables in {db}: {', '.join(tables)}")
                        
                        # Check products table structure
                        structure_query = "DESCRIBE products"
                        structure_result = conn.execute(text(structure_query))
                        structure_rows = structure_result.fetchall()
                        
                        print(f"\n📋 Products table structure in {db}:")
                        for row in structure_rows:
                            print(f"   - {row[0]}: {row[1]} ({row[2]})")
                        
                        # Check sample data
                        sample_query = "SELECT product_id, product_name, product_description FROM products LIMIT 5"
                        sample_result = conn.execute(text(sample_query))
                        sample_rows = sample_result.fetchall()
                        
                        print(f"\n📋 Sample products from {db}:")
                        for row in sample_rows:
                            print(f"   - ID: {row[0]}, Name: {row[1]}, Desc: {row[2][:50]}...")
                        
                        return db
                        
                except Exception as e:
                    print(f"   ⚠️ Could not check {db}: {e}")
            
            print("\n❌ Products table not found in any database!")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    check_databases() 