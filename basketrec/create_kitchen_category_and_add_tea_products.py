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

def create_kitchen_category_and_add_tea_products():
    """Create kitchen category and add tea products"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        print("🍽️ Mutfak kategorisi oluşturuluyor...")
        
        # 1. Create "Gıda & İçecek" category
        next_category_id = get_next_id(cursor, "categories", "category_id")
        
        cursor.execute("""
            INSERT INTO categories (category_id, category_name)
            VALUES (%s, %s)
        """, (next_category_id, "Gıda & İçecek"))
        
        print(f"✅ 'Gıda & İçecek' kategorisi oluşturuldu (ID: {next_category_id})")
        
        # 2. Create "Mutfak & Yemek" subcategory
        next_subcategory_id = get_next_id(cursor, "sub_categories", "sub_category_id")
        
        cursor.execute("""
            INSERT INTO sub_categories (sub_category_id, sub_category_name, category_id)
            VALUES (%s, %s, %s)
        """, (next_subcategory_id, "Mutfak & Yemek", next_category_id))
        
        print(f"✅ 'Mutfak & Yemek' alt kategorisi oluşturuldu (ID: {next_subcategory_id})")
        
        # 3. Add tea products
        print("\n🍵 Çay ürünleri ekleniyor...")
        
        next_product_id = get_next_id(cursor, "products", "product_id")
        
        # Tea products data
        tea_products = [
            # Çay Bardakları
            {
                'name': 'Porselen Çay Bardağı',
                'description': 'Elegant porselen çay bardağı, 200ml kapasite',
                'price': 89.99,
                'quantity': 50,
                'model': 'Porselen Çay Bardağı',
                'model_year': '2024'
            },
            {
                'name': 'Cam Çay Bardağı Seti',
                'description': '6 adet şeffaf cam çay bardağı, 180ml',
                'price': 129.99,
                'quantity': 30,
                'model': 'Cam Çay Bardağı Seti',
                'model_year': '2024'
            },
            {
                'name': 'Seramik Çay Bardağı',
                'description': 'El yapımı seramik çay bardağı, doğal renkler',
                'price': 69.99,
                'quantity': 40,
                'model': 'Seramik Çay Bardağı',
                'model_year': '2024'
            },
            {
                'name': 'Paslanmaz Çelik Çay Bardağı',
                'description': 'Isı yalıtımlı paslanmaz çelik çay bardağı',
                'price': 149.99,
                'quantity': 25,
                'model': 'Paslanmaz Çelik Çay Bardağı',
                'model_year': '2024'
            },
            
            # Çay Kaşıkları
            {
                'name': 'Gümüş Çay Kaşığı Seti',
                'description': '6 adet 925 ayar gümüş çay kaşığı',
                'price': 299.99,
                'quantity': 20,
                'model': 'Gümüş Çay Kaşığı Seti',
                'model_year': '2024'
            },
            {
                'name': 'Paslanmaz Çelik Çay Kaşığı',
                'description': 'Kaliteli paslanmaz çelik çay kaşığı, 12 adet',
                'price': 79.99,
                'quantity': 35,
                'model': 'Paslanmaz Çelik Çay Kaşığı',
                'model_year': '2024'
            },
            {
                'name': 'Ahşap Çay Kaşığı',
                'description': 'Doğal ahşap çay kaşığı, 8 adet',
                'price': 59.99,
                'quantity': 45,
                'model': 'Ahşap Çay Kaşığı',
                'model_year': '2024'
            },
            {
                'name': 'Melamin Çay Kaşığı',
                'description': 'Renkli melamin çay kaşığı seti, 10 adet',
                'price': 49.99,
                'quantity': 50,
                'model': 'Melamin Çay Kaşığı',
                'model_year': '2024'
            },
            
            # Çay Tabağı
            {
                'name': 'Porselen Çay Tabağı',
                'description': 'Elegant porselen çay tabağı, 15cm çap',
                'price': 45.99,
                'quantity': 60,
                'model': 'Porselen Çay Tabağı',
                'model_year': '2024'
            },
            {
                'name': 'Cam Çay Tabağı Seti',
                'description': '6 adet şeffaf cam çay tabağı',
                'price': 89.99,
                'quantity': 30,
                'model': 'Cam Çay Tabağı Seti',
                'model_year': '2024'
            },
            {
                'name': 'Seramik Çay Tabağı',
                'description': 'El yapımı seramik çay tabağı, doğal desenler',
                'price': 39.99,
                'quantity': 40,
                'model': 'Seramik Çay Tabağı',
                'model_year': '2024'
            },
            
            # Çay Setleri
            {
                'name': 'Çay Bardağı ve Tabağı Seti',
                'description': '6 adet porselen çay bardağı ve tabağı seti',
                'price': 199.99,
                'quantity': 25,
                'model': 'Çay Bardağı ve Tabağı Seti',
                'model_year': '2024'
            },
            {
                'name': 'Lüks Çay Seti',
                'description': '6 adet bardak, tabak ve kaşık içeren lüks çay seti',
                'price': 399.99,
                'quantity': 15,
                'model': 'Lüks Çay Seti',
                'model_year': '2024'
            },
            {
                'name': 'Cam Çay Seti',
                'description': '6 adet cam bardak, tabak ve kaşık seti',
                'price': 249.99,
                'quantity': 20,
                'model': 'Cam Çay Seti',
                'model_year': '2024'
            }
        ]
        
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
                    next_product_id,
                    product['name'],
                    product['description'],
                    product['price'],
                    product['quantity'],
                    product['model'],
                    product['model_year'],
                    image_url,
                    next_subcategory_id
                ))
                
                print(f"✅ {product['name']} eklendi (ID: {next_product_id})")
                next_product_id += 1
                added_count += 1
                
            except Exception as e:
                print(f"❌ {product['name']} eklenirken hata: {e}")
        
        conn.commit()
        print(f"\n🎉 Toplam {added_count} çay ürünü başarıyla eklendi!")
        
        # Show summary
        cursor.execute("SELECT COUNT(*) FROM products WHERE product_sub_category_id = %s", (next_subcategory_id,))
        total_products = cursor.fetchone()[0]
        print(f"📊 'Mutfak & Yemek' kategorisinde toplam {total_products} ürün var")
        
        # Show all categories
        print(f"\n📋 Tüm kategoriler:")
        cursor.execute("SELECT category_id, category_name FROM categories ORDER BY category_id")
        categories = cursor.fetchall()
        for cat in categories:
            print(f"   {cat[0]}: {cat[1]}")
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    create_kitchen_category_and_add_tea_products() 