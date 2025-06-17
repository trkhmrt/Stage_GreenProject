import pandas as pd
from sqlalchemy import text, create_engine
from datetime import datetime, timedelta
import random

def add_console_game_baskets():
    """Add console-game matching pairs to basket system"""
    
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
        
        print("🎮 Konsol-oyun eşleşmeleri basket sistemine ekleniyor...")
        
        # Get all products with model data
        products_query = '''
        SELECT product_id, product_name, product_model, product_model_year, product_price, product_quantity, product_sub_category_id
        FROM products
        WHERE product_model IS NOT NULL AND product_model_year IS NOT NULL
        '''
        products_df = pd.read_sql(text(products_query), product_engine)
        
        # Separate consoles and games
        consoles = products_df[products_df['product_sub_category_id'] == 27]  # Oyun Konsolları
        games = products_df[products_df['product_sub_category_id'] == 28]     # Konsol Oyunları
        
        print(f"🎮 Konsol sayısı: {len(consoles)}")
        print(f"🎮 Oyun sayısı: {len(games)}")
        
        # Create new baskets and units for console-game pairs
        basket_ids = []
        now = datetime.now()
        
        # 1. Her konsol için bir basket oluştur
        for idx, console in consoles.iterrows():
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
                basket_ids.append((basket_id, console['product_id'], console['product_model'], console['product_model_year']))
        
        print(f"✅ {len(basket_ids)} adet yeni basket oluşturuldu")
        
        # 2. Her basket için uyumlu oyunları basket_product_units tablosuna ekle
        insert_count = 0
        for basket_id, console_id, console_model, console_year in basket_ids:
            # Uyumlu oyunları bul (model ve yıl eşleşenler)
            compatible_games = games[(games['product_model'] == console_model) & 
                                   (games['product_model_year'] == console_year)]
            
            # Ayrıca geriye uyumlu oyunları da ekle (eski oyunlar yeni konsollarda çalışabilir)
            if console_model == "PlayStation 5":
                # PS5'te PS4 oyunları da çalışır
                ps4_games = games[(games['product_model'] == "PlayStation 4") & 
                                (games['product_model_year'].isin(['2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']))]
                compatible_games = pd.concat([compatible_games, ps4_games])
            elif console_model == "Xbox Series X":
                # Xbox Series X'te Xbox One oyunları da çalışır
                xbox_one_games = games[(games['product_model'] == "Xbox One") & 
                                     (games['product_model_year'].isin(['2013', '2014', '2015', '2016', '2017', '2018', '2019']))]
                compatible_games = pd.concat([compatible_games, xbox_one_games])
            elif console_model == "Xbox Series S":
                # Xbox Series S'te Xbox One oyunları da çalışır
                xbox_one_games = games[(games['product_model'] == "Xbox One") & 
                                     (games['product_model_year'].isin(['2013', '2014', '2015', '2016', '2017', '2018', '2019']))]
                compatible_games = pd.concat([compatible_games, xbox_one_games])
            
            # Duplicate'leri kaldır
            compatible_games = compatible_games.drop_duplicates(subset=['product_id'])
            
            for _, game in compatible_games.iterrows():
                unit = {
                    'product_id': game['product_id'],
                    'product_model': game['product_model'],
                    'product_model_year': game['product_model_year'],
                    'product_name': game['product_name'],
                    'product_quantity': 1,
                    'product_total_price': game['product_price'],
                    'product_unit_price': game['product_price'],
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
        
        print(f"✅ {insert_count} adet konsol-oyun eşleşmesi eklendi")
        
        # 3. Final statistics
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
        print(f"\n🎮 Örnek konsol-oyun eşleşmeleri:")
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
        WHERE bpu.product_model LIKE '%PlayStation%' OR bpu.product_model LIKE '%Xbox%'
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
    add_console_game_baskets() 