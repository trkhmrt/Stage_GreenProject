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

def add_missing_categories():
    """Add missing categories and subcategories"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        print("🔧 Eksik kategoriler ve alt kategoriler ekleniyor...")
        
        # Get next IDs
        next_category_id = get_next_id(cursor, "categories", "category_id")
        next_subcategory_id = get_next_id(cursor, "sub_categories", "sub_category_id")
        
        # Get existing categories
        cursor.execute("SELECT category_id, category_name FROM categories")
        categories = cursor.fetchall()
        category_map = {cat[1]: cat[0] for cat in categories}
        
        print(f"📋 Mevcut kategoriler:")
        for cat_name, cat_id in category_map.items():
            print(f"   {cat_id}: {cat_name}")
        
        # Add missing main categories
        missing_categories = [
            "Ev & Yaşam",
            "Spor & Fitness", 
            "Müzik & Ses",
            "Otomotiv",
            "Eğitim & Ofis"
        ]
        
        added_categories = 0
        for category_name in missing_categories:
            if category_name not in category_map:
                cursor.execute("""
                    INSERT INTO categories (category_id, category_name)
                    VALUES (%s, %s)
                """, (next_category_id, category_name))
                
                category_map[category_name] = next_category_id
                print(f"✅ '{category_name}' kategorisi eklendi (ID: {next_category_id})")
                next_category_id += 1
                added_categories += 1
            else:
                print(f"⚠️ '{category_name}' kategorisi zaten mevcut")
        
        # Add missing subcategories
        missing_subcategories = [
            ("Elektronik Ev Aletleri", "Ev & Yaşam"),
            ("Mobilya", "Ev & Yaşam"),
            ("Fitness Ekipmanları", "Spor & Fitness"),
            ("Bisiklet", "Spor & Fitness"),
            ("Kulaklıklar", "Müzik & Ses"),
            ("Hoparlörler", "Müzik & Ses"),
            ("Araç Aksesuarları", "Otomotiv")
        ]
        
        added_subcategories = 0
        for subcategory_name, category_name in missing_subcategories:
            if category_name in category_map:
                category_id = category_map[category_name]
                
                cursor.execute("""
                    INSERT INTO sub_categories (sub_category_id, sub_category_name, category_id)
                    VALUES (%s, %s, %s)
                """, (next_subcategory_id, subcategory_name, category_id))
                
                print(f"✅ '{subcategory_name}' alt kategorisi eklendi (ID: {next_subcategory_id}) -> {category_name}")
                next_subcategory_id += 1
                added_subcategories += 1
            else:
                print(f"❌ '{category_name}' kategorisi bulunamadı!")
        
        conn.commit()
        print(f"\n🎉 {added_categories} kategori ve {added_subcategories} alt kategori eklendi!")
        
        # Show summary
        cursor.execute("SELECT COUNT(*) FROM categories")
        total_categories = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM sub_categories")
        total_subcategories = cursor.fetchone()[0]
        print(f"📊 Toplam kategori sayısı: {total_categories}")
        print(f"📊 Toplam alt kategori sayısı: {total_subcategories}")
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    add_missing_categories() 