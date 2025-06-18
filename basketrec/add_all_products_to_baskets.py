#!/usr/bin/env python3
import mysql.connector
import random
from datetime import datetime, timedelta

# Database configurations
PRODUCT_DB = {
    'host': 'localhost',
    'port': 3301,
    'user': 'root',
    'password': 'root',
    'database': 'productservicedb'
}

BASKET_DB = {
    'host': 'localhost',
    'port': 3309,
    'user': 'root',
    'password': 'root',
    'database': 'basketservicedb'
}

def get_connection(db_config):
    return mysql.connector.connect(**db_config)

def get_new_products():
    """Get newly added products from productservicedb"""
    conn = get_connection(PRODUCT_DB)
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Get products with ID >= 708 (newly added)
        cursor.execute("""
            SELECT product_id, product_name, product_price, product_model, product_model_year
            FROM products 
            WHERE product_id >= 708
            ORDER BY product_id
        """)
        
        products = cursor.fetchall()
        print(f"🆕 {len(products)} yeni ürün bulundu")
        
        return products
        
    except Exception as e:
        print(f"❌ Ürünler alınırken hata: {e}")
        return []
    finally:
        conn.close()

def get_next_id(cursor, table, id_col):
    cursor.execute(f"SELECT MAX({id_col}) FROM {table}")
    result = cursor.fetchone()
    return (result[0] or 0) + 1

def create_comprehensive_baskets():
    """Create baskets with comprehensive product combinations"""
    products = get_new_products()
    
    if not products:
        print("❌ Yeni ürün bulunamadı!")
        return
    
    conn = get_connection(BASKET_DB)
    cursor = conn.cursor()
    
    try:
        next_basket_id = get_next_id(cursor, 'baskets', 'basket_id')
        next_bpu_id = get_next_id(cursor, 'basket_product_units', 'basket_product_unit_id')
        basket_status_ids = [1, 2, 3]
        customer_ids = list(range(1, 21))
        
        # Categorize products
        gaming_products = [p for p in products if any(keyword in p['product_name'].lower() for keyword in ['playstation', 'xbox', 'nintendo', 'gta', 'call of duty', 'mario', 'controller'])]
        computer_products = [p for p in products if any(keyword in p['product_name'].lower() for keyword in ['macbook', 'dell', 'lenovo', 'mouse', 'hub', 'stand'])]
        home_products = [p for p in products if any(keyword in p['product_name'].lower() for keyword in ['philips', 'bosch', 'siemens', 'arçelik', 'beko', 'ikea', 'bellona', 'çilek'])]
        fitness_products = [p for p in products if any(keyword in p['product_name'].lower() for keyword in ['bowflex', 'concept2', 'peloton', 'trek', 'specialized'])]
        audio_products = [p for p in products if any(keyword in p['product_name'].lower() for keyword in ['sony', 'bose', 'jbl'])]
        automotive_products = [p for p in products if any(keyword in p['product_name'].lower() for keyword in ['garmin', 'blackvue', 'carlinkit'])]
        fashion_products = [p for p in products if any(keyword in p['product_name'].lower() for keyword in ['nike', 'adidas', 'puma', 'zara', 'h&m', 'mavi'])]
        
        print(f"📦 Ürün kategorileri:")
        print(f"   🎮 Gaming: {len(gaming_products)} adet")
        print(f"   💻 Computer: {len(computer_products)} adet")
        print(f"   🏠 Home: {len(home_products)} adet")
        print(f"   🏃‍♂️ Fitness: {len(fitness_products)} adet")
        print(f"   🎵 Audio: {len(audio_products)} adet")
        print(f"   🚗 Automotive: {len(automotive_products)} adet")
        print(f"   👕 Fashion: {len(fashion_products)} adet")
        
        # Create logical basket combinations
        basket_combinations = []
        
        # 1. Gaming combinations
        for console in [p for p in gaming_products if 'playstation' in p['product_name'].lower() or 'xbox' in p['product_name'].lower() or 'nintendo' in p['product_name'].lower()]:
            for game in [p for p in gaming_products if 'gta' in p['product_name'].lower() or 'call of duty' in p['product_name'].lower() or 'mario' in p['product_name'].lower()]:
                for controller in [p for p in gaming_products if 'controller' in p['product_name'].lower()]:
                    basket_combinations.append([console, game, controller])
        
        # 2. Computer combinations
        for laptop in [p for p in computer_products if 'macbook' in p['product_name'].lower() or 'dell' in p['product_name'].lower() or 'lenovo' in p['product_name'].lower()]:
            for mouse in [p for p in computer_products if 'mouse' in p['product_name'].lower()]:
                for accessory in [p for p in computer_products if 'hub' in p['product_name'].lower() or 'stand' in p['product_name'].lower()]:
                    basket_combinations.append([laptop, mouse, accessory])
        
        # 3. Home combinations
        for appliance in [p for p in home_products if 'philips' in p['product_name'].lower() or 'bosch' in p['product_name'].lower() or 'siemens' in p['product_name'].lower()]:
            for furniture in [p for p in home_products if 'ikea' in p['product_name'].lower() or 'bellona' in p['product_name'].lower() or 'çilek' in p['product_name'].lower()]:
                basket_combinations.append([appliance, furniture])
        
        # 4. Fitness combinations
        for equipment in [p for p in fitness_products if 'bowflex' in p['product_name'].lower() or 'concept2' in p['product_name'].lower() or 'peloton' in p['product_name'].lower()]:
            for bike in [p for p in fitness_products if 'trek' in p['product_name'].lower() or 'specialized' in p['product_name'].lower()]:
                basket_combinations.append([equipment, bike])
        
        # 5. Audio combinations
        for headphone in [p for p in audio_products if 'sony' in p['product_name'].lower() or 'bose' in p['product_name'].lower()]:
            for speaker in [p for p in audio_products if 'jbl' in p['product_name'].lower()]:
                basket_combinations.append([headphone, speaker])
        
        # 6. Automotive combinations
        for gps in [p for p in automotive_products if 'garmin' in p['product_name'].lower()]:
            for dashcam in [p for p in automotive_products if 'blackvue' in p['product_name'].lower()]:
                for adapter in [p for p in automotive_products if 'carlinkit' in p['product_name'].lower()]:
                    basket_combinations.append([gps, dashcam, adapter])
        
        # 7. Fashion combinations
        for shoes in [p for p in fashion_products if 'nike' in p['product_name'].lower() or 'adidas' in p['product_name'].lower() or 'puma' in p['product_name'].lower()]:
            for clothing in [p for p in fashion_products if 'zara' in p['product_name'].lower() or 'h&m' in p['product_name'].lower() or 'mavi' in p['product_name'].lower()]:
                basket_combinations.append([shoes, clothing])
        
        # 8. Individual product baskets
        for product in products:
            basket_combinations.append([product])
        
        print(f"📋 {len(basket_combinations)} farklı sepet kombinasyonu hazırlandı")
        
        # Create baskets
        for products in basket_combinations:
            basket_id = next_basket_id
            create_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d %H:%M:%S')
            customer_id = random.choice(customer_ids)
            basket_status_id = random.choice(basket_status_ids)
            
            cursor.execute(
                "INSERT INTO baskets (basket_id, create_date, customer_id, basket_status_id) VALUES (%s, %s, %s, %s)",
                (basket_id, create_date, customer_id, basket_status_id)
            )
            
            for product in products:
                quantity = random.randint(1, 2)
                unit_price = float(product['product_price'])
                total_price = unit_price * quantity
                
                cursor.execute(
                    '''INSERT INTO basket_product_units (
                        basket_product_unit_id, product_id, product_model, product_model_year, product_name,
                        product_quantity, product_total_price, product_unit_price, basket_id
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                    (
                        next_bpu_id,
                        product['product_id'],
                        product['product_model'],
                        product['product_model_year'],
                        product['product_name'],
                        quantity,
                        total_price,
                        unit_price,
                        basket_id
                    )
                )
                next_bpu_id += 1
            
            next_basket_id += 1
        
        conn.commit()
        print(f"🎉 {len(basket_combinations)} yeni ürün sepeti başarıyla eklendi!")
        
        # Show summary
        cursor.execute("SELECT COUNT(*) FROM baskets")
        total_baskets = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM basket_product_units")
        total_products = cursor.fetchone()[0]
        
        print(f"\n📈 Genel istatistikler:")
        print(f"   Toplam sepet sayısı: {total_baskets}")
        print(f"   Toplam sepet ürünü: {total_products}")
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    create_comprehensive_baskets() 