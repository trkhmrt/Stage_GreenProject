#!/usr/bin/env python3
import mysql.connector

# Database configuration
PRODUCT_DB = {
    'host': 'localhost',
    'port': 3301,
    'user': 'root',
    'password': 'root',
    'database': 'productservicedb'
}

def get_connection():
    return mysql.connector.connect(**PRODUCT_DB)

def get_next_id(cursor, table_name, id_column):
    """Get the next available ID for a table"""
    cursor.execute(f"SELECT MAX({id_column}) FROM {table_name}")
    result = cursor.fetchone()
    return (result[0] or 0) + 1

def get_subcategory_id(cursor, subcategory_name):
    """Get subcategory_id by name"""
    cursor.execute("SELECT sub_category_id FROM sub_categories WHERE sub_category_name = %s", (subcategory_name,))
    result = cursor.fetchone()
    return result[0] if result else None

def add_products():
    """Add comprehensive product list to existing categories"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        print("📦 Ürünler ekleniyor...")
        
        # Get next product ID
        next_product_id = get_next_id(cursor, "products", "product_id")
        
        # Get subcategory IDs
        subcategory_ids = {}
        subcategories = [
            "Oyun Konsolları", "Konsol Oyunları", "Konsol Aksesuarları",
            "Laptop Kılıfı", "Mouse", "Adaptör", "Kablosuz Kulaklık",
            "Erkek Giyim", "Kadın Giyim", "Ayakkabı", "Spor Giyim", "Aksesuar",
            "Elektronik Ev Aletleri", "Mobilya", "Fitness Ekipmanları",
            "Bisiklet", "Kulaklıklar", "Hoparlörler", "Araç Aksesuarları"
        ]
        
        for subcategory_name in subcategories:
            subcategory_id = get_subcategory_id(cursor, subcategory_name)
            if subcategory_id:
                subcategory_ids[subcategory_name] = subcategory_id
                print(f"✅ {subcategory_name}: ID {subcategory_id}")
            else:
                print(f"❌ {subcategory_name} bulunamadı!")
        
        # Product list
        products = [
            # 🎮 Oyun & Eğlence
            {
                'name': 'PlayStation 5 Slim',
                'description': 'Sony PlayStation 5 Slim 1TB, 4K Gaming Console',
                'price': 24999.99,
                'quantity': 25,
                'model': 'PS5 Slim',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Oyun Konsolları')
            },
            {
                'name': 'Xbox Series X',
                'description': 'Microsoft Xbox Series X 1TB, 4K Gaming Console',
                'price': 22999.99,
                'quantity': 20,
                'model': 'Xbox Series X',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Oyun Konsolları')
            },
            {
                'name': 'Nintendo Switch OLED',
                'description': 'Nintendo Switch OLED Model, 7-inch OLED Screen',
                'price': 8999.99,
                'quantity': 30,
                'model': 'Nintendo Switch OLED',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Oyun Konsolları')
            },
            {
                'name': 'GTA 6',
                'description': 'Grand Theft Auto 6 - PlayStation 5',
                'price': 1299.99,
                'quantity': 50,
                'model': 'GTA 6 PS5',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Konsol Oyunları')
            },
            {
                'name': 'Call of Duty: Modern Warfare III',
                'description': 'Call of Duty: Modern Warfare III - Xbox Series X',
                'price': 1199.99,
                'quantity': 45,
                'model': 'COD MW3 Xbox',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Konsol Oyunları')
            },
            {
                'name': 'Mario Kart 8 Deluxe',
                'description': 'Mario Kart 8 Deluxe - Nintendo Switch',
                'price': 899.99,
                'quantity': 60,
                'model': 'Mario Kart 8 Switch',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Konsol Oyunları')
            },
            {
                'name': 'DualSense Controller',
                'description': 'Sony DualSense Wireless Controller for PS5',
                'price': 1299.99,
                'quantity': 40,
                'model': 'DualSense PS5',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Konsol Aksesuarları')
            },
            {
                'name': 'Xbox Controller',
                'description': 'Microsoft Xbox Wireless Controller',
                'price': 999.99,
                'quantity': 35,
                'model': 'Xbox Controller',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Konsol Aksesuarları')
            },
            {
                'name': 'Joy-Con Set',
                'description': 'Nintendo Joy-Con Controllers Set',
                'price': 799.99,
                'quantity': 50,
                'model': 'Joy-Con Set',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Konsol Aksesuarları')
            },
            
            # 💻 Bilgisayar & Teknoloji
            {
                'name': 'MacBook Pro 16" M3',
                'description': 'Apple MacBook Pro 16-inch M3 Chip, 18GB RAM, 512GB SSD',
                'price': 129999.99,
                'quantity': 15,
                'model': 'MacBook Pro 16 M3',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Laptop Kılıfı')
            },
            {
                'name': 'Dell XPS 15',
                'description': 'Dell XPS 15 9530, Intel i7, 16GB RAM, 512GB SSD',
                'price': 89999.99,
                'quantity': 20,
                'model': 'Dell XPS 15',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Laptop Kılıfı')
            },
            {
                'name': 'Lenovo ThinkPad X1',
                'description': 'Lenovo ThinkPad X1 Carbon, Intel i7, 16GB RAM',
                'price': 79999.99,
                'quantity': 18,
                'model': 'ThinkPad X1 Carbon',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Laptop Kılıfı')
            },
            {
                'name': 'Apple Magic Mouse',
                'description': 'Apple Magic Mouse 2 - Wireless Mouse',
                'price': 899.99,
                'quantity': 40,
                'model': 'Magic Mouse 2',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Mouse')
            },
            {
                'name': 'Dell Wireless Mouse',
                'description': 'Dell WM126 Wireless Optical Mouse',
                'price': 299.99,
                'quantity': 60,
                'model': 'Dell WM126',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Mouse')
            },
            {
                'name': 'Lenovo Mouse',
                'description': 'Lenovo ThinkPad Wireless Mouse',
                'price': 399.99,
                'quantity': 45,
                'model': 'ThinkPad Mouse',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Mouse')
            },
            {
                'name': 'USB-C Hub',
                'description': 'Anker USB-C Hub with HDMI, USB, SD Card Reader',
                'price': 599.99,
                'quantity': 50,
                'model': 'Anker USB-C Hub',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Adaptör')
            },
            {
                'name': 'Laptop Stand',
                'description': 'Rain Design mStand Laptop Stand for MacBook',
                'price': 799.99,
                'quantity': 30,
                'model': 'Rain Design mStand',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Adaptör')
            },
            
            # 🏠 Ev & Yaşam
            {
                'name': 'Philips Airfryer XXL',
                'description': 'Philips Airfryer XXL HD9654/90, 1.4kg Capacity',
                'price': 2499.99,
                'quantity': 25,
                'model': 'Philips Airfryer XXL',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Elektronik Ev Aletleri')
            },
            {
                'name': 'Bosch Çamaşır Makinesi',
                'description': 'Bosch WAT28440TR 9kg Çamaşır Makinesi',
                'price': 8999.99,
                'quantity': 15,
                'model': 'Bosch WAT28440TR',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Elektronik Ev Aletleri')
            },
            {
                'name': 'Siemens Bulaşık Makinesi',
                'description': 'Siemens SN236I03ME 12 Kişilik Bulaşık Makinesi',
                'price': 6799.99,
                'quantity': 12,
                'model': 'Siemens SN236I03ME',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Elektronik Ev Aletleri')
            },
            {
                'name': 'Arçelik Fırın',
                'description': 'Arçelik CFM 10000 X Built-in Fırın',
                'price': 4299.99,
                'quantity': 20,
                'model': 'Arçelik CFM 10000 X',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Elektronik Ev Aletleri')
            },
            {
                'name': 'Beko Mikrodalga',
                'description': 'Beko BM 20100 SS Mikrodalga Fırın',
                'price': 1899.99,
                'quantity': 35,
                'model': 'Beko BM 20100 SS',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Elektronik Ev Aletleri')
            },
            {
                'name': 'IKEA Malm Yatak Odası',
                'description': 'IKEA Malm Yatak Odası Takımı, Beyaz',
                'price': 3999.99,
                'quantity': 10,
                'model': 'IKEA Malm Set',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Mobilya')
            },
            {
                'name': 'Bellona Koltuk Takımı',
                'description': 'Bellona 3+3+1 Koltuk Takımı, Gri',
                'price': 12999.99,
                'quantity': 8,
                'model': 'Bellona 3+3+1',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Mobilya')
            },
            {
                'name': 'Çilek Masa Sandalye',
                'description': 'Çilek 6 Kişilik Yemek Masası ve Sandalye Seti',
                'price': 2499.99,
                'quantity': 15,
                'model': 'Çilek 6 Kişilik Set',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Mobilya')
            },
            
            # 🏃‍♂️ Spor & Fitness
            {
                'name': 'Bowflex SelectTech Dumbbells',
                'description': 'Bowflex SelectTech 552 Adjustable Dumbbells',
                'price': 8999.99,
                'quantity': 10,
                'model': 'Bowflex SelectTech 552',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Fitness Ekipmanları')
            },
            {
                'name': 'Concept2 Model D Rower',
                'description': 'Concept2 Model D Indoor Rowing Machine',
                'price': 15999.99,
                'quantity': 5,
                'model': 'Concept2 Model D',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Fitness Ekipmanları')
            },
            {
                'name': 'Peloton Bike+',
                'description': 'Peloton Bike+ with 24" HD Touchscreen',
                'price': 89999.99,
                'quantity': 3,
                'model': 'Peloton Bike+',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Fitness Ekipmanları')
            },
            {
                'name': 'Trek Domane SL6',
                'description': 'Trek Domane SL6 Road Bike, Carbon Frame',
                'price': 45999.99,
                'quantity': 8,
                'model': 'Trek Domane SL6',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Bisiklet')
            },
            {
                'name': 'Specialized Tarmac SL7',
                'description': 'Specialized Tarmac SL7 Pro Road Bike',
                'price': 89999.99,
                'quantity': 5,
                'model': 'Specialized Tarmac SL7',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Bisiklet')
            },
            
            # 🎵 Müzik & Ses
            {
                'name': 'Sony WH-1000XM5',
                'description': 'Sony WH-1000XM5 Wireless Noise Canceling Headphones',
                'price': 8999.99,
                'quantity': 25,
                'model': 'Sony WH-1000XM5',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Kulaklıklar')
            },
            {
                'name': 'Bose QuietComfort 45',
                'description': 'Bose QuietComfort 45 Wireless Headphones',
                'price': 7999.99,
                'quantity': 20,
                'model': 'Bose QC45',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Kulaklıklar')
            },
            {
                'name': 'JBL Charge 5',
                'description': 'JBL Charge 5 Portable Bluetooth Speaker',
                'price': 2999.99,
                'quantity': 40,
                'model': 'JBL Charge 5',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Hoparlörler')
            },
            {
                'name': 'Bose SoundLink Revolve',
                'description': 'Bose SoundLink Revolve+ Portable Speaker',
                'price': 3999.99,
                'quantity': 30,
                'model': 'Bose SoundLink Revolve+',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Hoparlörler')
            },
            
            # 🚗 Otomotiv
            {
                'name': 'Garmin DriveSmart 65',
                'description': 'Garmin DriveSmart 65 GPS Navigator',
                'price': 3999.99,
                'quantity': 20,
                'model': 'Garmin DriveSmart 65',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Araç Aksesuarları')
            },
            {
                'name': 'Dash Cam BlackVue DR750X',
                'description': 'BlackVue DR750X-2CH LTE Dash Cam',
                'price': 4999.99,
                'quantity': 15,
                'model': 'BlackVue DR750X-2CH',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Araç Aksesuarları')
            },
            {
                'name': 'CarPlay Adapter',
                'description': 'Carlinkit Wireless CarPlay Adapter',
                'price': 1999.99,
                'quantity': 25,
                'model': 'Carlinkit Wireless',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Araç Aksesuarları')
            },
            
            # 👕 Giyim & Moda
            {
                'name': 'Nike Air Jordan 1',
                'description': 'Nike Air Jordan 1 Retro High OG',
                'price': 4999.99,
                'quantity': 30,
                'model': 'Nike Air Jordan 1',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Ayakkabı')
            },
            {
                'name': 'Adidas Ultraboost 22',
                'description': 'Adidas Ultraboost 22 Running Shoes',
                'price': 3999.99,
                'quantity': 35,
                'model': 'Adidas Ultraboost 22',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Ayakkabı')
            },
            {
                'name': 'Puma RS-X',
                'description': 'Puma RS-X Reinvention Sneakers',
                'price': 2499.99,
                'quantity': 40,
                'model': 'Puma RS-X',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Ayakkabı')
            },
            {
                'name': 'Zara Kış Koleksiyonu',
                'description': 'Zara Kış Koleksiyonu Kadın Giyim Seti',
                'price': 899.99,
                'quantity': 50,
                'model': 'Zara Winter Collection',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Kadın Giyim')
            },
            {
                'name': 'H&M Casual Giyim',
                'description': 'H&M Casual Erkek Giyim Seti',
                'price': 599.99,
                'quantity': 60,
                'model': 'H&M Casual Set',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Erkek Giyim')
            },
            {
                'name': 'Mavi Jean Koleksiyonu',
                'description': 'Mavi Premium Jean Koleksiyonu',
                'price': 1299.99,
                'quantity': 45,
                'model': 'Mavi Premium Jeans',
                'model_year': '2024',
                'subcategory_id': subcategory_ids.get('Erkek Giyim')
            }
        ]
        
        # Insert products
        added_count = 0
        for product in products:
            if product['subcategory_id']:  # Only add if subcategory exists
                try:
                    # Generate image URL
                    image_url = f"https://example.com/products/{product['model'].lower().replace(' ', '_')}.jpg"
                    
                    cursor.execute("""
                        INSERT INTO products (
                            product_id, product_name, product_description, product_price, 
                            product_quantity, product_model, product_model_year, product_image_url, 
                            product_sub_category_id
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        next_product_id,
                        product['name'],
                        product['description'],
                        product['price'],
                        product['quantity'],
                        product['model'],
                        product['model_year'],
                        image_url,
                        product['subcategory_id']
                    ))
                    
                    print(f"✅ {product['name']} eklendi (ID: {next_product_id})")
                    next_product_id += 1
                    added_count += 1
                    
                except Exception as e:
                    print(f"❌ {product['name']} eklenirken hata: {e}")
            else:
                print(f"⚠️ {product['name']} için alt kategori bulunamadı, atlandı")
        
        conn.commit()
        print(f"\n🎉 Toplam {added_count} ürün başarıyla eklendi!")
        
        # Show summary
        cursor.execute("SELECT COUNT(*) FROM products")
        total_products = cursor.fetchone()[0]
        print(f"\n📊 Toplam ürün sayısı: {total_products}")
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    add_products() 