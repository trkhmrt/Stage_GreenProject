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

def check_categories():
    """Check available categories and subcategories"""
    try:
        conn = get_product_connection()
        cursor = conn.cursor(dictionary=True)
        
        print("🔍 Kategoriler kontrol ediliyor...")
        
        # Get categories
        cursor.execute("SELECT category_id, category_name FROM categories ORDER BY category_id")
        categories = cursor.fetchall()
        
        print("📊 Kategoriler:")
        for cat in categories:
            print(f"   {cat['category_id']}: {cat['category_name']}")
        
        # Get subcategories with category info
        cursor.execute("""
            SELECT sc.sub_category_id, sc.sub_category_name, c.category_name
            FROM sub_categories sc
            JOIN categories c ON sc.category_id = c.category_id
            ORDER BY sc.sub_category_id
        """)
        subcategories = cursor.fetchall()
        
        print("\n📊 Alt Kategoriler:")
        for subcat in subcategories:
            print(f"   {subcat['sub_category_id']}: {subcat['sub_category_name']} ({subcat['category_name']})")
        
        return categories, subcategories
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        return None, None
    finally:
        if 'conn' in locals():
            conn.close()

def get_products_by_subcategory(product_cursor, subcategory_id):
    """Get products by subcategory"""
    query = """
    SELECT product_id, product_name, product_model, product_model_year, product_price, product_quantity
    FROM products 
    WHERE product_sub_category_id = %s AND product_model IS NOT NULL AND product_model_year IS NOT NULL
    """
    product_cursor.execute(query, (subcategory_id,))
    return product_cursor.fetchall()

def get_existing_baskets(basket_cursor):
    """Get existing baskets"""
    query = "SELECT basket_id, customer_id, basket_status_id FROM baskets WHERE basket_status_id IN (1, 4)"
    basket_cursor.execute(query)
    return basket_cursor.fetchall()

def create_new_baskets(basket_cursor, count=50):
    """Create new baskets"""
    baskets_created = []
    for i in range(count):
        customer_id = random.randint(1, 100)
        basket_status_id = random.choice([1, 4])
        create_date = datetime.now() - timedelta(days=random.randint(1, 365))
        
        query = """
        INSERT INTO baskets (customer_id, basket_status_id, create_date)
        VALUES (%s, %s, %s)
        """
        basket_cursor.execute(query, (customer_id, basket_status_id, create_date))
        basket_id = basket_cursor.lastrowid
        baskets_created.append(basket_id)
    
    return baskets_created

def add_products_to_baskets():
    """Add products to baskets based on subcategories"""
    try:
        product_conn = get_product_connection()
        basket_conn = get_basket_connection()
        
        product_cursor = product_conn.cursor()
        basket_cursor = basket_conn.cursor()
        
        print("🚀 Ürünler sepete ekleniyor...")
        
        # Get existing baskets
        existing_baskets = get_existing_baskets(basket_cursor)
        basket_ids = [basket[0] for basket in existing_baskets]
        
        # Create new baskets if needed
        if len(basket_ids) < 50:
            print(f"📦 Yeni sepetler oluşturuluyor...")
            new_baskets = create_new_baskets(basket_cursor, 50 - len(basket_ids))
            basket_ids.extend(new_baskets)
            basket_conn.commit()
            print(f"✅ {len(new_baskets)} yeni sepet oluşturuldu")
        
        total_added = 0
        
        # Define product groups by subcategory
        product_groups = {
            'phones': [32],  # Akıllı Telefonlar
            'cases': [1],    # Telefon Kılıfı
            'consoles': [27], # Oyun Konsolları
            'games': [28],    # Konsol Oyunları
            'accessories': [2, 3, 12, 13, 14, 15, 16]  # Aksesuarlar
        }
        
        # Add phone-case combinations
        print("📱 Telefon-kılıf kombinasyonları ekleniyor...")
        phones = get_products_by_subcategory(product_cursor, 32)
        cases = get_products_by_subcategory(product_cursor, 1)
        
        if phones and cases:
            for basket_id in random.sample(basket_ids, min(20, len(basket_ids))):
                phone = random.choice(phones)
                
                # Find compatible cases
                compatible_cases = []
                for case in cases:
                    if phone[2] and case[2] and phone[2].lower() in case[1].lower():
                        compatible_cases.append(case)
                
                if compatible_cases:
                    case = random.choice(compatible_cases)
                    quantity = random.randint(1, 2)
                    
                    # Add phone
                    query = """
                    INSERT INTO basket_product_units 
                    (basket_id, product_id, product_name, product_model, product_model_year, 
                     product_quantity, product_unit_price, product_total_price)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    basket_cursor.execute(query, (
                        basket_id, phone[0], phone[1], phone[2], phone[3], 
                        quantity, phone[4], phone[4] * quantity
                    ))
                    
                    # Add case
                    basket_cursor.execute(query, (
                        basket_id, case[0], case[1], case[2], case[3], 
                        quantity, case[4], case[4] * quantity
                    ))
                    
                    total_added += 2
        
        # Add console-game combinations
        print("🎮 Konsol-oyun kombinasyonları ekleniyor...")
        consoles = get_products_by_subcategory(product_cursor, 27)
        games = get_products_by_subcategory(product_cursor, 28)
        
        if consoles and games:
            for basket_id in random.sample(basket_ids, min(25, len(basket_ids))):
                console = random.choice(consoles)
                
                # Find compatible games
                compatible_games = []
                for game in games:
                    if console[2] and game[2] and console[2].lower() in game[1].lower():
                        compatible_games.append(game)
                
                if compatible_games:
                    selected_games = random.sample(compatible_games, min(3, len(compatible_games)))
                    
                    # Add console
                    query = """
                    INSERT INTO basket_product_units 
                    (basket_id, product_id, product_name, product_model, product_model_year, 
                     product_quantity, product_unit_price, product_total_price)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    basket_cursor.execute(query, (
                        basket_id, console[0], console[1], console[2], console[3], 
                        1, console[4], console[4]
                    ))
                    
                    # Add games
                    for game in selected_games:
                        basket_cursor.execute(query, (
                            basket_id, game[0], game[1], game[2], game[3], 
                            1, game[4], game[4]
                        ))
                    
                    total_added += 1 + len(selected_games)
        
        # Add accessory combinations
        print("🎧 Aksesuar kombinasyonları ekleniyor...")
        for subcat_id in [2, 3, 12, 13, 14, 15, 16]:
            accessories = get_products_by_subcategory(product_cursor, subcat_id)
            if accessories:
                for basket_id in random.sample(basket_ids, min(15, len(basket_ids))):
                    selected_accessories = random.sample(accessories, min(2, len(accessories)))
                    
                    query = """
                    INSERT INTO basket_product_units 
                    (basket_id, product_id, product_name, product_model, product_model_year, 
                     product_quantity, product_unit_price, product_total_price)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    
                    for accessory in selected_accessories:
                        quantity = random.randint(1, 2)
                        basket_cursor.execute(query, (
                            basket_id, accessory[0], accessory[1], accessory[2], accessory[3], 
                            quantity, accessory[4], accessory[4] * quantity
                        ))
                    
                    total_added += len(selected_accessories)
        
        # Commit changes
        basket_conn.commit()
        
        print(f"\n🎉 Toplam {total_added} ürün eklendi!")
        
        # Verify no null values
        basket_cursor.execute("""
        SELECT COUNT(*) FROM basket_product_units 
        WHERE product_name IS NULL OR product_model IS NULL OR 
              product_model_year IS NULL OR product_unit_price IS NULL OR 
              product_quantity IS NULL
        """)
        null_count = basket_cursor.fetchone()[0]
        
        if null_count == 0:
            print("✅ Hiçbir sütunda null değer yok!")
        else:
            print(f"⚠️ {null_count} adet null değer bulundu")
        
        # Show summary
        basket_cursor.execute("SELECT COUNT(*) FROM basket_product_units")
        total_units = basket_cursor.fetchone()[0]
        
        basket_cursor.execute("SELECT COUNT(DISTINCT basket_id) FROM basket_product_units")
        total_baskets = basket_cursor.fetchone()[0]
        
        print(f"\n📊 Özet:")
        print(f"   - Toplam sepet ürünü: {total_units}")
        print(f"   - Toplam sepet: {total_baskets}")
        
    except Exception as e:
        print(f"❌ Hata: {e}")
    finally:
        if 'product_conn' in locals():
            product_conn.close()
        if 'basket_conn' in locals():
            basket_conn.close()

def main():
    """Main function"""
    print("🔍 Kategoriler kontrol ediliyor...")
    categories, subcategories = check_categories()
    
    if categories and subcategories:
        print("\n" + "="*50)
        add_products_to_baskets()
    else:
        print("❌ Kategoriler alınamadı!")

if __name__ == "__main__":
    main() 