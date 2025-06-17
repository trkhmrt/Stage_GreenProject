import pandas as pd
from sqlalchemy import text, create_engine

def check_phone_products():
    """Check existing phone and case products"""
    
    # Database configuration
    product_host = "localhost"
    product_port = 3301
    product_database = "productservicedb"
    username = "root"
    password = "root"
    
    # Connect to product database
    product_connection_string = f"mysql+mysqlconnector://{username}:{password}@{product_host}:{product_port}/{product_database}"
    product_engine = create_engine(product_connection_string)
    
    # Get all products with category info
    products_query = """
    SELECT 
        p.product_id,
        p.product_name,
        p.product_description,
        p.product_price,
        p.product_quantity,
        sc.sub_category_id,
        sc.sub_category_name,
        c.category_id,
        c.category_name
    FROM products p
    LEFT JOIN sub_categories sc ON p.product_sub_category_id = sc.sub_category_id
    LEFT JOIN categories c ON sc.category_id = c.category_id
    ORDER BY c.category_id, p.product_id
    """
    
    products_df = pd.read_sql(text(products_query), product_engine)
    
    print("📱 Mevcut Ürünler Analizi:")
    print("=" * 80)
    
    # Show all categories
    print("\n📂 Mevcut Kategoriler:")
    categories = products_df.groupby(['category_id', 'category_name']).size().reset_index()
    for _, cat in categories.iterrows():
        print(f"  Kategori {cat['category_id']}: {cat['category_name']} ({cat[0]} ürün)")
    
    # Find phones (category 1)
    phones = products_df[products_df['category_id'] == 1]
    print(f"\n📱 Kategori 1 - Telefonlar ({len(phones)} ürün):")
    print("-" * 60)
    for _, phone in phones.iterrows():
        print(f"  {phone['product_id']:3d}. {phone['product_name']:<40} | {phone['product_price']:8.2f} TL")
    
    # Find cases (category 32 or case-like products)
    cases = products_df[products_df['category_id'] == 32]
    if len(cases) > 0:
        print(f"\n📱 Kategori 32 - Kılıflar ({len(cases)} ürün):")
        print("-" * 60)
        for _, case in cases.iterrows():
            print(f"  {case['product_id']:3d}. {case['product_name']:<40} | {case['product_price']:8.2f} TL")
    
    # Find case-like products in other categories
    print(f"\n🔍 Kılıf Benzeri Ürünler:")
    print("-" * 60)
    case_keywords = ['kılıf', 'case', 'cover', 'koruma', 'şeffaf', 'silikon', 'deri', 'temperli']
    case_like_products = products_df[products_df['product_name'].str.contains('|'.join(case_keywords), case=False, na=False)]
    
    for _, product in case_like_products.iterrows():
        print(f"  {product['product_id']:3d}. {product['product_name']:<40} | Kategori {product['category_id']}: {product['category_name']}")
    
    return products_df, phones, cases, case_like_products

if __name__ == "__main__":
    check_phone_products() 