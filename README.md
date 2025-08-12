# 🌱 Ecolense Intelligence - Gıda İsrafı Analiz Platformu

## 📋 Proje Özeti

**Ecolense Intelligence**, küresel gıda israfı problemini analiz eden ve sürdürülebilir çözümler sunan kapsamlı bir veri analizi ve makine öğrenmesi platformudur. 20 ülke, 8 gıda kategorisi ve 5000+ gözlem ile geliştirilen bu platform, gıda israfının ekonomik, çevresel ve sosyal etkilerini derinlemesine analiz eder.

### 🎯 Ana Hedefler
- Küresel gıda israfı trendlerini analiz etmek
- Karbon ayak izi ve ekonomik kayıpları hesaplamak
- Sürdürülebilirlik skorları oluşturmak
- Politika önerileri geliştirmek
- İnteraktif dashboard ile veri görselleştirme

## 📊 Veri Seti ve Metodoloji

### Veri Kaynakları
- **Global Food Wastage Dataset**: 8 temel değişken (ülke, yıl, gıda kategorisi, toplam israf, ekonomik kayıp, vb.)
- **Material Footprint Dataset**: 32 değişken (ISO kodları, kıta, gelişmişlik seviyesi, vb.)

### Veri Zenginleştirme Süreci
- **Inner Join** ile iki veri setinin birleştirilmesi
- **ISO Code Mapping** ile ülke kodlarının standardizasyonu
- **29 yeni özellik** mühendisliği ile toplam 37 değişken
- **5000 gözlem** ile zenginleştirilmiş final veri seti

### Özellik Mühendisliği (01_veri_hazirlama.py'den)
- **Kişi başı metrikler**: İsraf, ekonomik kayıp, karbon ayak izi
- **Zaman özellikleri**: Pandemi dönemi, yıl trendleri, döngüsel özellikler
- **Coğrafi özellikler**: Kıta, yarıküre, gelişmişlik seviyesi
- **Türetilmiş özellikler**: Verimlilik, yoğunluk, pay oranları
- **Etkileşim özellikleri**: Nüfus-malzeme etkileşimi, yıl-nüfus etkileşimi
- **Zaman bazlı trendler**: 3 yıllık rolling average trendler
- **Kategori bazlı özellikler**: Kategori pay oranları

### Sürdürülebilirlik Skoru Hesaplama
```python
# 01_veri_hazirlama.py'den alınan formül
waste_score = max(0, 1 - (Waste_Per_Capita_kg / 0.5))
economic_score = max(0, 1 - (Economic_Loss_Per_Capita_USD / 300))
carbon_score = max(0, 1 - (Carbon_Per_Capita_kgCO2e / 0.5))
sustainability = (waste_score * 0.4 + economic_score * 0.3 + carbon_score * 0.3) * 100
```

### Veri Kalitesi İyileştirmeleri
- **Aykırı değer işleme**: Winsorization (%1-%99 aralığına kırpma)
- **Eksik değer doldurma**: KNN Imputer ve median imputation
- **Encoding**: Label Encoding kategorik değişkenler için

## 🤖 Makine Öğrenmesi Modelleri

### Model Seçimi ve Performans (02_model_egitimi.py'den)
- **Ana Model**: Gradient Boosting Regressor
- **Alternatif Modeller**: Random Forest, Linear Regression, Ridge, Lasso
- **Çoklu Hedef**: Toplam İsraf, Ekonomik Kayıp, Karbon Ayak İzi

### Model Performans Metrikleri
| Metrik | Değer |
|--------|-------|
| Test R² Skoru | %96.0 |
| Cross-Validation R² | %95.8 |
| Overfitting Gap | %0.8 |
| MAPE | %10.2 |

### Model Doğrulama
- **Train-Test Split**: %80/%20
- **Cross-Validation**: 3-fold CV
- **A/B Testing**: 27 farklı model-özellik kombinasyonu
- **SHAP Analizi**: Model açıklanabilirliği

### A/B Testing Sonuçları (03_ab_testing_analizi.py'den)
- **Toplam Test**: 27 kombinasyon
- **En İyi Model**: Gradient Boosting
- **En İyi Özellik Grubu**: Core + Trends
- **Hedef Değişkenler**: 3 (Atık, Ekonomik Kayıp, Karbon)

## 📈 Kritik Bulgular ve Çıkarımlar

### Gıda Kategorilerine Göre İsraf (Veri Setinden)
1. **Prepared Food**: En yüksek israf oranı
2. **Fruits & Vegetables**: İkinci sırada
3. **Dairy Products**: Üçüncü sırada
4. **Grains & Cereals**: Dördüncü sırada
5. **Beverages**: Beşinci sırada
6. **Meat & Seafood**: Altıncı sırada
7. **Frozen Food**: Yedinci sırada
8. **Bakery Items**: Sekizinci sırada

### Ülke Performansları (Dashboard Analizinden)
- **En Yüksek İsraf**: İspanya (50K ton), ABD (50K ton), Hindistan (50K ton)
- **En Düşük İsraf**: Avustralya, Kanada, Almanya
- **En Yüksek CO2**: İspanya (406 kg), İngiltere (385 kg), Almanya (166 kg)
- **Sürdürülebilirlik Lideri**: Çin (86.5), Rusya (86.2), İspanya (84.7)

### Pandemi Etkisi
- 2020-2021 döneminde %15-20 artış
- Ev tipi israfın %30 artması
- Restoran israfının %40 azalması

### Model Başarısı ve Çıkarımlar
- **%96.0 Test R²**: Model çok yüksek doğrulukla tahmin yapıyor
- **%0.8 Overfitting Gap**: Model genelleme yeteneği çok iyi
- **%10.2 MAPE**: Ortalama mutlak yüzde hata düşük
- **Gradient Boosting**: En iyi performans gösteren model

## 🎛️ Dashboard Modülleri (22 Modül)

### 📊 Analiz Modülleri
1. **Genel Bakış**: Proje özeti ve temel metrikler
2. **Veri Keşfi**: İnteraktif veri analizi
3. **Trend Analizi**: Zaman serisi görselleştirmeleri
4. **Coğrafi Analiz**: Ülke bazlı karşılaştırmalar
5. **Kategori Analizi**: Gıda türü bazlı incelemeler
6. **Sürdürülebilirlik Skorları**: Ülke performansları
7. **Karbon Ayak İzi**: Çevresel etki analizi
8. **Ekonomik Etki**: Finansal kayıp hesaplamaları

### 🤖 AI ve Model Modülleri
9. **Model Performansı**: ML model sonuçları
10. **SHAP Analizi**: Özellik önem dereceleri
11. **A/B Testing**: Model karşılaştırmaları
12. **Tahmin Motoru**: Gelecek projeksiyonları
13. **AI Asistan**: Akıllı öneriler sistemi

### 🎯 Politika ve Strateji Modülleri
14. **Politika Simülatörü**: What-if analizleri
15. **ROI Hesaplayıcı**: Yatırım getirisi
16. **Sürücü Analizi**: Faktör etki analizi
17. **Anomali İzleme**: Anormal durum tespiti
18. **Karbon Akışları**: Çevresel etki haritaları

### 📋 Raporlama Modülleri
19. **Rapor Oluşturucu**: Otomatik rapor üretimi
20. **Model Kartı**: Model dokümantasyonu
21. **Veri Kalitesi**: Veri doğruluk raporu
22. **Hakkında**: Proje bilgileri

## 🚀 Teknik Özellikler

### Teknoloji Stack
- **Frontend**: Streamlit
- **Backend**: Python
- **Veri İşleme**: Pandas, NumPy
- **Görselleştirme**: Plotly
- **ML**: Scikit-learn, SHAP
- **Deployment**: Streamlit Cloud

### Performans Özellikleri
- **Gerçek Zamanlı Analiz**: Anlık veri işleme
- **İnteraktif Grafikler**: Dinamik görselleştirmeler
- **Responsive Tasarım**: Mobil uyumlu arayüz
- **Hızlı Yükleme**: Optimize edilmiş performans

## 📊 Sonuçlar ve Öneriler

### Ana Bulgular
- Küresel gıda israfının %40'ı ev tipi
- Yıllık ekonomik kayıp: 1.3 trilyon USD
- Karbon ayak izi: 3.3 gigaton CO2e
- Sürdürülebilirlik skoru ortalaması: 84/100
- En yüksek sürdürülebilirlik: Çin (86.5/100)

### Kritik Çıkarımlar

#### 1. **Model Başarısı**
- **%96.0 doğruluk** ile çok yüksek tahmin başarısı
- **Düşük overfitting** (%0.8) ile güvenilir genelleme
- **Gradient Boosting** en etkili model

#### 2. **Veri Kalitesi**
- **29 yeni özellik** ile zenginleştirilmiş veri seti
- **Winsorization** ile aykırı değer kontrolü
- **KNN Imputation** ile eksik veri doldurma

#### 3. **Sürdürülebilirlik Analizi**
- **Çok faktörlü skorlama** sistemi
- **Ağırlıklı hesaplama** (atık %40, ekonomik %30, karbon %30)
- **0-100 aralığında** normalize edilmiş skorlar

#### 4. **Ülke Performansları**
- **İspanya, ABD, Hindistan** en yüksek israf
- **Çin, Rusya, İspanya** en yüksek sürdürülebilirlik
- **Coğrafi farklılıklar** belirgin

### Aksiyon Önerileri

#### 1. **Politika Seviyesi**
- **Gıda israfı yasaları** ve teşvikler
- **Uluslararası işbirliği** programları
- **Sürdürülebilirlik hedefleri** belirleme

#### 2. **Kurumsal Seviye**
- **Tedarik zinciri optimizasyonu**
- **Atık yönetimi sistemleri**
- **Yeşil teknoloji yatırımları**

#### 3. **Bireysel Seviye**
- **Farkındalık kampanyaları**
- **Eğitim programları**
- **Davranış değişikliği** teşvikleri

#### 4. **Teknolojik**
- **IoT ve AI destekli** çözümler
- **Blockchain** tedarik zinciri takibi
- **Akıllı atık yönetimi** sistemleri

### Gelecek Geliştirme Önerileri

#### 1. **Model İyileştirmeleri**
- **Deep Learning** modelleri entegrasyonu
- **Real-time** tahmin sistemleri
- **Ensemble** model kombinasyonları

#### 2. **Dashboard Geliştirmeleri**
- **Mobile app** geliştirme
- **API** entegrasyonu
- **Multi-language** desteği

#### 3. **Veri Genişletme**
- **Daha fazla ülke** ekleme
- **Yeni veri kaynakları** entegrasyonu
- **Real-time** veri akışı

## 🔗 Canlı Dashboard

**🌐 Erişim Linki**: [Ecolense Intelligence Dashboard](https://ecolense-intelligence.streamlit.app/)

## 📁 Proje Yapısı

```
EcolenseIntelligence/
├── app.py                          # Ana Streamlit uygulaması
├── 01_veri_hazirlama.py            # Veri hazırlama ve özellik mühendisliği
├── 02_model_egitimi.py             # Model eğitimi ve değerlendirme
├── 03_ab_testing_analizi.py        # A/B testing ve model karşılaştırma
├── data/                           # Veri setleri
├── models/                         # ML modelleri
├── static/                         # Görsel dosyalar
├── requirements.txt                # Python bağımlılıkları
└── README.md                       # Proje dokümantasyonu
```

## 👥 Proje Ekibi

**Miuul Data Scientist Bootcamp Final Projesi**

- **Özge Güneş**: Data Scientist

**Proje Dönemi**: 2025

## 📚 Referanslar

- FAO (Food and Agriculture Organization)
- OECD (Organisation for Economic Co-operation and Development)
- World Bank Development Indicators
- UN Environment Programme
- European Environment Agency

## 🛠️ Kurulum ve Çalıştırma

```bash
# Bağımlılıkları yükle
pip install -r requirements.txt

# Uygulamayı çalıştır
streamlit run app.py
```

---

**🌱 Sürdürülebilir bir gelecek için veri odaklı çözümler** 