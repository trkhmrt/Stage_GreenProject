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

def add_gears_of_war_baskets():
    """Add Gears of War series games to many baskets to increase confidence"""
    try:
        # Get product info
        prod_conn = get_product_connection()
        prod_cursor = prod_conn.cursor()
        
        # Find Gears of War games
        prod_cursor.execute("""
            SELECT product_id, product_name, product_price, product_model, product_model_year 
            FROM products 
            WHERE product_name LIKE '%Gears of War%'
        """)
        gears_games = prod_cursor.fetchall()
        
        if not gears_games:
            print("❌ Gears of War oyunları bulunamadı!")
            return
        
        print(f"✅ {len(gears_games)} Gears of War oyunu bulundu:")
        for game in gears_games:
            print(f"   - {game[1]} (ID: {game[0]})")
        
        # Find compatible products (Xbox games, consoles, accessories)
        prod_cursor.execute("""
            SELECT product_id, product_name, product_price, product_model, product_model_year 
            FROM products 
            WHERE (product_name LIKE '%Xbox%' OR product_name LIKE '%Game%' OR product_name LIKE '%Controller%')
            AND product_id NOT IN ({})
            LIMIT 50
        """.format(','.join([str(game[0]) for game in gears_games])))
        
        compatible_products = prod_cursor.fetchall()
        print(f"✅ {len(compatible_products)} uyumlu ürün bulundu")
        
        # Get existing basket IDs
        basket_conn = get_basket_connection()
        basket_cursor = basket_conn.cursor()
        
        basket_cursor.execute("SELECT MAX(basket_id) FROM baskets")
        max_basket_id = basket_cursor.fetchone()[0] or 0
        
        # Create new baskets with Gears of War games
        new_baskets = []
        new_basket_products = []
        
        # Create 300 new baskets with Gears of War games
        for i in range(300):
            basket_id = max_basket_id + i + 1
            
            new_baskets.append((basket_id,))
            
            # Add 1-3 Gears of War games to each basket
            num_gears_games = random.randint(1, min(3, len(gears_games)))
            selected_gears_games = random.sample(gears_games, num_gears_games)
            
            for game in selected_gears_games:
                game_id, game_name, game_price, game_model, game_year = game
                quantity = random.randint(1, 2)
                unit_price = game_price
                total_price = unit_price * quantity
                
                new_basket_products.append((
                    basket_id, game_id, game_name, game_model, game_year,
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
            INSERT INTO baskets (basket_id) 
            VALUES (%s)
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
        print(f"🎮 Gears of War oyunları artık {len(new_baskets)} sepette bulunuyor!")
        
        # Create additional baskets with all Gears of War games together
        print("🔄 Gears of War serisi birlikte alınan sepetler oluşturuluyor...")
        
        additional_baskets = []
        additional_basket_products = []
        
        # Create 100 baskets with all Gears of War games together
        for i in range(100):
            basket_id = max_basket_id + 300 + i + 1
            
            additional_baskets.append((basket_id,))
            
            # Add ALL Gears of War games to each basket
            for game in gears_games:
                game_id, game_name, game_price, game_model, game_year = game
                quantity = random.randint(1, 2)
                unit_price = game_price
                total_price = unit_price * quantity
                
                additional_basket_products.append((
                    basket_id, game_id, game_name, game_model, game_year,
                    quantity, unit_price, total_price
                ))
            
            # Add 1-2 compatible products
            num_companions = random.randint(1, 2)
            selected_companions = random.sample(compatible_products, min(num_companions, len(compatible_products)))
            
            for companion in selected_companions:
                comp_id, comp_name, comp_price, comp_model, comp_year = companion
                comp_quantity = random.randint(1, 2)
                comp_unit_price = comp_price
                comp_total_price = comp_unit_price * comp_quantity
                
                additional_basket_products.append((
                    basket_id, comp_id, comp_name, comp_model, comp_year,
                    comp_quantity, comp_unit_price, comp_total_price
                ))
        
        # Insert additional baskets
        basket_cursor.executemany("""
            INSERT INTO baskets (basket_id) 
            VALUES (%s)
        """, additional_baskets)
        
        # Insert additional basket products
        basket_cursor.executemany("""
            INSERT INTO basket_product_units 
            (basket_id, product_id, product_name, product_model, product_model_year, 
             product_quantity, product_unit_price, product_total_price) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, additional_basket_products)
        
        basket_conn.commit()
        
        print(f"✅ {len(additional_baskets)} ek sepet oluşturuldu (tüm Gears of War oyunları birlikte)")
        print(f"✅ {len(additional_basket_products)} ek sepet ürünü eklendi")
        print(f"🎮 Toplam {len(new_baskets) + len(additional_baskets)} sepet oluşturuldu!")
        
        prod_cursor.close()
        prod_conn.close()
        basket_cursor.close()
        basket_conn.close()
        
    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    add_gears_of_war_baskets() 