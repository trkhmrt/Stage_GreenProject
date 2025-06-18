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

def add_dell_xps_baskets():
    """Add Dell XPS 15 and Dell wireless mouse to many baskets to increase confidence"""
    try:
        # Get product info
        prod_conn = get_product_connection()
        prod_cursor = prod_conn.cursor()
        
        # Find Dell XPS 15 and Dell wireless mouse
        prod_cursor.execute("""
            SELECT product_id, product_name, product_price, product_model 
            FROM products 
            WHERE (product_name LIKE '%Dell XPS 15%' OR product_name LIKE '%Dell Wireless Mouse%')
            AND product_name IS NOT NULL
        """)
        
        dell_products = prod_cursor.fetchall()
        
        if not dell_products:
            print("❌ Dell XPS 15 veya Dell Wireless Mouse bulunamadı!")
            return
        
        print(f"✅ {len(dell_products)} adet Dell ürünü bulundu:")
        for product in dell_products:
            print(f"   - {product[1]} (ID: {product[0]})")
        
        # Get max basket_id
        basket_conn = get_basket_connection()
        basket_cursor = basket_conn.cursor()
        basket_cursor.execute("SELECT MAX(basket_id) FROM baskets")
        max_basket_id = basket_cursor.fetchone()[0] or 0
        
        # Create new baskets with Dell products
        new_baskets = []
        new_basket_products = []
        
        # Create 500 new baskets with Dell products
        for i in range(500):
            basket_id = max_basket_id + i + 1
            
            new_baskets.append((basket_id,))
            
            # Add 1-2 Dell products to each basket
            num_dell_products = random.randint(1, min(2, len(dell_products)))
            selected_dell_products = random.sample(dell_products, num_dell_products)
            
            for product in selected_dell_products:
                product_id, product_name, product_price, product_model = product
                quantity = random.randint(1, 2)
                unit_price = product_price
                total_price = unit_price * quantity
                product_model_year = None
                new_basket_products.append((
                    basket_id, product_id, product_name, product_model, product_model_year,
                    quantity, unit_price, total_price
                ))
        
        # Insert new baskets
        print(f"🔄 {len(new_baskets)} adet yeni sepet oluşturuluyor...")
        basket_cursor.executemany(
            "INSERT INTO baskets (basket_id) VALUES (%s)",
            new_baskets
        )
        
        # Insert basket products
        print(f"🔄 {len(new_basket_products)} adet sepet ürünü ekleniyor...")
        basket_cursor.executemany("""
            INSERT INTO basket_product_units 
            (basket_id, product_id, product_name, product_model, product_model_year, 
             product_quantity, product_unit_price, product_total_price) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, new_basket_products)
        
        # Create additional baskets with Dell XPS 15 + Dell Wireless Mouse together
        print("🔄 Dell XPS 15 + Dell Wireless Mouse birlikte alınan sepetler oluşturuluyor...")
        
        additional_baskets = []
        additional_basket_products = []
        
        # Create 200 baskets with Dell XPS 15 + Dell Wireless Mouse together
        for i in range(200):
            basket_id = max_basket_id + 500 + i + 1
            
            additional_baskets.append((basket_id,))
            
            # Add ALL Dell products to each basket
            for product in dell_products:
                product_id, product_name, product_price, product_model = product
                quantity = random.randint(1, 2)
                unit_price = product_price
                total_price = unit_price * quantity
                product_model_year = None
                additional_basket_products.append((
                    basket_id, product_id, product_name, product_model, product_model_year,
                    quantity, unit_price, total_price
                ))
        
        # Insert additional baskets
        basket_cursor.executemany(
            "INSERT INTO baskets (basket_id) VALUES (%s)",
            additional_baskets
        )
        
        # Insert additional basket products
        basket_cursor.executemany("""
            INSERT INTO basket_product_units 
            (basket_id, product_id, product_name, product_model, product_model_year, 
             product_quantity, product_unit_price, product_total_price) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, additional_basket_products)
        
        # Commit changes
        basket_conn.commit()
        
        print(f"✅ Toplam {len(new_baskets) + len(additional_baskets)} sepet oluşturuldu")
        print(f"✅ Toplam {len(new_basket_products) + len(additional_basket_products)} sepet ürünü eklendi")
        print("🎯 Dell XPS 15 ve Dell Wireless Mouse confidence değerleri artırıldı!")
        
        # Close connections
        prod_cursor.close()
        prod_conn.close()
        basket_cursor.close()
        basket_conn.close()
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        if 'prod_conn' in locals():
            prod_conn.close()
        if 'basket_conn' in locals():
            basket_conn.close()

if __name__ == "__main__":
    add_dell_xps_baskets() 