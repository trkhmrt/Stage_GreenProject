#!/usr/bin/env python3
import mysql.connector
import random

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

def get_next_product_id(cursor):
    """Get the next available product_id"""
    cursor.execute("SELECT MAX(product_id) FROM products")
    result = cursor.fetchone()
    return (result[0] or 0) + 1

def get_subcategory_id(cursor, subcategory_name):
    """Get subcategory_id by name"""
    cursor.execute("SELECT sub_category_id FROM sub_categories WHERE sub_category_name = %s", (subcategory_name,))
    result = cursor.fetchone()
    return result[0] if result else None

def add_tea_products():
    """Add tea-related products to the database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        print("🍵 Çay ürünleri ekleniyor...")
        
        # Get next product ID
        next_id = get_next_product_id(cursor)
        
        # Tea products data
        tea_products = [
            # Çay Bardakları
            {
                'name': 'Porselen Çay Bardağı',
                'description': 'Elegant porselen çay bardağı, 200ml kapasite',
                'price': 89.99,
                'quantity': 50,
                'model': 'Porselen Çay Bardağı',
                'model_year': '2024',
                'subcategory': 'Mutfak & Yemek'
            },
            {
                'name': 'Cam Çay Bardağı Seti',
                'description': '6 adet şeffaf cam çay bardağı, 180ml',
                'price': 129.99,
                'quantity': 30,
                'model': 'Cam Çay Bardağı Seti',
                'model_year': '2024',
                'subcategory': 'Mutfak & Yemek'
            },
            {
                'name': 'Seramik Çay Bardağı',
                'description': 'El yapımı seramik çay bardağı, doğal renkler',
                'price': 69.99,
                'quantity': 40,
                'model': 'Seramik Çay Bardağı',
                'model_year': '2024',
                'subcategory': 'Mutfak & Yemek'
            },
            {
                'name': 'Paslanmaz Çelik Çay Bardağı',
                'description': 'Isı yalıtımlı paslanmaz çelik çay bardağı',
                'price': 149.99,
                'quantity': 25,
                'model': 'Paslanmaz Çelik Çay Bardağı',
                'model_year': '2024',
                'subcategory': 'Mutfak & Yemek'
            },
            
            # Çay Kaşıkları
            {
                'name': 'Gümüş Çay Kaşığı Seti',
                'description': '6 adet 925 ayar gümüş çay kaşığı',
                'price': 299.99,
                'quantity': 20,
                'model': 'Gümüş Çay Kaşığı Seti',
                'model_year': '2024',
                'subcategory': 'Mutfak & Yemek'
            },
            {
                'name': 'Paslanmaz Çelik Çay Kaşığı',
                'description': 'Kaliteli paslanmaz çelik çay kaşığı, 12 adet',
                'price': 79.99,
                'quantity': 35,
                'model': 'Paslanmaz Çelik Çay Kaşığı',
                'model_year': '2024',
                'subcategory': 'Mutfak & Yemek'
            },
            {
                'name': 'Ahşap Çay Kaşığı',
                'description': 'Doğal ahşap çay kaşığı, 8 adet',
                'price': 59.99,
                'quantity': 45,
                'model': 'Ahşap Çay Kaşığı',
                'model_year': '2024',
                'subcategory': 'Mutfak & Yemek'
            },
            {
                'name': 'Melamin Çay Kaşığı',
                'description': 'Renkli melamin çay kaşığı seti, 10 adet',
                'price': 49.99,
                'quantity': 50,
                'model': 'Melamin Çay Kaşığı',
                'model_year': '2024',
                'subcategory': 'Mutfak & Yemek'
            },
            
            # Çay Tabağı
            {
                'name': 'Porselen Çay Tabağı',
                'description': 'Elegant porselen çay tabağı, 15cm çap',
                'price': 45.99,
                'quantity': 60,
                'model': 'Porselen Çay Tabağı',
                'model_year': '2024',
                'subcategory': 'Mutfak & Yemek'
            },
            {
                'name': 'Cam Çay Tabağı Seti',
                'description': '6 adet şeffaf cam çay tabağı',
                'price': 89.99,
                'quantity': 30,
                'model': 'Cam Çay Tabağı Seti',
                'model_year': '2024',
                'subcategory': 'Mutfak & Yemek'
            },
            {
                'name': 'Seramik Çay Tabağı',
                'description': 'El yapımı seramik çay tabağı, doğal desenler',
                'price': 39.99,
                'quantity': 40,
                'model': 'Seramik Çay Tabağı',
                'model_year': '2024',
                'subcategory': 'Mutfak & Yemek'
            },
            
            # Çay Setleri
            {
                'name': 'Çay Bardağı ve Tabağı Seti',
                'description': '6 adet porselen çay bardağı ve tabağı seti',
                'price': 199.99,
                'quantity': 25,
                'model': 'Çay Bardağı ve Tabağı Seti',
                'model_year': '2024',
                'subcategory': 'Mutfak & Yemek'
            },
            {
                'name': 'Lüks Çay Seti',
                'description': '6 adet bardak, tabak ve kaşık içeren lüks çay seti',
                'price': 399.99,
                'quantity': 15,
                'model': 'Lüks Çay Seti',
                'model_year': '2024',
                'subcategory': 'Mutfak & Yemek'
            },
            {
                'name': 'Cam Çay Seti',
                'description': '6 adet cam bardak, tabak ve kaşık seti',
                'price': 249.99,
                'quantity': 20,
                'model': 'Cam Çay Seti',
                'model_year': '2024',
                'subcategory': 'Mutfak & Yemek'
            }
        ]
        
        # Get subcategory_id for 'Mutfak & Yemek'
        subcategory_id = get_subcategory_id(cursor, 'Mutfak & Yemek')
        if not subcategory_id:
            print("❌ 'Mutfak & Yemek' alt kategorisi bulunamadı!")
            return
        
        print(f"✅ Alt kategori ID: {subcategory_id}")
        
        # Insert products
        added_count = 0
        for product in tea_products:
            try:
                # Generate image URL
                image_url = f"https://example.com/tea_products/{product['model'].lower().replace(' ', '_')}.jpg"
                
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
                    subcategory_id
                ))
                
                print(f"✅ {product['name']} eklendi (ID: {next_id})")
                next_id += 1
                added_count += 1
                
            except Exception as e:
                print(f"❌ {product['name']} eklenirken hata: {e}")
        
        conn.commit()
        print(f"\n🎉 Toplam {added_count} çay ürünü başarıyla eklendi!")
        
        # Show summary
        cursor.execute("SELECT COUNT(*) FROM products WHERE product_sub_category_id = %s", (subcategory_id,))
        total_products = cursor.fetchone()[0]
        print(f"📊 'Mutfak & Yemek' kategorisinde toplam {total_products} ürün var")
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    add_tea_products() 