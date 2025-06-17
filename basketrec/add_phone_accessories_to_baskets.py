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

def get_phone_products():
    """Get phones and accessories from productservicedb"""
    conn = get_connection(PRODUCT_DB)
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Get phones
        cursor.execute("""
            SELECT product_id, product_name, product_price, product_model, product_model_year
            FROM products 
            WHERE product_sub_category_id = 32  -- Akıllı Telefonlar
            ORDER BY product_id
        """)
        phones = cursor.fetchall()
        
        # Get Samsung chargers
        cursor.execute("""
            SELECT product_id, product_name, product_price, product_model, product_model_year
            FROM products 
            WHERE product_sub_category_id = 3  -- Şarj Aleti
            AND product_name LIKE '%Samsung%'
            ORDER BY product_id
        """)
        samsung_chargers = cursor.fetchall()
        
        # Get Apple chargers
        cursor.execute("""
            SELECT product_id, product_name, product_price, product_model, product_model_year
            FROM products 
            WHERE product_sub_category_id = 3  -- Şarj Aleti
            AND product_name LIKE '%Apple%'
            ORDER BY product_id
        """)
        apple_chargers = cursor.fetchall()
        
        # Get Samsung earbuds
        cursor.execute("""
            SELECT product_id, product_name, product_price, product_model, product_model_year
            FROM products 
            WHERE product_sub_category_id = 12  -- Kablosuz Kulaklık
            AND product_name LIKE '%Samsung%'
            ORDER BY product_id
        """)
        samsung_earbuds = cursor.fetchall()
        
        print(f"📱 Telefonlar: {len(phones)} adet")
        print(f"🔌 Samsung şarj cihazları: {len(samsung_chargers)} adet")
        print(f"🔌 Apple şarj cihazları: {len(apple_chargers)} adet")
        print(f"🎧 Samsung kulaklıklar: {len(samsung_earbuds)} adet")
        
        return phones, samsung_chargers, apple_chargers, samsung_earbuds
        
    except Exception as e:
        print(f"❌ Ürünler alınırken hata: {e}")
        return [], [], [], []
    finally:
        conn.close()

def get_next_id(cursor, table, id_col):
    cursor.execute(f"SELECT MAX({id_col}) FROM {table}")
    result = cursor.fetchone()
    return (result[0] or 0) + 1

def create_phone_accessory_baskets():
    """Create baskets with phone + accessory combinations"""
    phones, samsung_chargers, apple_chargers, samsung_earbuds = get_phone_products()
    
    if not phones:
        print("❌ Telefon bulunamadı!")
        return
    
    conn = get_connection(BASKET_DB)
    cursor = conn.cursor()
    
    try:
        next_basket_id = get_next_id(cursor, 'baskets', 'basket_id')
        next_bpu_id = get_next_id(cursor, 'basket_product_units', 'basket_product_unit_id')
        basket_status_ids = [1, 2, 3]
        customer_ids = list(range(1, 21))
        
        phone_baskets = []
        
        # 1. Samsung telefon + Samsung şarj cihazı
        samsung_phones = [p for p in phones if 'Samsung' in p['product_name']]
        for phone in samsung_phones:
            for charger in samsung_chargers:
                phone_baskets.append([phone, charger])
        
        # 2. iPhone + Apple şarj cihazı
        iphones = [p for p in phones if 'iPhone' in p['product_name']]
        for phone in iphones:
            for charger in apple_chargers:
                phone_baskets.append([phone, charger])
        
        # 3. Samsung telefon + Samsung kulaklık
        for phone in samsung_phones:
            for earbud in samsung_earbuds:
                phone_baskets.append([phone, earbud])
        
        # 4. Samsung telefon + şarj + kulaklık (tam set)
        for phone in samsung_phones:
            for charger in samsung_chargers:
                for earbud in samsung_earbuds:
                    phone_baskets.append([phone, charger, earbud])
        
        # 5. iPhone + Apple şarj + Samsung kulaklık (karışık set)
        for phone in iphones:
            for charger in apple_chargers:
                for earbud in samsung_earbuds:
                    phone_baskets.append([phone, charger, earbud])
        
        print(f"📋 {len(phone_baskets)} farklı telefon+aksesuar kombinasyonu hazırlandı")
        
        # Create baskets
        for products in phone_baskets:
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
        print(f"🎉 {len(phone_baskets)} telefon+aksesuar sepeti başarıyla eklendi!")
        
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
    create_phone_accessory_baskets() 