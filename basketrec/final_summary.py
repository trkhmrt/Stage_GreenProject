import pandas as pd
from sqlalchemy import text, create_engine

def final_summary():
    """Show final summary of all data in the system"""
    
    # Database configurations
    product_host = "localhost"
    product_port = 3301
    product_database = "productservicedb"
    basket_host = "localhost"
    basket_port = 3309
    basket_database = "basketservicedb"
    username = "root"
    password = "root"
    
    try:
        # Connect to databases
        product_connection_string = f"mysql+mysqlconnector://{username}:{password}@{product_host}:{product_port}/{product_database}"
        basket_connection_string = f"mysql+mysqlconnector://{username}:{password}@{basket_host}:{basket_port}/{basket_database}"
        product_engine = create_engine(product_connection_string)
        basket_engine = create_engine(basket_connection_string)
        
        print("📊 SİSTEM ÖZETİ")
        print("=" * 60)
        
        # Products summary
        print("\n📦 PRODUCTS VERİTABANI:")
        print("-" * 40)
        
        # Total products
        total_query = "SELECT COUNT(*) as total FROM products"
        total_count = pd.read_sql(text(total_query), product_engine)
        print(f"Toplam ürün: {total_count.iloc[0]['total']}")
        
        # Products by category
        category_query = """
        SELECT 
            sc.sub_category_name,
            COUNT(*) as count
        FROM products p
        LEFT JOIN sub_categories sc ON p.product_sub_category_id = sc.sub_category_id
        GROUP BY sc.sub_category_name
        ORDER BY count DESC
        """
        category_stats = pd.read_sql(text(category_query), product_engine)
        print("\nKategori bazında ürün dağılımı:")
        for _, cat in category_stats.iterrows():
            print(f"  {cat['sub_category_name']}: {cat['count']} ürün")
        
        # Products with model data
        model_query = """
        SELECT 
            COUNT(*) as with_model,
            SUM(CASE WHEN product_model IS NOT NULL AND product_model_year IS NOT NULL THEN 1 ELSE 0 END) as complete_model
        FROM products
        """
        model_stats = pd.read_sql(text(model_query), product_engine)
        print(f"\nModel bilgisi olan ürünler: {model_stats.iloc[0]['with_model']}")
        print(f"Tam model bilgisi olan ürünler: {model_stats.iloc[0]['complete_model']}")
        
        # Gaming products
        print(f"\n🎮 OYUN ÜRÜNLERİ:")
        gaming_query = """
        SELECT 
            product_name,
            product_model,
            product_model_year,
            product_price
        FROM products 
        WHERE product_sub_category_id IN (27, 28)
        ORDER BY product_sub_category_id, product_id
        """
        gaming_products = pd.read_sql(text(gaming_query), product_engine)
        print(f"Toplam oyun ürünü: {len(gaming_products)}")
        
        # Consoles
        consoles = gaming_products[gaming_products['product_name'].str.contains('PlayStation|Xbox', case=False, na=False)]
        print(f"Konsol sayısı: {len(consoles)}")
        
        # Games
        games = gaming_products[~gaming_products['product_name'].str.contains('PlayStation|Xbox', case=False, na=False)]
        print(f"Oyun sayısı: {len(games)}")
        
        # Basket summary
        print(f"\n🛒 BASKET VERİTABANI:")
        print("-" * 40)
        
        # Total baskets
        baskets_query = "SELECT COUNT(*) as total FROM baskets"
        baskets_count = pd.read_sql(text(baskets_query), basket_engine)
        print(f"Toplam sepet: {baskets_count.iloc[0]['total']}")
        
        # Total units
        units_query = "SELECT COUNT(*) as total FROM basket_product_units"
        units_count = pd.read_sql(text(units_query), basket_engine)
        print(f"Toplam basket_product_units: {units_count.iloc[0]['total']}")
        
        # Units with model data
        model_units_query = """
        SELECT COUNT(*) as with_model 
        FROM basket_product_units 
        WHERE product_model IS NOT NULL
        """
        model_units_count = pd.read_sql(text(model_units_query), basket_engine)
        print(f"Model bilgisi olan units: {model_units_count.iloc[0]['with_model']}")
        
        # Basket status distribution
        status_query = """
        SELECT 
            bs.basket_status_name,
            COUNT(*) as count
        FROM baskets b
        LEFT JOIN basket_statuses bs ON b.basket_status_id = bs.basket_status_id
        GROUP BY bs.basket_status_name
        """
        status_stats = pd.read_sql(text(status_query), basket_engine)
        print(f"\nSepet durumu dağılımı:")
        for _, status in status_stats.iterrows():
            print(f"  {status['basket_status_name']}: {status['count']} sepet")
        
        # Product types in baskets
        print(f"\n📦 SEPETLERDEKİ ÜRÜN TÜRLERİ:")
        basket_products_query = """
        SELECT 
            p.product_name,
            p.product_model,
            p.product_model_year,
            sc.sub_category_name,
            COUNT(*) as basket_count
        FROM basket_product_units bpu
        LEFT JOIN products p ON bpu.product_id = p.product_id
        LEFT JOIN sub_categories sc ON p.product_sub_category_id = sc.sub_category_id
        GROUP BY p.product_id
        ORDER BY basket_count DESC
        LIMIT 10
        """
        basket_products = pd.read_sql(text(basket_products_query), basket_engine)
        print("En çok sepette bulunan ürünler:")
        for _, product in basket_products.iterrows():
            print(f"  {product['product_name']} ({product['product_model']}) - {product['basket_count']} sepet")
        
        # Gaming products in baskets
        gaming_basket_query = """
        SELECT 
            p.product_name,
            p.product_model,
            p.product_model_year,
            COUNT(*) as basket_count
        FROM basket_product_units bpu
        LEFT JOIN products p ON bpu.product_id = p.product_id
        WHERE p.product_sub_category_id IN (27, 28)
        GROUP BY p.product_id
        ORDER BY basket_count DESC
        LIMIT 5
        """
        gaming_basket = pd.read_sql(text(gaming_basket_query), basket_engine)
        print(f"\n🎮 Sepetlerdeki oyun ürünleri:")
        for _, product in gaming_basket.iterrows():
            print(f"  {product['product_name']} ({product['product_model']}) - {product['basket_count']} sepet")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    final_summary() 