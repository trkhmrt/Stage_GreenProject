import os
from sqlalchemy import create_engine, text
import pandas as pd

class ProductDatabaseConfig:
    def __init__(self):
        self.host = "localhost"
        self.port = 3301  # Product database port
        self.database = "productservicedb"
        self.username = "root"
        self.password = "root"
        self.driver = "com.mysql.cj.jdbc.Driver"
        
    def get_connection_string(self):
        """Get SQLAlchemy connection string"""
        return f"mysql+mysqlconnector://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
    
    def get_engine(self):
        """Get SQLAlchemy engine"""
        return create_engine(self.get_connection_string())
    
    def test_connection(self):
        """Test database connection"""
        try:
            engine = self.get_engine()
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                print("Product database connection successful!")
                return True
        except Exception as e:
            print(f"Product database connection failed: {e}")
            return False
    
    def get_products(self):
        """Fetch all products with category and subcategory information"""
        try:
            engine = self.get_engine()
            query = """
            SELECT 
                p.product_id,
                p.product_name,
                p.product_description,
                p.product_price,
                p.product_quantity,
                p.product_sub_category_id,
                sc.sub_category_id,
                sc.sub_category_name,
                c.category_id,
                c.category_name
            FROM products p
            LEFT JOIN sub_categories sc ON p.product_sub_category_id = sc.sub_category_id
            LEFT JOIN categories c ON sc.category_id = c.category_id
            ORDER BY p.product_id
            """
            df = pd.read_sql(text(query), engine)
            return df
        except Exception as e:
            print(f"Error fetching products: {e}")
            return None
    
    def get_categories(self):
        """Fetch all categories"""
        try:
            engine = self.get_engine()
            query = "SELECT category_id, category_name FROM categories ORDER BY category_id"
            df = pd.read_sql(text(query), engine)
            return df
        except Exception as e:
            print(f"Error fetching categories: {e}")
            return None
    
    def get_subcategories(self):
        """Fetch all subcategories with category information"""
        try:
            engine = self.get_engine()
            query = """
            SELECT 
                sc.sub_category_id,
                sc.sub_category_name,
                sc.category_id,
                c.category_name
            FROM sub_categories sc
            LEFT JOIN categories c ON sc.category_id = c.category_id
            ORDER BY sc.sub_category_id
            """
            df = pd.read_sql(text(query), engine)
            return df
        except Exception as e:
            print(f"Error fetching subcategories: {e}")
            return None 