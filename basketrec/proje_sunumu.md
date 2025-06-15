# Sepet Analizi Tabanlı Ürün Öneri Sistemi
## Proje Sunumu

---

## Slayt 1: Proje Başlığı

### Sepet Analizi Tabanlı Ürün Öneri Sistemi
**Üniversite Bitirme Projesi**

- **Öğrenci:** [Adınız]
- **Danışman:** [Danışman Adı]
- **Bölüm:** [Bölüm Adı]
- **Tarih:** [Sunum Tarihi]

---

## Slayt 2: Proje Özeti

### Problem Tanımı
- E-ticaret platformlarında kişiselleştirilmiş öneri eksikliği
- Geleneksel öneri sistemlerinin yetersizliği
- Müşteri satın alma davranışlarının analiz edilmemesi

### Çözüm Yaklaşımı
- **Apriori Algoritması** ile sepet analizi
- **Birliktelik Kuralları** ile ürün ilişkileri
- **Gerçek zamanlı** öneri sistemi

---

## Slayt 3: Literatür Taraması

### Temel Kaynaklar
1. **Agrawal et al. (1993)** - İlk birliktelik kuralı algoritması
2. **Agrawal & Srikant (1994)** - Apriori algoritması
3. **Ricci et al. (2011)** - Öneri sistemleri el kitabı

### Mevcut Çalışmalar
- Market Basket Analysis
- Association Rule Mining
- Collaborative Filtering

---

## Slayt 4: Sistem Mimarisi

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

### Katmanlar
1. **Sunum Katmanı:** Web arayüzü ve API
2. **İş Mantığı:** Analiz algoritmaları
3. **Veri Katmanı:** MySQL veritabanları

---

## Slayt 5: Apriori Algoritması

### Algoritma Adımları
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

---

## Slayt 6: Veri Seti Özellikleri

### Veri İstatistikleri
- **Toplam Sepet:** 22,979
- **Toplam İşlem:** 4,841
- **Benzersiz Ürün:** 298
- **Ortalama Sepet Büyüklüğü:** 4.75

### Veri Kalitesi
- **Eksik Veri Oranı:** %0.5
- **Tutarlılık:** %99.8
- **Güncellik:** Gerçek zamanlı

---

## Slayt 7: Algoritma Performansı

### Sonuçlar
- **Sık Öğe Seti:** 545
- **Birliktelik Kuralı:** 1,210
- **Ortalama Yanıt Süresi:** 1.2s

### Örnek Kurallar
```
Akıllı Telefon → Telefon Kılıfı (Confidence: 0.85, Lift: 2.3)
Yatak → Nevresim Takımı (Confidence: 0.92, Lift: 3.1)
```

---

## Slayt 8: Sistem Özellikleri

### Web Arayüzü (Streamlit)
- Kullanıcı dostu arayüz
- Gerçek zamanlı öneriler
- Parametre ayarlama
- Sonuç görselleştirme

### API (Flask)
- RESTful API
- JSON formatında yanıt
- CORS desteği
- Hata yönetimi

---

## Slayt 9: Doğruluk Metrikleri

### Performans Değerlendirmesi
- **Precision@5:** 0.73
- **Recall@5:** 0.68
- **F1-Score:** 0.70

### Karşılaştırma
| Metrik | Bizim Sistem | Basit Öneri |
|--------|--------------|-------------|
| Precision | 0.73 | 0.45 |
| Recall | 0.68 | 0.52 |
| F1-Score | 0.70 | 0.48 |

---

## Slayt 10: Teknik Zorluklar ve Çözümler

### Karşılaşılan Zorluklar
1. **Büyük veri seti** işleme
2. **Algoritma optimizasyonu**
3. **Gerçek zamanlı** yanıt
4. **Veri tutarlılığı**

### Uygulanan Çözümler
1. **Chunk-based** işleme
2. **Minimum support** optimizasyonu
3. **Caching** mekanizması
4. **Veri doğrulama** kontrolleri

---

## Slayt 11: Gelecek Çalışmalar

### Planlanan İyileştirmeler
1. **Derin Öğrenme** entegrasyonu
2. **Gerçek zamanlı** öğrenme
3. **Kişiselleştirme** algoritmaları
4. **Mobil uygulama** geliştirme

### Araştırma Alanları
- Neural Collaborative Filtering
- Online Learning Algorithms
- User Profiling Techniques

---

## Slayt 12: Sonuç ve Katkılar

### Proje Katkıları
1. **Akademik:** Birliktelik kuralı tabanlı öneri sistemi
2. **Pratik:** E-ticaret için kullanılabilir çözüm
3. **Teknik:** Ölçeklenebilir sistem mimarisi

### Başarılar
- ✅ Gerçek zamanlı öneriler
- ✅ Yüksek doğruluk oranları
- ✅ Kullanıcı dostu arayüz
- ✅ API entegrasyonu

---

## Slayt 13: Demo

### Canlı Sistem Gösterimi
1. **Web Arayüzü** kullanımı
2. **API** testi
3. **Öneri** sonuçları
4. **Performans** metrikleri

### Test Senaryoları
- Farklı ürün kombinasyonları
- Çeşitli parametre değerleri
- Hata durumları

---

## Slayt 14: Sorular ve Tartışma

### Tartışma Konuları
1. Algoritma seçiminin doğruluğu
2. Performans optimizasyonu
3. Gelecek iyileştirmeler
4. Endüstriyel uygulama

### Sorular
**Dinleyicilerin sorularını bekliyoruz...**

---

## Slayt 15: Teşekkürler

### Teşekkür
- **Danışman:** [Danışman Adı]
- **Bölüm:** [Bölüm Adı]
- **Üniversite:** [Üniversite Adı]
- **Dinleyiciler:** Katılımınız için teşekkürler

### İletişim
- **E-posta:** [E-posta Adresiniz]
- **GitHub:** [GitHub Profiliniz]
- **LinkedIn:** [LinkedIn Profiliniz]

---

## Sunum Notları

### Sunum İpuçları
1. **Her slayt için 2-3 dakika** ayırın
2. **Demo kısmında** canlı sistem gösterin
3. **Sorulara** hazırlıklı olun
4. **Teknik detayları** açıklayın

### Önemli Noktalar
- Algoritmanın matematiksel temeli
- Sistemin pratik uygulanabilirliği
- Performans sonuçları
- Gelecek potansiyeli

### Sunum Sırası
1. Giriş ve problem tanımı (5 dk)
2. Literatür ve metodoloji (10 dk)
3. Sistem mimarisi (5 dk)
4. Algoritma detayları (10 dk)
5. Sonuçlar ve performans (10 dk)
6. Demo (10 dk)
7. Sorular ve tartışma (10 dk)

**Toplam Süre:** 60 dakika 