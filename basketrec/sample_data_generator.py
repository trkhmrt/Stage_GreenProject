#!/usr/bin/env python3
"""
Sample data generator for testing the basket recommendation system
"""

import pandas as pd
import numpy as np
import random
from sqlalchemy import create_engine, text
import warnings
warnings.filterwarnings('ignore')
from datetime import datetime, timedelta
import json

class ShoppingDataGenerator:
    def __init__(self):
        # Gerçekçi ürün kategorileri ve ürünler
        self.product_categories = {
            'Süt Ürünleri': [
                'Süt', 'Yoğurt', 'Peynir', 'Tereyağı', 'Krema', 'Ayran', 'Kefir'
            ],
            'Meyve & Sebze': [
                'Elma', 'Muz', 'Portakal', 'Domates', 'Salatalık', 'Patates', 'Soğan',
                'Havuç', 'Brokoli', 'Ispanak', 'Çilek', 'Üzüm', 'Kivi', 'Avokado'
            ],
            'Et & Balık': [
                'Tavuk Göğsü', 'Dana Eti', 'Kuzu Eti', 'Balık', 'Sucuk', 'Pastırma',
                'Salam', 'Jambon', 'Tavuk Kanadı', 'Kıyma'
            ],
            'Ekmek & Fırın': [
                'Ekmek', 'Börek', 'Poğaça', 'Simit', 'Kurabiye', 'Pasta', 'Kek'
            ],
            'İçecekler': [
                'Su', 'Kola', 'Meyve Suyu', 'Çay', 'Kahve', 'Soda', 'Limonata',
                'Ice Tea', 'Enerji İçeceği', 'Süt'
            ],
            'Temizlik': [
                'Deterjan', 'Şampuan', 'Sabun', 'Diş Macunu', 'Tuvalet Kağıdı',
                'Kağıt Havlu', 'Temizlik Bezi', 'Çamaşır Suyu'
            ],
            'Kişisel Bakım': [
                'Deodorant', 'Parfüm', 'Makyaj Malzemesi', 'Tıraş Bıçağı',
                'Saç Kremi', 'Nemlendirici', 'Güneş Kremi'
            ],
            'Atıştırmalık': [
                'Cips', 'Çikolata', 'Bisküvi', 'Kuruyemiş', 'Şeker', 'Sakız',
                'Dondurma', 'Gofret', 'Kraker'
            ],
            'Kahvaltılık': [
                'Reçel', 'Bal', 'Zeytin', 'Yumurta', 'Kahvaltılık Gevrek',
                'Fındık Ezmesi', 'Çikolata Ezmesi'
            ],
            'Dondurulmuş': [
                'Dondurulmuş Pizza', 'Dondurulmuş Sebze', 'Dondurulmuş Et',
                'Dondurma', 'Dondurulmuş Patates'
            ]
        }
        
        # Ürün fiyatları (gerçekçi fiyat aralıkları)
        self.price_ranges = {
            'Süt Ürünleri': (5, 50),
            'Meyve & Sebze': (3, 80),
            'Et & Balık': (20, 200),
            'Ekmek & Fırın': (2, 30),
            'İçecekler': (1, 25),
            'Temizlik': (5, 100),
            'Kişisel Bakım': (10, 150),
            'Atıştırmalık': (2, 40),
            'Kahvaltılık': (8, 60),
            'Dondurulmuş': (15, 80)
        }
        
        # Ürünler arası ilişkiler (birlikte alınma olasılığı yüksek olan ürünler)
        self.product_relationships = {
            'Ekmek': ['Peynir', 'Tereyağı', 'Süt', 'Reçel', 'Bal'],
            'Süt': ['Ekmek', 'Kahvaltılık Gevrek', 'Çikolata', 'Kahve'],
            'Kahve': ['Süt', 'Şeker', 'Bisküvi', 'Çikolata'],
            'Çay': ['Şeker', 'Bisküvi'],
            'Tavuk Göğsü': ['Patates', 'Soğan', 'Havuç'],
            'Dana Eti': ['Patates', 'Soğan', 'Havuç', 'Ekmek'],
            'Balık': ['Patates', 'Soğan'],
            'Domates': ['Salatalık', 'Soğan', 'Peynir', 'Ekmek'],
            'Salatalık': ['Domates', 'Yoğurt', 'Peynir'],
            'Patates': ['Soğan', 'Havuç', 'Tavuk Göğsü', 'Dana Eti', 'Balık'],
            'Soğan': ['Patates', 'Havuç', 'Domates', 'Tavuk Göğsü', 'Dana Eti'],
            'Havuç': ['Patates', 'Soğan', 'Tavuk Göğsü', 'Dana Eti'],
            'Elma': ['Muz', 'Portakal', 'Çikolata'],
            'Muz': ['Elma', 'Portakal', 'Süt'],
            'Portakal': ['Elma', 'Muz', 'Meyve Suyu'],
            'Çikolata': ['Süt', 'Bisküvi', 'Elma'],
            'Bisküvi': ['Çay', 'Kahve', 'Süt', 'Çikolata'],
            'Cips': ['Kola', 'Çikolata'],
            'Kola': ['Cips'],
            'Su': ['Herhangi bir ürün'],  # Su her şeyle birlikte alınabilir
            'Deterjan': ['Çamaşır Suyu'],
            'Şampuan': ['Saç Kremi', 'Nemlendirici'],
            'Diş Macunu': ['Sabun'],
            'Tuvalet Kağıdı': ['Kağıt Havlu', 'Temizlik Bezi'],
            'Kağıt Havlu': ['Tuvalet Kağıdı', 'Temizlik Bezi'],
            'Reçel': ['Ekmek', 'Peynir', 'Tereyağı'],
            'Bal': ['Ekmek', 'Peynir', 'Süt'],
            'Zeytin': ['Peynir', 'Ekmek'],
            'Yumurta': ['Ekmek', 'Peynir', 'Süt'],
            'Kahvaltılık Gevrek': ['Süt', 'Muz', 'Elma'],
            'Fındık Ezmesi': ['Ekmek', 'Süt'],
            'Çikolata Ezmesi': ['Ekmek', 'Süt'],
            'Dondurulmuş Pizza': ['Kola', 'Cips'],
            'Dondurulmuş Sebze': ['Tavuk Göğsü', 'Dana Eti'],
            'Dondurulmuş Et': ['Patates', 'Soğan'],
            'Dondurma': ['Çikolata', 'Elma', 'Muz'],
            'Dondurulmuş Patates': ['Tavuk Göğsü', 'Dana Eti', 'Balık']
        }
        
        # Tüm ürünleri düzleştir
        self.all_products = []
        for category, products in self.product_categories.items():
            for product in products:
                self.all_products.append(product)
        
        # Ürün ID'leri oluştur
        self.product_ids = {product: i+1 for i, product in enumerate(self.all_products)}
        
    def generate_product_price(self, product_name):
        """Ürün için gerçekçi fiyat oluştur"""
        # Ürünün kategorisini bul
        category = None
        for cat, products in self.product_categories.items():
            if product_name in products:
                category = cat
                break
        
        if category and category in self.price_ranges:
            min_price, max_price = self.price_ranges[category]
            # Normal dağılım kullanarak daha gerçekçi fiyatlar
            mean_price = (min_price + max_price) / 2
            std_price = (max_price - min_price) / 6
            price = np.random.normal(mean_price, std_price)
            price = max(min_price, min(max_price, price))
            return round(price, 2)
        else:
            # Varsayılan fiyat aralığı
            return round(random.uniform(5, 50), 2)
    
    def get_related_products(self, product_name, relationship_strength=0.7):
        """Bir ürünle ilişkili diğer ürünleri döndür"""
        related = []
        
        # Doğrudan ilişkili ürünler
        if product_name in self.product_relationships:
            related.extend(self.product_relationships[product_name])
        
        # Aynı kategorideki ürünler
        for category, products in self.product_categories.items():
            if product_name in products:
                related.extend([p for p in products if p != product_name])
                break
        
        # İlişki gücüne göre filtrele
        if random.random() < relationship_strength:
            return list(set(related))  # Tekrarları kaldır
        else:
            return []
    
    def generate_basket(self, basket_id, date, customer_type='regular'):
        """Tek bir sepet oluştur"""
        basket_items = []
        
        # Sepet boyutu (müşteri tipine göre değişir)
        if customer_type == 'small':
            basket_size = random.randint(1, 3)
        elif customer_type == 'large':
            basket_size = random.randint(8, 15)
        else:  # regular
            basket_size = random.randint(3, 8)
        
        # İlk ürünü rastgele seç
        first_product = random.choice(self.all_products)
        basket_items.append(first_product)
        
        # Diğer ürünleri ekle
        for _ in range(basket_size - 1):
            if basket_items and random.random() < 0.6:  # %60 ihtimalle ilişkili ürün
                # Mevcut ürünlerden birini seç ve ilişkili ürünlerini al
                base_product = random.choice(basket_items)
                related_products = self.get_related_products(base_product)
                
                if related_products:
                    new_product = random.choice(related_products)
                    if new_product not in basket_items:
                        basket_items.append(new_product)
                        continue
            
            # İlişkili ürün bulunamazsa rastgele ürün ekle
            new_product = random.choice(self.all_products)
            if new_product not in basket_items:
                basket_items.append(new_product)
        
        # Sepet öğelerini DataFrame formatına çevir
        basket_data = []
        for product_name in basket_items:
            unit_price = self.generate_product_price(product_name)
            quantity = random.randint(1, 3)  # 1-3 adet
            total_price = unit_price * quantity
            
            basket_data.append({
                'basket_id': basket_id,
                'product_id': self.product_ids[product_name],
                'product_name': product_name,
                'product_quantity': quantity,
                'product_unit_price': unit_price,
                'product_total_price': total_price,
                'purchase_date': date
            })
        
        return basket_data
    
    def generate_dataset(self, num_baskets=1000, days_back=30):
        """Tam veri seti oluştur"""
        all_baskets = []
        
        # Tarih aralığı
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        # Müşteri tipleri ve ağırlıkları
        customer_types = ['small', 'regular', 'large']
        customer_weights = [0.2, 0.6, 0.2]  # %20 küçük, %60 normal, %20 büyük sepet
        
        for basket_id in range(1, num_baskets + 1):
            # Rastgele tarih
            random_days = random.randint(0, days_back)
            purchase_date = start_date + timedelta(days=random_days)
            
            # Müşteri tipi seç
            customer_type = np.random.choice(customer_types, p=customer_weights)
            
            # Sepet oluştur
            basket_data = self.generate_basket(basket_id, purchase_date, customer_type)
            all_baskets.extend(basket_data)
        
        # DataFrame oluştur
        df = pd.DataFrame(all_baskets)
        
        # Tarihi string formatına çevir
        df['purchase_date'] = df['purchase_date'].dt.strftime('%Y-%m-%d')
        
        return df
    
    def save_to_database_format(self, df, filename='basket_data.csv'):
        """Veriyi CSV formatında kaydet"""
        df.to_csv(filename, index=False)
        print(f"Veri seti {filename} dosyasına kaydedildi.")
        print(f"Toplam {len(df)} kayıt, {df['basket_id'].nunique()} sepet oluşturuldu.")
        
        # İstatistikler
        print(f"\nVeri Seti İstatistikleri:")
        print(f"- Toplam ürün çeşidi: {df['product_name'].nunique()}")
        print(f"- Ortalama sepet boyutu: {len(df) / df['basket_id'].nunique():.2f}")
        print(f"- Toplam gelir: ${df['product_total_price'].sum():,.2f}")
        
        return df
    
    def generate_sample_baskets(self, num_samples=10):
        """Örnek sepetler oluştur ve göster"""
        print("Örnek Sepetler:")
        print("=" * 50)
        
        for i in range(num_samples):
            basket_data = self.generate_basket(i+1, datetime.now())
            
            print(f"\nSepet {i+1}:")
            total = 0
            for item in basket_data:
                print(f"  - {item['product_name']}: {item['product_quantity']} adet x ${item['product_unit_price']:.2f} = ${item['product_total_price']:.2f}")
                total += item['product_total_price']
            print(f"  Toplam: ${total:.2f}")
            print("-" * 30)

def main():
    """Ana fonksiyon - veri seti oluştur"""
    generator = ShoppingDataGenerator()
    
    print("🛒 Alışveriş Sepeti Veri Seti Oluşturucu")
    print("=" * 50)
    
    # Örnek sepetler göster
    generator.generate_sample_baskets(5)
    
    print("\n" + "=" * 50)
    print("Veri seti oluşturuluyor...")
    
    # Tam veri seti oluştur
    df = generator.generate_dataset(num_baskets=2000, days_back=60)
    
    # CSV olarak kaydet
    generator.save_to_database_format(df, 'basket_product_unit.csv')
    
    # Ürün kategorileri ve ilişkileri JSON olarak kaydet
    metadata = {
        'product_categories': generator.product_categories,
        'product_relationships': generator.product_relationships,
        'price_ranges': generator.price_ranges
    }
    
    with open('product_metadata.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print("\n✅ Veri seti başarıyla oluşturuldu!")
    print("📁 Dosyalar:")
    print("  - basket_product_unit.csv (ana veri seti)")
    print("  - product_metadata.json (ürün kategorileri ve ilişkileri)")
    
    return df

if __name__ == "__main__":
    df = main() 