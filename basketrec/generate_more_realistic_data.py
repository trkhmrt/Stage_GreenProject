#!/usr/bin/env python3
import mysql.connector
import random
from datetime import datetime, timedelta
import pandas as pd

# Database configurations
PRODUCT_DB = {
    'host': 'localhost',
    'port': 3301,
    'user': 'root',
    'password': 'root',
    'database': 'productservicedb'
}

BASKET_DB = {
    'host': 'localhost',
    'port': 3309,
    'user': 'root',
    'password': 'root',
    'database': 'basketservicedb'
}

def get_connection(db_config):
    return mysql.connector.connect(**db_config)

def get_next_id(cursor, table, id_col):
    cursor.execute(f"SELECT MAX({id_col}) FROM {table}")
    result = cursor.fetchone()
    return (result[0] or 0) + 1

def get_all_products():
    """Get all products from productservicedb"""
    conn = get_connection(PRODUCT_DB)
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT 
                product_id,
                product_name,
                product_price,
                product_model,
                product_model_year,
                product_sub_category_id
            FROM products
            ORDER BY product_id
        """)
        
        products = cursor.fetchall()
        print(f"📦 {len(products)} ürün productservicedb'den alındı")
        return products
        
    except Exception as e:
        print(f"❌ Ürün alma hatası: {e}")
        return []
    finally:
        conn.close()

def categorize_products(products):
    """Categorize products for logical combinations"""
    categories = {
        'gaming': [],
        'computer': [],
        'phone': [],
        'home': [],
        'fitness': [],
        'audio': [],
        'automotive': [],
        'fashion': [],
        'tea': []
    }
    
    for product in products:
        name = product['product_name'].lower()
        
        if any(keyword in name for keyword in ['playstation', 'xbox', 'nintendo', 'gta', 'call of duty', 'mario', 'controller', 'game']):
            categories['gaming'].append(product)
        elif any(keyword in name for keyword in ['macbook', 'dell', 'lenovo', 'mouse', 'hub', 'stand', 'laptop']):
            categories['computer'].append(product)
        elif any(keyword in name for keyword in ['samsung', 'iphone', 'huawei', 'xiaomi', 'phone', 'charger', 'earbuds']):
            categories['phone'].append(product)
        elif any(keyword in name for keyword in ['philips', 'bosch', 'siemens', 'arçelik', 'beko', 'ikea', 'bellona', 'çilek', 'mobilya']):
            categories['home'].append(product)
        elif any(keyword in name for keyword in ['bowflex', 'concept2', 'peloton', 'trek', 'specialized', 'fitness']):
            categories['fitness'].append(product)
        elif any(keyword in name for keyword in ['sony', 'bose', 'jbl', 'kulaklık', 'hoparlör']):
            categories['audio'].append(product)
        elif any(keyword in name for keyword in ['garmin', 'blackvue', 'carlinkit', 'gps', 'dashcam']):
            categories['automotive'].append(product)
        elif any(keyword in name for keyword in ['nike', 'adidas', 'puma', 'zara', 'h&m', 'mavi', 'jean', 'ayakkabı']):
            categories['fashion'].append(product)
        elif any(keyword in name for keyword in ['çay', 'fincan', 'kaşık', 'tabak', 'saucer']):
            categories['tea'].append(product)
    
    return categories

def generate_extensive_combinations():
    """Generate extensive realistic product combinations"""
    
    all_products = get_all_products()
    categories = categorize_products(all_products)
    
    print("\n📋 Ürün kategorileri:")
    for category, products in categories.items():
        print(f"   {category}: {len(products)} ürün")
    
    # Define extensive combination patterns
    combination_patterns = [
        # Gaming combinations (high frequency)
        {
            'name': 'Gaming Console + Game',
            'categories': ['gaming'],
            'min_products': 2,
            'max_products': 3,
            'count': 150
        },
        {
            'name': 'Gaming Console + Controller',
            'categories': ['gaming'],
            'min_products': 2,
            'max_products': 3,
            'count': 120
        },
        {
            'name': 'Gaming Full Setup',
            'categories': ['gaming'],
            'min_products': 3,
            'max_products': 4,
            'count': 80
        },
        
        # Computer combinations
        {
            'name': 'Laptop + Mouse',
            'categories': ['computer'],
            'min_products': 2,
            'max_products': 2,
            'count': 100
        },
        {
            'name': 'Laptop + Accessories',
            'categories': ['computer'],
            'min_products': 2,
            'max_products': 3,
            'count': 80
        },
        {
            'name': 'Computer Full Setup',
            'categories': ['computer'],
            'min_products': 3,
            'max_products': 4,
            'count': 60
        },
        
        # Phone combinations
        {
            'name': 'Phone + Charger',
            'categories': ['phone'],
            'min_products': 2,
            'max_products': 2,
            'count': 200
        },
        {
            'name': 'Phone + Earbuds',
            'categories': ['phone'],
            'min_products': 2,
            'max_products': 2,
            'count': 150
        },
        {
            'name': 'Phone + Accessories',
            'categories': ['phone'],
            'min_products': 2,
            'max_products': 3,
            'count': 100
        },
        
        # Home combinations
        {
            'name': 'Home Appliance + Furniture',
            'categories': ['home'],
            'min_products': 2,
            'max_products': 3,
            'count': 50
        },
        
        # Fitness combinations
        {
            'name': 'Fitness Equipment',
            'categories': ['fitness'],
            'min_products': 1,
            'max_products': 2,
            'count': 40
        },
        
        # Audio combinations
        {
            'name': 'Audio Setup',
            'categories': ['audio'],
            'min_products': 1,
            'max_products': 2,
            'count': 60
        },
        
        # Fashion combinations
        {
            'name': 'Shoes + Clothing',
            'categories': ['fashion'],
            'min_products': 2,
            'max_products': 3,
            'count': 120
        },
        {
            'name': 'Fashion Set',
            'categories': ['fashion'],
            'min_products': 3,
            'max_products': 4,
            'count': 80
        },
        
        # Tea combinations
        {
            'name': 'Tea Set Complete',
            'categories': ['tea'],
            'min_products': 3,
            'max_products': 4,
            'count': 60
        },
        
        # Cross-category combinations
        {
            'name': 'Gaming + Audio',
            'categories': ['gaming', 'audio'],
            'min_products': 2,
            'max_products': 3,
            'count': 80
        },
        {
            'name': 'Computer + Audio',
            'categories': ['computer', 'audio'],
            'min_products': 2,
            'max_products': 3,
            'count': 60
        },
        {
            'name': 'Phone + Fashion',
            'categories': ['phone', 'fashion'],
            'min_products': 2,
            'max_products': 3,
            'count': 100
        },
        {
            'name': 'Home + Tea',
            'categories': ['home', 'tea'],
            'min_products': 2,
            'max_products': 4,
            'count': 40
        },
        {
            'name': 'Gaming + Computer',
            'categories': ['gaming', 'computer'],
            'min_products': 2,
            'max_products': 3,
            'count': 50
        },
        {
            'name': 'Phone + Computer',
            'categories': ['phone', 'computer'],
            'min_products': 2,
            'max_products': 3,
            'count': 70
        }
    ]
    
    # Generate combinations
    all_combinations = []
    
    for pattern in combination_patterns:
        print(f"   🔄 {pattern['name']}: {pattern['count']} kombinasyon oluşturuluyor...")
        
        for _ in range(pattern['count']):
            combination = []
            
            # Select products from specified categories
            for category in pattern['categories']:
                if category in categories and categories[category]:
                    num_products = random.randint(
                        pattern['min_products'], 
                        min(pattern['max_products'], len(categories[category]))
                    )
                    selected_products = random.sample(categories[category], num_products)
                    combination.extend(selected_products)
            
            if combination:
                all_combinations.append({
                    'products': combination,
                    'pattern': pattern['name']
                })
    
    # Add single product baskets (high frequency items)
    high_frequency_products = []
    for category, products in categories.items():
        if category in ['phone', 'gaming', 'computer', 'fashion']:
            high_frequency_products.extend(products)
    
    for product in high_frequency_products:
        if random.random() < 0.3:  # 30% chance for high frequency products
            all_combinations.append({
                'products': [product],
                'pattern': 'Single Product'
            })
    
    # Add some random combinations
    for _ in range(200):
        category = random.choice(list(categories.keys()))
        if categories[category]:
            num_products = random.randint(1, min(3, len(categories[category])))
            selected_products = random.sample(categories[category], num_products)
            all_combinations.append({
                'products': selected_products,
                'pattern': f'Random {category.title()}'
            })
    
    print(f"\n🎯 Toplam {len(all_combinations)} farklı kombinasyon oluşturuldu")
    
    return all_combinations

def create_baskets_from_combinations(combinations):
    """Create actual basket records from combinations"""
    conn = get_connection(BASKET_DB)
    cursor = conn.cursor()
    
    try:
        next_basket_id = get_next_id(cursor, 'baskets', 'basket_id')
        next_bpu_id = get_next_id(cursor, 'basket_product_units', 'basket_product_unit_id')
        
        customer_ids = list(range(1, 101))  # 100 different customers
        basket_status_ids = [1, 2, 3, 4]  # Different statuses
        
        created_baskets = 0
        created_products = 0
        
        print(f"\n🛒 Sepetler oluşturuluyor...")
        
        for combo in combinations:
            # Create basket
            basket_id = next_basket_id
            create_date = (datetime.now() - timedelta(days=random.randint(1, 180))).strftime('%Y-%m-%d %H:%M:%S')
            customer_id = random.choice(customer_ids)
            basket_status_id = random.choice(basket_status_ids)
            
            cursor.execute(
                "INSERT INTO baskets (basket_id, create_date, customer_id, basket_status_id) VALUES (%s, %s, %s, %s)",
                (basket_id, create_date, customer_id, basket_status_id)
            )
            
            # Add products to basket
            for product in combo['products']:
                quantity = random.randint(1, 3)
                unit_price = float(product['product_price'])
                total_price = unit_price * quantity
                
                cursor.execute(
                    '''INSERT INTO basket_product_units (
                        basket_product_unit_id, product_id, product_model, product_model_year, product_name,
                        product_quantity, product_total_price, product_unit_price, basket_id
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                    (
                        next_bpu_id,
                        product['product_id'],
                        product['product_model'],
                        product['product_model_year'],
                        product['product_name'],
                        quantity,
                        total_price,
                        unit_price,
                        basket_id
                    )
                )
                next_bpu_id += 1
                created_products += 1
            
            next_basket_id += 1
            created_baskets += 1
            
            if created_baskets % 200 == 0:
                print(f"   ✅ {created_baskets} sepet oluşturuldu...")
        
        conn.commit()
        print(f"\n🎉 {created_baskets} sepet ve {created_products} sepet ürünü başarıyla oluşturuldu!")
        
        # Show summary
        cursor.execute("SELECT COUNT(*) FROM baskets")
        total_baskets = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM basket_product_units")
        total_products = cursor.fetchone()[0]
        
        print(f"\n📊 Genel istatistikler:")
        print(f"   Toplam sepet sayısı: {total_baskets}")
        print(f"   Toplam sepet ürünü: {total_products}")
        
    except Exception as e:
        print(f"❌ Sepet oluşturma hatası: {e}")
        conn.rollback()
    finally:
        conn.close()

def main():
    """Main function to generate extensive realistic basket data"""
    print("🚀 Kapsamlı gerçekçi sepet verileri oluşturuluyor...")
    print("=" * 60)
    
    # Generate combinations
    combinations = generate_extensive_combinations()
    
    # Create baskets
    create_baskets_from_combinations(combinations)
    
    print("\n✅ İşlem tamamlandı!")

if __name__ == "__main__":
    main() 