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

def get_tea_products():
    conn = get_connection(PRODUCT_DB)
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('''
            SELECT product_id, product_name, product_price, product_model, product_model_year
            FROM products
            WHERE product_sub_category_id = (SELECT sub_category_id FROM sub_categories WHERE sub_category_name = 'Mutfak & Yemek' LIMIT 1)
            AND (product_name LIKE '%çay%' OR product_name LIKE '%Çay%')
            ORDER BY product_id
        ''')
        return cursor.fetchall()
    finally:
        conn.close()

def get_next_id(cursor, table, id_col):
    cursor.execute(f"SELECT MAX({id_col}) FROM {table}")
    result = cursor.fetchone()
    return (result[0] or 0) + 1

def create_tea_baskets():
    tea_products = get_tea_products()
    if not tea_products:
        print("❌ Çay ürünleri bulunamadı!")
        return
    cups = [p for p in tea_products if 'bardağı' in p['product_name'].lower()]
    saucers = [p for p in tea_products if 'tabağı' in p['product_name'].lower()]
    spoons = [p for p in tea_products if 'kaşığı' in p['product_name'].lower()]
    sets = [p for p in tea_products if 'set' in p['product_name'].lower()]

    conn = get_connection(BASKET_DB)
    cursor = conn.cursor()
    try:
        next_basket_id = get_next_id(cursor, 'baskets', 'basket_id')
        next_bpu_id = get_next_id(cursor, 'basket_product_units', 'basket_product_unit_id')
        basket_status_ids = [1, 2, 3]  # örnek durumlar
        customer_ids = list(range(1, 21))  # 1-20 arası müşteri
        tea_baskets = []
        # Mantıklı kombinasyonlar
        for cup in cups:
            for saucer in saucers:
                for spoon in spoons:
                    tea_baskets.append([cup, saucer, spoon])
        for set_product in sets:
            tea_baskets.append([set_product])
        # Sepetleri ekle
        for products in tea_baskets:
            basket_id = next_basket_id
            create_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d %H:%M:%S')
            customer_id = random.choice(customer_ids)
            basket_status_id = random.choice(basket_status_ids)
            cursor.execute(
                "INSERT INTO baskets (basket_id, create_date, customer_id, basket_status_id) VALUES (%s, %s, %s, %s)",
                (basket_id, create_date, customer_id, basket_status_id)
            )
            for product in products:
                quantity = random.randint(1, 3)
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
        print(f"🎉 {len(tea_baskets)} çay sepeti ve ürünleri başarıyla eklendi!")
    except Exception as e:
        print(f"❌ Hata: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    create_tea_baskets() 