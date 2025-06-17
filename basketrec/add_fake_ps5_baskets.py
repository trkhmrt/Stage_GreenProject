import pandas as pd
from sqlalchemy import text, create_engine
import random
from datetime import datetime, timedelta

def add_fake_ps5_baskets():
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

    # 1. PS5 konsol ürününü bul
    ps5_console = pd.read_sql(
        text("SELECT * FROM products WHERE product_model = 'PlayStation 5' AND product_sub_category_id = 27"),
        product_engine
    )
    if ps5_console.empty:
        print("PS5 konsolu bulunamadı!")
        return
    ps5_console_id = int(ps5_console.iloc[0]['product_id'])
    ps5_console_name = ps5_console.iloc[0]['product_name']
    ps5_console_price = float(ps5_console.iloc[0]['product_price'])

    # 2. Tüm PS5 oyunlarını bul
    ps5_games = pd.read_sql(
        text("SELECT * FROM products WHERE product_model = 'PlayStation 5' AND product_sub_category_id = 28"),
        product_engine
    )
    if ps5_games.empty:
        print("PS5 oyunu bulunamadı!")
        return

    # 3. Bazı oyunları daha sık eklemek için ağırlıklı liste oluştur
    weighted_game_names = [
        "Marvel's Spider-Man: Miles Morales",
        "Demon's Souls",
        "Horizon Forbidden West"
    ]
    weighted_games = []
    for _, row in ps5_games.iterrows():
        name = row['product_name']
        if name in weighted_game_names:
            weighted_games.extend([row] * 6)  # Bu oyunlar daha sık
        else:
            weighted_games.extend([row] * 2)

    # 4. Fake kullanıcılar için sepet oluştur
    basket_count = 30
    basket_ids = []
    next_unit_id = pd.read_sql(text("SELECT IFNULL(MAX(basket_product_unit_id),0)+1 as next_id FROM basket_product_units"), basket_engine).iloc[0]['next_id']

    # Önce tüm baskets'leri oluştur
    with basket_engine.connect() as conn:
        for i in range(basket_count):
            customer_id = 1000 + i
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

    print(f"✅ {len(basket_ids)} adet yeni basket oluşturuldu")

    # 5. Her basket için PS5 konsolu ve oyunları ekle
    basket_product_units_rows = []
    
    for basket_id in basket_ids:
        # Her sepete 1 PS5 konsolu ekle
        basket_product_units_rows.append({
            'basket_product_unit_id': int(next_unit_id),
            'basket_id': basket_id,
            'product_id': ps5_console_id,
            'product_name': ps5_console_name,
            'product_model': 'PlayStation 5',
            'product_model_year': '2020',
            'product_quantity': 1,
            'product_total_price': ps5_console_price,
            'product_unit_price': ps5_console_price
        })
        next_unit_id += 1
        
        # 2-4 oyun ekle, bazıları daha sık
        game_count = random.choice([2,3,4])
        chosen_games = random.sample(weighted_games, k=game_count)
        for game in chosen_games:
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

    # 6. Basket product units'leri ekle
    with basket_engine.connect() as conn:
        for row in basket_product_units_rows:
            conn.execute(text("""
                INSERT INTO basket_product_units 
                (basket_product_unit_id, basket_id, product_id, product_name, product_model, product_model_year, product_quantity, product_total_price, product_unit_price) 
                VALUES (:basket_product_unit_id, :basket_id, :product_id, :product_name, :product_model, :product_model_year, :product_quantity, :product_total_price, :product_unit_price)
            """), row)
        conn.commit()
    
    print(f"✅ {len(basket_product_units_rows)} adet ürün basket_product_units'e eklendi")
    print(f"🎮 {basket_count} adet PS5 sepeti ve ilgili oyunlar başarıyla eklendi.")

if __name__ == "__main__":
    add_fake_ps5_baskets() 