import pandas as pd
from sqlalchemy import text, create_engine
import random

def enhance_products():
    """Add more products, categories, and subcategories to enhance recommendations"""
    
    # Database configuration
    host = "localhost"
    port = 3301
    database = "productservicedb"
    username = "root"
    password = "root"
    
    try:
        # Connect to database
        connection_string = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}"
        engine = create_engine(connection_string)
        
        print("🔍 Adding new categories and subcategories...")
        
        # Add new categories
        new_categories = [
            (9, 'Teknoloji & Aksesuar'),
            (10, 'Ev & Bahçe'),
            (11, 'Spor & Fitness'),
            (12, 'Kozmetik & Bakım'),
            (13, 'Oyuncak & Hobi'),
            (14, 'Otomotiv & Ulaşım'),
            (15, 'Müzik & Sanat'),
            (16, 'Ofis & İş')
        ]
        
        with engine.connect() as conn:
            for cat_id, cat_name in new_categories:
                try:
                    insert_cat_query = text("""
                        INSERT INTO categories (category_id, category_name) 
                        VALUES (:category_id, :category_name)
                        ON DUPLICATE KEY UPDATE category_name = :category_name
                    """)
                    conn.execute(insert_cat_query, {'category_id': cat_id, 'category_name': cat_name})
                except:
                    pass  # Category might already exist
        
        # Add new subcategories
        new_subcategories = [
            # Teknoloji & Aksesuar
            (33, 'Akıllı Ev Sistemleri', 9),
            (34, 'Gaming Ekipmanları', 9),
            (35, 'Mobil Aksesuarlar', 9),
            (36, 'Ses Sistemleri', 9),
            
            # Ev & Bahçe
            (37, 'Bahçe Mobilyası', 10),
            (38, 'Bahçe Dekorasyonu', 10),
            (39, 'Ev Güvenlik', 10),
            (40, 'Temizlik Ekipmanları', 10),
            
            # Spor & Fitness
            (41, 'Yoga & Pilates', 11),
            (42, 'Koşu Ekipmanları', 11),
            (43, 'Su Sporları', 11),
            (44, 'Takım Sporları', 11),
            
            # Kozmetik & Bakım
            (45, 'Cilt Bakımı', 12),
            (46, 'Saç Bakımı', 12),
            (47, 'Makyaj', 12),
            (48, 'Parfüm & Deodorant', 12),
            
            # Oyuncak & Hobi
            (49, 'Eğitici Oyuncaklar', 13),
            (50, 'Puzzle & Oyunlar', 13),
            (51, 'Koleksiyon', 13),
            (52, 'El Sanatları', 13),
            
            # Otomotiv & Ulaşım
            (53, 'Araba Aksesuarları', 14),
            (54, 'Motosiklet Ekipmanları', 14),
            (55, 'Bisiklet Aksesuarları', 14),
            (56, 'Seyahat Ekipmanları', 14),
            
            # Müzik & Sanat
            (57, 'Müzik Aletleri', 15),
            (58, 'Sanat Malzemeleri', 15),
            (59, 'Fotoğrafçılık', 15),
            (60, 'Dans & Tiyatro', 15),
            
            # Ofis & İş
            (61, 'Ofis Mobilyası', 16),
            (62, 'Yazıcı & Tarayıcı', 16),
            (63, 'Ofis Aksesuarları', 16),
            (64, 'İş Güvenliği', 16)
        ]
        
        with engine.connect() as conn:
            for sub_cat_id, sub_cat_name, cat_id in new_subcategories:
                try:
                    insert_subcat_query = text("""
                        INSERT INTO sub_categories (sub_category_id, sub_category_name, category_id) 
                        VALUES (:sub_category_id, :sub_category_name, :category_id)
                        ON DUPLICATE KEY UPDATE sub_category_name = :sub_category_name, category_id = :category_id
                    """)
                    conn.execute(insert_subcat_query, {
                        'sub_category_id': sub_cat_id, 
                        'sub_category_name': sub_cat_name, 
                        'category_id': cat_id
                    })
                except:
                    pass  # Subcategory might already exist
        
        conn.commit()
        print("✅ New categories and subcategories added!")
        
        # Get current product count
        current_count_query = "SELECT COUNT(*) as count FROM products"
        current_count_result = pd.read_sql(text(current_count_query), engine)
        current_count = current_count_result.iloc[0]['count']
        
        print(f"📊 Current product count: {current_count}")
        
        # Enhanced product templates
        enhanced_templates = {
            'Teknoloji & Aksesuar': [
                'Akıllı Ev Hub', 'Gaming Mouse', 'Gaming Keyboard', 'Gaming Headset', 'Gaming Monitor',
                'Mobil Şarj Cihazı', 'Bluetooth Kulaklık', 'Kablosuz Şarj', 'Akıllı Saat', 'Fitness Tracker',
                'Akıllı Hoparlör', 'Soundbar', 'Kablosuz Kulaklık', 'Mikrofon', 'Webcam', 'Streaming Mikrofon'
            ],
            'Ev & Bahçe': [
                'Bahçe Masası', 'Bahçe Sandalyesi', 'Bahçe Şemsiyesi', 'Bahçe Lambası', 'Bahçe Çit',
                'Akıllı Kilit', 'Güvenlik Kamerası', 'Alarm Sistemi', 'Robot Süpürge', 'Buharlı Temizleyici',
                'Vakum Temizleyici', 'Çamaşır Makinesi', 'Bulaşık Makinesi', 'Fırın', 'Mikrodalga'
            ],
            'Spor & Fitness': [
                'Yoga Matı', 'Pilates Topu', 'Dumbbell Set', 'Koşu Bandı', 'Bisiklet',
                'Su Matarası', 'Spor Çantası', 'Spor Ayakkabı', 'Fitness Tracker', 'Protein Tozu',
                'Koşu Şortu', 'Spor T-Shirt', 'Yoga Pantolonu', 'Pilates Bandı', 'Ağırlık Plakası'
            ],
            'Kozmetik & Bakım': [
                'Nemlendirici Krem', 'Güneş Kremi', 'Serum', 'Tonik', 'Peeling',
                'Şampuan', 'Saç Kremi', 'Saç Maskesi', 'Saç Fırçası', 'Saç Kurutma Makinesi',
                'Ruj', 'Maskara', 'Fondöten', 'Göz Farı', 'Tırnak Ojesi', 'Parfüm'
            ],
            'Oyuncak & Hobi': [
                'Eğitici Puzzle', 'Lego Seti', 'Robot Kit', 'Bilim Seti', 'Sanat Seti',
                'Koleksiyon Figürü', 'Model Araba', 'Kart Oyunu', 'Strateji Oyunu', 'El Sanatı Seti',
                'Boyama Kitabı', 'Origami Seti', 'Maket Seti', 'Müzik Kutusu', 'Oyuncak Piyano'
            ],
            'Otomotiv & Ulaşım': [
                'Araba Koltuğu', 'Araba Şarj Cihazı', 'Araba Hoparlörü', 'Araba Temizlik Seti',
                'Motosiklet Kaskı', 'Motosiklet Eldiveni', 'Motosiklet Montu', 'Motosiklet Botu',
                'Bisiklet Kaskı', 'Bisiklet Lambası', 'Bisiklet Çantası', 'Bisiklet Kilidi',
                'Seyahat Çantası', 'Seyahat Yastığı', 'Seyahat Adaptörü', 'Seyahat Organizatörü'
            ],
            'Müzik & Sanat': [
                'Gitar', 'Piyano', 'Keman', 'Flüt', 'Davul Seti', 'Synthesizer',
                'Resim Fırçası', 'Boya Seti', 'Tuval', 'Çizim Kalemi', 'Hobi Bıçağı',
                'DSLR Kamera', 'Aksiyon Kamerası', 'Tripod', 'Kamera Çantası', 'Lens',
                'Dans Ayakkabısı', 'Tiyatro Kostümü', 'Makyaj Seti', 'Peruk', 'Aksesuar'
            ],
            'Ofis & İş': [
                'Ofis Koltuğu', 'Ofis Masası', 'Dosya Dolabı', 'Ofis Lambası', 'Ofis Çiçeği',
                'Lazer Yazıcı', 'Mürekkep Püskürtmeli Yazıcı', 'Tarayıcı', 'Fotokopi Makinesi',
                'Ofis Kalemi', 'Not Defteri', 'Dosya Organizatörü', 'Pano', 'Takvim',
                'İş Güvenliği Gözlüğü', 'İş Eldiveni', 'Güvenlik Ayakkabısı', 'İş Montu'
            ]
        }
        
        # Get existing subcategories
        sub_categories_query = """
        SELECT 
            sc.sub_category_id,
            sc.sub_category_name,
            c.category_name
        FROM sub_categories sc
        LEFT JOIN categories c ON sc.category_id = c.category_id
        ORDER BY sc.sub_category_id
        """
        sub_categories_df = pd.read_sql(text(sub_categories_query), engine)
        
        print(f"📊 Found {len(sub_categories_df)} subcategories")
        
        # Create additional products
        print("\n🔄 Creating additional products...")
        
        new_products = []
        product_id = current_count + 1
        
        # Create products for new subcategories
        for _, sub_cat in sub_categories_df.iterrows():
            category_name = sub_cat['category_name']
            sub_category_name = sub_cat['sub_category_name']
            sub_category_id = sub_cat['sub_category_id']
            
            # Get templates for this category
            templates = enhanced_templates.get(category_name, ['Ürün'])
            
            # Create 3-8 products for each sub_category
            num_products = random.randint(3, 8)
            
            for i in range(num_products):
                # Select random template
                template = random.choice(templates)
                
                # Create unique product name
                product_name = f"{template} - {sub_category_name} - {product_id}"
                
                # Create unique description
                descriptions = [
                    f"Premium {template.lower()} ürünü. {sub_category_name} kategorisinde yer alır. Model: {product_id}",
                    f"Yüksek kaliteli {template.lower()} seçeneği. {category_name} kategorisinde bulunur. Seri: {product_id}",
                    f"Profesyonel {template.lower()} çözümü. {sub_category_name} için özel tasarlandı. Versiyon: {product_id}",
                    f"İnovatif {template.lower()} teknolojisi. {category_name} alanında öncü. Model: {product_id}",
                    f"Gelişmiş {template.lower()} özellikleri. {sub_category_name} kullanımı için optimize edildi. Seri: {product_id}",
                    f"Modern {template.lower()} tasarımı. {category_name} standartlarına uygun. Versiyon: {product_id}",
                    f"Ergonomik {template.lower()} yapısı. {sub_category_name} ihtiyaçlarına göre geliştirildi. Model: {product_id}",
                    f"Dayanıklı {template.lower()} malzemesi. {category_name} kalitesinde üretildi. Seri: {product_id}",
                    f"Konforlu {template.lower()} deneyimi. {sub_category_name} kullanıcıları için tasarlandı. Versiyon: {product_id}",
                    f"Güvenilir {template.lower()} performansı. {category_name} güvencesi ile. Model: {product_id}"
                ]
                
                description = random.choice(descriptions)
                
                # Generate random price (30-3000 TL)
                price = round(random.uniform(30, 3000), 2)
                
                # Generate random quantity (5-150)
                quantity = random.randint(5, 150)
                
                new_products.append({
                    'product_id': int(product_id),
                    'product_name': product_name,
                    'product_description': description,
                    'product_price': float(price),
                    'product_quantity': int(quantity),
                    'product_sub_category_id': int(sub_category_id)
                })
                
                product_id += 1
        
        print(f"📊 Created {len(new_products)} additional products")
        
        # Insert new products
        print("\n💾 Inserting new products...")
        
        with engine.connect() as conn:
            for product in new_products:
                insert_query = text("""
                    INSERT INTO products 
                    (product_id, product_name, product_description, product_price, product_quantity, product_sub_category_id)
                    VALUES (:product_id, :product_name, :product_description, :product_price, :product_quantity, :product_sub_category_id)
                """)
                conn.execute(insert_query, product)
            
            conn.commit()
        
        print("✅ All new products inserted!")
        
        # Final statistics
        final_count_query = "SELECT COUNT(*) as count FROM products"
        final_count_result = pd.read_sql(text(final_count_query), engine)
        final_count = final_count_result.iloc[0]['count']
        
        unique_desc_query = "SELECT COUNT(DISTINCT product_description) as unique_descriptions FROM products"
        unique_desc_result = pd.read_sql(text(unique_desc_query), engine)
        unique_count = unique_desc_result.iloc[0]['unique_descriptions']
        
        print(f"\n📊 Final Statistics:")
        print(f"   - Total products: {final_count}")
        print(f"   - Unique descriptions: {unique_count}")
        print(f"   - Products added: {final_count - current_count}")
        print(f"   - All descriptions unique: {'✅' if unique_count == final_count else '❌'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    enhance_products() 