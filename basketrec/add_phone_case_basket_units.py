import pandas as pd
from sqlalchemy import text, create_engine
import random

def add_phone_case_basket_units():
    """Match phones and cases by model/model year and insert into basket_product_units as phone-case pairs"""
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

    # Her telefon için uyumlu kılıfları bul ve basket_product_units tablosuna ekle
    basket_id = 1000  # örnek basket_id, isterseniz random veya artan verebilirsiniz
    insert_count = 0
    for _, phone in phones.iterrows():
        # Uyumlu kılıflar: model ve yıl eşleşenler
        compatible_cases = cases[(cases['product_model'] == phone['product_model']) &
                                 (cases['product_model_year'] == phone['product_model_year'])]
        for _, case in compatible_cases.iterrows():
            # Her eşleşme için bir kayıt ekle
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
        basket_id += 1
    print(f"Toplam {insert_count} telefon-kılıf eşleşmesi basket_product_units tablosuna eklendi.")

if __name__ == "__main__":
    add_phone_case_basket_units() 