import pandas as pd
from sqlalchemy import text, create_engine
import random
from datetime import datetime, timedelta

def add_ps_gta5_baskets():
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

    # 1. PlayStation konsollarını bul
    ps_consoles = pd.read_sql(
        text("SELECT * FROM products WHERE product_model LIKE '%PlayStation%' AND product_sub_category_id = 27"),
        product_engine
    )
    if ps_consoles.empty:
        print("PlayStation konsolu bulunamadı!")
        return

    # 2. GTA 5 oyunlarını bul (tüm PlayStation modelleri için)
    gta5_games = pd.read_sql(
        text("SELECT * FROM products WHERE product_name LIKE '%Grand Theft Auto V%' AND product_sub_category_id = 28"),
        product_engine
    )
    if gta5_games.empty:
        print("GTA 5 oyunu bulunamadı!")
        return

    print(f"🎮 PlayStation konsolları: {len(ps_consoles)}")
    print(f"🎮 GTA 5 oyunları: {len(gta5_games)}")

    # 3. Her PlayStation konsolu için GTA 5 ile sepetler oluştur
    basket_count_per_console = 15  # Her konsol için 15 sepet
    total_baskets = 0
    total_units = 0
    next_unit_id = pd.read_sql(text("SELECT IFNULL(MAX(basket_product_unit_id),0)+1 as next_id FROM basket_product_units"), basket_engine).iloc[0]['next_id']

    for _, console in ps_consoles.iterrows():
        console_id = int(console['product_id'])
        console_name = console['product_name']
        console_model = console['product_model']
        console_year = console['product_model_year']
        console_price = float(console['product_price'])
        
        print(f"\n🎮 {console_name} + GTA 5 için sepetler oluşturuluyor...")
        
        # Bu konsol için GTA 5 oyununu bul
        gta5_for_console = gta5_games[gta5_games['product_model'] == console_model]
        
        if gta5_for_console.empty:
            print(f"⚠️ {console_model} için GTA 5 bulunamadı, atlanıyor...")
            continue
        
        gta5_game = gta5_for_console.iloc[0]
        gta5_id = int(gta5_game['product_id'])
        gta5_name = gta5_game['product_name']
        gta5_price = float(gta5_game['product_price'])
        
        basket_ids = []
        
        # Önce bu konsol için baskets'leri oluştur
        with basket_engine.connect() as conn:
            for i in range(basket_count_per_console):
                customer_id = 3000 + total_baskets + i  # PS+GTA5 kullanıcıları için farklı ID aralığı
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

        print(f"✅ {len(basket_ids)} adet {console_name} + GTA 5 basket'i oluşturuldu")

        # Her basket için konsol ve GTA 5 ekle
        basket_product_units_rows = []
        
        for basket_id in basket_ids:
            # Her sepete 1 PlayStation konsolu ekle
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
            
            # Her sepete 1 GTA 5 oyunu ekle
            basket_product_units_rows.append({
                'basket_product_unit_id': int(next_unit_id),
                'basket_id': basket_id,
                'product_id': gta5_id,
                'product_name': gta5_name,
                'product_model': gta5_game['product_model'],
                'product_model_year': gta5_game['product_model_year'],
                'product_quantity': 1,
                'product_total_price': gta5_price,
                'product_unit_price': gta5_price
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
        print(f"✅ {len(basket_product_units_rows)} adet ürün ({console_name} + GTA 5) sepetlerine eklendi")

    print(f"\n🎮 TOPLAM SONUÇLAR:")
    print(f"✅ {total_baskets} adet PlayStation + GTA 5 sepeti oluşturuldu")
    print(f"✅ {total_units} adet ürün basket_product_units'e eklendi")
    print(f"🎮 PlayStation konsolları + GTA 5 oyunları başarıyla eklendi!")

    # 4. Örnek sepetleri göster
    print(f"\n📊 Örnek PlayStation + GTA 5 sepetleri:")
    examples_query = """
    SELECT 
        b.basket_id,
        b.customer_id,
        b.create_date,
        bpu1.product_name as console_name,
        bpu1.product_model as console_model,
        bpu2.product_name as game_name,
        bpu2.product_model as game_model
    FROM baskets b
    JOIN basket_product_units bpu1 ON b.basket_id = bpu1.basket_id AND bpu1.product_sub_category_id = 27
    JOIN basket_product_units bpu2 ON b.basket_id = bpu2.basket_id AND bpu2.product_name LIKE '%Grand Theft Auto V%'
    WHERE b.customer_id >= 3000
    ORDER BY b.basket_id DESC
    LIMIT 10
    """
    
    try:
        examples_df = pd.read_sql(text(examples_query), basket_engine)
        for _, example in examples_df.iterrows():
            print(f"  Basket {example['basket_id']}: {example['console_name']} + {example['game_name']} (Customer: {example['customer_id']})")
    except Exception as e:
        print(f"Örnek sepetler gösterilemedi: {e}")

if __name__ == "__main__":
    add_ps_gta5_baskets() 