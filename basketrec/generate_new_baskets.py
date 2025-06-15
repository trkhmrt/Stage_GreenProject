import pandas as pd
from sqlalchemy import text, create_engine
import random
from datetime import datetime, timedelta

def generate_new_baskets():
    """Generate new basket data using the newly created products"""
    
    # Database configurations
    basket_host = "localhost"
    basket_port = 3309
    basket_database = "basketservicedb"
    
    product_host = "localhost"
    product_port = 3301
    product_database = "productservicedb"
    
    username = "root"
    password = "root"
    
    try:
        # Connect to products database
        product_connection_string = f"mysql+mysqlconnector://{username}:{password}@{product_host}:{product_port}/{product_database}"
        product_engine = create_engine(product_connection_string)
        
        # Connect to basket database
        basket_connection_string = f"mysql+mysqlconnector://{username}:{password}@{basket_host}:{basket_port}/{basket_database}"
        basket_engine = create_engine(basket_connection_string)
        
        print("🔍 Getting products data...")
        
        # Get all products with category info
        products_query = """
        SELECT 
            p.product_id,
            p.product_name,
            p.product_description,
            p.product_price,
            p.product_quantity,
            sc.sub_category_name,
            c.category_name
        FROM products p
        LEFT JOIN sub_categories sc ON p.product_sub_category_id = sc.sub_category_id
        LEFT JOIN categories c ON sc.category_id = c.category_id
        ORDER BY p.product_id
        """
        
        products_df = pd.read_sql(text(products_query), product_engine)
        print(f"📊 Found {len(products_df)} products")
        
        # Clear existing basket data
        print("\n🗑️ Clearing existing basket data...")
        with basket_engine.connect() as conn:
            conn.execute(text("DELETE FROM basket_product_units"))
            conn.execute(text("DELETE FROM baskets"))
            conn.commit()
        print("✅ Existing basket data cleared!")
        
        # Generate new baskets
        print("\n🔄 Generating new baskets...")
        
        baskets = []
        basket_product_units = []
        basket_id = 1
        
        # Generate 500-1000 baskets
        num_baskets = random.randint(500, 1000)
        
        for i in range(num_baskets):
            # Generate basket
            customer_id = random.randint(1, 100)
            basket_status_id = random.choice([1, 4])  # 1: Active, 4: Completed
            create_date = datetime.now() - timedelta(days=random.randint(0, 30))
            
            baskets.append({
                'basket_id': basket_id,
                'customer_id': customer_id,
                'basket_status_id': basket_status_id,
                'create_date': create_date
            })
            
            # Generate 2-8 products per basket
            num_products = random.randint(2, 8)
            selected_products = products_df.sample(n=num_products)
            
            for _, product in selected_products.iterrows():
                quantity = random.randint(1, 5)
                unit_price = product['product_price']
                total_price = unit_price * quantity
                
                basket_product_units.append({
                    'basket_id': basket_id,
                    'product_id': product['product_id'],
                    'product_name': product['product_name'],
                    'product_quantity': quantity,
                    'product_total_price': total_price,
                    'product_unit_price': unit_price
                })
            
            basket_id += 1
        
        print(f"📊 Created {len(baskets)} baskets with {len(basket_product_units)} product units")
        
        # Insert baskets
        print("\n💾 Inserting baskets...")
        with basket_engine.connect() as conn:
            for basket in baskets:
                insert_basket_query = text("""
                    INSERT INTO baskets 
                    (basket_id, customer_id, basket_status_id, create_date)
                    VALUES (:basket_id, :customer_id, :basket_status_id, :create_date)
                """)
                conn.execute(insert_basket_query, basket)
            
            conn.commit()
        print("✅ Baskets inserted!")
        
        # Insert basket product units in chunks
        print("\n💾 Inserting basket product units...")
        chunk_size = 100
        
        with basket_engine.connect() as conn:
            for i in range(0, len(basket_product_units), chunk_size):
                chunk = basket_product_units[i:i+chunk_size]
                
                for unit in chunk:
                    insert_unit_query = text("""
                        INSERT INTO basket_product_units 
                        (basket_id, product_id, product_name, product_quantity, product_total_price, product_unit_price)
                        VALUES (:basket_id, :product_id, :product_name, :product_quantity, :product_total_price, :product_unit_price)
                    """)
                    conn.execute(insert_unit_query, unit)
                
                conn.commit()
                print(f"   Inserted chunk {i//chunk_size + 1}/{(len(basket_product_units) + chunk_size - 1)//chunk_size}")
        
        print("✅ All basket product units inserted!")
        
        # Verify the results
        print("\n📊 Verifying results...")
        
        # Check basket count
        basket_count_query = "SELECT COUNT(*) as basket_count FROM baskets"
        basket_count_result = pd.read_sql(text(basket_count_query), basket_engine)
        basket_count = basket_count_result.iloc[0]['basket_count']
        
        # Check product unit count
        unit_count_query = "SELECT COUNT(*) as unit_count FROM basket_product_units"
        unit_count_result = pd.read_sql(text(unit_count_query), basket_engine)
        unit_count = unit_count_result.iloc[0]['unit_count']
        
        # Check unique products used
        unique_products_query = "SELECT COUNT(DISTINCT product_id) as unique_products FROM basket_product_units"
        unique_products_result = pd.read_sql(text(unique_products_query), basket_engine)
        unique_products = unique_products_result.iloc[0]['unique_products']
        
        # Check basket size distribution
        basket_sizes_query = """
        SELECT 
            basket_id,
            COUNT(*) as product_count
        FROM basket_product_units
        GROUP BY basket_id
        ORDER BY product_count DESC
        LIMIT 10
        """
        basket_sizes_result = pd.read_sql(text(basket_sizes_query), basket_engine)
        
        print(f"\n📊 Final Statistics:")
        print(f"   - Total baskets: {basket_count}")
        print(f"   - Total product units: {unit_count}")
        print(f"   - Unique products used: {unique_products}")
        print(f"   - Average products per basket: {unit_count/basket_count:.2f}")
        
        print(f"\n📋 Top 10 largest baskets:")
        print(basket_sizes_result.to_string(index=False))
        
        # Show sample data
        sample_query = """
        SELECT 
            bpu.basket_id,
            bpu.product_name,
            bpu.product_quantity,
            bpu.product_total_price
        FROM basket_product_units bpu
        ORDER BY bpu.basket_id, bpu.product_id
        LIMIT 15
        """
        sample_result = pd.read_sql(text(sample_query), basket_engine)
        
        print(f"\n📋 Sample basket data:")
        print(sample_result.to_string(index=False))
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    generate_new_baskets() 