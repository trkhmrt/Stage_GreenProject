import pandas as pd
import numpy as np
from sqlalchemy import text, create_engine
import random
from datetime import datetime, timedelta
import json

class RealisticDataGenerator:
    def __init__(self):
        # Database configurations
        self.product_host = "localhost"
        self.product_port = 3301
        self.product_database = "productservicedb"
        
        self.basket_host = "localhost"
        self.basket_port = 3309
        self.basket_database = "basketservicedb"
        
        self.username = "root"
        self.password = "root"
        
        # Realistic product categories and relationships
        self.realistic_categories = {
            'Elektronik': {
                'Akıllı Telefon': {
                    'related': ['Telefon Kılıfı', 'Ekran Koruyucu', 'Şarj Cihazı', 'Kulaklık', 'Power Bank'],
                    'price_range': (2000, 15000),
                    'description_template': 'Akıllı telefon - {brand} {model} - {features}'
                },
                'Laptop': {
                    'related': ['Laptop Çantası', 'Mouse', 'Klavye', 'Monitör', 'USB Hub'],
                    'price_range': (8000, 25000),
                    'description_template': 'Laptop - {brand} {model} - {specs}'
                },
                'Tablet': {
                    'related': ['Tablet Kılıfı', 'Tablet Kalemi', 'Bluetooth Klavye', 'Tablet Standı'],
                    'price_range': (3000, 12000),
                    'description_template': 'Tablet - {brand} {model} - {size} inç'
                },
                'Kulaklık': {
                    'related': ['Kulaklık Kılıfı', 'Bluetooth Adaptör', 'Kulaklık Standı'],
                    'price_range': (200, 2000),
                    'description_template': 'Kulaklık - {brand} {type} - {features}'
                }
            },
            'Giyim': {
                'Erkek T-Shirt': {
                    'related': ['Erkek Pantolon', 'Erkek Ayakkabı', 'Erkek Ceket', 'Erkek Gömlek'],
                    'price_range': (50, 300),
                    'description_template': 'Erkek T-Shirt - {brand} - {material} - {color}'
                },
                'Kadın Elbise': {
                    'related': ['Kadın Ayakkabı', 'Kadın Çanta', 'Kadın Takı', 'Kadın Şal'],
                    'price_range': (200, 800),
                    'description_template': 'Kadın Elbise - {brand} - {style} - {color}'
                },
                'Spor Ayakkabı': {
                    'related': ['Spor Çorap', 'Spor T-Shirt', 'Spor Şort', 'Spor Çanta'],
                    'price_range': (300, 1200),
                    'description_template': 'Spor Ayakkabı - {brand} - {type} - {color}'
                }
            },
            'Ev & Yaşam': {
                'Kahve Makinesi': {
                    'related': ['Kahve Çekirdeği', 'Kahve Filtresi', 'Kahve Fincanı', 'Kahve Değirmeni'],
                    'price_range': (500, 3000),
                    'description_template': 'Kahve Makinesi - {brand} - {type} - {capacity}'
                },
                'Robot Süpürge': {
                    'related': ['Süpürge Torbası', 'Temizlik Malzemesi', 'Mop', 'Paspas'],
                    'price_range': (2000, 8000),
                    'description_template': 'Robot Süpürge - {brand} - {features}'
                },
                'Yatak': {
                    'related': ['Yastık', 'Battaniye', 'Çarşaf', 'Nevresim Takımı'],
                    'price_range': (1000, 5000),
                    'description_template': 'Yatak - {brand} - {size} - {material}'
                }
            },
            'Spor & Outdoor': {
                'Bisiklet': {
                    'related': ['Bisiklet Kaskı', 'Bisiklet Lambası', 'Bisiklet Kilidi', 'Bisiklet Çantası'],
                    'price_range': (1500, 8000),
                    'description_template': 'Bisiklet - {brand} - {type} - {size}'
                },
                'Kamp Çadırı': {
                    'related': ['Uyku Tulumu', 'Kamp Lambası', 'Kamp Sandalyesi', 'Kamp Masası'],
                    'price_range': (500, 3000),
                    'description_template': 'Kamp Çadırı - {brand} - {capacity} kişilik'
                },
                'Yoga Matı': {
                    'related': ['Yoga Topu', 'Yoga Bloku', 'Yoga Kemeri', 'Meditasyon Yastığı'],
                    'price_range': (100, 500),
                    'description_template': 'Yoga Matı - {brand} - {thickness}mm - {material}'
                }
            },
            'Kozmetik & Bakım': {
                'Şampuan': {
                    'related': ['Saç Kremi', 'Saç Maskesi', 'Saç Fırçası', 'Saç Kurutma Makinesi'],
                    'price_range': (30, 200),
                    'description_template': 'Şampuan - {brand} - {type} - {volume}ml'
                },
                'Nemlendirici Krem': {
                    'related': ['Güneş Kremi', 'Serum', 'Tonik', 'Peeling'],
                    'price_range': (50, 300),
                    'description_template': 'Nemlendirici Krem - {brand} - {type} - {volume}ml'
                },
                'Ruj': {
                    'related': ['Maskara', 'Fondöten', 'Göz Farı', 'Tırnak Ojesi'],
                    'price_range': (80, 400),
                    'description_template': 'Ruj - {brand} - {color} - {type}'
                }
            },
            'Kitap & Hobi': {
                'Roman': {
                    'related': ['Kitap Ayracı', 'Okuma Gözlüğü', 'Kitap Kılıfı', 'Mürekkep'],
                    'price_range': (30, 150),
                    'description_template': 'Roman - {author} - {title} - {pages} sayfa'
                },
                'Puzzle': {
                    'related': ['Puzzle Yapıştırıcısı', 'Puzzle Matı', 'Puzzle Çerçevesi'],
                    'price_range': (50, 300),
                    'description_template': 'Puzzle - {brand} - {pieces} parça - {theme}'
                },
                'Gitar': {
                    'related': ['Gitar Teli', 'Gitar Kılıfı', 'Gitar Standı', 'Metronom'],
                    'price_range': (800, 5000),
                    'description_template': 'Gitar - {brand} - {type} - {strings} telli'
                }
            }
        }
        
        # Customer behavior patterns
        self.customer_types = {
            'single_buyer': {
                'basket_size': (1, 2),
                'frequency': 0.3,
                'categories': ['random']
            },
            'casual_shopper': {
                'basket_size': (2, 4),
                'frequency': 0.4,
                'categories': ['related']
            },
            'bulk_buyer': {
                'basket_size': (4, 8),
                'frequency': 0.2,
                'categories': ['related', 'complementary']
            },
            'deal_hunter': {
                'basket_size': (3, 6),
                'frequency': 0.1,
                'categories': ['related', 'promotional']
            }
        }
        
        # Brand names for realism
        self.brands = {
            'Elektronik': ['Samsung', 'Apple', 'Xiaomi', 'Huawei', 'Sony', 'LG', 'Asus', 'Lenovo'],
            'Giyim': ['Nike', 'Adidas', 'Zara', 'H&M', 'Mavi', 'Koton', 'LC Waikiki'],
            'Ev & Yaşam': ['IKEA', 'Arçelik', 'Beko', 'Vestel', 'Philips', 'Bosch'],
            'Spor & Outdoor': ['Decathlon', 'Columbia', 'The North Face', 'Salomon'],
            'Kozmetik & Bakım': ['L\'Oreal', 'Garnier', 'Nivea', 'Neutrogena', 'Maybelline'],
            'Kitap & Hobi': ['Penguin', 'Can Yayınları', 'Yapı Kredi', 'İş Bankası']
        }
        
    def clear_existing_data(self):
        """Clear existing data from both databases"""
        print("🗑️ Clearing existing data...")
        
        # Clear product database
        product_engine = create_engine(f"mysql+mysqlconnector://{self.username}:{self.password}@{self.product_host}:{self.product_port}/{self.product_database}")
        with product_engine.connect() as conn:
            conn.execute(text("DELETE FROM products"))
            conn.execute(text("DELETE FROM sub_categories"))
            conn.execute(text("DELETE FROM categories"))
            conn.commit()
        
        # Clear basket database
        basket_engine = create_engine(f"mysql+mysqlconnector://{self.username}:{self.password}@{self.basket_host}:{self.basket_port}/{self.basket_database}")
        with basket_engine.connect() as conn:
            conn.execute(text("DELETE FROM basket_product_units"))
            conn.execute(text("DELETE FROM baskets"))
            conn.commit()
        
        print("✅ Existing data cleared!")
    
    def create_realistic_categories(self):
        """Create realistic categories and subcategories"""
        print("📂 Creating realistic categories...")
        
        product_engine = create_engine(f"mysql+mysqlconnector://{self.username}:{self.password}@{self.product_host}:{self.product_port}/{self.product_database}")
        
        with product_engine.connect() as conn:
            # Create categories
            for cat_id, (cat_name, subcategories) in enumerate(self.realistic_categories.items(), 1):
                conn.execute(text("""
                    INSERT INTO categories (category_id, category_name) 
                    VALUES (:category_id, :category_name)
                """), {'category_id': cat_id, 'category_name': cat_name})
            
            # Create subcategories
            sub_cat_id = 1
            for cat_id, (cat_name, subcategories) in enumerate(self.realistic_categories.items(), 1):
                for sub_cat_name in subcategories.keys():
                    conn.execute(text("""
                        INSERT INTO sub_categories (sub_category_id, sub_category_name, category_id) 
                        VALUES (:sub_category_id, :sub_category_name, :category_id)
                    """), {
                        'sub_category_id': sub_cat_id,
                        'sub_category_name': sub_cat_name,
                        'category_id': cat_id
                    })
                    sub_cat_id += 1
            
            conn.commit()
        
        print(f"✅ Created {len(self.realistic_categories)} categories and {sub_cat_id-1} subcategories!")
    
    def generate_realistic_products(self):
        """Generate realistic products with proper relationships"""
        print("🔄 Generating realistic products...")
        
        product_engine = create_engine(f"mysql+mysqlconnector://{self.username}:{self.password}@{self.product_host}:{self.product_port}/{self.product_database}")
        
        products = []
        product_id = 1
        
        for category_name, subcategories in self.realistic_categories.items():
            category_brands = self.brands.get(category_name, ['Generic'])
            
            for sub_cat_name, sub_cat_info in subcategories.items():
                # Get subcategory ID
                sub_cat_query = """
                SELECT sub_category_id FROM sub_categories 
                WHERE sub_category_name = :sub_cat_name
                """
                sub_cat_result = pd.read_sql(text(sub_cat_query), product_engine, params={'sub_cat_name': sub_cat_name})
                if sub_cat_result.empty:
                    continue
                
                sub_cat_id = sub_cat_result.iloc[0]['sub_category_id']
                
                # Generate main products
                num_products = random.randint(8, 15)
                for i in range(num_products):
                    brand = random.choice(category_brands)
                    price_range = sub_cat_info['price_range']
                    price = round(random.uniform(price_range[0], price_range[1]), 2)
                    
                    # Generate product name and description
                    product_name = f"{sub_cat_name} - {brand} - {product_id}"
                    
                    # Create realistic description
                    description_template = sub_cat_info['description_template']
                    description = self.generate_realistic_description(description_template, brand, sub_cat_name, product_id)
                    
                    products.append({
                        'product_id': int(product_id),
                        'product_name': product_name,
                        'product_description': description,
                        'product_price': float(price),
                        'product_quantity': int(random.randint(10, 200)),
                        'product_sub_category_id': int(sub_cat_id),
                        'category': category_name,
                        'sub_category': sub_cat_name,
                        'brand': brand,
                        'related_products': sub_cat_info['related']
                    })
                    
                    product_id += 1
                
                # Generate related products
                for related_product in sub_cat_info['related']:
                    brand = random.choice(category_brands)
                    price = round(random.uniform(20, price_range[1] * 0.3), 2)
                    
                    product_name = f"{related_product} - {brand} - {product_id}"
                    description = f"Tamamlayıcı ürün - {related_product} - {brand} - Model: {product_id}"
                    
                    products.append({
                        'product_id': int(product_id),
                        'product_name': product_name,
                        'product_description': description,
                        'product_price': float(price),
                        'product_quantity': int(random.randint(10, 200)),
                        'product_sub_category_id': int(sub_cat_id),
                        'category': category_name,
                        'sub_category': sub_cat_name,
                        'brand': brand,
                        'related_products': [sub_cat_name]
                    })
                    
                    product_id += 1
        
        print(f"📊 Generated {len(products)} realistic products")
        
        # Insert products
        print("💾 Inserting products...")
        with product_engine.connect() as conn:
            for product in products:
                conn.execute(text("""
                    INSERT INTO products 
                    (product_id, product_name, product_description, product_price, product_quantity, product_sub_category_id)
                    VALUES (:product_id, :product_name, :product_description, :product_price, :product_quantity, :product_sub_category_id)
                """), product)
            
            conn.commit()
        
        print("✅ Products inserted successfully!")
        return products
    
    def generate_realistic_description(self, template, brand, product_type, product_id):
        """Generate realistic product descriptions"""
        # Product-specific features
        features = {
            'Akıllı Telefon': ['128GB Depolama', '6.1 inç Ekran', '48MP Kamera', '5000mAh Batarya'],
            'Laptop': ['Intel i7 İşlemci', '16GB RAM', '512GB SSD', '15.6 inç Ekran'],
            'Tablet': ['10.1 inç Ekran', '64GB Depolama', '8MP Kamera', '6000mAh Batarya'],
            'Kulaklık': ['Bluetooth 5.0', 'Aktif Gürültü Önleme', '30 Saat Pil Ömrü', 'Su Geçirmez'],
            'Erkek T-Shirt': ['%100 Pamuk', 'Regular Fit', 'Çoklu Renk', 'Yıkama Talimatlı'],
            'Kadın Elbise': ['Viskon Kumaş', 'Günlük Kullanım', 'Çoklu Beden', 'Ütü Gerektirmez'],
            'Spor Ayakkabı': ['Hafif Taban', 'Nefes Alabilir', 'Çoklu Renk', 'Ortopedik Taban'],
            'Kahve Makinesi': ['Otomatik Programlar', '1.5L Su Haznesi', 'Filtre Sistemi', 'LCD Ekran'],
            'Robot Süpürge': ['Akıllı Haritalama', 'WiFi Bağlantı', '2 Saat Pil Ömrü', 'Otomatik Şarj'],
            'Yatak': ['Orta Sertlik', 'Çoklu Boyut', 'Anti-Alerjik', '10 Yıl Garanti'],
            'Bisiklet': ['21 Vites', 'Alüminyum Gövde', 'Disk Fren', 'Ayarlanabilir Sele'],
            'Kamp Çadırı': ['Su Geçirmez', 'Hızlı Kurulum', 'Rüzgar Dirençli', 'Havalandırma'],
            'Yoga Matı': ['6mm Kalınlık', 'Kaymaz Taban', 'Çevre Dostu', 'Yıkama Talimatlı'],
            'Şampuan': ['Saç Tipine Özel', 'Paraben İçermez', '500ml', 'Doğal İçerik'],
            'Nemlendirici Krem': ['24 Saat Nemlendirme', 'Hassas Cilt Uyumlu', '50ml', 'Paraben İçermez'],
            'Ruj': ['Uzun Süre Kalıcı', 'Mat Bitiş', 'Çoklu Renk', 'Vitamin E İçerikli'],
            'Roman': ['Bestseller', 'Çok Satan', 'Yeni Baskı', 'Özel Kapak'],
            'Puzzle': ['1000 Parça', 'Eğitici', 'Dayanıklı Kart', 'Koleksiyon'],
            'Gitar': ['Klasik Gitar', 'Naylon Tel', 'Doğal Ahşap', 'Profesyonel']
        }
        
        feature = random.choice(features.get(product_type, ['Kaliteli', 'Dayanıklı', 'Güvenilir']))
        model = f"Model-{product_id}"
        
        return template.format(brand=brand, model=model, features=feature, type=product_type, 
                             specs=feature, size=random.choice(['10.1', '12.9', '9.7']), 
                             material=random.choice(['Pamuk', 'Polyester', 'Keten']),
                             color=random.choice(['Siyah', 'Beyaz', 'Mavi', 'Kırmızı']),
                             style=random.choice(['Günlük', 'Şık', 'Spor']), capacity=random.choice(['1.5L', '2L', '1L']),
                             thickness=random.choice(['4mm', '6mm', '8mm']), volume=random.choice(['250ml', '500ml', '1000ml']),
                             author=random.choice(['Ahmet Hamdi Tanpınar', 'Orhan Pamuk', 'Elif Şafak']),
                             title=f"Roman {product_id}", pages=random.randint(200, 500),
                             pieces=random.choice(['500', '1000', '1500']), theme=random.choice(['Doğa', 'Şehir', 'Sanat']),
                             strings=random.choice(['6', '12']))
    
    def generate_realistic_baskets(self, products):
        """Generate more and higher-quality, highly related baskets"""
        print("🛒 Generating more and higher-quality, highly related baskets...")
        
        basket_engine = create_engine(f"mysql+mysqlconnector://{self.username}:{self.password}@{self.basket_host}:{self.basket_port}/{self.basket_database}")
        
        # Find the maximum existing basket ID to avoid conflicts
        max_basket_id = 0
        try:
            max_basket_result = pd.read_sql(text("SELECT MAX(basket_id) as max_id FROM baskets"), basket_engine)
            if not max_basket_result.empty and max_basket_result.iloc[0]['max_id'] is not None:
                max_basket_id = int(max_basket_result.iloc[0]['max_id'])
        except:
            pass
        
        basket_id = max_basket_id + 1
        print(f"Starting from basket ID: {basket_id}")
        
        baskets = []
        basket_product_units = []
        
        # Generate 2000-2500 baskets
        num_baskets = random.randint(2000, 2500)
        for i in range(num_baskets):
            basket_products = []
            # %70 olasılıkla ilişkili ürünlü "paket" sepet
            if random.random() < 0.7:
                main_product = random.choice(products)
                basket_products = [main_product]
                # İlişkili ürünlerin çoğunu ekle (%90 olasılıkla)
                for rel_name in main_product['related_products']:
                    if random.random() < 0.9:
                        rel_candidates = [p for p in products if rel_name in p['product_name'] and p['category'] == main_product['category']]
                        if rel_candidates:
                            rel_product = random.choice(rel_candidates)
                            if rel_product not in basket_products:
                                basket_products.append(rel_product)
                # Sepet boyutunu tamamla (3-8 ürün)
                basket_size = random.randint(max(3, len(basket_products)), 8)
                if len(basket_products) < basket_size:
                    others = [p for p in products if p not in basket_products]
                    basket_products += random.sample(others, min(basket_size - len(basket_products), len(others)))
            # %20 olasılıkla çoklu kategori sepeti
            elif random.random() < 0.3:
                categories = random.sample(list(self.realistic_categories.keys()), 2)
                cat_products = [p for p in products if p['category'] in categories]
                basket_size = random.randint(3, 8)
                basket_products = random.sample(cat_products, min(basket_size, len(cat_products)))
            # %10 olasılıkla tamamen rastgele sepet
            else:
                basket_size = random.randint(2, 6)
                basket_products = random.sample(products, basket_size)

            customer_id = random.randint(1, 200)
            basket_status_id = random.choice([1, 4])
            create_date = datetime.now() - timedelta(days=random.randint(0, 90))
            
            baskets.append({
                'basket_id': int(basket_id),
                'customer_id': int(customer_id),
                'basket_status_id': int(basket_status_id),
                'create_date': create_date
            })
            
            for product in basket_products:
                quantity = random.randint(1, 3)
                unit_price = product['product_price']
                total_price = unit_price * quantity
                basket_product_units.append({
                    'basket_id': int(basket_id),
                    'product_id': int(product['product_id']),
                    'product_name': product['product_name'],
                    'product_quantity': int(quantity),
                    'product_total_price': float(total_price),
                    'product_unit_price': float(unit_price)
                })
            basket_id += 1
        print(f"📊 Generated {len(baskets)} baskets with {len(basket_product_units)} product units (very high relatedness)")
        # Insert baskets
        print("💾 Inserting baskets...")
        with basket_engine.connect() as conn:
            for basket in baskets:
                conn.execute(text("""
                    INSERT INTO baskets 
                    (basket_id, customer_id, basket_status_id, create_date)
                    VALUES (:basket_id, :customer_id, :basket_status_id, :create_date)
                """), basket)
            conn.commit()
        # Insert basket product units in chunks
        print("💾 Inserting basket product units...")
        chunk_size = 100
        with basket_engine.connect() as conn:
            for i in range(0, len(basket_product_units), chunk_size):
                chunk = basket_product_units[i:i+chunk_size]
                for unit in chunk:
                    conn.execute(text("""
                        INSERT INTO basket_product_units 
                        (basket_id, product_id, product_name, product_quantity, product_total_price, product_unit_price)
                        VALUES (:basket_id, :product_id, :product_name, :product_quantity, :product_total_price, :product_unit_price)
                    """), unit)
                conn.commit()
                print(f"   Inserted chunk {i//chunk_size + 1}/{(len(basket_product_units) + chunk_size - 1)//chunk_size}")
        print("✅ Baskets inserted successfully!")
    
    def select_realistic_products(self, products, customer_type, basket_size):
        """Select realistic products based on customer type and relationships"""
        selected_products = []
        
        if customer_type == 'single_buyer':
            # Random single products
            selected_products = random.sample(products, min(basket_size, len(products)))
        
        elif customer_type == 'casual_shopper':
            # Related products from same category
            category = random.choice(list(self.realistic_categories.keys()))
            category_products = [p for p in products if p['category'] == category]
            selected_products = random.sample(category_products, min(basket_size, len(category_products)))
        
        elif customer_type == 'bulk_buyer':
            # Main product + related products
            main_product = random.choice(products)
            selected_products = [main_product]
            
            # Add related products
            related_products = [p for p in products if p['product_name'] in main_product['related_products']]
            if related_products:
                selected_products.extend(random.sample(related_products, min(basket_size-1, len(related_products))))
            
            # Fill remaining slots with random products
            remaining_slots = basket_size - len(selected_products)
            if remaining_slots > 0:
                available_products = [p for p in products if p not in selected_products]
                selected_products.extend(random.sample(available_products, min(remaining_slots, len(available_products))))
        
        elif customer_type == 'deal_hunter':
            # Mix of related and promotional products
            category = random.choice(list(self.realistic_categories.keys()))
            category_products = [p for p in products if p['category'] == category]
            selected_products = random.sample(category_products, min(basket_size//2, len(category_products)))
            
            # Add some promotional/cheaper products
            cheap_products = [p for p in products if p['product_price'] < 100]
            if cheap_products:
                selected_products.extend(random.sample(cheap_products, min(basket_size-len(selected_products), len(cheap_products))))
        
        return selected_products[:basket_size]
    
    def generate_all_data(self):
        """Generate all realistic data"""
        print("🚀 Starting realistic data generation...")
        
        # Don't clear existing data - just add new baskets
        # self.clear_existing_data()
        
        # Check if categories exist, if not create them
        product_engine = create_engine(f"mysql+mysqlconnector://{self.username}:{self.password}@{self.product_host}:{self.product_port}/{self.product_database}")
        existing_categories = pd.read_sql(text("SELECT COUNT(*) as count FROM categories"), product_engine).iloc[0]['count']
        
        if existing_categories == 0:
            print("📂 Creating realistic categories...")
            self.create_realistic_categories()
            print("🔄 Generating realistic products...")
            products = self.generate_realistic_products()
        else:
            print("📂 Categories already exist, loading existing products...")
            products = pd.read_sql(text("SELECT * FROM products"), product_engine).to_dict('records')
            # Add category and related_products info
            for product in products:
                sub_cat_query = """
                SELECT sc.sub_category_name, c.category_name 
                FROM sub_categories sc 
                JOIN categories c ON sc.category_id = c.category_id 
                WHERE sc.sub_category_id = :sub_cat_id
                """
                sub_cat_result = pd.read_sql(text(sub_cat_query), product_engine, params={'sub_cat_id': product['product_sub_category_id']})
                if not sub_cat_result.empty:
                    product['sub_category'] = sub_cat_result.iloc[0]['sub_category_name']
                    product['category'] = sub_cat_result.iloc[0]['category_name']
                    # Find related products based on subcategory
                    for cat_name, subcategories in self.realistic_categories.items():
                        if cat_name == product['category']:
                            for sub_cat_name, sub_cat_info in subcategories.items():
                                if sub_cat_name == product['sub_category']:
                                    product['related_products'] = sub_cat_info['related']
                                    break
                            break
        
        # Generate new baskets with high confidence
        self.generate_realistic_baskets(products)
        
        print("🎉 High-confidence basket generation completed!")
        
        # Final statistics
        basket_engine = create_engine(f"mysql+mysqlconnector://{self.username}:{self.password}@{self.basket_host}:{self.basket_port}/{self.basket_database}")
        
        product_count = pd.read_sql(text("SELECT COUNT(*) as count FROM products"), product_engine).iloc[0]['count']
        basket_count = pd.read_sql(text("SELECT COUNT(*) as count FROM baskets"), basket_engine).iloc[0]['count']
        unit_count = pd.read_sql(text("SELECT COUNT(*) as count FROM basket_product_units"), basket_engine).iloc[0]['count']
        
        print(f"\n📊 Final Statistics:")
        print(f"   - Total products: {product_count}")
        print(f"   - Total baskets: {basket_count}")
        print(f"   - Total product units: {unit_count}")
        print(f"   - Average products per basket: {unit_count/basket_count:.2f}")

if __name__ == "__main__":
    generator = RealisticDataGenerator()
    generator.generate_all_data() 