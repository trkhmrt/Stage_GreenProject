import pandas as pd
from sqlalchemy import text, create_engine
from datetime import datetime, timedelta
import random

def clean_and_recreate_basket_data():
    """Delete all basket data and recreate with fresh phone-case matching"""
    
    # Database configurations
    product_host = "localhost"
    product_port = 3301
    product_database = "productservicedb"
    basket_host = "localhost"
    basket_port = 3309
    basket_database = "basketservicedb"
    username = "root"
    password = "root"
    
    try:
        # Connect to databases
        product_connection_string = f"mysql+mysqlconnector://{username}:{password}@{product_host}:{product_port}/{product_database}"
        basket_connection_string = f"mysql+mysqlconnector://{username}:{password}@{basket_host}:{basket_port}/{basket_database}"
        product_engine = create_engine(product_connection_string)
        basket_engine = create_engine(basket_connection_string)
        
        print("🧹 Mevcut basket verileri temizleniyor...")
        
        # 1. Önce basket_product_units tablosunu temizle (foreign key constraint nedeniyle)
        with basket_engine.connect() as conn:
            conn.execute(text("DELETE FROM basket_product_units"))
            conn.commit()
            print("✅ basket_product_units tablosu temizlendi")
        
        # 2. Sonra baskets tablosunu temizle
        with basket_engine.connect() as conn:
            conn.execute(text("DELETE FROM baskets"))
            conn.commit()
            print("✅ baskets tablosu temizlendi")
        
        # 3. Auto increment değerlerini sıfırla
        with basket_engine.connect() as conn:
            conn.execute(text("ALTER TABLE baskets AUTO_INCREMENT = 1"))
            conn.execute(text("ALTER TABLE basket_product_units AUTO_INCREMENT = 1"))
            conn.commit()
            print("✅ Auto increment değerleri sıfırlandı")
        
        print("\n🔄 Yeni veriler oluşturuluyor...")
        
        # Get all products with model data
        products_query = '''
        SELECT product_id, product_name, product_model, product_model_year, product_price, product_quantity, product_sub_category_id
        FROM products
        WHERE product_model IS NOT NULL AND product_model_year IS NOT NULL
        '''
        products_df = pd.read_sql(text(products_query), product_engine)
        
        # Separate phones and cases
        phones = products_df[products_df['product_sub_category_id'] == 1]
        cases = products_df[(products_df['product_sub_category_id'] == 32) |
                           (products_df['product_name'].str.contains('kılıf|case|cover|koruma', case=False, na=False))]
        
        print(f"📱 Telefon sayısı: {len(phones)}")
        print(f"📱 Kılıf sayısı: {len(cases)}")
        
        # Create new baskets and units
        basket_ids = []
        now = datetime.now()
        
        # 4. Her telefon için bir basket oluştur
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
                conn.execute(insert_basket_query, basket)
                conn.commit()
                # Son eklenen basket_id'yi al
                basket_id = conn.execute(text('SELECT LAST_INSERT_ID()')).scalar()
                basket_ids.append((basket_id, phone['product_id'], phone['product_model'], phone['product_model_year']))
        
        print(f"✅ {len(basket_ids)} adet yeni basket oluşturuldu")
        
        # 5. Her basket için uyumlu kılıfları basket_product_units tablosuna ekle
        insert_count = 0
        for basket_id, phone_id, phone_model, phone_year in basket_ids:
            # Uyumlu kılıfları bul
            compatible_cases = cases[(cases['product_model'] == phone_model) & 
                                   (cases['product_model_year'] == phone_year)]
            
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
        
        print(f"✅ {insert_count} adet telefon-kılıf eşleşmesi eklendi")
        
        # 6. Final statistics
        print(f"\n📊 Final istatistikler:")
        
        # Count baskets
        baskets_count_query = "SELECT COUNT(*) as total_baskets FROM baskets"
        baskets_count = pd.read_sql(text(baskets_count_query), basket_engine)
        print(f"Toplam sepet: {baskets_count.iloc[0]['total_baskets']}")
        
        # Count units
        units_count_query = "SELECT COUNT(*) as total_units FROM basket_product_units"
        units_count = pd.read_sql(text(units_count_query), basket_engine)
        print(f"Toplam basket_product_units: {units_count.iloc[0]['total_units']}")
        
        # Count units with model data
        model_units_query = """
        SELECT COUNT(*) as units_with_model 
        FROM basket_product_units 
        WHERE product_model IS NOT NULL
        """
        model_units_count = pd.read_sql(text(model_units_query), basket_engine)
        print(f"Model bilgisi olan units: {model_units_count.iloc[0]['units_with_model']}")
        
        # Show some examples
        print(f"\n📱 Örnek yeni kayıtlar:")
        examples_query = """
        SELECT 
            bpu.basket_product_unit_id,
            bpu.product_name,
            bpu.product_model,
            bpu.product_model_year,
            bpu.basket_id,
            b.create_date
        FROM basket_product_units bpu
        LEFT JOIN baskets b ON bpu.basket_id = b.basket_id
        ORDER BY bpu.basket_product_unit_id DESC
        LIMIT 10
        """
        examples_df = pd.read_sql(text(examples_query), basket_engine)
        for _, example in examples_df.iterrows():
            print(f"  {example['basket_product_unit_id']:4d}. {example['product_name']} -> {example['product_model']} ({example['product_model_year']}) - Basket: {example['basket_id']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    clean_and_recreate_basket_data() 