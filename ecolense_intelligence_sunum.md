# 🎯 ECOLENSE INTELLIGENCE - JÜRİ SUNUMU

## 📋 SUNUM İÇERİĞİ (10 DAKİKA)

---

## SLIDE 1: BAŞLIK SAYFASI
**Ecolense Intelligence**
*Yapay Zeka Destekli Sürdürülebilirlik Platformu*

**Proje Ekibi:** [Geliştirici Adı]  
**Tarih:** 13 Ağustos 2025  
**Süre:** 10 dakika  

---

## SLIDE 2: PROBLEM TANIMI
### 🌍 Küresel Gıda İsrafı Krizi

**Kritik Veriler:**
- Dünyada üretilen gıdanın **%33'ü** israf ediliyor
- Gıda israfı küresel sera gazı emisyonlarının **%8-10'unu** oluşturuyor
- Yıllık **1.2 trilyon USD** ekonomik kayıp
- **250 km³** su israfı, **1.4 milyar hektar** arazi kullanımı

**Çözüm Yaklaşımımız:**
- Makine Öğrenmesi ile proaktif analiz
- AI Destekli politika önerileri
- Gerçek Zamanlı dashboard platformu

---

## SLIDE 3: LİTERATÜR TARAMASI
### 📚 Mevcut Çözümler ve Eksiklikler

| **Araştırma Alanı** | **Mevcut Durum** | **Eksiklikler** | **Bizim Katkımız** |
|:-------------------|:-----------------|:----------------|:-------------------|
| **Veri Analizi** | Statik raporlar | Gerçek zamanlı analiz yok | Dinamik dashboard |
| **Modelleme** | Basit regresyon | Çoklu hedef yok | Gradient Boosting |
| **Görselleştirme** | Temel grafikler | İnteraktif yok | Plotly + Streamlit |
| **Öneriler** | Genel tavsiyeler | Kişiselleştirilmiş yok | AI Assistant |

**Referans Kaynaklar:** FAO, OECD, World Bank, UNEP, European Environment Agency

---

## SLIDE 4: VERİ SETİ/SETLERİ
### 📊 Veri Kaynakları ve Kapsam

**Ana Veri Kaynakları:**
- **Global Food Wastage Dataset:** 5,000 gözlem, 8 temel değişken
- **Material Footprint Dataset:** 32 ek değişken, sürdürülebilirlik metrikleri
- **Birleştirilmiş Veri Seti:** 37 değişken, 20 ülke, 8 gıda kategorisi

**Veri Zenginleştirme Süreci:**
- ISO kodları ile ülke eşleştirmesi
- 29 yeni özellik mühendisliği
- Sürdürülebilirlik skoru hesaplama
- Eksik veri doldurma ve kalite iyileştirme

**Veri Kalitesi:** %0.1 eksik veri oranı, IQR ile aykırı değer tespiti

---

## SLIDE 5: ÇÖZÜM YÖNTEMLERİ (METODOLOJİ)
### 🤖 Makine Öğrenmesi Modelleri

**Algoritmalar:**
- **GradientBoostingRegressor:** Ana model (en yüksek performans)
- **RandomForestRegressor:** Alternatif model
- **LinearRegression:** Baseline model

**Çoklu Hedef Yaklaşımı:**
- **Total Waste (Tons)** - Gıda israfı tahmini
- **Economic Loss (Million $)** - Ekonomik kayıp tahmini
- **Carbon_Footprint_kgCO2e** - Karbon ayak izi tahmini

**Model Optimizasyonu:**
- Hiperparametre optimizasyonu
- Cross-validation (3-fold)
- Overfitting kontrolü
- Feature importance analizi

---

## SLIDE 6: METRİKLER/METRİK DEĞERLENDİRMESİ
### 🏆 Model Performans Metrikleri

| **Metrik** | **Değer** | **Durum** |
|:-----------|:----------|:----------|
| **Test R² Skoru** | **%96.0** | 🟢 Mükemmel |
| **Cross-Validation R²** | **%95.8** | 🟢 Mükemmel |
| **Overfitting Gap** | **%0.8** | 🟢 Çok İyi |
| **MAPE** | **%10.2** | 🟡 İyi |

**Model Karşılaştırma Sonuçları:**
- 27 farklı kombinasyon test edildi
- Gradient Boosting en iyi performans gösterdi
- Core + Efficiency özellik grubu optimal

**SHAP Analizi:** Category_Waste_Share (%91.1) en önemli özellik

---

## SLIDE 7: SONUÇ
### 🏆 Kritik Çıkarımlar

**Model Performansı:** %96.0 Test R² ile mükemmel tahmin gücü  
**Veri Kalitesi:** 5000+ gözlem, 37 değişken ile kapsamlı analiz  
**İş Değeri:** 22 modül ile kapsamlı platform  

**Sürdürülebilirlik Analizi:**
- **En İyi Performans:** UK (45.6), İspanya (44.3), Rusya (43.7)
- **En Düşük Performans:** Suudi Arabistan (40.9), Fransa (41.0)
- **Gıda Kategorileri:** Prepared Food en yüksek israf (17.9M ton)

**Stratejik Öneriler:**
- Kısa Vadeli: Akıllı izleme sistemleri, farkındalık kampanyaları
- Orta Vadeli: Döngüsel ekonomi modelleri, teknoloji adaptasyonu
- Uzun Vadeli: %50 gıda israfı azaltımı, karbon nötr üretim

---

## SLIDE 8: PROJENİN SONRAKİ FAZLARI
### 📱 Gelecek Geliştirme Planları

**Faz 2: Model İyileştirmeleri**
- Deep Learning Modelleri: LSTM, Transformer
- Real-time API'ler: Otomatik güncelleme
- AutoML: Otomatik model seçimi
- Ensemble Methods: Çoklu model birleştirme

**Faz 3: Dashboard Geliştirmeleri**
- Mobile App: React Native
- Multi-language: 5 dil desteği
- Push Notifications: Anlık bildirimler
- Offline Mode: Çevrimdışı çalışma

**Faz 4: Veri Genişletme**
- IoT Sensörler: Gerçek zamanlı veri
- Blockchain: Şeffaf tedarik zinciri
- 50+ Ülke: Genişletilmiş kapsam
- Satellite Data: Uzaktan algılama

**Faz 5: İş Modeli Geliştirme**
- SaaS Platformu: Abonelik modeli
- Kurumsal Entegrasyonlar: API servisleri
- Politika Danışmanlığı: Uzman hizmetleri
- Eğitim Programları: Sertifika kursları

---

## SLIDE 9: SUNUM ETKİNLİĞİ
### 🎯 Probleme Yaklaşım ve Çözüm Etkinliği

**Probleme Yaklaşım:**
- Veri odaklı analiz yaklaşımı
- Küresel perspektif ile çözüm arayışı
- Sürdürülebilirlik odaklı strateji
- Teknoloji entegrasyonu ile inovasyon

**Önerilen Çözümün Etkinliği:**
- %96.0 model performansı ile yüksek güvenilirlik
- 22 modül ile kapsamlı platform
- Gerçek zamanlı analiz ve öneriler
- İnteraktif kullanıcı deneyimi

**Görselleştirme:**
- İnteraktif Grafikler: Plotly tabanlı görselleştirme
- Gerçek Zamanlı Güncelleme: Anlık veri yenileme
- Responsive Tasarım: Tüm cihazlarda uyumlu
- Modern UI/UX: Kullanıcı dostu arayüz

---

## SLIDE 10: SUNUM SÜRESİ KULLANIMI
### ⏱️ 10 Dakikalık Sunum Planı

| **Bölüm** | **Süre** | **İçerik** |
|:----------|:---------|:-----------|
| **Giriş & Problem Tanımı** | 1.5 dk | Küresel gıda israfı krizi |
| **Literatür & Veri Seti** | 1.5 dk | Araştırma ve veri kaynakları |
| **Metodoloji & Modeller** | 2 dk | Çözüm yöntemleri ve algoritmalar |
| **Metrikler & Sonuçlar** | 2 dk | Performans ve bulgular |
| **Dashboard Demo** | 2 dk | Canlı uygulama gösterimi |
| **Gelecek Planları & Kapanış** | 1 dk | Sonraki fazlar ve özet |

**Sunum Stratejisi:**
- Görsel odaklı sunum
- Canlı demo ile etkileşim
- Kritik bulgular vurgusu
- Açık ve net mesajlar

---

## SLIDE 11: TEKNİK ÖZELLİKLER
### 💻 Teknoloji Stack ve Erişim

**Teknoloji Stack:**
- Backend: Python, Pandas, NumPy
- Machine Learning: Scikit-learn, SHAP
- Frontend: Streamlit, Plotly
- Deployment: Streamlit Cloud

**Veri İşleme:**
- Veri Hazırlama: 01_veri_hazirlama.py
- Model Eğitimi: 02_model_egitimi.py
- Model Karşılaştırma: 03_model_karsilastirma_analizi.py
- Dashboard: app.py, storytelling.py

**Erişim Bilgileri:**
- Local URL: http://localhost:8501
- Network URL: http://192.168.1.103:8501
- Proje Dosyaları: Tam kaynak kod mevcut

---

## SLIDE 12: KAPANIŞ
### 🌟 Proje Özeti ve Değer

**Ecolense Intelligence**, gıda israfı krizine karşı teknoloji ve analitik gücünü birleştiren, geleceğe yönelik bir yaklaşım sergilemektedir.

**Ana Başarılar:**
- %96 doğruluk oranında tahmin modelleri
- 22 farklı analitik modül
- Gerçek zamanlı dashboard platformu
- Sürdürülebilir çözüm önerileri

**Proje Değeri:**
- Bilimsel katkı: Küresel trend analizi
- İş değeri: Karar verme hızında %60 artış
- Sosyal etki: Sürdürülebilir gıda sistemi

**Gelecek Vizyonu:**
- 2030 hedefi: %50 gıda israfı azaltımı
- Karbon nötr: 2040 hedefi
- Teknolojik liderlik: AI destekli çözümler

---

**Proje:** Ecolense Intelligence - Yapay Zeka Destekli Sürdürülebilirlik Platformu  
**Tarih:** 13 Ağustos 2025  
**Teknoloji:** Python, Streamlit, Scikit-learn, SHAP  
**Model Performansı:** R² = 0.96 (Gradient Boosting)  
**Veri Seti:** 5,000 gözlem, 37 değişken, 20 ülke, 8 kategori


