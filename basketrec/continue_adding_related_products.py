#!/usr/bin/env python3
import mysql.connector
import random
from datetime import datetime, timedelta

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 3309,
    'user': 'root',
    'password': 'root',
    'database': 'basketservicedb'
}

# Add product DB config
PRODUCT_DB_CONFIG = {
    'host': 'localhost',
    'port': 3301,
    'user': 'root',
    'password': 'root',
    'database': 'productservicedb'
}

def get_db_connection():
    """Create database connection"""
    return mysql.connector.connect(**DB_CONFIG)

def get_product_db_connection():
    return mysql.connector.connect(**PRODUCT_DB_CONFIG)

def get_products_by_category(product_cursor, category_id):
    """Get products by category from productservicedb"""
    query = """
    SELECT p.product_id, p.product_name, p.product_model, p.product_model_year, p.product_price
    FROM products p
    JOIN sub_categories sc ON p.product_sub_category_id = sc.sub_category_id
    JOIN categories c ON sc.category_id = c.category_id
    WHERE c.category_id = %s AND p.product_model IS NOT NULL AND p.product_model_year IS NOT NULL
    """
    product_cursor.execute(query, (category_id,))
    return product_cursor.fetchall()

def get_existing_baskets(cursor):
    """Get existing baskets"""
    query = "SELECT basket_id, customer_id, basket_status_id FROM baskets WHERE basket_status_id IN (1, 4)"
    cursor.execute(query)
    return cursor.fetchall()

def create_new_baskets(cursor, customer_count=50):
    """Create new baskets for customers"""
    # Generate customer IDs (assuming they exist in customer table)
    customer_ids = list(range(1, customer_count + 1))
    
    baskets_created = []
    for i in range(customer_count):
        customer_id = random.choice(customer_ids)
        basket_status = random.choice([1, 4])  # 1: active, 4: paid
        created_date = datetime.now() - timedelta(days=random.randint(1, 365))
        
        query = """
        INSERT INTO baskets (customer_id, basket_status, created_date, updated_date)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (customer_id, basket_status, created_date, created_date))
        basket_id = cursor.lastrowid
        baskets_created.append(basket_id)
    
    return baskets_created

def add_phone_case_combinations(cursor, baskets, product_cursor):
    """Add phone-case combinations"""
    print("📱 Telefon-kılıf kombinasyonları ekleniyor...")
    
    # Get phones and cases
    phones = get_products_by_category(product_cursor, 1)  # phones
    cases = get_products_by_category(product_cursor, 32)  # cases
    
    if not phones or not cases:
        print("❌ Telefon veya kılıf bulunamadı")
        return 0
    
    added_count = 0
    
    for basket_id in random.sample(baskets, min(30, len(baskets))):
        phone = random.choice(phones)
        
        # Find compatible cases for this phone
        compatible_cases = []
        for case in cases:
            # Match by model
            if (phone[3] and case[3] and phone[3].lower() in case[2].lower()) or \
               (phone[2] and case[2] and phone[2].lower() in case[2].lower()):
                compatible_cases.append(case)
        
        if compatible_cases:
            case = random.choice(compatible_cases)
            quantity = random.randint(1, 2)
            
            # Add phone
            query = """
            INSERT INTO basket_product_units 
            (basket_id, product_id, product_name, product_model, product_model_year, 
             product_unit_price, product_quantity, created_date, updated_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                basket_id, phone[0], phone[1], phone[2], phone[3], 
                phone[4], quantity, datetime.now(), datetime.now()
            ))
            
            # Add case
            cursor.execute(query, (
                basket_id, case[0], case[1], case[2], case[3], 
                case[4], quantity, datetime.now(), datetime.now()
            ))
            
            added_count += 2
    
    print(f"✅ {added_count} telefon-kılıf kombinasyonu eklendi")
    return added_count

def add_console_game_combinations(cursor, baskets, product_cursor):
    """Add console-game combinations"""
    print("🎮 Konsol-oyun kombinasyonları ekleniyor...")
    
    # Get consoles and games
    consoles = get_products_by_category(product_cursor, 33)  # gaming consoles
    games = get_products_by_category(product_cursor, 34)  # games
    
    if not consoles or not games:
        print("❌ Konsol veya oyun bulunamadı")
        return 0
    
    added_count = 0
    
    for basket_id in random.sample(baskets, min(40, len(baskets))):
        console = random.choice(consoles)
        
        # Find compatible games for this console
        compatible_games = []
        for game in games:
            # Match by platform
            if (console[2].lower() in game[2].lower()) or \
               (game[2].lower() in console[2].lower()):
                compatible_games.append(game)
        
        if compatible_games:
            # Add 2-4 games per console
            selected_games = random.sample(compatible_games, min(3, len(compatible_games)))
            
            # Add console
            query = """
            INSERT INTO basket_product_units 
            (basket_id, product_id, product_name, product_model, product_model_year, 
             product_unit_price, product_quantity, created_date, updated_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                basket_id, console[0], console[1], console[2], console[3], 
                console[4], 1, datetime.now(), datetime.now()
            ))
            
            # Add games
            for game in selected_games:
                cursor.execute(query, (
                    basket_id, game[0], game[1], game[2], game[3], 
                    game[4], 1, datetime.now(), datetime.now()
                ))
            
            added_count += 1 + len(selected_games)
    
    print(f"✅ {added_count} konsol-oyun kombinasyonu eklendi")
    return added_count

def add_accessory_combinations(cursor, baskets, product_cursor):
    """Add accessory combinations"""
    print("🎧 Aksesuar kombinasyonları ekleniyor...")
    
    # Get accessories (headphones, chargers, etc.)
    accessories = get_products_by_category(product_cursor, 35)  # accessories
    
    if not accessories:
        print("❌ Aksesuar bulunamadı")
        return 0
    
    added_count = 0
    
    for basket_id in random.sample(baskets, min(20, len(baskets))):
        # Add 2-3 accessories per basket
        selected_accessories = random.sample(accessories, min(3, len(accessories)))
        
        query = """
        INSERT INTO basket_product_units 
        (basket_id, product_id, product_name, product_model, product_model_year, 
         product_unit_price, product_quantity, created_date, updated_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        for accessory in selected_accessories:
            cursor.execute(query, (
                basket_id, accessory[0], accessory[1], accessory[2], accessory[3], 
                accessory[4], random.randint(1, 2), datetime.now(), datetime.now()
            ))
        
        added_count += len(selected_accessories)
    
    print(f"✅ {added_count} aksesuar kombinasyonu eklendi")
    return added_count

def add_brand_family_combinations(cursor, baskets, product_cursor):
    """Add products from same brand family"""
    print("🏷️ Marka ailesi kombinasyonları ekleniyor...")
    
    # Get all products with brands
    query = """
    SELECT product_id, product_name, product_model, product_model_year, product_price
    FROM products 
    WHERE product_model IS NOT NULL AND product_model_year IS NOT NULL
    """
    product_cursor.execute(query)
    all_products = product_cursor.fetchall()
    
    # Group by model
    model_groups = {}
    for product in all_products:
        model = product[2]
        if model not in model_groups:
            model_groups[model] = []
        model_groups[model].append(product)
    
    added_count = 0
    
    for basket_id in random.sample(baskets, min(25, len(baskets))):
        # Choose a random model
        model = random.choice(list(model_groups.keys()))
        model_products = model_groups[model]
        
        if len(model_products) >= 2:
            # Add 2-3 products from same model
            selected_products = random.sample(model_products, min(3, len(model_products)))
            
            query = """
            INSERT INTO basket_product_units 
            (basket_id, product_id, product_name, product_model, product_model_year, 
             product_unit_price, product_quantity, created_date, updated_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            for product in selected_products:
                cursor.execute(query, (
                    basket_id, product[0], product[1], product[2], product[3], 
                    product[4], random.randint(1, 2), datetime.now(), datetime.now()
                ))
            
            added_count += len(selected_products)
    
    print(f"✅ {added_count} marka ailesi kombinasyonu eklendi")
    return added_count

def main():
    """Main function to add related products"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print("🚀 İlişkili ürünler ekleniyor...")
        
        # Get existing baskets
        existing_baskets = get_existing_baskets(cursor)
        basket_ids = [basket[0] for basket in existing_baskets]
        
        # Create new baskets if needed
        if len(basket_ids) < 50:
            print(f"📦 Yeni sepetler oluşturuluyor...")
            new_baskets = create_new_baskets(cursor, 50 - len(basket_ids))
            basket_ids.extend(new_baskets)
            conn.commit()
            print(f"✅ {len(new_baskets)} yeni sepet oluşturuldu")
        
        total_added = 0
        
        # Add different types of combinations
        product_conn = get_product_db_connection()
        product_cursor = product_conn.cursor()
        total_added += add_phone_case_combinations(cursor, basket_ids, product_cursor)
        total_added += add_console_game_combinations(cursor, basket_ids, product_cursor)
        total_added += add_accessory_combinations(cursor, basket_ids, product_cursor)
        total_added += add_brand_family_combinations(cursor, basket_ids, product_cursor)
        
        # Commit changes
        conn.commit()
        
        print(f"\n🎉 Toplam {total_added} ilişkili ürün eklendi!")
        
        # Verify no null values
        cursor.execute("""
        SELECT COUNT(*) FROM basket_product_units 
        WHERE product_name IS NULL OR product_model IS NULL OR 
              product_model_year IS NULL OR product_unit_price IS NULL OR 
              product_quantity IS NULL
        """)
        null_count = cursor.fetchone()[0]
        
        if null_count == 0:
            print("✅ Hiçbir sütunda null değer yok!")
        else:
            print(f"⚠️ {null_count} adet null değer bulundu")
        
        # Show summary
        cursor.execute("SELECT COUNT(*) FROM basket_product_units")
        total_units = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT basket_id) FROM basket_product_units")
        total_baskets = cursor.fetchone()[0]
        
        print(f"\n📊 Özet:")
        print(f"   - Toplam sepet ürünü: {total_units}")
        print(f"   - Toplam sepet: {total_baskets}")
        
    except mysql.connector.Error as err:
        print(f"❌ Veritabanı hatası: {err}")
    except Exception as e:
        print(f"❌ Hata: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
        if 'product_conn' in locals():
            product_conn.close()

if __name__ == "__main__":
    main() 