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

def analyze_existing_relationships():
    """Analyze existing basket data to understand product relationships"""
    conn = get_connection(BASKET_DB)
    cursor = conn.cursor(dictionary=True)
    
    try:
        print("🔍 Mevcut sepet verilerini analiz ediliyor...")
        
        # Get all basket data
        cursor.execute("""
            SELECT 
                bpu.basket_id,
                bpu.product_name,
                bpu.product_model,
                bpu.product_model_year,
                b.customer_id,
                b.basket_status_id
            FROM basket_product_units bpu
            JOIN baskets b ON bpu.basket_id = b.basket_id
            ORDER BY bpu.basket_id, bpu.product_name
        """)
        
        basket_data = cursor.fetchall()
        
        # Group products by basket
        basket_products = {}
        for row in basket_data:
            basket_id = row['basket_id']
            if basket_id not in basket_products:
                basket_products[basket_id] = []
            basket_products[basket_id].append(row['product_name'])
        
        # Analyze product relationships
        product_relationships = {}
        product_frequency = {}
        
        for basket_id, products in basket_products.items():
            # Count individual product frequency
            for product in products:
                product_frequency[product] = product_frequency.get(product, 0) + 1
            
            # Analyze product pairs
            for i in range(len(products)):
                for j in range(i + 1, len(products)):
                    pair = tuple(sorted([products[i], products[j]]))
                    product_relationships[pair] = product_relationships.get(pair, 0) + 1
        
        print(f"📊 {len(basket_products)} sepet analiz edildi")
        print(f"📦 {len(product_frequency)} farklı ürün bulundu")
        print(f"🔗 {len(product_relationships)} ürün çifti ilişkisi bulundu")
        
        return product_relationships, product_frequency, basket_products
        
    except Exception as e:
        print(f"❌ Analiz hatası: {e}")
        return {}, {}, {}
    finally:
        conn.close()

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

def generate_realistic_combinations():
    """Generate realistic product combinations based on categories and relationships"""
    
    # Analyze existing data
    relationships, frequency, existing_baskets = analyze_existing_relationships()
    all_products = get_all_products()
    categories = categorize_products(all_products)
    
    print("\n📋 Ürün kategorileri:")
    for category, products in categories.items():
        print(f"   {category}: {len(products)} ürün")
    
    # Define realistic combination patterns
    combination_patterns = [
        # Gaming combinations
        {
            'name': 'Gaming Setup',
            'categories': ['gaming'],
            'min_products': 2,
            'max_products': 4,
            'weight': 0.15
        },
        # Computer combinations
        {
            'name': 'Computer Setup',
            'categories': ['computer'],
            'min_products': 2,
            'max_products': 4,
            'weight': 0.12
        },
        # Phone combinations
        {
            'name': 'Phone Accessories',
            'categories': ['phone'],
            'min_products': 2,
            'max_products': 3,
            'weight': 0.10
        },
        # Home combinations
        {
            'name': 'Home Setup',
            'categories': ['home'],
            'min_products': 2,
            'max_products': 3,
            'weight': 0.08
        },
        # Fitness combinations
        {
            'name': 'Fitness Setup',
            'categories': ['fitness'],
            'min_products': 1,
            'max_products': 2,
            'weight': 0.05
        },
        # Audio combinations
        {
            'name': 'Audio Setup',
            'categories': ['audio'],
            'min_products': 1,
            'max_products': 2,
            'weight': 0.08
        },
        # Fashion combinations
        {
            'name': 'Fashion Set',
            'categories': ['fashion'],
            'min_products': 2,
            'max_products': 4,
            'weight': 0.12
        },
        # Tea combinations
        {
            'name': 'Tea Set',
            'categories': ['tea'],
            'min_products': 3,
            'max_products': 4,
            'weight': 0.05
        },
        # Cross-category combinations
        {
            'name': 'Gaming + Audio',
            'categories': ['gaming', 'audio'],
            'min_products': 2,
            'max_products': 3,
            'weight': 0.08
        },
        {
            'name': 'Computer + Audio',
            'categories': ['computer', 'audio'],
            'min_products': 2,
            'max_products': 3,
            'weight': 0.06
        },
        {
            'name': 'Phone + Fashion',
            'categories': ['phone', 'fashion'],
            'min_products': 2,
            'max_products': 3,
            'weight': 0.06
        },
        {
            'name': 'Home + Tea',
            'categories': ['home', 'tea'],
            'min_products': 2,
            'max_products': 4,
            'weight': 0.05
        }
    ]
    
    # Generate combinations
    all_combinations = []
    
    for pattern in combination_patterns:
        num_combinations = int(100 * pattern['weight'])  # Generate based on weight
        
        for _ in range(num_combinations):
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
    
    # Add some single product baskets
    for product in all_products:
        if random.random() < 0.1:  # 10% chance for single product
            all_combinations.append({
                'products': [product],
                'pattern': 'Single Product'
            })
    
    # Add some random combinations based on existing relationships
    for pair, frequency in relationships.items():
        if frequency >= 2 and random.random() < 0.3:  # 30% chance for frequent pairs
            all_combinations.append({
                'products': list(pair),
                'pattern': 'Frequent Pair'
            })
    
    print(f"\n🎯 {len(all_combinations)} farklı kombinasyon oluşturuldu")
    
    return all_combinations

def create_baskets_from_combinations(combinations):
    """Create actual basket records from combinations"""
    conn = get_connection(BASKET_DB)
    cursor = conn.cursor()
    
    try:
        next_basket_id = get_next_id(cursor, 'baskets', 'basket_id')
        next_bpu_id = get_next_id(cursor, 'basket_product_units', 'basket_product_unit_id')
        
        customer_ids = list(range(1, 51))  # 50 different customers
        basket_status_ids = [1, 2, 3, 4]  # Different statuses
        
        created_baskets = 0
        created_products = 0
        
        print(f"\n🛒 Sepetler oluşturuluyor...")
        
        for combo in combinations:
            # Create basket
            basket_id = next_basket_id
            create_date = (datetime.now() - timedelta(days=random.randint(1, 90))).strftime('%Y-%m-%d %H:%M:%S')
            customer_id = random.choice(customer_ids)
            basket_status_id = random.choice(basket_status_ids)
            
            cursor.execute(
                "INSERT INTO baskets (basket_id, create_date, customer_id, basket_status_id) VALUES (%s, %s, %s, %s)",
                (basket_id, create_date, customer_id, basket_status_id)
            )
            
            # Add products to basket
            for product in combo['products']:
                # Check if product is a dictionary (from database) or string (from relationships)
                if isinstance(product, dict):
                    # Product from database
                    product_id = product['product_id']
                    product_model = product['product_model']
                    product_model_year = product['product_model_year']
                    product_name = product['product_name']
                    product_price = float(product['product_price'])
                else:
                    # Product name from relationships - skip for now
                    continue
                
                quantity = random.randint(1, 3)
                unit_price = product_price
                total_price = unit_price * quantity
                
                cursor.execute(
                    '''INSERT INTO basket_product_units (
                        basket_product_unit_id, product_id, product_model, product_model_year, product_name,
                        product_quantity, product_total_price, product_unit_price, basket_id
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                    (
                        next_bpu_id,
                        product_id,
                        product_model,
                        product_model_year,
                        product_name,
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
            
            if created_baskets % 100 == 0:
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
    """Main function to generate realistic basket data"""
    print("🚀 Gerçekçi sepet verileri oluşturuluyor...")
    print("=" * 60)
    
    # Generate combinations
    combinations = generate_realistic_combinations()
    
    # Create baskets
    create_baskets_from_combinations(combinations)
    
    print("\n✅ İşlem tamamlandı!")

if __name__ == "__main__":
    main() 