import pandas as pd
from sqlalchemy import text, create_engine
import random

def add_gaming_consoles_and_games():
    """Add gaming consoles and games to the database"""
    
    # Database configuration
    product_host = "localhost"
    product_port = 3301
    product_database = "productservicedb"
    username = "root"
    password = "root"
    
    try:
        # Connect to product database
        product_connection_string = f"mysql+mysqlconnector://{username}:{password}@{product_host}:{product_port}/{product_database}"
        product_engine = create_engine(product_connection_string)
        
        print("🎮 Oyun konsolları ve oyunları ekleniyor...")
        
        # Gaming consoles data
        consoles = [
            # PlayStation Consoles
            {
                "product_id": 501,
                "product_name": "PlayStation 5",
                "product_description": "Sony'nin en güçlü oyun konsolu, 4K gaming, ray tracing ve ultra hızlı SSD ile oyun deneyimini yeniden tanımlıyor.",
                "product_image_url": "https://example.com/ps5.jpg",
                "product_model": "PlayStation 5",
                "product_model_year": "2020",
                "product_price": 15999.99,
                "product_quantity": 30,
                "product_sub_category_id": 27  # Oyun Konsolları
            },
            {
                "product_id": 502,
                "product_name": "PlayStation 5 Digital Edition",
                "product_description": "Disk sürücüsü olmayan, dijital oyun odaklı PS5 versiyonu.",
                "product_image_url": "https://example.com/ps5-digital.jpg",
                "product_model": "PlayStation 5 Digital",
                "product_model_year": "2020",
                "product_price": 12999.99,
                "product_quantity": 25,
                "product_sub_category_id": 27
            },
            {
                "product_id": 503,
                "product_name": "PlayStation 4 Pro",
                "product_description": "4K gaming ve HDR desteği ile geliştirilmiş PS4 deneyimi.",
                "product_image_url": "https://example.com/ps4-pro.jpg",
                "product_model": "PlayStation 4 Pro",
                "product_model_year": "2016",
                "product_price": 8999.99,
                "product_quantity": 40,
                "product_sub_category_id": 27
            },
            {
                "product_id": 504,
                "product_name": "PlayStation 4 Slim",
                "product_description": "Kompakt tasarımda tam PS4 deneyimi.",
                "product_image_url": "https://example.com/ps4-slim.jpg",
                "product_model": "PlayStation 4 Slim",
                "product_model_year": "2016",
                "product_price": 6999.99,
                "product_quantity": 50,
                "product_sub_category_id": 27
            },
            {
                "product_id": 505,
                "product_name": "PlayStation 4",
                "product_description": "Klasik PS4 konsolu, güçlü performans ve geniş oyun kütüphanesi.",
                "product_image_url": "https://example.com/ps4.jpg",
                "product_model": "PlayStation 4",
                "product_model_year": "2013",
                "product_price": 5999.99,
                "product_quantity": 35,
                "product_sub_category_id": 27
            },
            {
                "product_id": 506,
                "product_name": "PlayStation 3",
                "product_description": "Blu-ray oynatıcı ve online gaming özellikli klasik konsol.",
                "product_image_url": "https://example.com/ps3.jpg",
                "product_model": "PlayStation 3",
                "product_model_year": "2006",
                "product_price": 2999.99,
                "product_quantity": 20,
                "product_sub_category_id": 27
            },
            
            # Xbox Consoles
            {
                "product_id": 507,
                "product_name": "Xbox Series X",
                "product_description": "Microsoft'un en güçlü konsolu, 4K 120fps gaming ve ray tracing desteği.",
                "product_image_url": "https://example.com/xbox-series-x.jpg",
                "product_model": "Xbox Series X",
                "product_model_year": "2020",
                "product_price": 14999.99,
                "product_quantity": 30,
                "product_sub_category_id": 27
            },
            {
                "product_id": 508,
                "product_name": "Xbox Series S",
                "product_description": "Kompakt tasarımda 1440p gaming deneyimi, Game Pass uyumlu.",
                "product_image_url": "https://example.com/xbox-series-s.jpg",
                "product_model": "Xbox Series S",
                "product_model_year": "2020",
                "product_price": 8999.99,
                "product_quantity": 40,
                "product_sub_category_id": 27
            },
            {
                "product_id": 509,
                "product_name": "Xbox One X",
                "product_description": "4K gaming ve HDR desteği ile geliştirilmiş Xbox One deneyimi.",
                "product_image_url": "https://example.com/xbox-one-x.jpg",
                "product_model": "Xbox One X",
                "product_model_year": "2017",
                "product_price": 7999.99,
                "product_quantity": 35,
                "product_sub_category_id": 27
            },
            {
                "product_id": 510,
                "product_name": "Xbox One S",
                "product_description": "Kompakt tasarımda 4K video desteği ile Xbox One deneyimi.",
                "product_image_url": "https://example.com/xbox-one-s.jpg",
                "product_model": "Xbox One S",
                "product_model_year": "2016",
                "product_price": 5999.99,
                "product_quantity": 45,
                "product_sub_category_id": 27
            },
            {
                "product_id": 511,
                "product_name": "Xbox One",
                "product_description": "Klasik Xbox One konsolu, Kinect uyumlu ve geniş oyun kütüphanesi.",
                "product_image_url": "https://example.com/xbox-one.jpg",
                "product_model": "Xbox One",
                "product_model_year": "2013",
                "product_price": 4999.99,
                "product_quantity": 30,
                "product_sub_category_id": 27
            },
            {
                "product_id": 512,
                "product_name": "Xbox 360",
                "product_description": "Klasik Xbox 360 konsolu, retro gaming deneyimi.",
                "product_image_url": "https://example.com/xbox-360.jpg",
                "product_model": "Xbox 360",
                "product_model_year": "2005",
                "product_price": 1999.99,
                "product_quantity": 25,
                "product_sub_category_id": 27
            }
        ]
        
        # Games data - organized by console compatibility
        games = [
            # PS5 Games
            {
                "product_id": 601,
                "product_name": "God of War Ragnarök",
                "product_description": "Kratos ve Atreus'un epik macerası, PS5'in gücüyle hayat buluyor.",
                "product_image_url": "https://example.com/god-of-war-ragnarok.jpg",
                "product_model": "PlayStation 5",
                "product_model_year": "2022",
                "product_price": 899.99,
                "product_quantity": 100,
                "product_sub_category_id": 28  # Konsol Oyunları
            },
            {
                "product_id": 602,
                "product_name": "Spider-Man 2",
                "product_description": "Peter Parker ve Miles Morales'in birlikte savaştığı açık dünya aksiyon oyunu.",
                "product_image_url": "https://example.com/spider-man-2.jpg",
                "product_model": "PlayStation 5",
                "product_model_year": "2023",
                "product_price": 899.99,
                "product_quantity": 120,
                "product_sub_category_id": 28
            },
            {
                "product_id": 603,
                "product_name": "Final Fantasy XVI",
                "product_description": "Epik fantazi RPG, PS5'in grafik gücüyle destekleniyor.",
                "product_image_url": "https://example.com/final-fantasy-16.jpg",
                "product_model": "PlayStation 5",
                "product_model_year": "2023",
                "product_price": 799.99,
                "product_quantity": 80,
                "product_sub_category_id": 28
            },
            
            # PS4 Games
            {
                "product_id": 604,
                "product_name": "The Last of Us Part II",
                "product_description": "Post-apokaliptik dünyada geçen dramatik aksiyon-macera oyunu.",
                "product_image_url": "https://example.com/last-of-us-2.jpg",
                "product_model": "PlayStation 4",
                "product_model_year": "2020",
                "product_price": 699.99,
                "product_quantity": 150,
                "product_sub_category_id": 28
            },
            {
                "product_id": 605,
                "product_name": "Red Dead Redemption 2",
                "product_description": "Vahşi Batı'da geçen epik açık dünya aksiyon oyunu.",
                "product_image_url": "https://example.com/red-dead-2.jpg",
                "product_model": "PlayStation 4",
                "product_model_year": "2018",
                "product_price": 599.99,
                "product_quantity": 200,
                "product_sub_category_id": 28
            },
            {
                "product_id": 606,
                "product_name": "Uncharted 4: A Thief's End",
                "product_description": "Nathan Drake'in son macerası, aksiyon-macera türünün başyapıtı.",
                "product_image_url": "https://example.com/uncharted-4.jpg",
                "product_model": "PlayStation 4",
                "product_model_year": "2016",
                "product_price": 499.99,
                "product_quantity": 180,
                "product_sub_category_id": 28
            },
            
            # PS3 Games
            {
                "product_id": 607,
                "product_name": "The Last of Us",
                "product_description": "Klasik post-apokaliptik aksiyon-macera oyunu.",
                "product_image_url": "https://example.com/last-of-us-1.jpg",
                "product_model": "PlayStation 3",
                "product_model_year": "2013",
                "product_price": 299.99,
                "product_quantity": 100,
                "product_sub_category_id": 28
            },
            {
                "product_id": 608,
                "product_name": "God of War III",
                "product_description": "Kratos'un Olimpos tanrılarına karşı savaşı.",
                "product_image_url": "https://example.com/god-of-war-3.jpg",
                "product_model": "PlayStation 3",
                "product_model_year": "2010",
                "product_price": 249.99,
                "product_quantity": 80,
                "product_sub_category_id": 28
            },
            
            # Xbox Series X Games
            {
                "product_id": 609,
                "product_name": "Halo Infinite",
                "product_description": "Master Chief'in dönüşü, Xbox Series X'in gücüyle destekleniyor.",
                "product_image_url": "https://example.com/halo-infinite.jpg",
                "product_model": "Xbox Series X",
                "product_model_year": "2021",
                "product_price": 799.99,
                "product_quantity": 120,
                "product_sub_category_id": 28
            },
            {
                "product_id": 610,
                "product_name": "Forza Horizon 5",
                "product_description": "Meksika'da geçen açık dünya yarış oyunu.",
                "product_image_url": "https://example.com/forza-horizon-5.jpg",
                "product_model": "Xbox Series X",
                "product_model_year": "2021",
                "product_price": 699.99,
                "product_quantity": 100,
                "product_sub_category_id": 28
            },
            
            # Xbox One Games
            {
                "product_id": 611,
                "product_name": "Gears 5",
                "product_description": "Epik üçüncü şahıs nişancı oyunu.",
                "product_image_url": "https://example.com/gears-5.jpg",
                "product_model": "Xbox One",
                "product_model_year": "2019",
                "product_price": 599.99,
                "product_quantity": 150,
                "product_sub_category_id": 28
            },
            {
                "product_id": 612,
                "product_name": "Sea of Thieves",
                "product_description": "Çok oyunculu korsan macera oyunu.",
                "product_image_url": "https://example.com/sea-of-thieves.jpg",
                "product_model": "Xbox One",
                "product_model_year": "2018",
                "product_price": 499.99,
                "product_quantity": 120,
                "product_sub_category_id": 28
            },
            
            # Xbox 360 Games
            {
                "product_id": 613,
                "product_name": "Halo 3",
                "product_description": "Master Chief'in klasik macerası.",
                "product_image_url": "https://example.com/halo-3.jpg",
                "product_model": "Xbox 360",
                "product_model_year": "2007",
                "product_price": 199.99,
                "product_quantity": 80,
                "product_sub_category_id": 28
            },
            {
                "product_id": 614,
                "product_name": "Gears of War",
                "product_description": "Epik üçüncü şahıs nişancı serisinin ilk oyunu.",
                "product_image_url": "https://example.com/gears-of-war.jpg",
                "product_model": "Xbox 360",
                "product_model_year": "2006",
                "product_price": 149.99,
                "product_quantity": 60,
                "product_sub_category_id": 28
            },
            
            # Cross-platform Games
            {
                "product_id": 615,
                "product_name": "FIFA 24",
                "product_description": "En güncel futbol simülasyonu, PS5 ve Xbox Series X'te 4K grafiklerle.",
                "product_image_url": "https://example.com/fifa-24.jpg",
                "product_model": "PlayStation 5",
                "product_model_year": "2023",
                "product_price": 899.99,
                "product_quantity": 200,
                "product_sub_category_id": 28
            },
            {
                "product_id": 616,
                "product_name": "FIFA 24",
                "product_description": "En güncel futbol simülasyonu, Xbox Series X'te 4K grafiklerle.",
                "product_image_url": "https://example.com/fifa-24-xbox.jpg",
                "product_model": "Xbox Series X",
                "product_model_year": "2023",
                "product_price": 899.99,
                "product_quantity": 180,
                "product_sub_category_id": 28
            },
            {
                "product_id": 617,
                "product_name": "Call of Duty: Modern Warfare III",
                "product_description": "Modern Warfare serisinin devamı, PS5'te ray tracing ile.",
                "product_image_url": "https://example.com/cod-mw3.jpg",
                "product_model": "PlayStation 5",
                "product_model_year": "2023",
                "product_price": 999.99,
                "product_quantity": 150,
                "product_sub_category_id": 28
            },
            {
                "product_id": 618,
                "product_name": "Call of Duty: Modern Warfare III",
                "product_description": "Modern Warfare serisinin devamı, Xbox Series X'te ray tracing ile.",
                "product_image_url": "https://example.com/cod-mw3-xbox.jpg",
                "product_model": "Xbox Series X",
                "product_model_year": "2023",
                "product_price": 999.99,
                "product_quantity": 140,
                "product_sub_category_id": 28
            }
        ]
        
        # Insert consoles
        print("🎮 Konsollar ekleniyor...")
        for console in consoles:
            insert_console_query = text('''
                INSERT INTO products 
                (product_id, product_name, product_description, product_image_url, product_model, product_model_year, product_price, product_quantity, product_sub_category_id)
                VALUES (:product_id, :product_name, :product_description, :product_image_url, :product_model, :product_model_year, :product_price, :product_quantity, :product_sub_category_id)
            ''')
            
            with product_engine.connect() as conn:
                conn.execute(insert_console_query, console)
                conn.commit()
        
        print(f"✅ {len(consoles)} adet konsol eklendi")
        
        # Insert games
        print("🎮 Oyunlar ekleniyor...")
        for game in games:
            insert_game_query = text('''
                INSERT INTO products 
                (product_id, product_name, product_description, product_image_url, product_model, product_model_year, product_price, product_quantity, product_sub_category_id)
                VALUES (:product_id, :product_name, :product_description, :product_image_url, :product_model, :product_model_year, :product_price, :product_quantity, :product_sub_category_id)
            ''')
            
            with product_engine.connect() as conn:
                conn.execute(insert_game_query, game)
                conn.commit()
        
        print(f"✅ {len(games)} adet oyun eklendi")
        
        # Final statistics
        print(f"\n📊 Final istatistikler:")
        
        # Count total products
        total_query = "SELECT COUNT(*) as total_products FROM products"
        total_count = pd.read_sql(text(total_query), product_engine)
        print(f"Toplam ürün: {total_count.iloc[0]['total_products']}")
        
        # Count consoles
        consoles_query = "SELECT COUNT(*) as total_consoles FROM products WHERE product_sub_category_id = 27"
        consoles_count = pd.read_sql(text(consoles_query), product_engine)
        print(f"Toplam konsol: {consoles_count.iloc[0]['total_consoles']}")
        
        # Count games
        games_query = "SELECT COUNT(*) as total_games FROM products WHERE product_sub_category_id = 28"
        games_count = pd.read_sql(text(games_query), product_engine)
        print(f"Toplam oyun: {games_count.iloc[0]['total_games']}")
        
        # Show some examples
        print(f"\n🎮 Örnek konsollar:")
        consoles_example_query = """
        SELECT product_id, product_name, product_model, product_model_year, product_price
        FROM products 
        WHERE product_sub_category_id = 27
        ORDER BY product_id
        LIMIT 5
        """
        consoles_examples = pd.read_sql(text(consoles_example_query), product_engine)
        for _, console in consoles_examples.iterrows():
            print(f"  {console['product_id']:3d}. {console['product_name']} -> {console['product_model']} ({console['product_model_year']}) - {console['product_price']} TL")
        
        print(f"\n🎮 Örnek oyunlar:")
        games_example_query = """
        SELECT product_id, product_name, product_model, product_model_year, product_price
        FROM products 
        WHERE product_sub_category_id = 28
        ORDER BY product_id
        LIMIT 5
        """
        games_examples = pd.read_sql(text(games_example_query), product_engine)
        for _, game in games_examples.iterrows():
            print(f"  {game['product_id']:3d}. {game['product_name']} -> {game['product_model']} ({game['product_model_year']}) - {game['product_price']} TL")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    add_gaming_consoles_and_games() 