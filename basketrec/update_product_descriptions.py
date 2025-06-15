import pandas as pd
from sqlalchemy import text, create_engine

def update_product_descriptions():
    """Update product descriptions to make them unique"""
    
    # Products database configuration
    host = "localhost"
    port = 3301
    database = "productservicedb"
    username = "root"
    password = "root"
    
    try:
        # Connect to products database
        connection_string = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}"
        engine = create_engine(connection_string)
        
        # Get all products
        query = """
        SELECT 
            product_id,
            product_name,
            product_description,
            product_price,
            product_sub_category_id
        FROM products 
        ORDER BY product_id
        """
        
        df = pd.read_sql(text(query), engine)
        
        print(f"📊 Total products: {len(df)}")
        print(f"📊 Unique descriptions before: {df['product_description'].nunique()}")
        
        # Create unique descriptions for each product
        unique_descriptions = []
        
        for idx, row in df.iterrows():
            product_name = row['product_name']
            product_id = row['product_id']
            
            # Create unique description based on product name and ID
            if "Keyboard" in product_name:
                desc = f"Ergonomik tasarımı ile uzun süreli kullanım için ideal klavye. Model: {product_id}"
            elif "Koltuk" in product_name:
                desc = f"Konforlu ve dayanıklı koltuk takımı. Seri: {product_id}"
            elif "Telefon" in product_name:
                desc = f"Akıllı telefon teknolojisi. Versiyon: {product_id}"
            elif "Laptop" in product_name:
                desc = f"Yüksek performanslı laptop bilgisayar. Model: {product_id}"
            elif "Tablet" in product_name:
                desc = f"Ultra hafif tablet bilgisayar. Seri: {product_id}"
            elif "Kamera" in product_name:
                desc = f"Profesyonel fotoğraf makinesi. Model: {product_id}"
            elif "Aksiyon" in product_name:
                desc = f"Aksiyon kamerası - macera için tasarlandı. Seri: {product_id}"
            elif "Kulaklık" in product_name:
                desc = f"Noise cancelling kulaklık. Model: {product_id}"
            elif "Speaker" in product_name:
                desc = f"Waterproof bluetooth speaker. Versiyon: {product_id}"
            elif "Drone" in product_name:
                desc = f"4K kameralı drone. Model: {product_id}"
            elif "Robot" in product_name:
                desc = f"Robot vacuum cleaner. Seri: {product_id}"
            elif "Şarj" in product_name:
                desc = f"Solar şarj cihazı. Model: {product_id}"
            elif "Kamp" in product_name:
                desc = f"Kamp ekipmanı. Seri: {product_id}"
            elif "Elbise" in product_name:
                desc = f"Şık kadın elbisesi. Model: {product_id}"
            elif "Kot" in product_name:
                desc = f"Erkek kot pantolon. Seri: {product_id}"
            elif "Jeans" in product_name:
                desc = f"Slim fit jeans. Model: {product_id}"
            elif "Gömlek" in product_name:
                desc = f"Pamuklu gömlek. Seri: {product_id}"
            elif "T-Shirt" in product_name:
                desc = f"Organik pamuklu t-shirt. Model: {product_id}"
            elif "Ayakkabı" in product_name:
                desc = f"Spor ayakkabı. Seri: {product_id}"
            elif "Cüzdan" in product_name:
                desc = f"Deri cüzdan. Model: {product_id}"
            elif "Masa" in product_name:
                desc = f"Ahşap yemek masası. Seri: {product_id}"
            elif "Kitaplık" in product_name:
                desc = f"Modern kitaplık. Model: {product_id}"
            elif "Lamba" in product_name:
                desc = f"Yatak odası lambası. Seri: {product_id}"
            elif "Kitap" in product_name:
                desc = f"Klasik roman kitabı. Model: {product_id}"
            elif "Roman" in product_name:
                desc = f"Klasik roman. Seri: {product_id}"
            elif "Hikaye" in product_name:
                desc = f"Çocuk hikaye kitabı. Model: {product_id}"
            elif "Gelişim" in product_name:
                desc = f"Kişisel gelişim kitabı. Seri: {product_id}"
            elif "Bilim" in product_name:
                desc = f"Bilim kurgu kitabı. Model: {product_id}"
            elif "Yapay" in product_name:
                desc = f"Yapay zeka kitabı. Seri: {product_id}"
            elif "Suç" in product_name:
                desc = f"Suç ve ceza kitabı. Model: {product_id}"
            elif "Krem" in product_name:
                desc = f"Anti-aging krem. Seri: {product_id}"
            elif "Serum" in product_name:
                desc = f"Nemlendirici serum. Model: {product_id}"
            elif "Şampuan" in product_name:
                desc = f"Bitkisel şampuan. Seri: {product_id}"
            elif "Sabun" in product_name:
                desc = f"Doğal sabun. Model: {product_id}"
            elif "Temizleyici" in product_name:
                desc = f"Cilt temizleyici. Seri: {product_id}"
            elif "Vitamin" in product_name:
                desc = f"Multi-vitamin takviyesi. Model: {product_id}"
            elif "C Vitamini" in product_name:
                desc = f"C vitamini takviyesi. Seri: {product_id}"
            elif "Omega" in product_name:
                desc = f"Omega-3 kapsül. Model: {product_id}"
            elif "Probiyotik" in product_name:
                desc = f"Probiyotik takviye. Seri: {product_id}"
            elif "Bağışıklık" in product_name:
                desc = f"Bağışıklık güçlendirici. Model: {product_id}"
            elif "Bal" in product_name:
                desc = f"Organik bal. Seri: {product_id}"
            elif "Makası" in product_name:
                desc = f"Bahçe makası. Model: {product_id}"
            elif "Çadır" in product_name:
                desc = f"Kamp çadırı. Seri: {product_id}"
            elif "Sandalye" in product_name:
                desc = f"Kamp sandalyesi. Model: {product_id}"
            elif "Lamba" in product_name:
                desc = f"Kamp lambası. Seri: {product_id}"
            elif "Çanta" in product_name:
                desc = f"Doğa yürüyüşü sırt çantası. Model: {product_id}"
            elif "Matara" in product_name:
                desc = f"Su matarası. Seri: {product_id}"
            elif "Mouse" in product_name:
                desc = f"Wireless gaming mouse. Model: {product_id}"
            elif "SSD" in product_name:
                desc = f"Portable SSD 1TB. Seri: {product_id}"
            elif "Tracker" in product_name:
                desc = f"Smart fitness tracker. Model: {product_id}"
            elif "Saat" in product_name:
                desc = f"Akıllı saat. Seri: {product_id}"
            elif "Projektör" in product_name:
                desc = f"Taşınabilir projektör. Model: {product_id}"
            elif "Top" in product_name:
                desc = f"Yoga topu. Seri: {product_id}"
            else:
                desc = f"Kaliteli ürün. Model: {product_id}"
            
            unique_descriptions.append(desc)
        
        # Update the dataframe
        df['new_description'] = unique_descriptions
        
        print(f"📊 Unique descriptions after: {len(set(unique_descriptions))}")
        
        # Update database
        with engine.connect() as conn:
            for idx, row in df.iterrows():
                update_query = text("""
                    UPDATE products 
                    SET product_description = :description 
                    WHERE product_id = :product_id
                """)
                conn.execute(update_query, {
                    'description': row['new_description'],
                    'product_id': row['product_id']
                })
            
            conn.commit()
        
        print("✅ All product descriptions updated successfully!")
        
        # Verify the update
        verify_query = """
        SELECT 
            product_id,
            product_name,
            product_description
        FROM products 
        ORDER BY product_id
        LIMIT 10
        """
        
        verify_df = pd.read_sql(text(verify_query), engine)
        print(f"\n📋 Sample updated products:")
        print(verify_df.to_string(index=False))
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    update_product_descriptions() 