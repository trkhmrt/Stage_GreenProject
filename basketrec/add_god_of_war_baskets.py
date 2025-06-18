#!/usr/bin/env python3
import mysql.connector
import random
from datetime import datetime, timedelta

# Database configurations
PRODUCT_DB_CONFIG = {
    'host': 'localhost',
    'port': 3301,
    'user': 'root',
    'password': 'root',
    'database': 'productservicedb'
}

BASKET_DB_CONFIG = {
    'host': 'localhost',
    'port': 3309,
    'user': 'root',
    'password': 'root',
    'database': 'basketservicedb'
}

def get_product_connection():
    return mysql.connector.connect(**PRODUCT_DB_CONFIG)

def get_basket_connection():
    return mysql.connector.connect(**BASKET_DB_CONFIG)

def add_god_of_war_baskets():
    """Add God of War 3 to many baskets to increase confidence"""
    try:
        # Get product info
        prod_conn = get_product_connection()
        prod_cursor = prod_conn.cursor()
        
        # Find God of War 3
        prod_cursor.execute("""
            SELECT product_id, product_name, product_price, product_model, product_model_year 
            FROM products 
            WHERE product_name LIKE '%God of War%' AND product_name LIKE '%3%'
        """)
        god_of_war = prod_cursor.fetchone()
        
        if not god_of_war:
            print("❌ God of War 3 bulunamadı!")
            return
        
        god_of_war_id, god_of_war_name, god_of_war_price, god_of_war_model, god_of_war_year = god_of_war
        print(f"✅ God of War 3 bulundu: {god_of_war_name}")
        
        # Find compatible products (PlayStation games, consoles, accessories)
        prod_cursor.execute("""
            SELECT product_id, product_name, product_price, product_model, product_model_year 
            FROM products 
            WHERE (product_name LIKE '%PlayStation%' OR product_name LIKE '%PS%' OR product_name LIKE '%DualShock%' OR product_name LIKE '%Game%')
            AND product_id != %s
            LIMIT 50
        """, (god_of_war_id,))
        
        compatible_products = prod_cursor.fetchall()
        print(f"✅ {len(compatible_products)} uyumlu ürün bulundu")
        
        # Get existing basket IDs
        basket_conn = get_basket_connection()
        basket_cursor = basket_conn.cursor()
        
        basket_cursor.execute("SELECT MAX(basket_id) FROM baskets")
        max_basket_id = basket_cursor.fetchone()[0] or 0
        
        # Create new baskets with God of War 3
        new_baskets = []
        new_basket_products = []
        
        # Create 200 new baskets with God of War 3
        for i in range(200):
            basket_id = max_basket_id + i + 1
            basket_date = datetime.now() - timedelta(days=random.randint(1, 365))
            
            new_baskets.append((basket_id, basket_date))
            
            # Add God of War 3 to every basket
            quantity = random.randint(1, 2)
            unit_price = god_of_war_price
            total_price = unit_price * quantity
            
            new_basket_products.append((
                basket_id, god_of_war_id, god_of_war_name, god_of_war_model, god_of_war_year,
                quantity, unit_price, total_price
            ))
            
            # Add 1-3 compatible products to each basket
            num_companions = random.randint(1, 3)
            selected_companions = random.sample(compatible_products, min(num_companions, len(compatible_products)))
            
            for companion in selected_companions:
                comp_id, comp_name, comp_price, comp_model, comp_year = companion
                comp_quantity = random.randint(1, 2)
                comp_unit_price = comp_price
                comp_total_price = comp_unit_price * comp_quantity
                
                new_basket_products.append((
                    basket_id, comp_id, comp_name, comp_model, comp_year,
                    comp_quantity, comp_unit_price, comp_total_price
                ))
        
        # Insert new baskets
        basket_cursor.executemany("""
            INSERT INTO baskets (basket_id, basket_date) 
            VALUES (%s, %s)
        """, new_baskets)
        
        # Insert basket products
        basket_cursor.executemany("""
            INSERT INTO basket_product_units 
            (basket_id, product_id, product_name, product_model, product_model_year, 
             product_quantity, product_unit_price, product_total_price) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, new_basket_products)
        
        basket_conn.commit()
        
        print(f"✅ {len(new_baskets)} yeni sepet oluşturuldu")
        print(f"✅ {len(new_basket_products)} sepet ürünü eklendi")
        print(f"🎮 God of War 3 artık {len(new_baskets)} sepette bulunuyor!")
        
        prod_cursor.close()
        prod_conn.close()
        basket_cursor.close()
        basket_conn.close()
        
    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    add_god_of_war_baskets() 