#!/usr/bin/env python3
import mysql.connector
import random
from datetime import datetime, timedelta

# Database configurations
PRODUCT_DB_CONFIG = {
    'host': 'localhost',
    'port': 3301,
    'user': 'root',
    'password': 'root',
    'database': 'productservicedb'
}

BASKET_DB_CONFIG = {
    'host': 'localhost',
    'port': 3309,
    'user': 'root',
    'password': 'root',
    'database': 'basketservicedb'
}

def get_product_connection():
    return mysql.connector.connect(**PRODUCT_DB_CONFIG)

def get_basket_connection():
    return mysql.connector.connect(**BASKET_DB_CONFIG)

def add_gaming_subcategories():
    """Add gaming-specific subcategories"""
    try:
        conn = get_product_connection()
        cursor = conn.cursor()
        
        print("🎮 Oyuncu alt kategorileri ekleniyor...")
        
        # Gaming subcategories for Bilgisayar category (3)
        gaming_subcategories = [
            (41, 'Oyuncu Klavyesi', 3),
            (42, 'Oyuncu Mouse', 3),
            (43, 'Mouse Pad', 3),
            (44, 'Bilek Desteği', 3)
        ]
        
        for subcat_id, subcat_name, cat_id in gaming_subcategories:
            try:
                cursor.execute("""
                    INSERT INTO sub_categories (sub_category_id, sub_category_name, category_id) 
                    VALUES (%s, %s, %s)
                """, (subcat_id, subcat_name, cat_id))
                print(f"✅ {subcat_name} eklendi")
            except mysql.connector.IntegrityError:
                print(f"⚠️ {subcat_name} zaten mevcut")
        
        conn.commit()
        print("✅ Oyuncu alt kategorileri eklendi!")
        
    except Exception as e:
        print(f"❌ Hata: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def add_gaming_products():
    """Add gaming peripherals products"""
    try:
        conn = get_product_connection()
        cursor = conn.cursor()
        
        print("🎮 Oyuncu ürünleri ekleniyor...")
        
        # Gaming Keyboards (Subcategory 41)
        gaming_keyboards = [
            ('Razer BlackWidow V3 Pro', 'BlackWidow V3 Pro', 2023, 2499.99, 50),
            ('Razer Huntsman V2', 'Huntsman V2', 2023, 1899.99, 45),
            ('Razer Ornata V3', 'Ornata V3', 2023, 899.99, 60),
            ('HyperX Alloy Origins Core', 'Alloy Origins Core', 2023, 1299.99, 40),
            ('HyperX Alloy Elite 2', 'Alloy Elite 2', 2023, 1799.99, 35),
            ('HyperX Alloy FPS Pro', 'Alloy FPS Pro', 2023, 999.99, 55),
            ('ASUS ROG Strix Scope II', 'Strix Scope II', 2023, 1599.99, 30),
            ('ASUS ROG Azoth', 'Azoth', 2023, 2999.99, 25),
            ('ASUS ROG Claymore II', 'Claymore II', 2023, 2199.99, 20),
            ('Logitech G Pro X', 'G Pro X', 2023, 1699.99, 40),
            ('Logitech G915 TKL', 'G915 TKL', 2023, 1999.99, 35),
            ('Logitech G513', 'G513', 2023, 1299.99, 50),
            ('SteelSeries Apex Pro', 'Apex Pro', 2023, 2499.99, 25),
            ('SteelSeries Apex 7', 'Apex 7', 2023, 1799.99, 30),
            ('Corsair K100 RGB', 'K100 RGB', 2023, 2899.99, 20),
            ('Corsair K70 RGB Pro', 'K70 RGB Pro', 2023, 1899.99, 35),
            ('Corsair K65 RGB', 'K65 RGB', 2023, 1499.99, 40),
            ('Glorious GMMK Pro', 'GMMK Pro', 2023, 2199.99, 25),
            ('Glorious GMMK 2', 'GMMK 2', 2023, 1599.99, 30),
            ('Glorious GMMK TKL', 'GMMK TKL', 2023, 1299.99, 35)
        ]
        
        # Gaming Mice (Subcategory 42)
        gaming_mice = [
            ('Razer DeathAdder V3 Pro', 'DeathAdder V3 Pro', 2023, 1299.99, 45),
            ('Razer Viper V3 HyperSpeed', 'Viper V3 HyperSpeed', 2023, 999.99, 50),
            ('Razer Basilisk V3 Pro', 'Basilisk V3 Pro', 2023, 1499.99, 35),
            ('Razer Naga Pro', 'Naga Pro', 2023, 1699.99, 30),
            ('HyperX Pulsefire Haste', 'Pulsefire Haste', 2023, 799.99, 60),
            ('HyperX Pulsefire Dart', 'Pulsefire Dart', 2023, 999.99, 40),
            ('HyperX Pulsefire Surge', 'Pulsefire Surge', 2023, 899.99, 45),
            ('ASUS ROG Harpe Ace', 'Harpe Ace', 2023, 1199.99, 35),
            ('ASUS ROG Chakram X', 'Chakram X', 2023, 1899.99, 25),
            ('ASUS ROG Spatha X', 'Spatha X', 2023, 2499.99, 20),
            ('Logitech G Pro X Superlight', 'G Pro X Superlight', 2023, 1299.99, 40),
            ('Logitech G502 X Plus', 'G502 X Plus', 2023, 1499.99, 35),
            ('Logitech G703', 'G703', 2023, 999.99, 45),
            ('SteelSeries Prime Pro', 'Prime Pro', 2023, 1099.99, 40),
            ('SteelSeries Rival 5', 'Rival 5', 2023, 899.99, 50),
            ('SteelSeries Aerox 9', 'Aerox 9', 2023, 1299.99, 30),
            ('Corsair M65 RGB Ultra', 'M65 RGB Ultra', 2023, 1199.99, 35),
            ('Corsair Sabre RGB Pro', 'Sabre RGB Pro', 2023, 999.99, 40),
            ('Corsair Ironclaw RGB', 'Ironclaw RGB', 2023, 1099.99, 35),
            ('Glorious Model O Wireless', 'Model O Wireless', 2023, 999.99, 40),
            ('Glorious Model D Wireless', 'Model D Wireless', 2023, 1099.99, 35),
            ('Glorious Model I', 'Model I', 2023, 899.99, 45)
        ]
        
        # Mouse Pads (Subcategory 43)
        mouse_pads = [
            ('Razer Gigantus V3', 'Gigantus V3', 2023, 299.99, 80),
            ('Razer Firefly V2', 'Firefly V2', 2023, 599.99, 60),
            ('Razer Goliathus Extended', 'Goliathus Extended', 2023, 399.99, 70),
            ('HyperX Fury S Pro', 'Fury S Pro', 2023, 249.99, 85),
            ('HyperX Fury S Speed', 'Fury S Speed', 2023, 199.99, 90),
            ('HyperX Fury S Control', 'Fury S Control', 2023, 199.99, 90),
            ('ASUS ROG Sheath', 'Sheath', 2023, 349.99, 75),
            ('ASUS ROG Scabbard', 'Scabbard', 2023, 449.99, 65),
            ('ASUS ROG Balteus', 'Balteus', 2023, 799.99, 50),
            ('SteelSeries QcK Heavy', 'QcK Heavy', 2023, 299.99, 80),
            ('SteelSeries QcK Edge', 'QcK Edge', 2023, 249.99, 85),
            ('SteelSeries QcK Prism', 'QcK Prism', 2023, 399.99, 70),
            ('Corsair MM700', 'MM700', 2023, 349.99, 75),
            ('Corsair MM300', 'MM300', 2023, 199.99, 90),
            ('Corsair MM800', 'MM800', 2023, 499.99, 60),
            ('Glorious Elements', 'Elements', 2023, 199.99, 90),
            ('Glorious 3XL Extended', '3XL Extended', 2023, 299.99, 80),
            ('Glorious Fire', 'Fire', 2023, 249.99, 85),
            ('Logitech G840', 'G840', 2023, 399.99, 70),
            ('Logitech G440', 'G440', 2023, 299.99, 80),
            ('Logitech G240', 'G240', 2023, 199.99, 90)
        ]
        
        # Wrist Rests (Subcategory 44)
        wrist_rests = [
            ('Razer Ergonomic Wrist Rest', 'Ergonomic Wrist Rest', 2023, 399.99, 70),
            ('Razer Pro Type Ultra', 'Pro Type Ultra', 2023, 299.99, 80),
            ('HyperX Wrist Rest', 'Wrist Rest', 2023, 249.99, 85),
            ('HyperX Memory Foam', 'Memory Foam', 2023, 199.99, 90),
            ('ASUS ROG Wrist Rest', 'ROG Wrist Rest', 2023, 349.99, 75),
            ('SteelSeries Wrist Rest', 'Wrist Rest', 2023, 299.99, 80),
            ('Corsair MM200', 'MM200', 2023, 249.99, 85),
            ('Glorious Wrist Rest', 'Wrist Rest', 2023, 199.99, 90),
            ('Glorious Memory Foam', 'Memory Foam', 2023, 179.99, 95),
            ('Logitech G840 Wrist Rest', 'G840 Wrist Rest', 2023, 299.99, 80),
            ('Gaming Wrist Rest Pro', 'Wrist Rest Pro', 2023, 399.99, 70),
            ('Ergonomic Wrist Support', 'Wrist Support', 2023, 349.99, 75),
            ('Memory Foam Wrist Cushion', 'Wrist Cushion', 2023, 199.99, 90),
            ('Gel Wrist Rest', 'Gel Wrist Rest', 2023, 249.99, 85),
            ('Leather Wrist Rest', 'Leather Wrist Rest', 2023, 399.99, 70),
            ('Bamboo Wrist Rest', 'Bamboo Wrist Rest', 2023, 449.99, 65),
            ('Aluminum Wrist Rest', 'Aluminum Wrist Rest', 2023, 599.99, 55),
            ('Carbon Fiber Wrist Rest', 'Carbon Fiber Wrist Rest', 2023, 799.99, 45),
            ('RGB Wrist Rest', 'RGB Wrist Rest', 2023, 499.99, 60),
            ('Heated Wrist Rest', 'Heated Wrist Rest', 2023, 699.99, 50)
        ]
        
        # Get next product ID
        cursor.execute("SELECT MAX(product_id) FROM products")
        max_id = cursor.fetchone()[0] or 0
        next_id = max_id + 1
        
        # Insert products
        all_products = []
        
        # Add keyboards
        for name, model, year, price, quantity in gaming_keyboards:
            all_products.append((next_id, name, model, year, price, quantity, 41))
            next_id += 1
        
        # Add mice
        for name, model, year, price, quantity in gaming_mice:
            all_products.append((next_id, name, model, year, price, quantity, 42))
            next_id += 1
        
        # Add mouse pads
        for name, model, year, price, quantity in mouse_pads:
            all_products.append((next_id, name, model, year, price, quantity, 43))
            next_id += 1
        
        # Add wrist rests
        for name, model, year, price, quantity in wrist_rests:
            all_products.append((next_id, name, model, year, price, quantity, 44))
            next_id += 1
        
        # Insert all products
        for product_id, name, model, year, price, quantity, subcat_id in all_products:
            cursor.execute("""
                INSERT INTO products (product_id, product_name, product_model, product_model_year, 
                                    product_price, product_quantity, product_sub_category_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (product_id, name, model, year, price, quantity, subcat_id))
        
        conn.commit()
        print(f"✅ {len(all_products)} oyuncu ürünü eklendi!")
        
        return all_products
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        return []
    finally:
        if 'conn' in locals():
            conn.close()

def create_gaming_baskets():
    """Create logical gaming peripheral basket combinations"""
    try:
        product_conn = get_product_connection()
        basket_conn = get_basket_connection()
        
        product_cursor = product_conn.cursor(dictionary=True)
        basket_cursor = basket_conn.cursor()
        
        print("🛒 Oyuncu sepet kombinasyonları oluşturuluyor...")
        
        # Get gaming products by subcategory
        gaming_products = {}
        for subcat_id in [41, 42, 43, 44]:  # Keyboard, Mouse, Mouse Pad, Wrist Rest
            product_cursor.execute("""
                SELECT product_id, product_name, product_price 
                FROM products 
                WHERE product_sub_category_id = %s
            """, (subcat_id,))
            gaming_products[subcat_id] = product_cursor.fetchall()
        
        # Get existing baskets
        basket_cursor.execute("SELECT basket_id FROM baskets WHERE basket_status_id IN (1, 4)")
        existing_baskets = [row[0] for row in basket_cursor.fetchall()]
        
        if not existing_baskets:
            print("❌ Mevcut sepet bulunamadı!")
            return
        
        # Create logical combinations
        combinations = []
        
        # Mouse + Mouse Pad combinations
        for mouse in gaming_products[42]:  # Mice
            for mousepad in gaming_products[43]:  # Mouse Pads
                combinations.append([mouse, mousepad])
        
        # Keyboard + Wrist Rest combinations
        for keyboard in gaming_products[41]:  # Keyboards
            for wristrest in gaming_products[44]:  # Wrist Rests
                combinations.append([keyboard, wristrest])
        
        # Complete gaming setup combinations
        for keyboard in gaming_products[41][:10]:  # First 10 keyboards
            for mouse in gaming_products[42][:10]:  # First 10 mice
                for mousepad in gaming_products[43][:5]:  # First 5 mouse pads
                    for wristrest in gaming_products[44][:5]:  # First 5 wrist rests
                        combinations.append([keyboard, mouse, mousepad, wristrest])
        
        # Brand-specific combinations (Razer, HyperX, ASUS, etc.)
        razer_products = []
        hyperx_products = []
        asus_products = []
        logitech_products = []
        steelseries_products = []
        corsair_products = []
        glorious_products = []
        
        for subcat_id in [41, 42, 43, 44]:
            for product in gaming_products[subcat_id]:
                if 'Razer' in product['product_name']:
                    razer_products.append(product)
                elif 'HyperX' in product['product_name']:
                    hyperx_products.append(product)
                elif 'ASUS' in product['product_name']:
                    asus_products.append(product)
                elif 'Logitech' in product['product_name']:
                    logitech_products.append(product)
                elif 'SteelSeries' in product['product_name']:
                    steelseries_products.append(product)
                elif 'Corsair' in product['product_name']:
                    corsair_products.append(product)
                elif 'Glorious' in product['product_name']:
                    glorious_products.append(product)
        
        # Add brand-specific combinations
        for brand_products in [razer_products, hyperx_products, asus_products, 
                              logitech_products, steelseries_products, corsair_products, glorious_products]:
            if len(brand_products) >= 2:
                # Create combinations of 2-4 products from same brand
                for i in range(min(20, len(brand_products) // 2)):  # Max 20 combinations per brand
                    if len(brand_products) >= 4:
                        combinations.append(brand_products[i*4:i*4+4])
                    elif len(brand_products) >= 3:
                        combinations.append(brand_products[i*3:i*3+3])
                    else:
                        combinations.append(brand_products[i*2:i*2+2])
        
        print(f"📦 {len(combinations)} kombinasyon hazırlandı")
        
        # Create baskets and basket products
        baskets_created = 0
        products_added = 0
        
        for combo in combinations:
            if len(combo) < 2:
                continue
                
            # Select random basket
            basket_id = random.choice(existing_baskets)
            
            # Add products to basket
            for product in combo:
                try:
                    basket_cursor.execute("""
                        INSERT INTO basket_product_units 
                        (basket_id, product_id, product_unit_price, product_quantity)
                        VALUES (%s, %s, %s, %s)
                    """, (basket_id, product['product_id'], product['product_price'], 1))
                    products_added += 1
                except mysql.connector.IntegrityError:
                    pass  # Product might already be in this basket
            
            baskets_created += 1
            
            # Create new basket for next combination
            if baskets_created % 50 == 0:  # Create new basket every 50 combinations
                try:
                    basket_cursor.execute("""
                        INSERT INTO baskets (customer_id, basket_status_id)
                        VALUES (%s, %s)
                    """, (random.randint(1, 100), random.choice([1, 4])))
                    new_basket_id = basket_cursor.lastrowid
                    existing_baskets.append(new_basket_id)
                except:
                    pass
        
        basket_conn.commit()
        print(f"✅ {baskets_created} sepet kombinasyonu oluşturuldu!")
        print(f"✅ {products_added} ürün sepete eklendi!")
        
    except Exception as e:
        print(f"❌ Hata: {e}")
    finally:
        if 'product_conn' in locals():
            product_conn.close()
        if 'basket_conn' in locals():
            basket_conn.close()

def main():
    print("🎮 Oyuncu Periferikleri Ekleme Başlıyor...")
    print("=" * 50)
    
    # Step 1: Add gaming subcategories
    add_gaming_subcategories()
    
    # Step 2: Add gaming products
    products = add_gaming_products()
    
    # Step 3: Create gaming baskets
    create_gaming_baskets()
    
    print("=" * 50)
    print("🎉 Oyuncu periferikleri başarıyla eklendi!")

if __name__ == "__main__":
    main() 