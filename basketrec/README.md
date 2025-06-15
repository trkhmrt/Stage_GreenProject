# Sepet Analizi Tabanlı Ürün Öneri Sistemi

Bu proje, e-ticaret platformlarında müşteri satın alma davranışlarını analiz ederek kişiselleştirilmiş ürün önerileri sunan bir sistemdir. Apriori algoritması ve birliktelik kuralları (association rules) kullanılarak geliştirilmiştir.

## 🎯 Proje Amacı

- Müşteri sepetlerindeki ürün birlikteliklerini tespit etme
- Anlamlı ürün ilişkilerini matematiksel olarak modelleme
- Gerçek zamanlı öneri sistemi geliştirme
- Kullanıcı dostu arayüz ile önerileri sunma

## 🏗️ Sistem Mimarisi

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   Flask API     │    │   MySQL DB      │
│   Web Arayüzü   │◄──►│   Endpoint      │◄──►│   Veritabanları │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Python Core   │
                    │   Algoritmaları │
                    └─────────────────┘
```

## 📋 Gereksinimler

### Sistem Gereksinimleri
- Python 3.8+
- MySQL 8.0+
- 4GB RAM (minimum)
- 2GB disk alanı

### Python Paketleri
```
pandas>=1.3.0
numpy>=1.21.0
streamlit>=1.0.0
flask>=2.0.0
flask-cors>=3.0.0
sqlalchemy>=1.4.0
mysql-connector-python>=8.0.0
mlxtend>=0.19.0
scikit-learn>=1.0.0
```

## 🚀 Kurulum

### 1. Projeyi İndirin
```bash
git clone https://github.com/kullaniciadi/basketrec.git
cd basketrec
```

### 2. Sanal Ortam Oluşturun
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate     # Windows
```

### 3. Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 4. Veritabanı Kurulumu
```sql
-- Ürün veritabanı oluşturun
CREATE DATABASE product_db;
USE product_db;

-- Tabloları oluşturun (database_schema.sql dosyasını çalıştırın)
```

### 5. Konfigürasyon
`config.py` dosyasını düzenleyin:
```python
# Veritabanı bağlantı bilgileri
username = "your_username"
password = "your_password"
product_host = "localhost"
basket_host = "localhost"
product_port = 3306
basket_port = 3306
product_database = "product_db"
basket_database = "basket_db"
```

## 📊 Veri Hazırlama

### 1. Örnek Veri Oluşturma
```bash
python generate_sample_data.py
```

### 2. Veri Yükleme
```bash
python load_data_to_db.py
```

## 🎮 Kullanım

### Web Arayüzü (Streamlit)
```bash
streamlit run streamlit_app.py
```
Tarayıcınızda `http://localhost:8501` adresine gidin.

### API Sunucusu
```bash
python recommendation_api.py
```
API `http://localhost:5000` adresinde çalışacaktır.

### API Kullanımı
```bash
# Öneri alma
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{"products": ["Süt", "Ekmek"]}'

# Tüm ürünleri listele
curl -X GET http://localhost:5000/products

# Sağlık kontrolü
curl -X GET http://localhost:5000/health
```

## 🔧 API Endpoints

### POST /recommend
Ürün önerileri alın.

**Request:**
```json
{
  "products": ["Ürün Adı 1", "Ürün Adı 2"]
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "product_id": 123,
      "product_name": "Önerilen Ürün",
      "product_price": 15.50,
      "product_description": "Ürün açıklaması",
      "sub_category_name": "Alt Kategori",
      "category_name": "Ana Kategori"
    }
  ]
}
```

### GET /products
Tüm ürünleri listele.

### GET /health
API sağlık kontrolü.

## 📈 Algoritma Detayları

### Apriori Algoritması
1. **1-öğe setlerini** oluştur
2. **Minimum support** ile filtrele
3. **Aday setleri** oluştur
4. **Sık öğe setlerini** bul
5. **Birliktelik kurallarını** türet

### Matematiksel Formüller
```
Support(X) = |X| / |T|
Confidence(X→Y) = Support(X∪Y) / Support(X)
Lift(X→Y) = Confidence(X→Y) / Support(Y)
```

## 📊 Performans Metrikleri

| Metrik | Değer |
|--------|-------|
| Toplam Sepet | 22,979 |
| Sık Öğe Seti | 545 |
| Birliktelik Kuralı | 1,210 |
| Ortalama Yanıt Süresi | 1.2s |
| Precision@5 | 0.73 |
| Recall@5 | 0.68 |

## 🧪 Test

### Birim Testleri
```bash
python -m pytest tests/
```

### Entegrasyon Testleri
```bash
python test_api.py
```

### Performans Testleri
```bash
python performance_test.py
```

## 📁 Proje Yapısı

```
basketrec/
├── streamlit_app.py          # Streamlit web arayüzü
├── recommendation_api.py     # Flask API
├── config.py                 # Konfigürasyon dosyası
├── database_schema.sql       # Veritabanı şeması
├── generate_sample_data.py   # Örnek veri oluşturma
├── load_data_to_db.py       # Veri yükleme
├── requirements.txt          # Python bağımlılıkları
├── tests/                    # Test dosyaları
├── docs/                     # Dokümantasyon
│   ├── bitirme_projesi_raporu.md
│   ├── algoritma_diyagramlari.md
│   └── proje_sunumu.md
└── README.md                 # Bu dosya
```

## 🔍 Sorun Giderme

### Yaygın Sorunlar

1. **Veritabanı Bağlantı Hatası**
   - MySQL servisinin çalıştığından emin olun
   - Bağlantı bilgilerini kontrol edin

2. **Modül Bulunamadı Hatası**
   - Sanal ortamın aktif olduğundan emin olun
   - `pip install -r requirements.txt` komutunu çalıştırın

3. **Port Çakışması**
   - Farklı portlar kullanın
   - Çalışan servisleri durdurun

### Log Dosyaları
- Streamlit: `~/.streamlit/logs/`
- Flask: Konsol çıktısı
- Veritabanı: MySQL error log

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 👥 Yazar

- **Adınız** - [E-posta Adresiniz]
- **GitHub:** [GitHub Profiliniz]
- **LinkedIn:** [LinkedIn Profiliniz]

## 🙏 Teşekkürler

- **Danışman:** [Danışman Adı]
- **Bölüm:** [Bölüm Adı]
- **Üniversite:** [Üniversite Adı]

## 📚 Kaynaklar

1. Agrawal, R., Imieliński, T., & Swami, A. (1993). Mining association rules between sets of items in large databases.
2. Agrawal, R., & Srikant, R. (1994). Fast algorithms for mining association rules.
3. Ricci, F., Rokach, L., & Shapira, B. (2011). Introduction to recommender systems handbook.

## 📞 İletişim

Sorularınız için:
- **E-posta:** [E-posta Adresiniz]
- **GitHub Issues:** [GitHub Issues Link]

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın! 