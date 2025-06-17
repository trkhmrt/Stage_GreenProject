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

def check_subcategories():
    """Check all available subcategories"""
    conn = mysql.connector.connect(**PRODUCT_DB)
    cursor = conn.cursor(dictionary=True)
    
    try:
        print("🔍 Alt kategoriler kontrol ediliyor...")
        
        # Get all subcategories with category info
        cursor.execute("""
            SELECT sc.sub_category_id, sc.sub_category_name, c.category_name
            FROM sub_categories sc
            JOIN categories c ON sc.category_id = c.category_id
            ORDER BY sc.sub_category_id
        """)
        
        subcategories = cursor.fetchall()
        
        print(f"📊 {len(subcategories)} alt kategori bulundu:")
        print("=" * 60)
        
        for subcat in subcategories:
            print(f"ID: {subcat['sub_category_id']:2d} | {subcat['sub_category_name']:<25} | {subcat['category_name']}")
        
        # Check for kitchen/food related categories
        print("\n🍽️ Mutfak/Yemek ile ilgili kategoriler:")
        print("-" * 40)
        
        kitchen_keywords = ['mutfak', 'yemek', 'gıda', 'içecek', 'çay', 'kahve', 'bardağı', 'tabak']
        
        for subcat in subcategories:
            subcat_name = subcat['sub_category_name'].lower()
            if any(keyword in subcat_name for keyword in kitchen_keywords):
                print(f"✅ {subcat['sub_category_id']}: {subcat['sub_category_name']} ({subcat['category_name']})")
        
    except Exception as e:
        print(f"❌ Hata: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_subcategories() 