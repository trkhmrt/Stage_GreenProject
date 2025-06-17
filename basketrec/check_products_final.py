import pandas as pd
from sqlalchemy import text, create_engine

def check_products_final():
    """Final check of existing products"""
    
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
        
        # Get all products
        products_query = """
        SELECT 
            p.product_id,
            p.product_name,
            p.product_price,
            c.category_id,
            c.category_name
        FROM products p
        LEFT JOIN sub_categories sc ON p.product_sub_category_id = sc.sub_category_id
        LEFT JOIN categories c ON sc.category_id = c.category_id
        ORDER BY c.category_id, p.product_id
        """
        
        products_df = pd.read_sql(text(products_query), product_engine)
        
        print(f"📦 Toplam {len(products_df)} ürün bulundu")
        
        # Show categories
        categories = products_df.groupby(['category_id', 'category_name']).size().reset_index()
        print(f"\n📂 Kategoriler:")
        for _, cat in categories.iterrows():
            print(f"  Kategori {cat['category_id']}: {cat['category_name']} ({cat[0]} ürün)")
        
        # Show phones (category 1)
        phones = products_df[products_df['category_id'] == 1]
        print(f"\n📱 Telefonlar (Kategori 1):")
        for _, phone in phones.iterrows():
            print(f"  {phone['product_id']:3d}. {phone['product_name']}")
        
        # Show case-like products
        case_keywords = ['kılıf', 'case', 'cover', 'koruma']
        case_products = products_df[products_df['product_name'].str.contains('|'.join(case_keywords), case=False, na=False)]
        print(f"\n📱 Kılıf Benzeri Ürünler:")
        for _, case in case_products.iterrows():
            print(f"  {case['product_id']:3d}. {case['product_name']} (Kategori {case['category_id']})")
        
        return products_df, phones, case_products
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None, None, None

if __name__ == "__main__":
    check_products_final() 