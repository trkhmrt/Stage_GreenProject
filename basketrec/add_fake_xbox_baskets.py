import pandas as pd
from sqlalchemy import text, create_engine
import random
from datetime import datetime, timedelta

def add_fake_xbox_baskets():
    # DB config
    basket_host = "localhost"
    basket_port = 3309
    basket_database = "basketservicedb"
    product_host = "localhost"
    product_port = 3301
    product_database = "productservicedb"
    username = "root"
    password = "root"

    # Connect to DBs
    product_engine = create_engine(f"mysql+mysqlconnector://{username}:{password}@{product_host}:{product_port}/{product_database}")
    basket_engine = create_engine(f"mysql+mysqlconnector://{username}:{password}@{basket_host}:{basket_port}/{basket_database}")

    # 1. Xbox konsollarını bul
    xbox_consoles = pd.read_sql(
        text("SELECT * FROM products WHERE product_model LIKE '%Xbox%' AND product_sub_category_id = 27"),
        product_engine
    )
    if xbox_consoles.empty:
        print("Xbox konsolu bulunamadı!")
        return

    # 2. Tüm Xbox oyunlarını bul
    xbox_games = pd.read_sql(
        text("SELECT * FROM products WHERE product_model LIKE '%Xbox%' AND product_sub_category_id = 28"),
        product_engine
    )
    if xbox_games.empty:
        print("Xbox oyunu bulunamadı!")
        return

    print(f"🎮 Xbox konsolları: {len(xbox_consoles)}")
    print(f"🎮 Xbox oyunları: {len(xbox_games)}")

    # 3. Bazı oyunları daha sık eklemek için ağırlıklı liste oluştur
    weighted_game_names = [
        "Halo: The Master Chief Collection",
        "Forza Horizon 4", 
        "Gears of War 4",
        "Starfield",
        "Redfall"
    ]
    weighted_games = []
    for _, row in xbox_games.iterrows():
        name = row['product_name']
        if name in weighted_game_names:
            weighted_games.extend([row] * 6)  # Bu oyunlar daha sık
        else:
            weighted_games.extend([row] * 2)

    # 4. Her Xbox konsolu için fake sepetler oluştur
    basket_count_per_console = 20  # Her konsol için 20 sepet
    total_baskets = 0
    total_units = 0
    next_unit_id = pd.read_sql(text("SELECT IFNULL(MAX(basket_product_unit_id),0)+1 as next_id FROM basket_product_units"), basket_engine).iloc[0]['next_id']

    for _, console in xbox_consoles.iterrows():
        console_id = int(console['product_id'])
        console_name = console['product_name']
        console_model = console['product_model']
        console_year = console['product_model_year']
        console_price = float(console['product_price'])
        
        print(f"\n🎮 {console_name} için sepetler oluşturuluyor...")
        
        basket_ids = []
        
        # Önce bu konsol için baskets'leri oluştur
        with basket_engine.connect() as conn:
            for i in range(basket_count_per_console):
                customer_id = 2000 + total_baskets + i  # Xbox kullanıcıları için farklı ID aralığı
                basket = {
                    'create_date': datetime.now() - timedelta(days=random.randint(0, 365)),
                    'customer_id': customer_id,
                    'basket_status_id': 4
                }
                
                insert_basket_query = text('''
                    INSERT INTO baskets (create_date, customer_id, basket_status_id)
                    VALUES (:create_date, :customer_id, :basket_status_id)
                ''')
                
                conn.execute(insert_basket_query, basket)
                conn.commit()
                # Son eklenen basket_id'yi al
                basket_id = conn.execute(text('SELECT LAST_INSERT_ID()')).scalar()
                basket_ids.append(basket_id)

        print(f"✅ {len(basket_ids)} adet {console_name} basket'i oluşturuldu")

        # Bu konsol için uyumlu oyunları bul
        compatible_games = xbox_games[xbox_games['product_model'] == console_model]
        
        # Geriye uyumluluk için ek oyunlar ekle
        if console_model == "Xbox Series X":
            # Xbox Series X'te Xbox One oyunları da çalışır
            xbox_one_games = xbox_games[(xbox_games['product_model'] == "Xbox One") & 
                                      (xbox_games['product_model_year'].isin(['2013', '2014', '2015', '2016', '2017', '2018', '2019']))]
            compatible_games = pd.concat([compatible_games, xbox_one_games])
        elif console_model == "Xbox Series S":
            # Xbox Series S'te Xbox One oyunları da çalışır
            xbox_one_games = xbox_games[(xbox_games['product_model'] == "Xbox One") & 
                                      (xbox_games['product_model_year'].isin(['2013', '2014', '2015', '2016', '2017', '2018', '2019']))]
            compatible_games = pd.concat([compatible_games, xbox_one_games])
        
        # Duplicate'leri kaldır
        compatible_games = compatible_games.drop_duplicates(subset=['product_id'])
        
        # Her basket için konsol ve oyunları ekle
        basket_product_units_rows = []
        
        for basket_id in basket_ids:
            # Her sepete 1 Xbox konsolu ekle
            basket_product_units_rows.append({
                'basket_product_unit_id': int(next_unit_id),
                'basket_id': basket_id,
                'product_id': console_id,
                'product_name': console_name,
                'product_model': console_model,
                'product_model_year': console_year,
                'product_quantity': 1,
                'product_total_price': console_price,
                'product_unit_price': console_price
            })
            next_unit_id += 1
            
            # 2-4 oyun ekle, bazıları daha sık
            game_count = random.choice([2,3,4])
            if len(compatible_games) > 0:
                chosen_games = compatible_games.sample(n=min(game_count, len(compatible_games)))
                for _, game in chosen_games.iterrows():
                    basket_product_units_rows.append({
                        'basket_product_unit_id': int(next_unit_id),
                        'basket_id': basket_id,
                        'product_id': int(game['product_id']),
                        'product_name': game['product_name'],
                        'product_model': game['product_model'],
                        'product_model_year': game['product_model_year'],
                        'product_quantity': 1,
                        'product_total_price': float(game['product_price']),
                        'product_unit_price': float(game['product_price'])
                    })
                    next_unit_id += 1

        # Basket product units'leri ekle
        with basket_engine.connect() as conn:
            for row in basket_product_units_rows:
                conn.execute(text("""
                    INSERT INTO basket_product_units 
                    (basket_product_unit_id, basket_id, product_id, product_name, product_model, product_model_year, product_quantity, product_total_price, product_unit_price) 
                    VALUES (:basket_product_unit_id, :basket_id, :product_id, :product_name, :product_model, :product_model_year, :product_quantity, :product_total_price, :product_unit_price)
                """), row)
            conn.commit()
        
        total_baskets += len(basket_ids)
        total_units += len(basket_product_units_rows)
        print(f"✅ {len(basket_product_units_rows)} adet ürün {console_name} sepetlerine eklendi")

    print(f"\n🎮 TOPLAM SONUÇLAR:")
    print(f"✅ {total_baskets} adet Xbox sepeti oluşturuldu")
    print(f"✅ {total_units} adet ürün basket_product_units'e eklendi")
    print(f"🎮 Xbox konsolları ve oyunları başarıyla eklendi!")

if __name__ == "__main__":
    add_fake_xbox_baskets() 