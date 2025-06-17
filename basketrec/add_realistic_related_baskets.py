#!/usr/bin/env python3
import mysql.connector
import random
from datetime import datetime, timedelta

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

def get_conn(db):
    return mysql.connector.connect(**db)

def get_phones_and_cases(product_cursor):
    # Phones: sub_category_id=32, Cases: sub_category_id=1
    product_cursor.execute("""
        SELECT product_id, product_name, product_model, product_model_year, product_price
        FROM products WHERE product_sub_category_id=32 AND product_model IS NOT NULL AND product_model_year IS NOT NULL
    """)
    phones = product_cursor.fetchall()
    product_cursor.execute("""
        SELECT product_id, product_name, product_model, product_model_year, product_price
        FROM products WHERE product_sub_category_id=1 AND product_model IS NOT NULL AND product_model_year IS NOT NULL
    """)
    cases = product_cursor.fetchall()
    return phones, cases

def get_consoles_and_games(product_cursor):
    # Consoles: sub_category_id=27, Games: sub_category_id=28
    product_cursor.execute("""
        SELECT product_id, product_name, product_model, product_model_year, product_price
        FROM products WHERE product_sub_category_id=27 AND product_model IS NOT NULL AND product_model_year IS NOT NULL
    """)
    consoles = product_cursor.fetchall()
    product_cursor.execute("""
        SELECT product_id, product_name, product_model, product_model_year, product_price
        FROM products WHERE product_sub_category_id=28 AND product_model IS NOT NULL AND product_model_year IS NOT NULL
    """)
    games = product_cursor.fetchall()
    return consoles, games

def create_basket(basket_cursor, customer_id=None, status_id=4):
    if customer_id is None:
        customer_id = random.randint(1, 1000)
    create_date = datetime.now() - timedelta(days=random.randint(0, 365))
    basket_cursor.execute(
        "INSERT INTO baskets (customer_id, basket_status_id, create_date) VALUES (%s, %s, %s)",
        (customer_id, status_id, create_date)
    )
    return basket_cursor.lastrowid

def insert_basket_product_unit(basket_cursor, basket_id, product, quantity=1):
    query = """
        INSERT INTO basket_product_units (
            basket_id, product_id, product_name, product_model, product_model_year,
            product_quantity, product_unit_price, product_total_price
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    unit_price = product[4]
    total_price = unit_price * quantity
    basket_cursor.execute(query, (
        basket_id, product[0], product[1], product[2], product[3],
        quantity, unit_price, total_price
    ))

def main():
    product_conn = get_conn(PRODUCT_DB)
    basket_conn = get_conn(BASKET_DB)
    product_cursor = product_conn.cursor()
    basket_cursor = basket_conn.cursor()
    try:
        print("🧹 Eski basket_product_units temizleniyor...")
        basket_cursor.execute("DELETE FROM basket_product_units")
        basket_conn.commit()
        print("✅ Temizlendi.")

        # 1. Telefonlar ve kılıflar
        phones, cases = get_phones_and_cases(product_cursor)
        phone_case_count = 0
        for phone in phones:
            compatible_cases = [case for case in cases if phone[2] and phone[2].lower() in case[1].lower()]
            if len(compatible_cases) >= 2:
                for _ in range(2):  # Her telefon için 2 farklı sepet
                    basket_id = create_basket(basket_cursor)
                    insert_basket_product_unit(basket_cursor, basket_id, phone, 1)
                    selected_cases = random.sample(compatible_cases, min(3, len(compatible_cases)))
                    for case in selected_cases:
                        insert_basket_product_unit(basket_cursor, basket_id, case, 1)
                    phone_case_count += 1
        print(f"📱 {phone_case_count} telefon + çoklu kılıf sepeti eklendi.")

        # 2. Konsollar ve oyunlar
        consoles, games = get_consoles_and_games(product_cursor)
        console_game_count = 0
        for console in consoles:
            compatible_games = [game for game in games if console[2] and console[2].lower() in game[2].lower()]
            if len(compatible_games) >= 2:
                for _ in range(2):  # Her konsol için 2 farklı sepet
                    basket_id = create_basket(basket_cursor)
                    insert_basket_product_unit(basket_cursor, basket_id, console, 1)
                    selected_games = random.sample(compatible_games, min(4, len(compatible_games)))
                    for game in selected_games:
                        insert_basket_product_unit(basket_cursor, basket_id, game, 1)
                    console_game_count += 1
        print(f"🎮 {console_game_count} konsol + çoklu oyun sepeti eklendi.")

        basket_conn.commit()
        print("✅ Sepetler ve ürünler başarıyla eklendi!")

        # Null kontrolü
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

        # Özet
        basket_cursor.execute("SELECT COUNT(*) FROM basket_product_units")
        total_units = basket_cursor.fetchone()[0]
        basket_cursor.execute("SELECT COUNT(DISTINCT basket_id) FROM basket_product_units")
        total_baskets = basket_cursor.fetchone()[0]
        print(f"\n📊 Özet:")
        print(f"   - Toplam sepet ürünü: {total_units}")
        print(f"   - Toplam sepet: {total_baskets}")
    finally:
        product_conn.close()
        basket_conn.close()

if __name__ == "__main__":
    main() 