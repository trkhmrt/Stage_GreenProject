import pandas as pd
from sqlalchemy import create_engine, text
from database_config import DatabaseConfig

def clean_duplicate_products():
    """Veritabanından tekrarlı ürünleri temizle"""
    print("🧹 Tekrarlı ürünleri temizleme işlemi başlatılıyor...")
    
    # Veritabanı bağlantısı
    db_config = DatabaseConfig()
    engine = db_config.get_engine()
    
    try:
        with engine.connect() as conn:
            # Önce tekrarlı ürünleri kontrol et
            print("📊 Tekrarlı ürünler kontrol ediliyor...")
            
            # Tüm ürünleri çek
            query = """
            SELECT 
                basket_product_unit_id,
                basket_id,
                product_id,
                product_name,
                product_quantity,
                product_unit_price,
                product_total_price
            FROM basket_product_units
            ORDER BY product_name, basket_product_unit_id
            """
            
            df = pd.read_sql(text(query), engine)
            
            print(f"📋 Toplam kayıt sayısı: {len(df)}")
            print(f"📋 Benzersiz ürün sayısı: {df['product_name'].nunique()}")
            
            # Tekrarlı ürünleri bul
            duplicate_products = df[df.duplicated(subset=['product_name'], keep=False)]
            
            if len(duplicate_products) > 0:
                print(f"⚠️ Tekrarlı ürün sayısı: {len(duplicate_products)}")
                
                # Her ürün için sadece ilk kaydı tut
                df_clean = df.drop_duplicates(subset=['product_name'], keep='first')
                
                print(f"✅ Temizlenmiş kayıt sayısı: {len(df_clean)}")
                print(f"🗑️ Silinecek kayıt sayısı: {len(df) - len(df_clean)}")
                
                # Mevcut tabloyu temizle
                conn.execute(text("DELETE FROM basket_product_units"))
                conn.commit()
                print("🗑️ Mevcut veriler silindi")
                
                # Temizlenmiş verileri ekle
                df_clean.to_sql('basket_product_units', engine, if_exists='append', index=False, method='multi', chunksize=100)
                print("✅ Temizlenmiş veriler eklendi")
                
                # Sepet ID'lerini yeniden düzenle
                print("🔄 Sepet ID'leri yeniden düzenleniyor...")
                
                # Benzersiz sepet ID'lerini al
                unique_baskets = df_clean['basket_id'].unique()
                
                # Yeni sepet ID'leri oluştur
                basket_mapping = {old_id: new_id for new_id, old_id in enumerate(unique_baskets, 1)}
                
                # Sepet ID'lerini güncelle
                for old_id, new_id in basket_mapping.items():
                    conn.execute(text(f"UPDATE basket_product_units SET basket_id = {new_id} WHERE basket_id = {old_id}"))
                
                conn.commit()
                print("✅ Sepet ID'leri güncellendi")
                
                # Baskets tablosunu da güncelle
                print("🔄 Baskets tablosu güncelleniyor...")
                
                # Foreign key kısıtlamalarını geçici olarak kaldır
                conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
                conn.execute(text("DELETE FROM baskets"))
                conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
                conn.commit()
                
                # Yeni basket kayıtları oluştur
                for new_basket_id in range(1, len(unique_baskets) + 1):
                    conn.execute(text(f"""
                    INSERT INTO baskets (basket_id, customer_id, basket_status_id, create_date)
                    VALUES ({new_basket_id}, {new_basket_id % 1000 + 1}, {1 if new_basket_id % 2 == 0 else 4}, NOW())
                    """))
                
                conn.commit()
                print("✅ Baskets tablosu güncellendi")
                
                # Son durumu kontrol et
                final_check = pd.read_sql(text("SELECT COUNT(*) as count FROM basket_product_units"), engine)
                print(f"📊 Son durum - Toplam kayıt: {final_check['count'].iloc[0]}")
                
                # Benzersiz ürün sayısını kontrol et
                unique_check = pd.read_sql(text("SELECT COUNT(DISTINCT product_name) as unique_count FROM basket_product_units"), engine)
                print(f"📊 Benzersiz ürün sayısı: {unique_check['unique_count'].iloc[0]}")
                
            else:
                print("✅ Tekrarlı ürün bulunamadı!")
                
    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    clean_duplicate_products() 