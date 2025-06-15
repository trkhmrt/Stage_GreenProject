import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import json
from product_database_config import ProductDatabaseConfig

class RealisticBasketGenerator:
    def __init__(self):
        self.db_config = ProductDatabaseConfig()
        self.products_df = None
        self.categories_df = None
        self.subcategories_df = None
        
        # Veritabanından verileri çek
        self.load_database_data()
        
        # Ürün ilişkileri (kategori bazlı)
        self.category_relationships = {
            'Süt Ürünleri': ['Ekmek & Fırın', 'Kahvaltılık', 'İçecekler'],
            'Meyve & Sebze': ['Süt Ürünleri', 'Ekmek & Fırın', 'İçecekler'],
            'Et & Balık': ['Meyve & Sebze', 'Ekmek & Fırın', 'İçecekler'],
            'Ekmek & Fırın': ['Süt Ürünleri', 'Kahvaltılık', 'İçecekler'],
            'İçecekler': ['Atıştırmalık', 'Ekmek & Fırın'],
            'Temizlik': ['Kişisel Bakım'],
            'Kişisel Bakım': ['Temizlik'],
            'Atıştırmalık': ['İçecekler', 'Süt Ürünleri'],
            'Kahvaltılık': ['Süt Ürünleri', 'Ekmek & Fırın'],
            'Dondurulmuş': ['İçecekler', 'Atıştırmalık']
        }
        
        # Müşteri tipleri ve sepet davranışları
        self.customer_types = {
            'small': {'basket_size': (1, 3), 'frequency': 0.2},
            'regular': {'basket_size': (3, 8), 'frequency': 0.6},
            'large': {'basket_size': (8, 15), 'frequency': 0.2}
        }
    
    def load_database_data(self):
        """Veritabanından ürün, kategori ve alt kategori verilerini çek"""
        print("📊 Veritabanından veriler çekiliyor...")
        
        # Ürünleri çek
        self.products_df = self.db_config.get_products()
        if self.products_df is not None:
            print(f"✅ {len(self.products_df)} ürün çekildi")
        else:
            print("❌ Ürün verileri çekilemedi!")
            return
        
        # Kategorileri çek
        self.categories_df = self.db_config.get_categories()
        if self.categories_df is not None:
            print(f"✅ {len(self.categories_df)} kategori çekildi")
        
        # Alt kategorileri çek
        self.subcategories_df = self.db_config.get_subcategories()
        if self.subcategories_df is not None:
            print(f"✅ {len(self.subcategories_df)} alt kategori çekildi")
        
        # Ürün fiyatlarını kontrol et ve düzelt
        self.products_df['product_price'] = self.products_df['product_price'].fillna(10.0)
        self.products_df['product_price'] = self.products_df['product_price'].apply(lambda x: max(1.0, float(x)))
    
    def get_products_by_category(self, category_name):
        """Belirli bir kategorideki ürünleri döndür"""
        if self.products_df is None:
            return []
        
        category_products = self.products_df[
            self.products_df['category_name'] == category_name
        ]
        return category_products.to_dict('records')
    
    def get_related_products(self, product_record, relationship_strength=0.7):
        """Bir ürünle ilişkili diğer ürünleri döndür"""
        related_products = []
        
        if self.products_df is None:
            return related_products
        
        category_name = product_record.get('category_name', '')
        
        # Aynı kategorideki diğer ürünler
        same_category = self.products_df[
            (self.products_df['category_name'] == category_name) & 
            (self.products_df['product_id'] != product_record['product_id'])
        ]
        related_products.extend(same_category.to_dict('records'))
        
        # İlişkili kategorilerdeki ürünler
        if category_name in self.category_relationships:
            related_categories = self.category_relationships[category_name]
            for related_category in related_categories:
                category_products = self.get_products_by_category(related_category)
                related_products.extend(category_products)
        
        # İlişki gücüne göre filtrele
        if random.random() < relationship_strength and related_products:
            return random.sample(related_products, min(len(related_products), 5))
        else:
            return []
    
    def generate_basket(self, basket_id, customer_id, date, customer_type='regular'):
        """Tek bir sepet oluştur"""
        basket_items = []
        
        # Sepet boyutunu belirle
        min_size, max_size = self.customer_types[customer_type]['basket_size']
        basket_size = random.randint(min_size, max_size)
        
        if self.products_df is None or len(self.products_df) == 0:
            return []
        
        # İlk ürünü rastgele seç
        first_product = self.products_df.sample(1).iloc[0].to_dict()
        basket_items.append(first_product)
        
        # Diğer ürünleri ekle
        for _ in range(basket_size - 1):
            if basket_items and random.random() < 0.6:  # %60 ihtimalle ilişkili ürün
                # Mevcut ürünlerden birini seç ve ilişkili ürünlerini al
                base_product = random.choice(basket_items)
                related_products = self.get_related_products(base_product)
                
                if related_products:
                    new_product = random.choice(related_products)
                    # Aynı ürünü tekrar ekleme
                    if not any(item['product_id'] == new_product['product_id'] for item in basket_items):
                        basket_items.append(new_product)
                        continue
            
            # İlişkili ürün bulunamazsa rastgele ürün ekle
            available_products = self.products_df[
                ~self.products_df['product_id'].isin([item['product_id'] for item in basket_items])
            ]
            
            if len(available_products) > 0:
                new_product = available_products.sample(1).iloc[0].to_dict()
                basket_items.append(new_product)
        
        # Sepet öğelerini DataFrame formatına çevir
        basket_data = []
        for product in basket_items:
            unit_price = float(product['product_price'])
            quantity = random.randint(1, 3)  # 1-3 adet
            total_price = unit_price * quantity
            
            basket_data.append({
                'basket_product_unit_id': None,  # Auto increment
                'basket_id': basket_id,
                'product_id': product['product_id'],
                'product_name': product['product_name'],
                'product_quantity': quantity,
                'product_unit_price': unit_price,
                'product_total_price': total_price
            })
        
        return basket_data
    
    def generate_baskets(self, num_baskets=1000, days_back=30):
        """Basket tablosu için veri oluştur"""
        baskets = []
        
        # Tarih aralığı
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        # Müşteri ID'leri (1-1000 arası)
        customer_ids = list(range(1, 1001))
        
        for basket_id in range(1, num_baskets + 1):
            # Rastgele tarih
            random_days = random.randint(0, days_back)
            created_date = start_date + timedelta(days=random_days)
            
            # Müşteri tipi seç
            customer_type = np.random.choice(
                list(self.customer_types.keys()), 
                p=[self.customer_types[ct]['frequency'] for ct in self.customer_types.keys()]
            )
            
            # Rastgele müşteri ID
            customer_id = random.choice(customer_ids)
            
            # Basket durumu (1: Aktif, 4: Paid)
            basket_status_id = random.choices([1, 4], weights=[0.4, 0.6])[0]
            
            baskets.append({
                'basket_id': basket_id,
                'customer_id': customer_id,
                'basket_status_id': basket_status_id,
                'create_date': created_date.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return pd.DataFrame(baskets)
    
    def generate_basket_product_units(self, baskets_df):
        """Basket_product_unit tablosu için veri oluştur"""
        all_units = []
        unit_id = 1
        
        for _, basket in baskets_df.iterrows():
            basket_id = basket['basket_id']
            customer_id = basket['customer_id']
            create_date = datetime.strptime(basket['create_date'], '%Y-%m-%d %H:%M:%S')
            
            # Müşteri tipini belirle (customer_id'ye göre)
            customer_type = 'regular'
            if customer_id % 5 == 0:
                customer_type = 'small'
            elif customer_id % 3 == 0:
                customer_type = 'large'
            
            # Sepet öğelerini oluştur
            basket_items = self.generate_basket(basket_id, customer_id, create_date, customer_type)
            
            for item in basket_items:
                item['basket_product_unit_id'] = unit_id
                all_units.append(item)
                unit_id += 1
        
        return pd.DataFrame(all_units)
    
    def save_to_csv(self, baskets_df, units_df):
        """Verileri CSV dosyalarına kaydet"""
        # Basket verilerini kaydet
        baskets_df.to_csv('baskets.csv', index=False)
        print(f"✅ {len(baskets_df)} basket kaydı 'baskets.csv' dosyasına kaydedildi")
        
        # Basket product unit verilerini kaydet
        units_df.to_csv('basket_product_units.csv', index=False)
        print(f"✅ {len(units_df)} basket product unit kaydı 'basket_product_units.csv' dosyasına kaydedildi")
        
        # İstatistikler
        print(f"\n📊 Veri Seti İstatistikleri:")
        print(f"- Toplam sepet sayısı: {len(baskets_df)}")
        print(f"- Toplam ürün birimi: {len(units_df)}")
        print(f"- Ortalama sepet boyutu: {len(units_df) / len(baskets_df):.2f}")
        print(f"- Toplam gelir: ${units_df['product_total_price'].sum():,.2f}")
        print(f"- Benzersiz müşteri sayısı: {baskets_df['customer_id'].nunique()}")
        print(f"- Benzersiz ürün sayısı: {units_df['product_id'].nunique()}")
        
        # Kategori bazlı analiz
        if self.products_df is not None:
            category_stats = units_df.merge(
                self.products_df[['product_id', 'category_name']], 
                on='product_id', 
                how='left'
            ).groupby('category_name').agg({
                'product_total_price': 'sum',
                'product_quantity': 'sum'
            }).sort_values('product_total_price', ascending=False)
            
            print(f"\n🏆 Kategori Bazlı Satış:")
            for category, stats in category_stats.head(5).iterrows():
                print(f"  - {category}: ${stats['product_total_price']:,.2f} ({stats['product_quantity']} adet)")
    
    def create_sample_baskets(self, num_samples=5):
        """Örnek sepetler oluştur ve göster"""
        print("🛒 Örnek Sepetler:")
        print("=" * 60)
        
        for i in range(num_samples):
            basket_id = i + 1
            customer_id = random.randint(1, 100)
            date = datetime.now()
            
            basket_items = self.generate_basket(basket_id, customer_id, date)
            
            if basket_items:
                print(f"\n📦 Sepet {basket_id} (Müşteri {customer_id}):")
                total = 0
                for item in basket_items:
                    print(f"  - {item['product_name']}: {item['product_quantity']} adet x ${item['product_unit_price']:.2f} = ${item['product_total_price']:.2f}")
                    total += item['product_total_price']
                print(f"  💰 Toplam: ${total:.2f}")
                print("-" * 50)

def main():
    """Ana fonksiyon"""
    print("🛒 Gerçekçi Basket Veri Seti Oluşturucu")
    print("=" * 60)
    
    generator = RealisticBasketGenerator()
    
    if generator.products_df is None:
        print("❌ Veritabanı bağlantısı başarısız! Lütfen veritabanı ayarlarını kontrol edin.")
        return
    
    # Örnek sepetler göster
    generator.create_sample_baskets(5)
    
    print("\n" + "=" * 60)
    print("📊 Veri seti oluşturuluyor...")
    
    # Basket verilerini oluştur
    baskets_df = generator.generate_baskets(num_baskets=2000, days_back=60)
    
    # Basket product unit verilerini oluştur
    units_df = generator.generate_basket_product_units(baskets_df)
    
    # CSV dosyalarına kaydet
    generator.save_to_csv(baskets_df, units_df)
    
    print("\n✅ Veri seti başarıyla oluşturuldu!")
    print("📁 Oluşturulan dosyalar:")
    print("  - baskets.csv (sepet verileri)")
    print("  - basket_product_units.csv (sepet ürün birimleri)")
    
    return baskets_df, units_df

if __name__ == "__main__":
    baskets_df, units_df = main() 