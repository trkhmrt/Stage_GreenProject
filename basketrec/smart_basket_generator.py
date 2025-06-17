import pandas as pd
import random
from datetime import datetime, timedelta
from sqlalchemy import text, create_engine

class SmartBasketGenerator:
    def __init__(self):
        # Database configurations
        self.username = "root"
        self.password = "root"
        
        # Product database
        self.product_host = "localhost"
        self.product_port = 3301
        self.product_database = "productservicedb"
        
        # Basket database
        self.basket_host = "localhost"
        self.basket_port = 3309
        self.basket_database = "basketservicedb"
        
        # Smart product combinations
        self.product_combinations = {
            # iPhone combinations
            'iPhone 15 Pro Max': [
                'iPhone 15 Pro Max Deri Kılıf (Kum Beji)',
                'iPhone 15 Pro Max Kamera Koruyucu Metal Lens',
                'Apple MagSafe Şarj Cihazı',
                'Apple USB-C to Lightning Kablo (1m)',
                'Apple AirPods Pro (2. Nesil)'
            ],
            'iPhone 14': [
                'iPhone 14 Şeffaf MagSafe Kılıf',
                'iPhone 14 Pro Silikon Kılıf (Gece Yarısı)',
                'Apple MagSafe Şarj Cihazı',
                'Apple USB-C to Lightning Kablo (1m)',
                'iPhone 13 Kamera Lens Koruyucu'
            ],
            'iPhone SE (2022)': [
                'iPhone 14 Pro Silikon Kılıf (Gece Yarısı)',
                'Apple MagSafe Şarj Cihazı',
                'Apple USB-C to Lightning Kablo (1m)',
                'Apple AirPods Pro (2. Nesil)'
            ],
            
            # MacBook combinations
            'MacBook Air M2': [
                'MacBook Air 13.6 Taşıma Kılıfı',
                'MacBook Pro USB-C Dijital AV Multiport Adaptör',
                'Apple Magic Mouse 2',
                'Apple Magic Trackpad 2',
                'Apple USB-C to Lightning Kablo (1m)'
            ],
            'MacBook Pro 16 M2 Max': [
                'MacBook Pro 14 Taşıma Çantası',
                'MacBook Pro USB-C Dijital AV Multiport Adaptör',
                'Apple Magic Mouse 2',
                'Apple Magic Trackpad 2',
                'Apple USB-C to Lightning Kablo (1m)'
            ],
            
            # iPad combinations
            'iPad Pro 12.9': [
                'iPad Pro 12.9 Magic Keyboard',
                'Apple Pencil (2. Nesil)',
                'Apple Pencil 2. Nesil',
                'iPad Air 5 Smart Folio Kılıf (Lila)',
                'iPad Mini 6 Temperli Cam Ekran Koruyucu'
            ],
            
            # Samsung combinations
            'Samsung Galaxy Z Fold 5': [
                'Samsung Galaxy Buds 2 Pro',
                'Samsung Galaxy Watch 6 Classic',
                'Samsung Portable SSD T7'
            ],
            'Samsung Galaxy S23 Ultra': [
                'Samsung Galaxy Buds 2 Pro',
                'Samsung Galaxy Watch 6 Classic',
                'Samsung Portable SSD T7'
            ],
            'Samsung Galaxy Tab S9+': [
                'Samsung Galaxy Buds 2 Pro',
                'Samsung Galaxy Watch 6 Classic',
                'Samsung Smart Monitor M8'
            ],
            
            # Gaming combinations
            'Asus ROG Strix G16': [
                'Asus ROG Chakram X',
                'Asus TUF Gaming VG27AQ',
                'Asus ROG Swift PG32UQX',
                'Asus RT-AX86U'
            ],
            'Asus TUF Gaming F15': [
                'Asus ROG Chakram X',
                'Asus TUF Gaming VG27AQ',
                'Asus RT-AX86U'
            ],
            'HP Victus 16': [
                'HP Wireless Keyboard and Mouse 300',
                'HP USB-C Travel Hub G2',
                'HP EliteDisplay E243'
            ]
        }
        
        # Brand relationships for additional products
        self.brand_relationships = {
            'Apple': {
                'iPhone': ['AirPods', 'Apple Watch', 'MagSafe', 'Lightning'],
                'MacBook': ['Magic Mouse', 'Magic Trackpad', 'USB-C', 'Travel'],
                'iPad': ['Apple Pencil', 'Magic Keyboard', 'Smart Folio']
            },
            'Samsung': {
                'Galaxy': ['Galaxy Buds', 'Galaxy Watch', 'Portable SSD'],
                'Samsung': ['Smart Monitor', 'SmartThings']
            },
            'Asus': {
                'ROG': ['ROG Chakram', 'ROG Swift', 'RT-AX86U'],
                'TUF': ['TUF Gaming', 'RT-AX86U']
            },
            'HP': {
                'HP': ['HP Wireless', 'HP USB-C', 'HP EliteDisplay']
            }
        }
    
    def find_compatible_products(self, main_product_name, all_products):
        """Find products that are compatible with the main product"""
        compatible_products = []
        
        # Check exact matches first
        if main_product_name in self.product_combinations:
            for compatible_name in self.product_combinations[main_product_name]:
                for product in all_products:
                    if compatible_name.lower() in product['product_name'].lower():
                        compatible_products.append(product)
        
        # Check brand relationships
        for brand, relationships in self.brand_relationships.items():
            if brand.lower() in main_product_name.lower():
                for product in all_products:
                    product_name_lower = product['product_name'].lower()
                    for category, keywords in relationships.items():
                        if any(keyword.lower() in product_name_lower for keyword in keywords):
                            if product not in compatible_products:
                                compatible_products.append(product)
        
        return compatible_products
    
    def generate_smart_baskets(self):
        """Generate baskets with smart product combinations"""
        print("🧠 Akıllı sepet oluşturucu başlatılıyor...")
        
        # Connect to databases
        product_engine = create_engine(f"mysql+mysqlconnector://{self.username}:{self.password}@{self.product_host}:{self.product_port}/{self.product_database}")
        basket_engine = create_engine(f"mysql+mysqlconnector://{self.username}:{self.password}@{self.basket_host}:{self.basket_port}/{self.basket_database}")
        
        # Load products
        print("📂 Ürünler yükleniyor...")
        products_query = """
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
        """
        
        products_df = pd.read_sql(text(products_query), product_engine)
        products = products_df.to_dict('records')
        
        print(f"📦 {len(products)} ürün yüklendi")
        
        # Clear existing baskets
        print("🗑️ Mevcut sepetler temizleniyor...")
        with basket_engine.connect() as conn:
            conn.execute(text("DELETE FROM basket_product_units"))
            conn.execute(text("DELETE FROM baskets"))
            conn.commit()
        
        # Generate smart baskets
        print("🛒 Akıllı sepetler oluşturuluyor...")
        
        baskets = []
        basket_product_units = []
        basket_id = 1
        
        # Generate 1000-1500 smart baskets
        num_baskets = random.randint(1000, 1500)
        
        for i in range(num_baskets):
            basket_products = []
            
            # 70% chance for smart combination, 30% for random
            if random.random() < 0.7:
                # Smart combination
                main_product = random.choice(products)
                basket_products = [main_product]
                
                # Find compatible products
                compatible_products = self.find_compatible_products(main_product['product_name'], products)
                
                # Add compatible products (80% chance for each)
                for compatible_product in compatible_products:
                    if random.random() < 0.8 and len(basket_products) < 5:
                        basket_products.append(compatible_product)
                
                # Fill remaining slots with same category products
                basket_size = random.randint(3, 6)
                if len(basket_products) < basket_size:
                    same_category = [p for p in products if p['category'] == main_product['category'] and p not in basket_products]
                    if same_category:
                        additional = random.sample(same_category, min(basket_size - len(basket_products), len(same_category)))
                        basket_products.extend(additional)
                
                # Still need more? Add random products
                if len(basket_products) < basket_size:
                    remaining = [p for p in products if p not in basket_products]
                    if remaining:
                        extra = random.sample(remaining, min(basket_size - len(basket_products), len(remaining)))
                        basket_products.extend(extra)
            
            else:
                # Random basket
                basket_size = random.randint(3, 8)
                basket_products = random.sample(products, min(basket_size, len(products)))
            
            # Create basket
            customer_id = random.randint(1, 200)
            basket_status_id = random.choices([1, 4], weights=[0.3, 0.7])[0]  # 30% active, 70% paid
            create_date = datetime.now() - timedelta(days=random.randint(0, 90))
            
            baskets.append({
                'basket_id': basket_id,
                'customer_id': customer_id,
                'basket_status_id': basket_status_id,
                'create_date': create_date
            })
            
            # Add products to basket
            for product in basket_products:
                quantity = random.randint(1, 3)
                unit_price = product['product_price']
                total_price = unit_price * quantity
                
                basket_product_units.append({
                    'basket_id': basket_id,
                    'product_id': product['product_id'],
                    'product_name': product['product_name'],
                    'product_quantity': quantity,
                    'product_total_price': total_price,
                    'product_unit_price': unit_price
                })
            
            basket_id += 1
        
        print(f"📊 {len(baskets)} akıllı sepet oluşturuldu ({len(basket_product_units)} ürün birimi)")
        
        # Insert baskets
        print("💾 Sepetler veritabanına ekleniyor...")
        with basket_engine.connect() as conn:
            for basket in baskets:
                conn.execute(text("""
                    INSERT INTO baskets 
                    (basket_id, customer_id, basket_status_id, create_date)
                    VALUES (:basket_id, :customer_id, :basket_status_id, :create_date)
                """), basket)
            conn.commit()
        
        # Insert basket product units
        print("💾 Sepet ürünleri ekleniyor...")
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
                print(f"   Chunk {i//chunk_size + 1}/{(len(basket_product_units) + chunk_size - 1)//chunk_size} eklendi")
        
        print("✅ Akıllı sepetler başarıyla oluşturuldu!")
        
        # Show sample baskets
        print("\n🛒 Örnek Akıllı Sepetler:")
        sample_baskets = pd.read_sql(text("""
            SELECT b.basket_id, b.customer_id, b.basket_status_id, 
                   GROUP_CONCAT(bpu.product_name SEPARATOR ' | ') as products
            FROM baskets b
            JOIN basket_product_units bpu ON b.basket_id = bpu.basket_id
            GROUP BY b.basket_id
            ORDER BY b.basket_id DESC
            LIMIT 10
        """), basket_engine)
        
        for _, basket in sample_baskets.iterrows():
            print(f"   Sepet {basket['basket_id']} (Müşteri {basket['customer_id']}, Durum {basket['basket_status_id']}):")
            print(f"     Ürünler: {basket['products']}")
            print()

if __name__ == "__main__":
    generator = SmartBasketGenerator()
    generator.generate_smart_baskets() 