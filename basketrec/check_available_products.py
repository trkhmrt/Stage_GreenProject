#!/usr/bin/env python3
import mysql.connector

# Database configuration
PRODUCT_DB_CONFIG = {
    'host': 'localhost',
    'port': 3301,
    'user': 'root',
    'password': 'root',
    'database': 'productservicedb'
}

def check_available_products():
    """Check what products are available in the database"""
    try:
        conn = mysql.connector.connect(**PRODUCT_DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        print("🔍 Mevcut ürünler kontrol ediliyor...")
        
        # Get all products with subcategory info
        cursor.execute("""
            SELECT p.product_id, p.product_name, p.product_model, p.product_model_year, 
                   p.product_price, p.product_sub_category_id, sc.sub_category_name
            FROM products p
            JOIN sub_categories sc ON p.product_sub_category_id = sc.sub_category_id
            WHERE p.product_model IS NOT NULL AND p.product_model_year IS NOT NULL
            ORDER BY sc.sub_category_id, p.product_id
        """)
        
        products = cursor.fetchall()
        
        print(f"📊 Toplam {len(products)} ürün bulundu:")
        print("=" * 80)
        
        # Group by subcategory
        subcategory_products = {}
        for product in products:
            subcat_id = product['product_sub_category_id']
            if subcat_id not in subcategory_products:
                subcategory_products[subcat_id] = []
            subcategory_products[subcat_id].append(product)
        
        for subcat_id in sorted(subcategory_products.keys()):
            products_in_subcat = subcategory_products[subcat_id]
            if products_in_subcat:
                print(f"\n📦 Subcategory {subcat_id}: {products_in_subcat[0]['sub_category_name']} ({len(products_in_subcat)} ürün)")
                for product in products_in_subcat[:5]:  # Show first 5 products
                    print(f"   - {product['product_id']}: {product['product_name']} ({product['product_model']}) - {product['product_price']} TL")
                if len(products_in_subcat) > 5:
                    print(f"   ... ve {len(products_in_subcat) - 5} ürün daha")
        
        return subcategory_products
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        return None
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    check_available_products() 