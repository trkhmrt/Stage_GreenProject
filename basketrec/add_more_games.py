import pandas as pd
from sqlalchemy import text, create_engine
import random

def add_more_games():
    """Add many more games to the database"""
    
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
        
        print("🎮 Daha fazla oyun ekleniyor...")
        
        # Get current max product_id
        max_id_query = "SELECT MAX(product_id) as max_id FROM products"
        max_id_result = pd.read_sql(text(max_id_query), product_engine)
        current_max_id = int(max_id_result.iloc[0]['max_id'])
        next_id = current_max_id + 1
        
        # Games data - organized by console compatibility
        games = [
            # PS5 Games
            {
                "product_id": next_id,
                "product_name": "Marvel's Spider-Man: Miles Morales",
                "product_description": "Miles Morales'in hikayesi, PS5'in gücüyle hayat buluyor.",
                "product_image_url": "https://example.com/spider-man-miles-morales.jpg",
                "product_model": "PlayStation 5",
                "product_model_year": "2020",
                "product_price": 799.99,
                "product_quantity": 150,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 1,
                "product_name": "Demon's Souls",
                "product_description": "Klasik Souls oyununun PS5 için yeniden yapılmış versiyonu.",
                "product_image_url": "https://example.com/demons-souls.jpg",
                "product_model": "PlayStation 5",
                "product_model_year": "2020",
                "product_price": 899.99,
                "product_quantity": 100,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 2,
                "product_name": "Ratchet & Clank: Rift Apart",
                "product_description": "Dimension hopping aksiyon-macera oyunu.",
                "product_image_url": "https://example.com/ratchet-clank-rift-apart.jpg",
                "product_model": "PlayStation 5",
                "product_model_year": "2021",
                "product_price": 899.99,
                "product_quantity": 120,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 3,
                "product_name": "Returnal",
                "product_description": "Roguelike üçüncü şahıs nişancı oyunu.",
                "product_image_url": "https://example.com/returnal.jpg",
                "product_model": "PlayStation 5",
                "product_model_year": "2021",
                "product_price": 799.99,
                "product_quantity": 80,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 4,
                "product_name": "Horizon Forbidden West",
                "product_description": "Aloy'un yeni macerası, açık dünya aksiyon RPG.",
                "product_image_url": "https://example.com/horizon-forbidden-west.jpg",
                "product_model": "PlayStation 5",
                "product_model_year": "2022",
                "product_price": 899.99,
                "product_quantity": 200,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 5,
                "product_name": "Gran Turismo 7",
                "product_description": "Gerçekçi yarış simülasyonu, PS5'in gücüyle.",
                "product_image_url": "https://example.com/gran-turismo-7.jpg",
                "product_model": "PlayStation 5",
                "product_model_year": "2022",
                "product_price": 899.99,
                "product_quantity": 180,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 6,
                "product_name": "Ghost of Tsushima Director's Cut",
                "product_description": "Samuray aksiyon-macera oyununun geliştirilmiş versiyonu.",
                "product_image_url": "https://example.com/ghost-of-tsushima-directors-cut.jpg",
                "product_model": "PlayStation 5",
                "product_model_year": "2021",
                "product_price": 799.99,
                "product_quantity": 160,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 7,
                "product_name": "Death Stranding Director's Cut",
                "product_description": "Hideo Kojima'nın post-apokaliptik aksiyon oyunu.",
                "product_image_url": "https://example.com/death-stranding-directors-cut.jpg",
                "product_model": "PlayStation 5",
                "product_model_year": "2021",
                "product_price": 699.99,
                "product_quantity": 90,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 8,
                "product_name": "Resident Evil 4 Remake",
                "product_description": "Klasik survival horror oyununun yeniden yapılmış versiyonu.",
                "product_image_url": "https://example.com/resident-evil-4-remake.jpg",
                "product_model": "PlayStation 5",
                "product_model_year": "2023",
                "product_price": 999.99,
                "product_quantity": 140,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 9,
                "product_name": "Street Fighter 6",
                "product_description": "Klasik dövüş oyunu serisinin en yeni versiyonu.",
                "product_image_url": "https://example.com/street-fighter-6.jpg",
                "product_model": "PlayStation 5",
                "product_model_year": "2023",
                "product_price": 899.99,
                "product_quantity": 110,
                "product_sub_category_id": 28
            },
            
            # PS4 Games
            {
                "product_id": next_id + 10,
                "product_name": "God of War",
                "product_description": "Kratos'un yeni macerası, İskandinav mitolojisinde.",
                "product_image_url": "https://example.com/god-of-war-2018.jpg",
                "product_model": "PlayStation 4",
                "product_model_year": "2018",
                "product_price": 599.99,
                "product_quantity": 250,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 11,
                "product_name": "Horizon Zero Dawn",
                "product_description": "Robot dinozorlarla dolu açık dünya aksiyon RPG.",
                "product_image_url": "https://example.com/horizon-zero-dawn.jpg",
                "product_model": "PlayStation 4",
                "product_model_year": "2017",
                "product_price": 499.99,
                "product_quantity": 300,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 12,
                "product_name": "Bloodborne",
                "product_description": "Gothic horror aksiyon RPG, Souls serisinin ruhani devamı.",
                "product_image_url": "https://example.com/bloodborne.jpg",
                "product_model": "PlayStation 4",
                "product_model_year": "2015",
                "product_price": 399.99,
                "product_quantity": 180,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 13,
                "product_name": "Persona 5 Royal",
                "product_description": "Japon RPG, geliştirilmiş versiyon.",
                "product_image_url": "https://example.com/persona-5-royal.jpg",
                "product_model": "PlayStation 4",
                "product_model_year": "2020",
                "product_price": 699.99,
                "product_quantity": 120,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 14,
                "product_name": "Death Stranding",
                "product_description": "Hideo Kojima'nın post-apokaliptik aksiyon oyunu.",
                "product_image_url": "https://example.com/death-stranding.jpg",
                "product_model": "PlayStation 4",
                "product_model_year": "2019",
                "product_price": 599.99,
                "product_quantity": 150,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 15,
                "product_name": "Days Gone",
                "product_description": "Zombi apokaliptik açık dünya aksiyon oyunu.",
                "product_image_url": "https://example.com/days-gone.jpg",
                "product_model": "PlayStation 4",
                "product_model_year": "2019",
                "product_price": 499.99,
                "product_quantity": 200,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 16,
                "product_name": "Ghost of Tsushima",
                "product_description": "Samuray aksiyon-macera oyunu.",
                "product_image_url": "https://example.com/ghost-of-tsushima.jpg",
                "product_model": "PlayStation 4",
                "product_model_year": "2020",
                "product_price": 699.99,
                "product_quantity": 180,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 17,
                "product_name": "Spider-Man",
                "product_description": "Marvel's Spider-Man, açık dünya aksiyon oyunu.",
                "product_image_url": "https://example.com/spider-man.jpg",
                "product_model": "PlayStation 4",
                "product_model_year": "2018",
                "product_price": 599.99,
                "product_quantity": 220,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 18,
                "product_name": "Uncharted: The Lost Legacy",
                "product_description": "Chloe ve Nadine'in macerası.",
                "product_image_url": "https://example.com/uncharted-lost-legacy.jpg",
                "product_model": "PlayStation 4",
                "product_model_year": "2017",
                "product_price": 399.99,
                "product_quantity": 160,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 19,
                "product_name": "Infamous: Second Son",
                "product_description": "Süper güçlü açık dünya aksiyon oyunu.",
                "product_image_url": "https://example.com/infamous-second-son.jpg",
                "product_model": "PlayStation 4",
                "product_model_year": "2014",
                "product_price": 299.99,
                "product_quantity": 140,
                "product_sub_category_id": 28
            },
            
            # PS3 Games
            {
                "product_id": next_id + 20,
                "product_name": "Uncharted 3: Drake's Deception",
                "product_description": "Nathan Drake'in üçüncü macerası.",
                "product_image_url": "https://example.com/uncharted-3.jpg",
                "product_model": "PlayStation 3",
                "product_model_year": "2011",
                "product_price": 199.99,
                "product_quantity": 80,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 21,
                "product_name": "Uncharted 2: Among Thieves",
                "product_description": "Nathan Drake'in ikinci macerası.",
                "product_image_url": "https://example.com/uncharted-2.jpg",
                "product_model": "PlayStation 3",
                "product_model_year": "2009",
                "product_price": 149.99,
                "product_quantity": 70,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 22,
                "product_name": "Metal Gear Solid 4: Guns of the Patriots",
                "product_description": "Solid Snake'in son macerası.",
                "product_image_url": "https://example.com/metal-gear-solid-4.jpg",
                "product_model": "PlayStation 3",
                "product_model_year": "2008",
                "product_price": 199.99,
                "product_quantity": 60,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 23,
                "product_name": "LittleBigPlanet",
                "product_description": "Yaratıcı platform oyunu.",
                "product_image_url": "https://example.com/littlebigplanet.jpg",
                "product_model": "PlayStation 3",
                "product_model_year": "2008",
                "product_price": 149.99,
                "product_quantity": 100,
                "product_sub_category_id": 28
            },
            
            # Xbox Series X Games
            {
                "product_id": next_id + 24,
                "product_name": "Starfield",
                "product_description": "Bethesda'nın uzay RPG'si.",
                "product_image_url": "https://example.com/starfield.jpg",
                "product_model": "Xbox Series X",
                "product_model_year": "2023",
                "product_price": 999.99,
                "product_quantity": 200,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 25,
                "product_name": "Redfall",
                "product_description": "Vampir avcısı açık dünya aksiyon oyunu.",
                "product_image_url": "https://example.com/redfall.jpg",
                "product_model": "Xbox Series X",
                "product_model_year": "2023",
                "product_price": 899.99,
                "product_quantity": 150,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 26,
                "product_name": "Microsoft Flight Simulator",
                "product_description": "Gerçekçi uçuş simülasyonu.",
                "product_image_url": "https://example.com/microsoft-flight-simulator.jpg",
                "product_model": "Xbox Series X",
                "product_model_year": "2021",
                "product_price": 799.99,
                "product_quantity": 80,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 27,
                "product_name": "Psychonauts 2",
                "product_description": "Psikolojik platform oyunu.",
                "product_image_url": "https://example.com/psychonauts-2.jpg",
                "product_model": "Xbox Series X",
                "product_model_year": "2021",
                "product_price": 599.99,
                "product_quantity": 90,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 28,
                "product_name": "The Medium",
                "product_description": "Psikolojik korku oyunu.",
                "product_image_url": "https://example.com/the-medium.jpg",
                "product_model": "Xbox Series X",
                "product_model_year": "2021",
                "product_price": 699.99,
                "product_quantity": 70,
                "product_sub_category_id": 28
            },
            
            # Xbox One Games
            {
                "product_id": next_id + 29,
                "product_name": "Halo: The Master Chief Collection",
                "product_description": "Tüm Halo oyunlarının toplandığı koleksiyon.",
                "product_image_url": "https://example.com/halo-master-chief-collection.jpg",
                "product_model": "Xbox One",
                "product_model_year": "2014",
                "product_price": 499.99,
                "product_quantity": 300,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 30,
                "product_name": "Forza Horizon 4",
                "product_description": "İngiltere'de geçen açık dünya yarış oyunu.",
                "product_image_url": "https://example.com/forza-horizon-4.jpg",
                "product_model": "Xbox One",
                "product_model_year": "2018",
                "product_price": 599.99,
                "product_quantity": 250,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 31,
                "product_name": "Gears of War 4",
                "product_description": "Gears serisinin dördüncü oyunu.",
                "product_image_url": "https://example.com/gears-of-war-4.jpg",
                "product_model": "Xbox One",
                "product_model_year": "2016",
                "product_price": 499.99,
                "product_quantity": 200,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 32,
                "product_name": "Quantum Break",
                "product_description": "Zaman manipülasyonu aksiyon oyunu.",
                "product_image_url": "https://example.com/quantum-break.jpg",
                "product_model": "Xbox One",
                "product_model_year": "2016",
                "product_price": 399.99,
                "product_quantity": 120,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 33,
                "product_name": "Sunset Overdrive",
                "product_description": "Açık dünya aksiyon oyunu.",
                "product_image_url": "https://example.com/sunset-overdrive.jpg",
                "product_model": "Xbox One",
                "product_model_year": "2014",
                "product_price": 299.99,
                "product_quantity": 100,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 34,
                "product_name": "Ryse: Son of Rome",
                "product_description": "Roma dönemi aksiyon oyunu.",
                "product_image_url": "https://example.com/ryse-son-of-rome.jpg",
                "product_model": "Xbox One",
                "product_model_year": "2013",
                "product_price": 249.99,
                "product_quantity": 80,
                "product_sub_category_id": 28
            },
            
            # Xbox 360 Games
            {
                "product_id": next_id + 35,
                "product_name": "Halo: Reach",
                "product_description": "Halo serisinin prequel oyunu.",
                "product_image_url": "https://example.com/halo-reach.jpg",
                "product_model": "Xbox 360",
                "product_model_year": "2010",
                "product_price": 199.99,
                "product_quantity": 120,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 36,
                "product_name": "Halo 4",
                "product_description": "Master Chief'in yeni macerası.",
                "product_image_url": "https://example.com/halo-4.jpg",
                "product_model": "Xbox 360",
                "product_model_year": "2012",
                "product_price": 249.99,
                "product_quantity": 150,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 37,
                "product_name": "Gears of War 2",
                "product_description": "Gears serisinin ikinci oyunu.",
                "product_image_url": "https://example.com/gears-of-war-2.jpg",
                "product_model": "Xbox 360",
                "product_model_year": "2008",
                "product_price": 149.99,
                "product_quantity": 100,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 38,
                "product_name": "Gears of War 3",
                "product_description": "Gears serisinin üçüncü oyunu.",
                "product_image_url": "https://example.com/gears-of-war-3.jpg",
                "product_model": "Xbox 360",
                "product_model_year": "2011",
                "product_price": 199.99,
                "product_quantity": 110,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 39,
                "product_name": "Fable II",
                "product_description": "Fantazi RPG oyunu.",
                "product_image_url": "https://example.com/fable-2.jpg",
                "product_model": "Xbox 360",
                "product_model_year": "2008",
                "product_price": 149.99,
                "product_quantity": 80,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 40,
                "product_name": "Fable III",
                "product_description": "Fable serisinin üçüncü oyunu.",
                "product_image_url": "https://example.com/fable-3.jpg",
                "product_model": "Xbox 360",
                "product_model_year": "2010",
                "product_price": 179.99,
                "product_quantity": 90,
                "product_sub_category_id": 28
            },
            
            # Cross-platform Games - PS5
            {
                "product_id": next_id + 41,
                "product_name": "Cyberpunk 2077",
                "product_description": "Cyberpunk RPG, PS5'te ray tracing ile.",
                "product_image_url": "https://example.com/cyberpunk-2077-ps5.jpg",
                "product_model": "PlayStation 5",
                "product_model_year": "2022",
                "product_price": 899.99,
                "product_quantity": 180,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 42,
                "product_name": "Assassin's Creed Valhalla",
                "product_description": "Viking dönemi açık dünya aksiyon oyunu.",
                "product_image_url": "https://example.com/assassins-creed-valhalla-ps5.jpg",
                "product_model": "PlayStation 5",
                "product_model_year": "2020",
                "product_price": 799.99,
                "product_quantity": 200,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 43,
                "product_name": "Watch Dogs: Legion",
                "product_description": "Londra'da geçen siberpunk aksiyon oyunu.",
                "product_image_url": "https://example.com/watch-dogs-legion-ps5.jpg",
                "product_model": "PlayStation 5",
                "product_model_year": "2020",
                "product_price": 699.99,
                "product_quantity": 160,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 44,
                "product_name": "Control Ultimate Edition",
                "product_description": "Psikolojik aksiyon oyunu.",
                "product_image_url": "https://example.com/control-ultimate-ps5.jpg",
                "product_model": "PlayStation 5",
                "product_model_year": "2021",
                "product_price": 599.99,
                "product_quantity": 120,
                "product_sub_category_id": 28
            },
            
            # Cross-platform Games - Xbox Series X
            {
                "product_id": next_id + 45,
                "product_name": "Cyberpunk 2077",
                "product_description": "Cyberpunk RPG, Xbox Series X'te ray tracing ile.",
                "product_image_url": "https://example.com/cyberpunk-2077-xbox.jpg",
                "product_model": "Xbox Series X",
                "product_model_year": "2022",
                "product_price": 899.99,
                "product_quantity": 170,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 46,
                "product_name": "Assassin's Creed Valhalla",
                "product_description": "Viking dönemi açık dünya aksiyon oyunu.",
                "product_image_url": "https://example.com/assassins-creed-valhalla-xbox.jpg",
                "product_model": "Xbox Series X",
                "product_model_year": "2020",
                "product_price": 799.99,
                "product_quantity": 190,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 47,
                "product_name": "Watch Dogs: Legion",
                "product_description": "Londra'da geçen siberpunk aksiyon oyunu.",
                "product_image_url": "https://example.com/watch-dogs-legion-xbox.jpg",
                "product_model": "Xbox Series X",
                "product_model_year": "2020",
                "product_price": 699.99,
                "product_quantity": 150,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 48,
                "product_name": "Control Ultimate Edition",
                "product_description": "Psikolojik aksiyon oyunu.",
                "product_image_url": "https://example.com/control-ultimate-xbox.jpg",
                "product_model": "Xbox Series X",
                "product_model_year": "2021",
                "product_price": 599.99,
                "product_quantity": 110,
                "product_sub_category_id": 28
            },
            
            # Cross-platform Games - PS4
            {
                "product_id": next_id + 49,
                "product_name": "The Witcher 3: Wild Hunt",
                "product_description": "Epik fantazi RPG oyunu.",
                "product_image_url": "https://example.com/witcher-3-ps4.jpg",
                "product_model": "PlayStation 4",
                "product_model_year": "2015",
                "product_price": 399.99,
                "product_quantity": 400,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 50,
                "product_name": "Grand Theft Auto V",
                "product_description": "Açık dünya aksiyon oyunu.",
                "product_image_url": "https://example.com/gta-5-ps4.jpg",
                "product_model": "PlayStation 4",
                "product_model_year": "2014",
                "product_price": 299.99,
                "product_quantity": 500,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 51,
                "product_name": "Fallout 4",
                "product_description": "Post-apokaliptik RPG oyunu.",
                "product_image_url": "https://example.com/fallout-4-ps4.jpg",
                "product_model": "PlayStation 4",
                "product_model_year": "2015",
                "product_price": 349.99,
                "product_quantity": 300,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 52,
                "product_name": "Skyrim Special Edition",
                "product_description": "Fantazi RPG oyununun geliştirilmiş versiyonu.",
                "product_image_url": "https://example.com/skyrim-special-ps4.jpg",
                "product_model": "PlayStation 4",
                "product_model_year": "2016",
                "product_price": 399.99,
                "product_quantity": 350,
                "product_sub_category_id": 28
            },
            
            # Cross-platform Games - Xbox One
            {
                "product_id": next_id + 53,
                "product_name": "The Witcher 3: Wild Hunt",
                "product_description": "Epik fantazi RPG oyunu.",
                "product_image_url": "https://example.com/witcher-3-xbox.jpg",
                "product_model": "Xbox One",
                "product_model_year": "2015",
                "product_price": 399.99,
                "product_quantity": 380,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 54,
                "product_name": "Grand Theft Auto V",
                "product_description": "Açık dünya aksiyon oyunu.",
                "product_image_url": "https://example.com/gta-5-xbox.jpg",
                "product_model": "Xbox One",
                "product_model_year": "2014",
                "product_price": 299.99,
                "product_quantity": 480,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 55,
                "product_name": "Fallout 4",
                "product_description": "Post-apokaliptik RPG oyunu.",
                "product_image_url": "https://example.com/fallout-4-xbox.jpg",
                "product_model": "Xbox One",
                "product_model_year": "2015",
                "product_price": 349.99,
                "product_quantity": 280,
                "product_sub_category_id": 28
            },
            {
                "product_id": next_id + 56,
                "product_name": "Skyrim Special Edition",
                "product_description": "Fantazi RPG oyununun geliştirilmiş versiyonu.",
                "product_image_url": "https://example.com/skyrim-special-xbox.jpg",
                "product_model": "Xbox One",
                "product_model_year": "2016",
                "product_price": 399.99,
                "product_quantity": 320,
                "product_sub_category_id": 28
            }
        ]
        
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
        
        print(f"✅ {len(games)} adet yeni oyun eklendi")
        
        # Final statistics
        print(f"\n📊 Final istatistikler:")
        
        # Count total products
        total_query = "SELECT COUNT(*) as total_products FROM products"
        total_count = pd.read_sql(text(total_query), product_engine)
        print(f"Toplam ürün: {total_count.iloc[0]['total_products']}")
        
        # Count games
        games_query = "SELECT COUNT(*) as total_games FROM products WHERE product_sub_category_id = 28"
        games_count = pd.read_sql(text(games_query), product_engine)
        print(f"Toplam oyun: {games_count.iloc[0]['total_games']}")
        
        # Count consoles
        consoles_query = "SELECT COUNT(*) as total_consoles FROM products WHERE product_sub_category_id = 27"
        consoles_count = pd.read_sql(text(consoles_query), product_engine)
        print(f"Toplam konsol: {consoles_count.iloc[0]['total_consoles']}")
        
        # Show some examples
        print(f"\n🎮 Örnek yeni oyunlar:")
        examples_query = """
        SELECT product_id, product_name, product_model, product_model_year, product_price
        FROM products 
        WHERE product_sub_category_id = 28
        ORDER BY product_id DESC
        LIMIT 10
        """
        examples_df = pd.read_sql(text(examples_query), product_engine)
        for _, game in examples_df.iterrows():
            print(f"  {game['product_id']:3d}. {game['product_name']} -> {game['product_model']} ({game['product_model_year']}) - {game['product_price']} TL")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    add_more_games() 