#!/usr/bin/env python3
import mysql.connector

# Database configurations
BASKET_DB_CONFIG = {
    'host': 'localhost',
    'port': 3309,
    'user': 'root',
    'password': 'root',
    'database': 'basketservicedb'
}

def check_basket_data():
    """Check the current state of basket data"""
    try:
        conn = mysql.connector.connect(**BASKET_DB_CONFIG)
        cursor = conn.cursor()
        
        # Check total baskets
        cursor.execute("SELECT COUNT(*) FROM baskets")
        total_baskets = cursor.fetchone()[0]
        print(f"📊 Toplam sepet sayısı: {total_baskets}")
        
        # Check total basket products
        cursor.execute("SELECT COUNT(*) FROM basket_product_units")
        total_basket_products = cursor.fetchone()[0]
        print(f"📊 Toplam sepet ürünü sayısı: {total_basket_products}")
        
        # Check Dell products in basket_product_units
        cursor.execute("""
            SELECT COUNT(*) FROM basket_product_units 
            WHERE product_name LIKE '%Dell%'
        """)
        dell_products_count = cursor.fetchone()[0]
        print(f"📊 Dell ürünleri sayısı: {dell_products_count}")
        
        # Show some Dell products
        cursor.execute("""
            SELECT basket_id, product_name, product_quantity, product_unit_price 
            FROM basket_product_units 
            WHERE product_name LIKE '%Dell%'
            LIMIT 10
        """)
        dell_products = cursor.fetchall()
        
        if dell_products:
            print("\n🔍 İlk 10 Dell ürünü:")
            for product in dell_products:
                print(f"   - Sepet {product[0]}: {product[1]} (Adet: {product[2]}, Fiyat: {product[3]})")
        else:
            print("\n❌ Dell ürünü bulunamadı!")
        
        # Check recent baskets
        cursor.execute("""
            SELECT basket_id FROM baskets 
            ORDER BY basket_id DESC 
            LIMIT 5
        """)
        recent_baskets = cursor.fetchall()
        print(f"\n🔍 Son 5 sepet ID: {[b[0] for b in recent_baskets]}")
        
        # Check if there are any products in recent baskets
        if recent_baskets:
            max_basket_id = recent_baskets[0][0]
            cursor.execute("""
                SELECT COUNT(*) FROM basket_product_units 
                WHERE basket_id = %s
            """, (max_basket_id,))
            products_in_max_basket = cursor.fetchone()[0]
            print(f"🔍 En son sepet ({max_basket_id}) içindeki ürün sayısı: {products_in_max_basket}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    check_basket_data() 