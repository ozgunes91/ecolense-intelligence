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

### Özellik Mühendisliği
- **Kişi başı metrikler**: İsraf, ekonomik kayıp, karbon ayak izi
- **Zaman özellikleri**: Pandemi dönemi, yıl trendleri, döngüsel özellikler
- **Coğrafi özellikler**: Kıta, yarıküre, gelişmişlik seviyesi
- **Türetilmiş özellikler**: Verimlilik, yoğunluk, pay oranları

## 🤖 Makine Öğrenmesi Modelleri

### Model Seçimi ve Performans
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

## 📈 Kritik Bulgular

### Gıda Kategorilerine Göre İsraf
1. **Hazır Gıdalar**: En yüksek israf oranı
2. **Meyve & Sebzeler**: İkinci sırada
3. **Süt Ürünleri**: Üçüncü sırada
4. **Tahıl Ürünleri**: Dördüncü sırada

### Ülke Performansları
- **En Yüksek İsraf**: Çin, ABD, Hindistan
- **En Düşük İsraf**: Avustralya, Kanada, Almanya
- **Sürdürülebilirlik Lideri**: Çin (86.5), Rusya (86.2), İspanya (84.7)

### Pandemi Etkisi
- 2020-2021 döneminde %15-20 artış
- Ev tipi israfın %30 artması
- Restoran israfının %40 azalması

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

### Aksiyon Önerileri
1. **Politika Seviyesi**: Gıda israfı yasaları ve teşvikler
2. **Kurumsal Seviye**: Tedarik zinciri optimizasyonu
3. **Bireysel Seviye**: Farkındalık kampanyaları
4. **Teknolojik**: IoT ve AI destekli çözümler

## 🔗 Canlı Dashboard

**🌐 Erişim Linki**: [Ecolense Intelligence Dashboard](https://ecolense-intelligence.streamlit.app/)

## 📁 Proje Yapısı

```
EcolenseIntelligence/
├── app.py                          # Ana Streamlit uygulaması
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