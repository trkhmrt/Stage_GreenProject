import pandas as pd
from sqlalchemy import text, create_engine

def initialize_basket_statuses():
    """Initialize the basket_statuses table with required status data"""
    
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
        
        print("🔍 Connecting to basket database...")
        
        # Check if basket_statuses table exists
        with basket_engine.connect() as conn:
            # Create table if it doesn't exist
            create_table_query = """
            CREATE TABLE IF NOT EXISTS basket_statuses (
                basket_status_id INT PRIMARY KEY,
                basket_status_name VARCHAR(50) NOT NULL
            )
            """
            conn.execute(text(create_table_query))
            conn.commit()
            print("✅ Basket statuses table created/verified!")
        
        # Define the basket statuses based on BasketStatusName.java
        basket_statuses = [
            (1, 'Aktif'),
            (2, 'Pasif'),
            (3, 'Ödemeye_Hazir'),
            (4, 'Ödendi'),
            (5, 'Iptal'),
            (6, 'Silindi')
        ]
        
        print("📝 Inserting basket statuses...")
        
        with basket_engine.connect() as conn:
            # Clear existing data
            conn.execute(text("DELETE FROM basket_statuses"))
            conn.commit()
            
            # Insert new data
            for status_id, status_name in basket_statuses:
                insert_query = text("""
                    INSERT INTO basket_statuses (basket_status_id, basket_status_name)
                    VALUES (:status_id, :status_name)
                """)
                conn.execute(insert_query, {'status_id': status_id, 'status_name': status_name})
            
            conn.commit()
        
        print("✅ Basket statuses initialized successfully!")
        
        # Verify the data
        print("\n📊 Verifying basket statuses...")
        status_df = pd.read_sql(text("SELECT * FROM basket_statuses ORDER BY basket_status_id"), basket_engine)
        print(status_df.to_string(index=False))
        
        return True
        
    except Exception as e:
        print(f"❌ Error initializing basket statuses: {e}")
        return False

if __name__ == "__main__":
    initialize_basket_statuses() 