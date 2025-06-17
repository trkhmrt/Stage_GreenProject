import pandas as pd
from sqlalchemy import text, create_engine

def check_current_data():
    """Check current data in both databases"""
    
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
        
        print("🔍 Güncel veri durumu kontrol ediliyor...")
        
        # Check products with model data
        print("\n📱 Products tablosu - Model bilgisi olan ürünler:")
        products_query = """
        SELECT product_id, product_name, product_model, product_model_year
        FROM products 
        WHERE product_model IS NOT NULL 
        ORDER BY product_id 
        LIMIT 10
        """
        products_df = pd.read_sql(text(products_query), product_engine)
        print(products_df)
        
        # Check baskets
        print(f"\n🛒 Baskets tablosu - Toplam sepet sayısı:")
        baskets_query = "SELECT COUNT(*) as total_baskets FROM baskets"
        baskets_count = pd.read_sql(text(baskets_query), basket_engine)
        print(f"Toplam sepet: {baskets_count.iloc[0]['total_baskets']}")
        
        # Check basket_product_units
        print(f"\n📦 Basket Product Units tablosu - Son eklenen kayıtlar:")
        units_query = """
        SELECT 
            bpu.basket_product_unit_id,
            bpu.product_id,
            bpu.product_name,
            bpu.product_model,
            bpu.product_model_year,
            bpu.basket_id,
            b.create_date
        FROM basket_product_units bpu
        LEFT JOIN baskets b ON bpu.basket_id = b.basket_id
        ORDER BY bpu.basket_product_unit_id DESC
        LIMIT 10
        """
        units_df = pd.read_sql(text(units_query), basket_engine)
        print(units_df)
        
        # Check total units count
        units_count_query = "SELECT COUNT(*) as total_units FROM basket_product_units"
        units_count = pd.read_sql(text(units_count_query), basket_engine)
        print(f"\nToplam basket_product_units: {units_count.iloc[0]['total_units']}")
        
        # Check if there are any units with model data
        model_units_query = """
        SELECT COUNT(*) as units_with_model 
        FROM basket_product_units 
        WHERE product_model IS NOT NULL
        """
        model_units_count = pd.read_sql(text(model_units_query), basket_engine)
        print(f"Model bilgisi olan units: {model_units_count.iloc[0]['units_with_model']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    check_current_data() 