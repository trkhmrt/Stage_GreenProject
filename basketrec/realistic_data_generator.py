import pandas as pd
import numpy as np
from sqlalchemy import text, create_engine
import random
from datetime import datetime, timedelta
import json
import re

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
        
        # Brand patterns for matching
        self.brand_patterns = {
            'Apple': ['iPhone', 'iPad', 'MacBook', 'iMac', 'AirPods', 'Apple Watch', 'Apple TV', 'HomePod', 'Magic'],
            'Samsung': ['Galaxy', 'Samsung', 'Note', 'Fold', 'Flip', 'Tab'],
            'Xiaomi': ['Xiaomi', 'Redmi', 'Mi', 'POCO'],
            'Huawei': ['Huawei', 'P', 'Mate', 'Nova', 'Honor'],
            'Sony': ['Sony', 'PlayStation', 'PS', 'Xperia'],
            'LG': ['LG', 'G', 'V', 'K'],
            'Asus': ['Asus', 'ROG', 'ZenBook', 'VivoBook'],
            'Lenovo': ['Lenovo', 'ThinkPad', 'IdeaPad', 'Yoga'],
            'Nike': ['Nike', 'Air', 'Jordan'],
            'Adidas': ['Adidas', 'Ultraboost', 'Stan Smith'],
            'Zara': ['Zara'],
            'H&M': ['H&M', 'H&M'],
            'Mavi': ['Mavi'],
            'Koton': ['Koton'],
            'LC Waikiki': ['LC Waikiki', 'LCW'],
            'IKEA': ['IKEA'],
            'Arçelik': ['Arçelik', 'Beko'],
            'Beko': ['Beko'],
            'Vestel': ['Vestel'],
            'Philips': ['Philips'],
            'Bosch': ['Bosch'],
            'Decathlon': ['Decathlon'],
            'Columbia': ['Columbia'],
            'The North Face': ['The North Face', 'North Face'],
            'Salomon': ['Salomon'],
            'L\'Oreal': ['L\'Oreal', 'L\'Oréal'],
            'Garnier': ['Garnier'],
            'Nivea': ['Nivea'],
            'Neutrogena': ['Neutrogena'],
            'Maybelline': ['Maybelline'],
            'Penguin': ['Penguin'],
            'Can Yayınları': ['Can Yayınları'],
            'Yapı Kredi': ['Yapı Kredi'],
            'İş Bankası': ['İş Bankası']
        }
        
        # Product relationships by brand and category
        self.brand_relationships = {
            'Apple': {
                'iPhone': ['Telefon Kılıfı', 'Koruma Aksesuarı', 'Şarj Aleti', 'Kablosuz Kulaklık', 'Kablosuz Şarj Ünitesi'],
                'iPad': ['Tablet Kılıfı', 'Stylus Kalem', 'Klavye', 'Ekran Koruyucu'],
                'MacBook': ['Laptop Kılıfı', 'Mouse', 'Adaptör', 'Touchpad'],
                'AirPods': ['Kulaklık Kılıfı', 'Kablosuz Kulaklık'],
                'Apple Watch': ['Saat Kayışı', 'Kablosuz Şarj Ünitesi']
            },
            'Samsung': {
                'Galaxy': ['Telefon Kılıfı', 'Koruma Aksesuarı', 'Şarj Aleti', 'Kablosuz Kulaklık', 'Kablosuz Şarj Ünitesi'],
                'Tab': ['Tablet Kılıfı', 'Stylus Kalem', 'Klavye', 'Ekran Koruyucu'],
                'Note': ['Telefon Kılıfı', 'Koruma Aksesuarı', 'Şarj Aleti', 'Stylus Kalem']
            },
            'Nike': {
                'Ayakkabı': ['Spor Çorap', 'Spor T-Shirt', 'Spor Şort', 'Spor Çanta'],
                'T-Shirt': ['Spor Şort', 'Spor Ayakkabı', 'Spor Çorap'],
                'Şort': ['Spor T-Shirt', 'Spor Ayakkabı', 'Spor Çorap']
            },
            'Adidas': {
                'Ayakkabı': ['Spor Çorap', 'Spor T-Shirt', 'Spor Şort', 'Spor Çanta'],
                'T-Shirt': ['Spor Şort', 'Spor Ayakkabı', 'Spor Çorap'],
                'Şort': ['Spor T-Shirt', 'Spor Ayakkabı', 'Spor Çorap']
            }
        }
        
    def extract_brand_and_model(self, product_name, product_description):
        """Extract brand and model from product name and description"""
        product_text = f"{product_name} {product_description}".lower()
        
        for brand, patterns in self.brand_patterns.items():
            for pattern in patterns:
                if pattern.lower() in product_text:
                    return brand, pattern
        
        return None, None
    
    def get_related_products_by_brand(self, main_product, all_products):
        """Get related products from the same brand"""
        brand, model = self.extract_brand_and_model(main_product['product_name'], main_product['product_description'])
        
        if not brand:
            return []
        
        related_products = []
        
        # Find products with the same brand
        for product in all_products:
            product_brand, product_model = self.extract_brand_and_model(product['product_name'], product['product_description'])
            
            if product_brand == brand and product['product_id'] != main_product['product_id']:
                # Check if it's a related product type
                if brand in self.brand_relationships:
                    product_text = f"{product['product_name']} {product['product_description']}".lower()
                    for model_type, related_types in self.brand_relationships[brand].items():
                        if model_type.lower() in product_text:
                            related_products.append(product)
                            break
                else:
                    # If no specific relationship defined, add products from same category
                    if product['category'] == main_product['category']:
                        related_products.append(product)
        
        return related_products
    
    def generate_brand_aware_baskets(self, products):
        """Generate baskets with products from the same brand"""
        print("🛒 Generating brand-aware realistic baskets...")
        
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
            
            # %80 olasılıkla aynı marka ürünleri sepet
            if random.random() < 0.8:
                # Ana ürünü seç
                main_product = random.choice(products)
                basket_products = [main_product]
                
                # Aynı markadan ilişkili ürünleri bul
                related_products = self.get_related_products_by_brand(main_product, products)
                
                # İlişkili ürünlerin çoğunu ekle (%85 olasılıkla)
                for related_product in related_products:
                    if random.random() < 0.85 and len(basket_products) < 6:
                        basket_products.append(related_product)
                
                # Sepet boyutunu tamamla (3-8 ürün)
                basket_size = random.randint(max(3, len(basket_products)), 8)
                if len(basket_products) < basket_size:
                    # Aynı kategoriden diğer ürünleri ekle
                    same_category_products = [p for p in products if p['category'] == main_product['category'] and p not in basket_products]
                    if same_category_products:
                        additional_products = random.sample(same_category_products, min(basket_size - len(basket_products), len(same_category_products)))
                        basket_products.extend(additional_products)
                    
                    # Hala eksikse rastgele ürünler ekle
                    if len(basket_products) < basket_size:
                        other_products = [p for p in products if p not in basket_products]
                        if other_products:
                            remaining_products = random.sample(other_products, min(basket_size - len(basket_products), len(other_products)))
                            basket_products.extend(remaining_products)
            
            # %20 olasılıkla çoklu marka sepeti
            else:
                basket_size = random.randint(3, 8)
                basket_products = random.sample(products, min(basket_size, len(products)))

            customer_id = random.randint(1, 200)
            # %70 olasılıkla status 4 (paid), %30 olasılıkla status 1 (active)
            basket_status_id = random.choices([1, 4], weights=[0.3, 0.7])[0]
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
        
        print(f"📊 Generated {len(baskets)} brand-aware baskets with {len(basket_product_units)} product units")
        
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
        
        print("✅ Brand-aware baskets inserted successfully!")
    
    def generate_all_data(self):
        """Generate all realistic data with brand awareness"""
        print("🚀 Starting brand-aware realistic data generation...")
        
        # Load existing products from ProductService
        product_engine = create_engine(f"mysql+mysqlconnector://{self.username}:{self.password}@{self.product_host}:{self.product_port}/{self.product_database}")
        
        print("📂 Loading existing products from ProductService...")
        products = pd.read_sql(text("SELECT * FROM products"), product_engine).to_dict('records')
        
        # Add category information
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
        
        print(f"📦 Loaded {len(products)} products from ProductService")
        
        # Generate brand-aware baskets
        self.generate_brand_aware_baskets(products)
        
        print("🎉 Brand-aware basket generation completed!")
        
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
        
        # Show some example baskets
        print(f"\n🛒 Sample Brand-Aware Baskets:")
        sample_baskets = pd.read_sql(text("""
            SELECT b.basket_id, b.customer_id, b.basket_status_id, 
                   GROUP_CONCAT(bpu.product_name SEPARATOR ' | ') as products
            FROM baskets b
            JOIN basket_product_units bpu ON b.basket_id = bpu.basket_id
            GROUP BY b.basket_id
            ORDER BY b.basket_id DESC
            LIMIT 5
        """), basket_engine)
        
        for _, basket in sample_baskets.iterrows():
            print(f"   Basket {basket['basket_id']} (Customer {basket['customer_id']}, Status {basket['basket_status_id']}):")
            print(f"     Products: {basket['products']}")
            print()

# Usage
if __name__ == "__main__":
    generator = RealisticDataGenerator()
    generator.generate_all_data() 