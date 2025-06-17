import pandas as pd
from sqlalchemy import text, create_engine
import re

def update_products_with_model_data():
    """Update products with proper model and model year data"""
    
    # Database configuration
    product_host = "localhost"
    product_port = 3301
    product_database = "productservicedb"
    username = "root"
    password = "root"
    
    try:
        # Connect to product database
        product_connection_string = f"mysql+mysqlconnector://{username}:{password}@{product_host}:{product_port}/{product_database}"
        product_engine = create_engine(product_connection_string)
        
        print("🔍 Ürünler güncelleniyor...")
        
        # Get all products
        products_query = """
        SELECT 
            product_id,
            product_name,
            product_description,
            product_price,
            product_quantity,
            product_model,
            product_model_year,
            product_image_url,
            product_sub_category_id
        FROM products
        ORDER BY product_id
        """
        
        products_df = pd.read_sql(text(products_query), product_engine)
        
        print(f"📦 Toplam {len(products_df)} ürün bulundu")
        
        # Define phone models and their years
        phone_models = {
            # iPhone models
            'iPhone 15': {'model': 'iPhone 15', 'year': '2023'},
            'iPhone 15 Pro': {'model': 'iPhone 15 Pro', 'year': '2023'},
            'iPhone 15 Pro Max': {'model': 'iPhone 15 Pro Max', 'year': '2023'},
            'iPhone 15 Plus': {'model': 'iPhone 15 Plus', 'year': '2023'},
            'iPhone 14': {'model': 'iPhone 14', 'year': '2022'},
            'iPhone 14 Pro': {'model': 'iPhone 14 Pro', 'year': '2022'},
            'iPhone 14 Pro Max': {'model': 'iPhone 14 Pro Max', 'year': '2022'},
            'iPhone 14 Plus': {'model': 'iPhone 14 Plus', 'year': '2022'},
            'iPhone 13': {'model': 'iPhone 13', 'year': '2021'},
            'iPhone 13 Pro': {'model': 'iPhone 13 Pro', 'year': '2021'},
            'iPhone 13 Pro Max': {'model': 'iPhone 13 Pro Max', 'year': '2021'},
            'iPhone 13 mini': {'model': 'iPhone 13 mini', 'year': '2021'},
            'iPhone 12': {'model': 'iPhone 12', 'year': '2020'},
            'iPhone 12 Pro': {'model': 'iPhone 12 Pro', 'year': '2020'},
            'iPhone 12 Pro Max': {'model': 'iPhone 12 Pro Max', 'year': '2020'},
            'iPhone 12 mini': {'model': 'iPhone 12 mini', 'year': '2020'},
            'iPhone 11': {'model': 'iPhone 11', 'year': '2019'},
            'iPhone 11 Pro': {'model': 'iPhone 11 Pro', 'year': '2019'},
            'iPhone 11 Pro Max': {'model': 'iPhone 11 Pro Max', 'year': '2019'},
            'iPhone XR': {'model': 'iPhone XR', 'year': '2018'},
            'iPhone XS': {'model': 'iPhone XS', 'year': '2018'},
            'iPhone XS Max': {'model': 'iPhone XS Max', 'year': '2018'},
            'iPhone X': {'model': 'iPhone X', 'year': '2017'},
            'iPhone 8': {'model': 'iPhone 8', 'year': '2017'},
            'iPhone 8 Plus': {'model': 'iPhone 8 Plus', 'year': '2017'},
            'iPhone SE': {'model': 'iPhone SE', 'year': '2020'},
            'iPhone SE 2': {'model': 'iPhone SE 2', 'year': '2020'},
            'iPhone SE 3': {'model': 'iPhone SE 3', 'year': '2022'},
            
            # Samsung models
            'Galaxy S24': {'model': 'Galaxy S24', 'year': '2024'},
            'Galaxy S24 Plus': {'model': 'Galaxy S24 Plus', 'year': '2024'},
            'Galaxy S24 Ultra': {'model': 'Galaxy S24 Ultra', 'year': '2024'},
            'Galaxy S23': {'model': 'Galaxy S23', 'year': '2023'},
            'Galaxy S23 Plus': {'model': 'Galaxy S23 Plus', 'year': '2023'},
            'Galaxy S23 Ultra': {'model': 'Galaxy S23 Ultra', 'year': '2023'},
            'Galaxy S22': {'model': 'Galaxy S22', 'year': '2022'},
            'Galaxy S22 Plus': {'model': 'Galaxy S22 Plus', 'year': '2022'},
            'Galaxy S22 Ultra': {'model': 'Galaxy S22 Ultra', 'year': '2022'},
            'Galaxy S21': {'model': 'Galaxy S21', 'year': '2021'},
            'Galaxy S21 Plus': {'model': 'Galaxy S21 Plus', 'year': '2021'},
            'Galaxy S21 Ultra': {'model': 'Galaxy S21 Ultra', 'year': '2021'},
            'Galaxy S20': {'model': 'Galaxy S20', 'year': '2020'},
            'Galaxy S20 Plus': {'model': 'Galaxy S20 Plus', 'year': '2020'},
            'Galaxy S20 Ultra': {'model': 'Galaxy S20 Ultra', 'year': '2020'},
            'Galaxy Note 20': {'model': 'Galaxy Note 20', 'year': '2020'},
            'Galaxy Note 20 Ultra': {'model': 'Galaxy Note 20 Ultra', 'year': '2020'},
            'Galaxy Z Fold': {'model': 'Galaxy Z Fold', 'year': '2023'},
            'Galaxy Z Flip': {'model': 'Galaxy Z Flip', 'year': '2023'},
            'Galaxy A54': {'model': 'Galaxy A54', 'year': '2023'},
            'Galaxy A34': {'model': 'Galaxy A34', 'year': '2023'},
            'Galaxy A24': {'model': 'Galaxy A24', 'year': '2023'},
            'Galaxy A14': {'model': 'Galaxy A14', 'year': '2023'},
            
            # Other brands
            'Pixel 8': {'model': 'Pixel 8', 'year': '2023'},
            'Pixel 8 Pro': {'model': 'Pixel 8 Pro', 'year': '2023'},
            'Pixel 7': {'model': 'Pixel 7', 'year': '2022'},
            'Pixel 7 Pro': {'model': 'Pixel 7 Pro', 'year': '2022'},
            'OnePlus 11': {'model': 'OnePlus 11', 'year': '2023'},
            'OnePlus 10': {'model': 'OnePlus 10', 'year': '2022'},
            'Xiaomi 13': {'model': 'Xiaomi 13', 'year': '2023'},
            'Xiaomi 12': {'model': 'Xiaomi 12', 'year': '2022'},
            'Huawei P60': {'model': 'Huawei P60', 'year': '2023'},
            'Huawei P50': {'model': 'Huawei P50', 'year': '2022'},
        }
        
        # Update products with model and year data
        updated_count = 0
        
        for idx, product in products_df.iterrows():
            product_name = product['product_name']
            current_model = product['product_model']
            current_year = product['product_model_year']
            
            # Skip if already has model and year data
            if current_model and current_year:
                continue
                
            # Find matching model
            matched_model = None
            for model_key, model_data in phone_models.items():
                if model_key.lower() in product_name.lower():
                    matched_model = model_data
                    break
            
            if matched_model:
                # Update the product
                update_query = """
                UPDATE products 
                SET product_model = %s, product_model_year = %s
                WHERE product_id = %s
                """
                
                with product_engine.connect() as conn:
                    conn.execute(text(update_query), 
                                (matched_model['model'], matched_model['year'], product['product_id']))
                    conn.commit()
                
                print(f"✅ Güncellendi: {product_name} -> {matched_model['model']} ({matched_model['year']})")
                updated_count += 1
            else:
                print(f"⚠️  Eşleşme bulunamadı: {product_name}")
        
        print(f"\n🎉 Toplam {updated_count} ürün güncellendi!")
        
        # Show final results
        print(f"\n📊 Güncelleme sonrası durum:")
        final_query = """
        SELECT 
            COUNT(*) as total_products,
            SUM(CASE WHEN product_model IS NOT NULL THEN 1 ELSE 0 END) as with_model,
            SUM(CASE WHEN product_model_year IS NOT NULL THEN 1 ELSE 0 END) as with_year
        FROM products
        """
        
        final_stats = pd.read_sql(text(final_query), product_engine)
        print(f"Toplam ürün: {final_stats.iloc[0]['total_products']}")
        print(f"Model bilgisi olan: {final_stats.iloc[0]['with_model']}")
        print(f"Yıl bilgisi olan: {final_stats.iloc[0]['with_year']}")
        
        # Show some examples
        print(f"\n📱 Örnek güncellenmiş ürünler:")
        examples_query = """
        SELECT product_id, product_name, product_model, product_model_year
        FROM products 
        WHERE product_model IS NOT NULL 
        ORDER BY product_id 
        LIMIT 10
        """
        
        examples_df = pd.read_sql(text(examples_query), product_engine)
        for _, example in examples_df.iterrows():
            print(f"  {example['product_id']:3d}. {example['product_name']} -> {example['product_model']} ({example['product_model_year']})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    update_products_with_model_data() 