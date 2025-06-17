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

def add_phone_accessories():
    """Add phone accessories to the database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        print("📱 Telefon aksesuarları ekleniyor...")
        
        # Get next product ID
        next_id = get_next_id(cursor, "products", "product_id")
        
        # Get subcategory IDs
        phone_subcategory_id = get_subcategory_id(cursor, "Telefon Kılıfı")
        accessory_subcategory_id = get_subcategory_id(cursor, "Kablosuz Kulaklık")
        charger_subcategory_id = get_subcategory_id(cursor, "Şarj Aleti")
        
        if not phone_subcategory_id:
            print("❌ 'Telefon Kılıfı' alt kategorisi bulunamadı!")
            return
        
        if not accessory_subcategory_id:
            print("❌ 'Kablosuz Kulaklık' alt kategorisi bulunamadı!")
            return
            
        if not charger_subcategory_id:
            print("❌ 'Şarj Aleti' alt kategorisi bulunamadı!")
            return
        
        print(f"✅ Alt kategori ID'leri: Telefon({phone_subcategory_id}), Kulaklık({accessory_subcategory_id}), Şarj({charger_subcategory_id})")
        
        # Phone accessories data
        accessories = [
            # Samsung Şarj Cihazları
            {
                'name': 'Samsung 25W Super Fast Charging Adapter',
                'description': 'Samsung Galaxy S24, S23, S22 serisi için hızlı şarj adaptörü',
                'price': 299.99,
                'quantity': 50,
                'model': 'Samsung 25W Super Fast Charging',
                'model_year': '2024',
                'subcategory_id': charger_subcategory_id
            },
            {
                'name': 'Samsung 45W Super Fast Charging 2.0',
                'description': 'Samsung Galaxy S24 Ultra için ultra hızlı şarj adaptörü',
                'price': 499.99,
                'quantity': 30,
                'model': 'Samsung 45W Super Fast Charging 2.0',
                'model_year': '2024',
                'subcategory_id': charger_subcategory_id
            },
            {
                'name': 'Samsung Wireless Charger Pad',
                'description': 'Samsung kablosuz şarj pedi, 15W hızlı şarj',
                'price': 399.99,
                'quantity': 40,
                'model': 'Samsung Wireless Charger Pad',
                'model_year': '2024',
                'subcategory_id': charger_subcategory_id
            },
            {
                'name': 'Samsung Wireless Charger Stand',
                'description': 'Samsung kablosuz şarj standı, dikey şarj',
                'price': 449.99,
                'quantity': 25,
                'model': 'Samsung Wireless Charger Stand',
                'model_year': '2024',
                'subcategory_id': charger_subcategory_id
            },
            
            # iPhone Şarj Cihazları
            {
                'name': 'Apple 20W USB-C Power Adapter',
                'description': 'iPhone 15, 14, 13 serisi için Apple orijinal şarj adaptörü',
                'price': 199.99,
                'quantity': 60,
                'model': 'Apple 20W USB-C Power Adapter',
                'model_year': '2024',
                'subcategory_id': charger_subcategory_id
            },
            {
                'name': 'Apple MagSafe Charger',
                'description': 'iPhone 15, 14, 13 serisi için Apple MagSafe kablosuz şarj',
                'price': 599.99,
                'quantity': 35,
                'model': 'Apple MagSafe Charger',
                'model_year': '2024',
                'subcategory_id': charger_subcategory_id
            },
            {
                'name': 'Apple MagSafe Duo Charger',
                'description': 'iPhone ve Apple Watch için çift kablosuz şarj',
                'price': 1299.99,
                'quantity': 20,
                'model': 'Apple MagSafe Duo Charger',
                'model_year': '2024',
                'subcategory_id': charger_subcategory_id
            },
            {
                'name': 'Apple 35W Dual USB-C Power Adapter',
                'description': 'iPhone ve iPad için çift port şarj adaptörü',
                'price': 399.99,
                'quantity': 30,
                'model': 'Apple 35W Dual USB-C Power Adapter',
                'model_year': '2024',
                'subcategory_id': charger_subcategory_id
            },
            
            # Samsung Kablosuz Kulak İçi Kulaklıklar
            {
                'name': 'Samsung Galaxy Buds2 Pro',
                'description': 'Samsung Galaxy Buds2 Pro kablosuz kulak içi kulaklık',
                'price': 1999.99,
                'quantity': 40,
                'model': 'Samsung Galaxy Buds2 Pro',
                'model_year': '2024',
                'subcategory_id': accessory_subcategory_id
            },
            {
                'name': 'Samsung Galaxy Buds FE',
                'description': 'Samsung Galaxy Buds FE ekonomik kablosuz kulaklık',
                'price': 899.99,
                'quantity': 50,
                'model': 'Samsung Galaxy Buds FE',
                'model_year': '2024',
                'subcategory_id': accessory_subcategory_id
            },
            {
                'name': 'Samsung Galaxy Buds Live',
                'description': 'Samsung Galaxy Buds Live fasulye şeklinde kulaklık',
                'price': 1299.99,
                'quantity': 35,
                'model': 'Samsung Galaxy Buds Live',
                'model_year': '2024',
                'subcategory_id': accessory_subcategory_id
            },
            {
                'name': 'Samsung Galaxy Buds2',
                'description': 'Samsung Galaxy Buds2 kablosuz kulak içi kulaklık',
                'price': 1499.99,
                'quantity': 45,
                'model': 'Samsung Galaxy Buds2',
                'model_year': '2024',
                'subcategory_id': accessory_subcategory_id
            }
        ]
        
        # Insert products
        added_count = 0
        for product in accessories:
            try:
                # Generate image URL
                image_url = f"https://example.com/phone_accessories/{product['model'].lower().replace(' ', '_')}.jpg"
                
                cursor.execute("""
                    INSERT INTO products (
                        product_id, product_name, product_description, product_price, 
                        product_quantity, product_model, product_model_year, product_image_url, 
                        product_sub_category_id
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    next_id,
                    product['name'],
                    product['description'],
                    product['price'],
                    product['quantity'],
                    product['model'],
                    product['model_year'],
                    image_url,
                    product['subcategory_id']
                ))
                
                print(f"✅ {product['name']} eklendi (ID: {next_id})")
                next_id += 1
                added_count += 1
                
            except Exception as e:
                print(f"❌ {product['name']} eklenirken hata: {e}")
        
        conn.commit()
        print(f"\n🎉 Toplam {added_count} telefon aksesuarı başarıyla eklendi!")
        
        # Show summary by category
        cursor.execute("SELECT COUNT(*) FROM products WHERE product_sub_category_id = %s", (charger_subcategory_id,))
        charger_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM products WHERE product_sub_category_id = %s", (accessory_subcategory_id,))
        accessory_count = cursor.fetchone()[0]
        
        print(f"📊 Şarj cihazları: {charger_count} adet")
        print(f"📊 Kablosuz kulaklıklar: {accessory_count} adet")
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    add_phone_accessories() 