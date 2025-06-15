import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from product_database_config import ProductDatabaseConfig
from realistic_basket_generator import RealisticBasketGenerator
from sqlalchemy.types import Integer, String, Float, DateTime, DECIMAL

class DatabaseWriter:
    def __init__(self):
        # Basket veritabanı konfigürasyonu (basketservicedb)
        self.basket_host = "localhost"
        self.basket_port = 3309  # Basket database port
        self.basket_database = "basketservicedb"
        self.basket_username = "root"
        self.basket_password = "root"
        
        # Ürün veritabanı konfigürasyonu (productservicedb)
        self.product_config = ProductDatabaseConfig()
        
    def get_basket_connection_string(self):
        """Basket veritabanı için connection string"""
        return f"mysql+mysqlconnector://{self.basket_username}:{self.basket_password}@{self.basket_host}:{self.basket_port}/{self.basket_database}"
    
    def get_basket_engine(self):
        """Basket veritabanı için engine"""
        return create_engine(self.get_basket_connection_string())
    
    def test_basket_connection(self):
        """Basket veritabanı bağlantısını test et"""
        try:
            engine = self.get_basket_engine()
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                print("✅ Basket database connection successful!")
                return True
        except Exception as e:
            print(f"❌ Basket database connection failed: {e}")
            return False
    
    def create_basket_tables(self):
        """Baskets ve basket_product_units tablolarını oluştur"""
        try:
            engine = self.get_basket_engine()
            # Baskets tablosu (created_date eklendi)
            create_baskets_table = """
            CREATE TABLE IF NOT EXISTS baskets (
                basket_id INT PRIMARY KEY,
                customer_id INT NOT NULL,
                basket_status_id INT NOT NULL,
                created_date DATETIME NOT NULL,
                INDEX idx_customer_id (customer_id),
                INDEX idx_basket_status_id (basket_status_id),
                INDEX idx_created_date (created_date)
            )
            """
            # Basket product units tablosu
            create_basket_product_units_table = """
            CREATE TABLE IF NOT EXISTS basket_product_units (
                basket_product_unit_id INT AUTO_INCREMENT PRIMARY KEY,
                basket_id INT NOT NULL,
                product_id INT NOT NULL,
                product_name VARCHAR(255) NOT NULL,
                product_quantity INT NOT NULL,
                product_unit_price DECIMAL(10,2) NOT NULL,
                product_total_price DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (basket_id) REFERENCES baskets(basket_id)
            )
            """
            with engine.connect() as conn:
                conn.execute(text(create_baskets_table))
                conn.execute(text(create_basket_product_units_table))
            print("✅ Baskets tables created successfully!")
            return True
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            return False
    
    def clear_existing_data(self):
        """Mevcut verileri temizle"""
        try:
            engine = self.get_basket_engine()
            with engine.connect() as conn:
                conn.execute(text("DELETE FROM basket_product_units"))
                conn.execute(text("DELETE FROM baskets"))
                conn.commit()
                print("✅ Existing data cleared!")
                return True
        except Exception as e:
            print(f"❌ Error clearing data: {e}")
            return False
    
    def insert_baskets(self, baskets_df):
        """Baskets verilerini veritabanına ekle"""
        try:
            engine = self.get_basket_engine()
            baskets_df['basket_id'] = baskets_df['basket_id'].astype(int)
            baskets_df['customer_id'] = baskets_df['customer_id'].astype(int)
            baskets_df['basket_status_id'] = baskets_df['basket_status_id'].astype(int)
            baskets_df['create_date'] = pd.to_datetime(baskets_df['create_date'])
            dtype = {
                'basket_id': Integer(),
                'customer_id': Integer(),
                'basket_status_id': Integer(),
                'create_date': DateTime()
            }
            # Sütun adını veritabanı ile uyumlu hale getir
            if 'created_date' in baskets_df.columns:
                baskets_df = baskets_df.rename(columns={"created_date": "create_date"})
            baskets_df.to_sql('baskets', engine, if_exists='append', index=False, method='multi', dtype=dtype, chunksize=100)
            print(f"✅ {len(baskets_df)} baskets records inserted!")
            return True
        except Exception as e:
            print(f"❌ Error inserting baskets: {e}")
            return False
    
    def insert_basket_product_units(self, units_df):
        """Basket product units verilerini veritabanına ekle"""
        try:
            engine = self.get_basket_engine()
            if 'basket_product_unit_id' in units_df.columns:
                units_df_clean = units_df.drop('basket_product_unit_id', axis=1)
            else:
                units_df_clean = units_df.copy()
            units_df_clean['basket_id'] = units_df_clean['basket_id'].astype(int)
            units_df_clean['product_id'] = units_df_clean['product_id'].astype(int)
            units_df_clean['product_name'] = units_df_clean['product_name'].astype(str)
            units_df_clean['product_quantity'] = units_df_clean['product_quantity'].astype(int)
            units_df_clean['product_unit_price'] = units_df_clean['product_unit_price'].astype(float)
            units_df_clean['product_total_price'] = units_df_clean['product_total_price'].astype(float)
            dtype = {
                'basket_id': Integer(),
                'product_id': Integer(),
                'product_name': String(255),
                'product_quantity': Integer(),
                'product_unit_price': DECIMAL(10,2),
                'product_total_price': DECIMAL(10,2)
            }
            units_df_clean.to_sql('basket_product_units', engine, if_exists='append', index=False, method='multi', dtype=dtype, chunksize=100)
            print(f"✅ {len(units_df_clean)} basket product units records inserted!")
            return True
        except Exception as e:
            print(f"❌ Error inserting basket product units: {e}")
            return False
    
    def verify_data(self):
        """Veritabanındaki verileri doğrula"""
        try:
            engine = self.get_basket_engine()
            
            with engine.connect() as conn:
                # Baskets sayısı
                basket_count = conn.execute(text("SELECT COUNT(*) FROM baskets")).fetchone()[0]
                print(f"📊 Baskets count: {basket_count}")
                
                # Basket product units sayısı
                unit_count = conn.execute(text("SELECT COUNT(*) FROM basket_product_units")).fetchone()[0]
                print(f"📊 Basket product units count: {unit_count}")
                
                # Ortalama sepet boyutu
                avg_basket_size = conn.execute(text("""
                    SELECT AVG(basket_size) FROM (
                        SELECT basket_id, COUNT(*) as basket_size 
                        FROM basket_product_units 
                        GROUP BY basket_id
                    ) as basket_sizes
                """)).fetchone()[0]
                print(f"📊 Average basket size: {avg_basket_size:.2f}")
                
                # Toplam gelir
                total_revenue = conn.execute(text("SELECT SUM(product_total_price) FROM basket_product_units")).fetchone()[0]
                print(f"📊 Total revenue: ${total_revenue:,.2f}")
                
                # Benzersiz müşteri sayısı
                unique_customers = conn.execute(text("SELECT COUNT(DISTINCT customer_id) FROM baskets")).fetchone()[0]
                print(f"📊 Unique customers: {unique_customers}")
                
                # Benzersiz ürün sayısı
                unique_products = conn.execute(text("SELECT COUNT(DISTINCT product_id) FROM basket_product_units")).fetchone()[0]
                print(f"📊 Unique products: {unique_products}")
                
                return True
                
        except Exception as e:
            print(f"❌ Error verifying data: {e}")
            return False
    
    def insert_realistic_baskets(self, num_baskets=3000, days_back=90):
        """Gerçekçi ve öneri algoritmasına uygun sepet verisi üret ve ekle"""
        generator = RealisticBasketGenerator()
        if generator.products_df is None:
            print("❌ Ürün veritabanı bağlantısı başarısız!")
            return
        # Her sepette 2-8 ürün olacak şekilde sepetler oluştur
        baskets = []
        units = []
        end_date = pd.Timestamp.now()
        start_date = end_date - pd.Timedelta(days=days_back)
        customer_ids = list(range(1, 1001))
        basket_id = 1
        unit_id = 1
        for _ in range(num_baskets):
            basket_size = np.random.randint(2, 9)
            basket_products = generator.products_df.sample(basket_size, replace=False)
            customer_id = np.random.choice(customer_ids)
            basket_status_id = np.random.choice([1, 4], p=[0.4, 0.6])
            create_date = start_date + pd.Timedelta(days=np.random.randint(0, days_back))
            baskets.append({
                'basket_id': basket_id,
                'customer_id': customer_id,
                'basket_status_id': basket_status_id,
                'create_date': create_date
            })
            for _, prod in basket_products.iterrows():
                quantity = np.random.randint(1, 4)
                unit_price = float(prod['product_price'])
                total_price = unit_price * quantity
                units.append({
                    'basket_product_unit_id': unit_id,
                    'basket_id': basket_id,
                    'product_id': prod['product_id'],
                    'product_name': prod['product_name'],
                    'product_quantity': quantity,
                    'product_unit_price': unit_price,
                    'product_total_price': total_price
                })
                unit_id += 1
            basket_id += 1
        baskets_df = pd.DataFrame(baskets)
        units_df = pd.DataFrame(units)
        # Temizle ve ekle
        self.clear_existing_data()
        self.insert_baskets(baskets_df)
        self.insert_basket_product_units(units_df)
        self.verify_data()

if __name__ == "__main__":
    writer = DatabaseWriter()
    writer.insert_realistic_baskets(num_baskets=3000, days_back=90) 