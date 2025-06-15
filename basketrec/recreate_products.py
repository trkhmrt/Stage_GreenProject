import pandas as pd
from sqlalchemy import text, create_engine
import random

def recreate_products():
    """Delete existing products and recreate them based on categories and sub_categories"""
    
    # Products database configuration
    host = "localhost"
    port = 3301
    database = "productservicedb"
    username = "root"
    password = "root"
    
    try:
        # Connect to products database
        connection_string = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}"
        engine = create_engine(connection_string)
        
        print("🔍 Getting categories and sub_categories data...")
        
        # Get categories
        categories_query = "SELECT category_id, category_name FROM categories ORDER BY category_id"
        categories_df = pd.read_sql(text(categories_query), engine)
        print(f"📊 Found {len(categories_df)} categories")
        
        # Get sub_categories with category info
        sub_categories_query = """
        SELECT 
            sc.sub_category_id,
            sc.sub_category_name,
            sc.category_id,
            c.category_name
        FROM sub_categories sc
        LEFT JOIN categories c ON sc.category_id = c.category_id
        ORDER BY sc.sub_category_id
        """
        sub_categories_df = pd.read_sql(text(sub_categories_query), engine)
        print(f"📊 Found {len(sub_categories_df)} sub_categories")
        
        # Show sample data
        print("\n📋 Categories:")
        print(categories_df.to_string(index=False))
        
        print("\n📋 Sub-categories:")
        print(sub_categories_df.to_string(index=False))
        
        # Delete existing products
        print("\n🗑️ Deleting existing products...")
        with engine.connect() as conn:
            conn.execute(text("DELETE FROM products"))
            conn.commit()
        print("✅ Existing products deleted!")
        
        # Create new products based on categories and sub_categories
        print("\n🔄 Creating new products...")
        
        new_products = []
        product_id = 1
        
        # Product templates for each category
        product_templates = {
            'Elektronik': [
                'Akıllı Telefon', 'Laptop', 'Tablet', 'Kulaklık', 'Klavye', 'Mouse', 'Monitör', 'Yazıcı', 'Kamera', 'Drone',
                'Akıllı Saat', 'Bluetooth Speaker', 'Power Bank', 'SSD', 'RAM', 'İşlemci', 'Anakart', 'Ekran Kartı'
            ],
            'Giyim': [
                'T-Shirt', 'Gömlek', 'Pantolon', 'Elbise', 'Ceket', 'Mont', 'Sweatshirt', 'Şort', 'Etek', 'Kazak',
                'Ayakkabı', 'Spor Ayakkabı', 'Terlik', 'Çorap', 'İç Çamaşırı', 'Pijama', 'Takım Elbise'
            ],
            'Ev & Yaşam': [
                'Koltuk', 'Masa', 'Sandalye', 'Dolap', 'Kitaplık', 'Lamba', 'Halı', 'Perde', 'Yastık', 'Battaniye',
                'Çarşaf', 'Havlu', 'Mutfak Eşyası', 'Banyo Eşyası', 'Bahçe Eşyası', 'Dekorasyon'
            ],
            'Spor & Outdoor': [
                'Spor Ayakkabı', 'Spor Kıyafeti', 'Fitness Ekipmanı', 'Kamp Ekipmanı', 'Bisiklet', 'Yoga Matı',
                'Koşu Bandı', 'Dumbbell', 'Pilates Topu', 'Su Matarası', 'Sırt Çantası', 'Çadır', 'Uyku Tulumu'
            ],
            'Kitap & Hobi': [
                'Roman', 'Bilim Kurgu', 'Tarih Kitabı', 'Bilim Kitabı', 'Çocuk Kitabı', 'Dergi', 'Gazete',
                'Puzzle', 'Oyun', 'Müzik Aleti', 'Sanat Malzemesi', 'El Sanatı', 'Koleksiyon'
            ],
            'Sağlık & Güzellik': [
                'Şampuan', 'Sabun', 'Diş Macunu', 'Deodorant', 'Parfüm', 'Krem', 'Serum', 'Maskara', 'Ruj',
                'Vitamin', 'İlaç', 'Takviye', 'Probiyotik', 'Omega-3', 'C Vitamini', 'D Vitamini'
            ],
            'Otomotiv': [
                'Araba', 'Motosiklet', 'Bisiklet', 'Scooter', 'Araba Aksesuarı', 'Lastik', 'Yağ', 'Fren',
                'Far', 'Ayna', 'Koltuk Kılıfı', 'Temizlik Malzemesi'
            ],
            'Bebek & Çocuk': [
                'Bebek Bezi', 'Bebek Maması', 'Bebek Kıyafeti', 'Oyuncak', 'Bebek Arabası', 'Bebek Koltuğu',
                'Bebek Bakım Ürünü', 'Çocuk Kıyafeti', 'Çocuk Ayakkabısı', 'Eğitici Oyuncak'
            ]
        }
        
        # Create products for each sub_category
        for _, sub_cat in sub_categories_df.iterrows():
            category_name = sub_cat['category_name']
            sub_category_name = sub_cat['sub_category_name']
            sub_category_id = sub_cat['sub_category_id']
            
            # Get templates for this category
            templates = product_templates.get(category_name, ['Ürün'])
            
            # Create 5-15 products for each sub_category
            num_products = random.randint(5, 15)
            
            for i in range(num_products):
                # Select random template
                template = random.choice(templates)
                
                # Create unique product name
                product_name = f"{template} - {sub_category_name} - {product_id}"
                
                # Create unique description
                descriptions = [
                    f"Yüksek kaliteli {template.lower()} ürünü. {sub_category_name} kategorisinde yer alır. Model: {product_id}",
                    f"Premium {template.lower()} seçeneği. {category_name} kategorisinde bulunur. Seri: {product_id}",
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
                
                # Generate random price (50-2000 TL)
                price = round(random.uniform(50, 2000), 2)
                
                # Generate random quantity (10-100)
                quantity = random.randint(10, 100)
                
                new_products.append({
                    'product_id': product_id,
                    'product_name': product_name,
                    'product_description': description,
                    'product_price': price,
                    'product_quantity': quantity,
                    'product_sub_category_id': sub_category_id
                })
                
                product_id += 1
        
        print(f"📊 Created {len(new_products)} new products")
        
        # Insert new products into database
        print("\n💾 Inserting new products into database...")
        
        with engine.connect() as conn:
            for product in new_products:
                insert_query = text("""
                    INSERT INTO products 
                    (product_id, product_name, product_description, product_price, product_quantity, product_sub_category_id)
                    VALUES (:product_id, :product_name, :product_description, :product_price, :product_quantity, :product_sub_category_id)
                """)
                conn.execute(insert_query, product)
            
            conn.commit()
        
        print("✅ All new products inserted successfully!")
        
        # Verify the results
        verify_query = """
        SELECT 
            p.product_id,
            p.product_name,
            p.product_description,
            p.product_price,
            sc.sub_category_name,
            c.category_name
        FROM products p
        LEFT JOIN sub_categories sc ON p.product_sub_category_id = sc.sub_category_id
        LEFT JOIN categories c ON sc.category_id = c.category_id
        ORDER BY p.product_id
        LIMIT 15
        """
        
        verify_df = pd.read_sql(text(verify_query), engine)
        print(f"\n📋 Sample new products:")
        print(verify_df.to_string(index=False))
        
        # Check unique descriptions
        unique_desc_query = "SELECT COUNT(DISTINCT product_description) as unique_descriptions FROM products"
        unique_desc_result = pd.read_sql(text(unique_desc_query), engine)
        unique_count = unique_desc_result.iloc[0]['unique_descriptions']
        
        total_products_query = "SELECT COUNT(*) as total_products FROM products"
        total_products_result = pd.read_sql(text(total_products_query), engine)
        total_count = total_products_result.iloc[0]['total_products']
        
        print(f"\n📊 Final Statistics:")
        print(f"   - Total products: {total_count}")
        print(f"   - Unique descriptions: {unique_count}")
        print(f"   - All descriptions unique: {'✅' if unique_count == total_count else '❌'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    recreate_products() 