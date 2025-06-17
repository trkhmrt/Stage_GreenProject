import mysql.connector
import random

# Bağlantı ayarları
BASKET_DB = {
    'host': 'localhost',
    'port': 3309,
    'user': 'root',
    'password': 'root',
    'database': 'basketservicedb'
}
PRODUCT_DB = {
    'host': 'localhost',
    'port': 3301,
    'user': 'root',
    'password': 'root',
    'database': 'productservicedb'
}

# Uyumlu eşleşme kuralları (örnek, daha fazlası eklenebilir)
PHONE_CASE_COMPAT = {
    'iPhone 12 Pro': ['iPhone 12 Pro Kılıf', 'iPhone 12 Pro Silikon Kılıf', 'iPhone 12 Pro Şeffaf Kılıf'],
    'iPhone 13': ['iPhone 13 Kılıf', 'iPhone 13 Silikon Kılıf', 'iPhone 13 Şeffaf Kılıf'],
    'Samsung Galaxy S24': ['Samsung Galaxy S24 Kılıf', 'Samsung Galaxy S24 Silikon Kılıf'],
}
CONSOLE_GAME_COMPAT = {
    'PlayStation 5': [
        "Marvel's Spider-Man: Miles Morales", 'Horizon Forbidden West', 'Ratchet & Clank: Rift Apart',
        'Ghost of Tsushima Director\'s Cut', "Demon's Souls", 'Final Fantasy XVI', 'Resident Evil 4 Remake'
    ],
    'Xbox Series X': [
        'Halo Infinite', 'Forza Horizon 5', 'Gears 5', 'Psychonauts 2', 'Redfall'
    ],
}

# Yardımcı fonksiyonlar

def get_products_by_names(names, product_type):
    """Verilen isimlere göre ürünleri getirir."""
    connection = mysql.connector.connect(**PRODUCT_DB)
    try:
        cursor = connection.cursor(dictionary=True)
        format_strings = ','.join(['%s'] * len(names))
        query = f"""
            SELECT product_id, product_name, product_model, product_model_year, product_price
            FROM products
            WHERE product_name IN ({format_strings})
        """
        cursor.execute(query, tuple(names))
        products = cursor.fetchall()
        # Eksik alanları kontrol et
        for p in products:
            if not p['product_model']:
                p['product_model'] = p['product_name']
            if not p['product_model_year']:
                p['product_model_year'] = '2022'
            if not p['product_price']:
                p['product_price'] = random.randint(500, 20000) if product_type == 'phone' or product_type == 'console' else random.randint(100, 2000)
        return products
    finally:
        connection.close()

def clear_basket_product_units():
    connection = mysql.connector.connect(**BASKET_DB)
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM basket_product_units")
        connection.commit()
        print("basket_product_units tablosu temizlendi.")
    finally:
        connection.close()

def get_baskets():
    connection = mysql.connector.connect(**BASKET_DB)
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT basket_id FROM baskets WHERE basket_status_id = 4")
        return [row['basket_id'] for row in cursor.fetchall()]
    finally:
        connection.close()

def insert_basket_product_unit(basket_id, product, quantity=1):
    connection = mysql.connector.connect(**BASKET_DB)
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO basket_product_units (
                basket_id, product_id, product_name, product_model, product_model_year, product_quantity, product_unit_price, product_total_price
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        unit_price = product['product_price']
        total_price = unit_price * quantity
        cursor.execute(query, (
            basket_id,
            product['product_id'],
            product['product_name'],
            product['product_model'],
            product['product_model_year'],
            quantity,
            unit_price,
            total_price
        ))
        connection.commit()
    finally:
        connection.close()

def main():
    clear_basket_product_units()
    baskets = get_baskets()
    basket_idx = 0
    print(f"{len(baskets)} sepet bulundu.")

    # Telefon + kılıf eşleşmeleri
    for phone, cases in PHONE_CASE_COMPAT.items():
        phone_obj = get_products_by_names([phone], 'phone')
        case_objs = get_products_by_names(cases, 'case')
        if not phone_obj or not case_objs:
            continue
        for case in case_objs:
            # Her sepet için bir telefon ve bir kılıf ekle
            if basket_idx >= len(baskets):
                break
            basket_id = baskets[basket_idx]
            insert_basket_product_unit(basket_id, phone_obj[0], 1)
            insert_basket_product_unit(basket_id, case, 1)
            basket_idx += 1
    # Konsol + oyun eşleşmeleri
    for console, games in CONSOLE_GAME_COMPAT.items():
        console_obj = get_products_by_names([console], 'console')
        game_objs = get_products_by_names(games, 'game')
        if not console_obj or not game_objs:
            continue
        for game in game_objs:
            if basket_idx >= len(baskets):
                break
            basket_id = baskets[basket_idx]
            insert_basket_product_unit(basket_id, console_obj[0], 1)
            insert_basket_product_unit(basket_id, game, 1)
            basket_idx += 1
    print("Uyumlu ürünler başarıyla eklendi!")

if __name__ == "__main__":
    main() 