import pandas as pd
from sqlalchemy import text, create_engine
import random
from datetime import datetime, timedelta

def add_halo4_cross_platform():
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

    print("🎮 Halo 4 cross-platform satışı için hazırlık yapılıyor...")

    # 1. Mevcut Halo 4 oyununu bul (Xbox için)
    existing_halo4 = pd.read_sql(
        text("SELECT * FROM products WHERE product_name LIKE '%Halo 4%' AND product_sub_category_id = 28"),
        product_engine
    )
    
    if existing_halo4.empty:
        print("❌ Halo 4 oyunu bulunamadı!")
        return

    print(f"✅ Mevcut Halo 4 oyunları: {len(existing_halo4)}")

    # 2. PlayStation konsollarını bul
    ps_consoles = pd.read_sql(
        text("SELECT * FROM products WHERE product_model LIKE '%PlayStation%' AND product_sub_category_id = 27"),
        product_engine
    )
    
    # 3. Xbox konsollarını bul
    xbox_consoles = pd.read_sql(
        text("SELECT * FROM products WHERE product_model LIKE '%Xbox%' AND product_sub_category_id = 27"),
        product_engine
    )

    print(f"🎮 PlayStation konsolları: {len(ps_consoles)}")
    print(f"🎮 Xbox konsolları: {len(xbox_consoles)}")

    # 4. PlayStation için Halo 4 oyunları ekle
    print("\n🎮 PlayStation için Halo 4 oyunları ekleniyor...")
    
    # Mevcut max product_id'yi bul
    max_id_query = "SELECT MAX(product_id) as max_id FROM products"
    max_id_result = pd.read_sql(text(max_id_query), product_engine)
    next_id = int(max_id_result.iloc[0]['max_id']) + 1

    ps_halo4_games = []
    
    for _, console in ps_consoles.iterrows():
        # Her PlayStation konsolu için Halo 4 oyunu oluştur
        halo4_game = {
            "product_id": next_id,
            "product_name": "Halo 4",
            "product_description": "Master Chief'in yeni macerası, PlayStation versiyonu.",
            "product_image_url": "https://example.com/halo-4-ps.jpg",
            "product_model": console['product_model'],
            "product_model_year": console['product_model_year'],
            "product_price": 299.99,  # PlayStation versiyonu biraz daha ucuz
            "product_quantity": 100,
            "product_sub_category_id": 28
        }
        
        ps_halo4_games.append(halo4_game)
        next_id += 1

    # PlayStation Halo 4 oyunlarını ekle
    with product_engine.connect() as conn:
        for game in ps_halo4_games:
            insert_game_query = text('''
                INSERT INTO products 
                (product_id, product_name, product_description, product_image_url, product_model, product_model_year, product_price, product_quantity, product_sub_category_id)
                VALUES (:product_id, :product_name, :product_description, :product_image_url, :product_model, :product_model_year, :product_price, :product_quantity, :product_sub_category_id)
            ''')
            conn.execute(insert_game_query, game)
        conn.commit()

    print(f"✅ {len(ps_halo4_games)} adet PlayStation Halo 4 oyunu eklendi")

    # 5. Şimdi tüm Halo 4 oyunlarını al (Xbox + PlayStation)
    all_halo4_games = pd.read_sql(
        text("SELECT * FROM products WHERE product_name LIKE '%Halo 4%' AND product_sub_category_id = 28"),
        product_engine
    )
    
    print(f"🎮 Toplam Halo 4 oyunları: {len(all_halo4_games)}")

    # 6. Her konsol için Halo 4 ile sepetler oluştur
    basket_count_per_console = 12  # Her konsol için 12 sepet
    total_baskets = 0
    total_units = 0
    next_unit_id = pd.read_sql(text("SELECT IFNULL(MAX(basket_product_unit_id),0)+1 as next_id FROM basket_product_units"), basket_engine).iloc[0]['next_id']

    # Tüm konsolları birleştir
    all_consoles = pd.concat([ps_consoles, xbox_consoles], ignore_index=True)

    for _, console in all_consoles.iterrows():
        console_id = int(console['product_id'])
        console_name = console['product_name']
        console_model = console['product_model']
        console_year = console['product_model_year']
        console_price = float(console['product_price'])
        
        print(f"\n🎮 {console_name} + Halo 4 için sepetler oluşturuluyor...")
        
        # Bu konsol için Halo 4 oyununu bul
        halo4_for_console = all_halo4_games[all_halo4_games['product_model'] == console_model]
        
        if halo4_for_console.empty:
            print(f"⚠️ {console_model} için Halo 4 bulunamadı, atlanıyor...")
            continue
        
        halo4_game = halo4_for_console.iloc[0]
        halo4_id = int(halo4_game['product_id'])
        halo4_name = halo4_game['product_name']
        halo4_price = float(halo4_game['product_price'])
        
        basket_ids = []
        
        # Önce bu konsol için baskets'leri oluştur
        with basket_engine.connect() as conn:
            for i in range(basket_count_per_console):
                customer_id = 4000 + total_baskets + i  # Halo 4 kullanıcıları için farklı ID aralığı
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

        print(f"✅ {len(basket_ids)} adet {console_name} + Halo 4 basket'i oluşturuldu")

        # Her basket için konsol ve Halo 4 ekle
        basket_product_units_rows = []
        
        for basket_id in basket_ids:
            # Her sepete 1 konsol ekle
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
            
            # Her sepete 1 Halo 4 oyunu ekle
            basket_product_units_rows.append({
                'basket_product_unit_id': int(next_unit_id),
                'basket_id': basket_id,
                'product_id': halo4_id,
                'product_name': halo4_name,
                'product_model': halo4_game['product_model'],
                'product_model_year': halo4_game['product_model_year'],
                'product_quantity': 1,
                'product_total_price': halo4_price,
                'product_unit_price': halo4_price
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
        print(f"✅ {len(basket_product_units_rows)} adet ürün ({console_name} + Halo 4) sepetlerine eklendi")

    print(f"\n🎮 TOPLAM SONUÇLAR:")
    print(f"✅ {len(ps_halo4_games)} adet PlayStation Halo 4 oyunu eklendi")
    print(f"✅ {total_baskets} adet konsol + Halo 4 sepeti oluşturuldu")
    print(f"✅ {total_units} adet ürün basket_product_units'e eklendi")
    print(f"🎮 Halo 4 cross-platform satışı başarıyla tamamlandı!")

    # 7. Örnek sepetleri göster
    print(f"\n📊 Örnek Halo 4 sepetleri:")
    examples_query = """
    SELECT 
        b.basket_id,
        b.customer_id,
        bpu1.product_name as console_name,
        bpu1.product_model as console_model,
        bpu2.product_name as game_name,
        bpu2.product_model as game_model
    FROM baskets b
    JOIN basket_product_units bpu1 ON b.basket_id = bpu1.basket_id 
    JOIN basket_product_units bpu2 ON b.basket_id = bpu2.basket_id 
    WHERE b.customer_id >= 4000 
    AND bpu2.product_name LIKE '%Halo 4%'
    AND bpu1.product_name != bpu2.product_name
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
    add_halo4_cross_platform() 