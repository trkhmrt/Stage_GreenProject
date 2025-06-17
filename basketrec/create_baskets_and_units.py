import pandas as pd
from sqlalchemy import text, create_engine
from datetime import datetime, timedelta
import random

def create_baskets_and_units():
    # DB configs
    product_host = "localhost"
    product_port = 3301
    product_database = "productservicedb"
    basket_host = "localhost"
    basket_port = 3309
    basket_database = "basketservicedb"
    username = "root"
    password = "root"

    # Connect
    product_conn_str = f"mysql+mysqlconnector://{username}:{password}@{product_host}:{product_port}/{product_database}"
    basket_conn_str = f"mysql+mysqlconnector://{username}:{password}@{basket_host}:{basket_port}/{basket_database}"
    product_engine = create_engine(product_conn_str)
    basket_engine = create_engine(basket_conn_str)

    # Get all products
    products_query = '''
    SELECT product_id, product_name, product_model, product_model_year, product_price, product_quantity, product_sub_category_id
    FROM products
    '''
    products_df = pd.read_sql(text(products_query), product_engine)

    # Telefonlar (category 1) ve kılıflar (category 32)
    phones = products_df[products_df['product_sub_category_id'] == 1]
    cases = products_df[(products_df['product_sub_category_id'] == 32) |
                        (products_df['product_name'].str.contains('kılıf|case|cover|koruma', case=False, na=False))]

    print(f"Telefon sayısı: {len(phones)} | Kılıf sayısı: {len(cases)}")

    basket_ids = []
    now = datetime.now()
    # 1. Her telefon için bir basket oluştur
    for idx, phone in phones.iterrows():
        basket = {
            'create_date': now - timedelta(days=random.randint(0, 365)),
            'customer_id': random.randint(1, 500),
            'basket_status_id': 4  # Ödendi
        }
        insert_basket_query = text('''
            INSERT INTO baskets (create_date, customer_id, basket_status_id)
            VALUES (:create_date, :customer_id, :basket_status_id)
        ''')
        with basket_engine.connect() as conn:
            result = conn.execute(insert_basket_query, basket)
            conn.commit()
            # Son eklenen basket_id'yi al
            basket_id = conn.execute(text('SELECT LAST_INSERT_ID()')).scalar()
            basket_ids.append((basket_id, phone['product_id'], phone['product_model'], phone['product_model_year']))
    print(f"{len(basket_ids)} adet basket oluşturuldu.")

    # 2. Her basket için uyumlu kılıfları basket_product_units tablosuna ekle
    insert_count = 0
    for basket_id, phone_id, phone_model, phone_year in basket_ids:
        compatible_cases = cases[(cases['product_model'] == phone_model) & (cases['product_model_year'] == phone_year)]
        for _, case in compatible_cases.iterrows():
            unit = {
                'product_id': case['product_id'],
                'product_model': case['product_model'],
                'product_model_year': case['product_model_year'],
                'product_name': case['product_name'],
                'product_quantity': 1,
                'product_total_price': case['product_price'],
                'product_unit_price': case['product_price'],
                'basket_id': basket_id
            }
            insert_query = text('''
                INSERT INTO basket_product_units
                (product_id, product_model, product_model_year, product_name, product_quantity, product_total_price, product_unit_price, basket_id)
                VALUES (:product_id, :product_model, :product_model_year, :product_name, :product_quantity, :product_total_price, :product_unit_price, :basket_id)
            ''')
            with basket_engine.connect() as conn:
                conn.execute(insert_query, unit)
                conn.commit()
            insert_count += 1
    print(f"Toplam {insert_count} telefon-kılıf eşleşmesi basket_product_units tablosuna eklendi.")

if __name__ == "__main__":
    create_baskets_and_units() 