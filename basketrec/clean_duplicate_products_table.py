import pandas as pd
from sqlalchemy import create_engine, text
from product_database_config import ProductDatabaseConfig

def clean_duplicate_products_table():
    print("🧹 products tablosunda tekrarlı ürünleri temizleme başlatılıyor...")
    db_config = ProductDatabaseConfig()
    engine = db_config.get_engine()
    try:
        with engine.connect() as conn:
            # Tüm ürünleri çek
            query = """
            SELECT product_id, product_name FROM products ORDER BY product_name, product_id
            """
            df = pd.read_sql(text(query), engine)
            print(f"📋 Toplam ürün: {len(df)}")
            print(f"📋 Benzersiz ürün adı: {df['product_name'].nunique()}")
            # Tekrarlı ürünleri bul
            duplicates = df[df.duplicated(subset=['product_name'], keep=False)]
            if len(duplicates) > 0:
                print(f"⚠️ Tekrarlı ürün sayısı: {len(duplicates)}")
                # Sadece ilkini bırak, diğerlerini sil
                to_keep = df.drop_duplicates(subset=['product_name'], keep='first')
                to_delete = df[~df.index.isin(to_keep.index)]
                print(f"🗑️ Silinecek ürün sayısı: {len(to_delete)}")
                for idx, row in to_delete.iterrows():
                    conn.execute(text(f"DELETE FROM products WHERE product_id = {row['product_id']}"))
                conn.commit()
                print("✅ Tekrarlı ürünler silindi!")
            else:
                print("✅ Tekrarlı ürün bulunamadı!")
    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    clean_duplicate_products_table() 