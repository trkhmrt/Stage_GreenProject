import pandas as pd
import random
from datetime import datetime, timedelta
from sqlalchemy import text, create_engine

class PhoneCaseBasketGenerator:
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
        
        # Phone model to case compatibility mapping based on existing products
        self.phone_case_compatibility = {
            # iPhone Models and Compatible Cases
            'iPhone 15 Pro Max': [
                'iPhone 15 Pro Max Şeffaf Kılıf'
            ],
            'iPhone 15 Pro': [
                'iPhone 15 Pro Deri Kılıf'
            ],
            'iPhone 15': [
                'iPhone 15 Zırhlı Kılıf'
            ],
            'iPhone 15 Plus': [
                'iPhone 15 Plus Silikon Kılıf'
            ],
            'iPhone 14 Pro Max': [
                'iPhone 14 Pro Max Mavi Kılıf'
            ],
            'iPhone 14 Pro': [
                'iPhone 14 Pro Su Geçirmez Kılıf'
            ],
            'iPhone 14': [
                'iPhone 14 Mat Kılıf'
            ],
            'iPhone 14 Plus': [
                'iPhone 14 Plus Cüzdan Kılıf'
            ],
            'iPhone 13 Pro Max': [
                'iPhone 13 Pro Max Manyetik Kılıf'
            ],
            'iPhone 13 Pro': [
                'iPhone 13 Pro Ultra İnce Kılıf'
            ],
            'iPhone 13': [
                'iPhone 13 Sert Kılıf'
            ],
            'iPhone 13 mini': [
                'iPhone 13 mini Desenli Kılıf'
            ],
            'iPhone SE (3. Nesil)': [
                'iPhone SE 3. Nesil Şeffaf Kılıf'
            ],
            'iPhone 12 Pro Max': [
                'iPhone 12 Pro Max Kamera Kılıfı'
            ],
            'iPhone 12 Pro': [
                'iPhone 12 Pro Renkli Kılıf'
            ],
            'iPhone 12': [
                'iPhone 12 Kenar Korumalı Kılıf'
            ],
            'iPhone 12 mini': [
                'iPhone 12 mini Parıltılı Kılıf'
            ],
            'iPhone 11': [
                'iPhone 11 Ultra Koruyucu Kılıf'
            ],
            'iPhone SE (2. Nesil)': [
                'iPhone SE 2. Nesil Klasik Kılıf'
            ],
            
            # Samsung Models and Compatible Cases
            'Samsung Galaxy S24 Ultra': [
                'S24 Ultra S Pen Kılıf'
            ],
            'Samsung Galaxy S24+': [
                'S24+ Darbeye Dayanıklı Şeffaf Kılıf'
            ],
            'Samsung Galaxy S24': [
                'S24 Smart View Cüzdan Kılıf'
            ],
            'Samsung Galaxy Z Fold5': [
                'Z Fold5 Menteşe Korumalı Kılıf'
            ],
            'Samsung Galaxy Z Flip5': [
                'Z Flip5 Yüzüklü Kılıf'
            ],
            'Samsung Galaxy S23 Ultra': [
                'S23 Ultra Lens Korumalı Kılıf'
            ],
            'Samsung Galaxy S23': [
                'S23 Karbon Fiber Kılıf'
            ],
            'Samsung Galaxy A55': [
                'A55 Buzlu Mat Kılıf'
            ],
            'Samsung Galaxy A35': [
                'A35 Desenli Şeffaf Kılıf'
            ],
            'Samsung Galaxy A15': [
                'A15 Silikon Kılıf'
            ],
            'Samsung Galaxy Note20 Ultra': [
                'Note20 Ultra Kickstand Kılıf'
            ],
            'Samsung Galaxy Z Flip4': [
                'Z Flip4 Şeffaf Yüzüklü Kılıf'
            ],
            'Samsung Galaxy Z Fold4': [
                'Z Fold4 Kalem Tutuculu Kılıf'
            ],
            'Samsung Galaxy S22 Ultra': [
                'S22 Ultra Sağlam Kılıf'
            ],
            'Samsung Galaxy A73': [
                'A73 İnce Şeffaf Kılıf'
            ]
        }
        
        # Additional accessories that go well with phones
        self.phone_accessories = [
            'Apple AirPods Pro',
            'Samsung Galaxy Watch 6',
            'Apple MagSafe Şarj Cihazı',
            'Samsung Wireless Charger',
            'USB-C Kablo',
            'Lightning Kablo',
            'Power Bank',
            'Kablosuz Şarj Ünitesi',
            'Araç Şarj Cihazı',
            'Laptop Şarj Adaptörü'
        ]
    
    def find_compatible_products(self, phone_model, all_products):
        """Find products that are compatible with the phone model"""
        compatible_products = []
        
        # Find the phone model in our compatibility mapping
        if phone_model in self.phone_case_compatibility:
            compatible_case_names = self.phone_case_compatibility[phone_model]
            
            # Find matching products in the database
            for case_name in compatible_case_names:
                for product in all_products:
                    if case_name.lower() in product['product_name'].lower():
                        compatible_products.append(product)
        
        # Add general phone accessories (if they exist in database)
        for accessory_name in self.phone_accessories:
            for product in all_products:
                if accessory_name.lower() in product['product_name'].lower():
                    if product not in compatible_products:
                        compatible_products.append(product)
        
        return compatible_products
    
    def generate_phone_case_baskets(self):
        """Generate baskets with phone models and compatible cases"""
        print("📱 Telefon Kılıfı Sepet Oluşturucu Başlatılıyor...")
        
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
            p.product_quantity,
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
        
        # Generate phone case baskets
        print("🛒 Telefon kılıfı sepetleri oluşturuluyor...")
        
        baskets = []
        basket_product_units = []
        basket_id = 1
        
        # Generate 1000-1500 phone case baskets
        num_baskets = random.randint(1000, 1500)
        
        for i in range(num_baskets):
            basket_products = []
            
            # 85% chance for phone + case combination, 15% for random phone accessories
            if random.random() < 0.85:
                # Phone + Case combination
                phone_models = list(self.phone_case_compatibility.keys())
                selected_phone = random.choice(phone_models)
                
                # Find the phone in products
                phone_product = None
                for product in products:
                    if selected_phone.lower() in product['product_name'].lower():
                        phone_product = product
                        break
                
                if phone_product:
                    basket_products.append(phone_product)
                    
                    # Find compatible cases and accessories
                    compatible_products = self.find_compatible_products(selected_phone, products)
                    
                    # Add 1-3 compatible cases/accessories
                    num_accessories = random.randint(1, 3)
                    if compatible_products:
                        selected_accessories = random.sample(compatible_products, min(num_accessories, len(compatible_products)))
                        basket_products.extend(selected_accessories)
                
                # If no phone found, add random phone accessories
                if not phone_product:
                    phone_accessories = [p for p in products if any(keyword in p['product_name'].lower() for keyword in ['kılıf', 'airpods', 'galaxy watch', 'şarj', 'kablo'])]
                    if phone_accessories:
                        basket_products = random.sample(phone_accessories, min(3, len(phone_accessories)))
            
            else:
                # Random phone accessories basket
                phone_accessories = [p for p in products if any(keyword in p['product_name'].lower() for keyword in ['kılıf', 'airpods', 'galaxy watch', 'şarj', 'kablo', 'power bank'])]
                if phone_accessories:
                    basket_size = random.randint(2, 5)
                    basket_products = random.sample(phone_accessories, min(basket_size, len(phone_accessories)))
            
            # Create basket with status 4 (Ödendi)
            customer_id = random.randint(1, 500)
            basket_status_id = 4  # All baskets are paid (Ödendi)
            create_date = datetime.now() - timedelta(days=random.randint(1, 365))
            
            baskets.append({
                'basket_id': basket_id,
                'customer_id': customer_id,
                'basket_status_id': basket_status_id,
                'create_date': create_date
            })
            
            # Add products to basket
            for product in basket_products:
                quantity = random.randint(1, 2)  # Usually 1-2 items per product
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
        
        print(f"📊 {len(baskets)} telefon kılıfı sepeti oluşturuldu ({len(basket_product_units)} ürün birimi)")
        
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
        
        print("✅ Telefon kılıfı sepetleri başarıyla oluşturuldu!")
        
        # Show sample baskets
        print("\n🛒 Örnek Telefon Kılıfı Sepetleri:")
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
            status_text = "Ödendi" if basket['basket_status_id'] == 4 else "Aktif"
            print(f"   Sepet {basket['basket_id']} (Müşteri {basket['customer_id']}, Durum: {status_text}):")
            print(f"     Ürünler: {basket['products']}")
            print()
        
        # Show statistics
        print("📈 İstatistikler:")
        stats_query = """
        SELECT 
            COUNT(DISTINCT b.basket_id) as total_baskets,
            COUNT(bpu.basket_product_unit_id) as total_products,
            AVG(bpu.product_quantity) as avg_quantity,
            SUM(bpu.product_total_price) as total_revenue
        FROM baskets b
        JOIN basket_product_units bpu ON b.basket_id = bpu.basket_id
        """
        
        stats = pd.read_sql(text(stats_query), basket_engine)
        print(f"   Toplam Sepet: {stats.iloc[0]['total_baskets']}")
        print(f"   Toplam Ürün: {stats.iloc[0]['total_products']}")
        print(f"   Ortalama Ürün Adedi: {stats.iloc[0]['avg_quantity']:.2f}")
        print(f"   Toplam Gelir: {stats.iloc[0]['total_revenue']:,.2f} TL")

if __name__ == "__main__":
    generator = PhoneCaseBasketGenerator()
    generator.generate_phone_case_baskets() 