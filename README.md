# 🌱 **ECOLENSE INTELLIGENCE**
### *Premium Küresel Gıda İsrafı Analizi ve Sürdürülebilir Çözümler Platformu*

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3+-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](https://ecolense-intelligence.streamlit.app/)

---

## 📊 **PROJE ÖZETİ**

<div align="center">

| 🎯 **Hedef** | 📈 **Kapsam** | 🤖 **Teknoloji** | 📊 **Performans** |
|:-------------:|:-------------:|:----------------:|:-----------------:|
| Küresel gıda israfı analizi | 20 ülke, 8 kategori | Gradient Boosting | %96.0 Test R² |
| Sürdürülebilirlik skorlaması | 5000+ gözlem | SHAP Analizi | %0.8 Overfitting |
| Politika önerileri | 37 değişken | A/B Testing | 22 Modül |

</div>

---

## 🌍 **PROBLEM TANIMI**

### 📈 **Küresel Gıda İsrafı Krizi**

> **FAO Raporu (2021):** Dünyada üretilen gıdanın **%33'ü** israf ediliyor
> 
> **UNEP Çalışması:** Gıda israfı küresel sera gazı emisyonlarının **%8-10'unu** oluşturuyor
> 
> **World Bank Analizi:** Gelişmekte olan ülkelerde ev tipi israf, gelişmiş ülkelerde tedarik zinciri israfı
> 
> **OECD Araştırması:** Kişi başı israf oranları ülke gelişmişlik seviyesi ile ters orantılı

### 🎯 **Çözüm Yaklaşımımız**
- **Makine Öğrenmesi** ile proaktif analiz
- **AI Destekli** politika önerileri
- **Gerçek Zamanlı** dashboard platformu
- **Sürdürülebilirlik** odaklı çözümler

---

## 📚 **LİTERATÜR TARAMASI VE ARAŞTIRMA**

### 🔬 **Mevcut Çözümler ve Eksiklikler**

| **Araştırma Alanı** | **Mevcut Durum** | **Eksiklikler** | **Bizim Katkımız** |
|:-------------------|:-----------------|:----------------|:-------------------|
| **Veri Analizi** | Statik raporlar | Gerçek zamanlı analiz yok | Dinamik dashboard |
| **Modelleme** | Basit regresyon | Çoklu hedef yok | Gradient Boosting |
| **Görselleştirme** | Temel grafikler | İnteraktif yok | Plotly + Streamlit |
| **Öneriler** | Genel tavsiyeler | Kişiselleştirilmiş yok | AI Assistant |

### 📖 **Referans Kaynaklar**
- **FAO (Food and Agriculture Organization)** - Gıda güvenliği raporları
- **OECD (Organisation for Economic Co-operation and Development)** - Ekonomik analizler
- **World Bank** - Kalkınma göstergeleri
- **UN Environment Programme** - Çevresel etki değerlendirmeleri
- **European Environment Agency** - Sürdürülebilirlik metrikleri

---

## 📊 **VERİ SETİ VE METODOLOJİ**

### 🗂️ **Veri Kaynakları**

<div align="center">

| **Veri Seti** | **Değişken Sayısı** | **Gözlem Sayısı** | **Dönem** | **Kaynak** |
|:-------------:|:-------------------:|:-----------------:|:---------:|:----------:|
| **Global Food Wastage** | 8 | 5002 | 2018-2024 | Kaggle |
| **Material Footprint** | 32 | 197 | 1990-2021 | OECD |
| **Birleştirilmiş Veri** | 37 | 5001 | 2018-2024 | Inner Join |

</div>

### 🔧 **Veri Zenginleştirme Süreci**

#### **1. Veri Birleştirme (Inner Join)**
```python
# ISO kodları ile ülke eşleştirmesi
merged_df = food_waste.merge(material_footprint, 
                            left_on='Country', 
                            right_on='Country', 
                            how='inner')
```

#### **2. Özellik Mühendisliği (29 Yeni Değişken)**

| **Kategori** | **Özellikler** | **Sayı** | **Örnek** |
|:-------------|:---------------|:---------|:----------|
| **📊 Per-Capita Metrikler** | Kişi başı hesaplamalar | 6 | `Waste_Per_Capita_kg` |
| **⏰ Temporal Özellikler** | Zaman bazlı değişkenler | 8 | `Pandemic_Indicator` |
| **🌍 Coğrafi Özellikler** | Kıta, yarım küre | 4 | `Continent`, `Hemisphere` |
| **📈 Türetilmiş Özellikler** | Verimlilik, yoğunluk | 6 | `Waste_Efficiency` |
| **🔄 Etkileşim Özellikleri** | Çapraz hesaplamalar | 3 | `Population_Material_Interaction` |
| **📊 Zaman Bazlı Trendler** | Rolling average | 2 | `Waste_Trend_3Y` |

#### **3. Sürdürülebilirlik Skoru Hesaplama**
```python
def calculate_sustainability_score(row):
    waste_score = (100 - row['Waste_Per_Capita_kg']) / 100
    economic_score = (100 - row['Economic_Loss_Per_Capita_USD']) / 100
    carbon_score = (100 - row['Carbon_Per_Capita_kgCO2e']) / 100
    
    return (waste_score * 0.4 + economic_score * 0.3 + carbon_score * 0.3) * 100
```

### 🛠️ **Veri Kalitesi İyileştirmeleri**

| **İşlem** | **Metod** | **Etki** |
|:----------|:----------|:---------|
| **Aykırı Değerler** | Winsorization (1%-99%) | %15 iyileştirme |
| **Eksik Veriler** | KNN Imputer + Median | %100 tamamlama |
| **Kategorik Kodlama** | Label Encoding | Standartlaştırma |
| **Ölçeklendirme** | StandardScaler | Model performansı |

---

## 🤖 **MAKİNE ÖĞRENMESİ MODELLERİ**

### 🎯 **Model Seçimi ve Performans (02_model_egitimi.py'den)**

#### **🏆 Ana Model: Gradient Boosting Regressor**
- **Algoritma:** Gradient Boosting
- **Hiperparametreler:** n_estimators=100, max_depth=4, learning_rate=0.05
- **Seçim Kriteri:** A/B Testing Winner + CV R² + Overfitting Control

#### **🔄 Alternatif Modeller**
- **Random Forest:** Conservative approach
- **Linear Regression:** Baseline model
- **Ridge Regression:** Regularization
- **Lasso Regression:** Feature selection

#### **🎯 Çoklu Hedef Yaklaşımı**
- **Total Waste (Tons)**
- **Economic Loss (Million $)**
- **Carbon_Footprint_kgCO2e**

### 📊 **Model Performans Metrikleri**

<div align="center">

| **Metrik** | **Değer** | **Durum** |
|:-----------|:----------|:----------|
| **Test R² Skoru** | **%96.0** | 🟢 Mükemmel |
| **Cross-Validation R²** | **%95.8** | 🟢 Mükemmel |
| **Overfitting Gap** | **%0.8** | 🟢 Çok İyi |
| **MAPE** | **%10.2** | 🟡 İyi |

</div>

### ✅ **Model Doğrulama**

| **Yöntem** | **Detay** | **Sonuç** |
|:-----------|:----------|:----------|
| **Train-Test Split** | %80/%20 | ✅ Geçerli |
| **Cross-Validation** | 3-fold CV | ✅ Stabil |
| **A/B Testing** | 27 kombinasyon | ✅ Optimize |
| **SHAP Analizi** | Model açıklanabilirliği | ✅ Şeffaf |

---

## 🧪 **A/B TESTING SONUÇLARI (03_ab_testing_analizi.py'den)**

### 📈 **Test Kapsamı**

| **Test Grubu** | **Kombinasyon** | **Sonuç** |
|:---------------|:----------------|:----------|
| **Model Türleri** | 5 farklı model | Gradient Boosting kazandı |
| **Özellik Grupları** | 6 farklı grup | Core + Efficiency en iyi |
| **Toplam Test** | 27 kombinasyon | %96.0 başarı |

### 🏆 **En İyi Performans Gösteren Kombinasyonlar**

| **Hedef** | **Model** | **Özellik Grubu** | **Test R²** | **Overfitting** |
|:----------|:----------|:------------------|:------------|:----------------|
| **Total Waste** | Gradient Boosting | Core + Efficiency | 0.961 | 0.007 |
| **Economic Loss** | Gradient Boosting | Core + Trends | 0.959 | 0.009 |
| **Carbon Footprint** | Gradient Boosting | Core + Efficiency | 0.961 | 0.007 |

---

## 🔍 **KRİTİK BULGULAR VE ÇIKARIMLAR**

### 🏆 **Sürdürülebilirlik Liderleri**

<div align="center">

| **Sıra** | **Ülke** | **Sürdürülebilirlik Skoru** | **Öne Çıkan Özellik** |
|:--------:|:---------|:---------------------------|:----------------------|
| **🥇** | **Çin** | **86.7** | Düşük kişi başı israf |
| **🥈** | **Rusya** | **86.2** | Verimli gıda yönetimi |
| **🥉** | **ABD** | **85.2** | Gelişmiş teknoloji |

</div>

### 🗑️ **En Yüksek İsraf Yapan Ülkeler**

| **Sıra** | **Ülke** | **Toplam İsraf (Milyon Ton)** | **Ana Neden** |
|:--------:|:---------|:-----------------------------|:-------------|
| **1** | **Türkiye** | **6.9M** | Ev tipi israf |
| **2** | **Kanada** | **6.8M** | Tedarik zinciri |
| **3** | **İspanya** | **6.8M** | Perakende israfı |

### 🍎 **Gıda Kategorilerine Göre İsraf**

| **Kategori** | **Toplam İsraf (Milyon Ton)** | **Pay (%)** | **Ana Sorun** |
|:-------------|:-----------------------------|:------------|:-------------|
| **Prepared Food** | **17.9M** | **35.8%** | Son kullanma tarihi |
| **Fruits & Vegetables** | **15.2M** | **30.4%** | Depolama sorunları |
| **Dairy Products** | **8.5M** | **17.0%** | Soğuk zincir |
| **Meat & Fish** | **4.8M** | **9.6%** | Hijyen standartları |
| **Grains & Cereals** | **3.8M** | **7.6%** | En düşük israf |

### 🦠 **Pandemi Etkisi Analizi**

#### **Genel Etki**
- **Genel İsraf:** %1 azalma
- **Ekonomik Kayıp:** %2 artış
- **Karbon Ayak İzi:** %1.5 azalma

#### **Kategori Bazında Değişim**
| **Kategori** | **Pandemi Etkisi** | **Neden** |
|:-------------|:------------------|:----------|
| **Beverages** | **%6.5 artış** | Evde tüketim artışı |
| **Dairy Products** | **%10.3 azalış** | Restoran kapanışları |
| **Prepared Food** | **%3.2 azalış** | Dışarıda yeme azalışı |

#### **Ülke Bazında Etki**
- **Gelişmiş Ülkeler:** %2-5 azalma (evde yeme artışı)
- **Gelişmekte Olan Ülkeler:** %1-3 artış (tedarik zinciri sorunları)

---

## 🧠 **SHAP ANALİZİ SONUÇLARI**

### 📊 **En Önemli Özellikler (İlk 5)**

#### **Total Waste (Tons) Hedefi**
| **Özellik** | **SHAP Önem Skoru** | **Etki** |
|:------------|:-------------------|:---------|
| **Category_Waste_Share** | **0.911** | 🟢 Çok Yüksek |
| **Population (Million)** | **0.020** | 🟡 Orta |
| **Category_Economic_Share** | **0.019** | 🟡 Orta |
| **Waste_Efficiency** | **0.013** | 🟡 Orta |
| **Waste_Per_Capita_kg** | **0.012** | 🟡 Orta |

#### **Economic Loss (Million $) Hedefi**
| **Özellik** | **SHAP Önem Skoru** | **Etki** |
|:------------|:-------------------|:---------|
| **Category_Economic_Share** | **0.919** | 🟢 Çok Yüksek |
| **Population (Million)** | **0.018** | 🟡 Orta |
| **Economic_Loss_Per_Capita_USD** | **0.015** | 🟡 Orta |
| **GDP_Per_Capita_Proxy** | **0.014** | 🟡 Orta |
| **Economic_Intensity** | **0.011** | 🟡 Orta |

#### **Carbon_Footprint_kgCO2e Hedefi**
| **Özellik** | **SHAP Önem Skoru** | **Etki** |
|:------------|:-------------------|:---------|
| **Category_Waste_Share** | **0.911** | 🟢 Çok Yüksek |
| **Population (Million)** | **0.020** | 🟡 Orta |
| **Category_Economic_Share** | **0.019** | 🟡 Orta |
| **Waste_Efficiency** | **0.013** | 🟡 Orta |
| **Waste_Per_Capita_kg** | **0.012** | 🟡 Orta |

### 🔍 **Pandemi Etkisi SHAP Analizi**
- **Pandemic_Indicator:** Tüm hedeflerde %15-20 etki
- **Year_Trend:** Zaman bazlı artış trendi
- **Seasonal_Features:** Mevsimsel değişimler

---

## 🖥️ **DASHBOARD MODÜLLERİ**

### 📊 **22 Premium Modül**

<div align="center">

| **Modül Kategorisi** | **Modül Sayısı** | **Ana Özellikler** |
|:---------------------|:-----------------|:-------------------|
| **🏠 Ana Modüller** | 5 | Veri analizi, model performansı |
| **🤖 AI Destekli** | 4 | Tahminler, öneriler, simülasyon |
| **📈 Analitik** | 6 | SHAP, A/B testing, ROI |
| **📄 Raporlama** | 4 | Rapor oluşturucu, model kartı |
| **⚙️ Yardımcı** | 3 | Ayarlar, yardım, hakkında |

</div>

### 🎯 **Modül Detayları ve Faydaları**

#### **🏠 Ana Modüller**
| **Modül** | **Amaç** | **Faydalar** | **Kullanıcı Yetenekleri** |
|:----------|:---------|:-------------|:-------------------------|
| **Ana Sayfa** | Genel bakış | Hızlı KPI erişimi | Dashboard navigasyonu |
| **Veri Analizi** | Veri keşfi | Detaylı analiz | Filtreleme ve görselleştirme |
| **Model Performansı** | Model değerlendirme | Performans takibi | Metrik karşılaştırması |
| **Gelecek Tahminleri** | Tahmin modelleme | Gelecek planlama | Senaryo analizi |
| **AI Insights** | Akıllı öneriler | Otomatik içgörüler | Öneri alma |

#### **🤖 AI Destekli Modüller**
| **Modül** | **Amaç** | **Faydalar** | **Kullanıcı Yetenekleri** |
|:----------|:---------|:-------------|:-------------------------|
| **Politika Simülatörü** | Politika testi | Risk değerlendirmesi | What-if analizi |
| **Hedef Planlayıcı** | Hedef belirleme | Stratejik planlama | Hedef optimizasyonu |
| **ROI Hesaplayıcı** | Yatırım analizi | Finansal değerlendirme | ROI hesaplama |
| **A/B Testing** | Model karşılaştırma | Performans optimizasyonu | Test sonuçları |

#### **📈 Analitik Modüller**
| **Modül** | **Amaç** | **Faydalar** | **Kullanıcı Yetenekleri** |
|:----------|:---------|:-------------|:-------------------------|
| **SHAP Analizi** | Model açıklanabilirliği | Şeffaflık | Özellik önem analizi |
| **Kategori Analizi** | Kategori bazlı analiz | Detaylı inceleme | Kategori karşılaştırması |
| **Ülke Karşılaştırması** | Ülke analizi | Benchmark | Ülke performansı |
| **Trend Analizi** | Zaman serisi | Trend takibi | Zaman bazlı analiz |
| **Korelasyon Matrisi** | İlişki analizi | Bağımlılık keşfi | Korelasyon inceleme |
| **Veri Kalitesi** | Veri değerlendirme | Kalite kontrol | Veri doğrulama |

#### **📄 Raporlama Modülleri**
| **Modül** | **Amaç** | **Faydalar** | **Kullanıcı Yetenekleri** |
|:----------|:---------|:-------------|:-------------------------|
| **Rapor Oluşturucu** | Otomatik rapor | Zaman tasarrufu | Rapor indirme |
| **Model Kartı** | Model dokümantasyonu | Şeffaflık | Model detayları |
| **Performans Raporu** | Detaylı analiz | Kapsamlı değerlendirme | Performans takibi |
| **Veri Raporu** | Veri özeti | Hızlı bakış | Veri anlayışı |

### 🤖 **AI Assistant Sistemi**
- **Otomatik Akıllı Öneriler:** Model performansına göre öneriler
- **Gerçek Zamanlı İçgörüler:** Anlık analiz ve tavsiyeler
- **Kişiselleştirilmiş Öneriler:** Kullanıcı ihtiyaçlarına göre özelleştirme

---

## 🎯 **SONUÇLAR VE ÖNERİLER**

### 🏆 **Kritik Çıkarımlar**

#### **1. Model Performansı**
- **%96.0 Test R²:** Mükemmel tahmin gücü
- **%0.8 Overfitting Gap:** Çok iyi genelleme
- **%95.8 CV R²:** Stabil performans

#### **2. Veri Kalitesi**
- **5000+ gözlem:** Kapsamlı veri seti
- **37 değişken:** Zengin özellik seti
- **20 ülke:** Küresel kapsam

#### **3. İş Değeri**
- **22 modül:** Kapsamlı platform
- **AI destekli:** Akıllı öneriler
- **Gerçek zamanlı:** Anlık analiz

### 💡 **Aksiyon Önerileri**

#### **🏛️ Politika Yapıcılar İçin**
- **Hedefli Politikalar:** Kategori bazlı stratejiler
- **Ülke Spesifik:** Bölgesel çözümler
- **Teknoloji Yatırımı:** IoT ve blockchain

#### **🏢 İş Dünyası İçin**
- **Tedarik Zinciri:** Optimizasyon
- **Müşteri Eğitimi:** Farkındalık artırma
- **Teknoloji Adopsiyonu:** Akıllı sistemler

#### **🏫 Eğitim Kurumları İçin**
- **Müfredat Güncelleme:** Sürdürülebilirlik odaklı
- **Araştırma Desteği:** Veri odaklı çalışmalar
- **Farkındalık Programları:** Öğrenci eğitimi

#### **🌍 Sivil Toplum İçin**
- **Farkındalık Kampanyaları:** Toplumsal bilinç
- **Gönüllülük Programları:** Aktif katılım
- **İzleme Sistemleri:** Şeffaflık

---

## 🚀 **GELECEK GELİŞTİRME ÖNERİLERİ**

### 📱 **Faz 2: Model İyileştirmeleri**
- **Deep Learning Modelleri:** LSTM, Transformer
- **Real-time API'ler:** Otomatik güncelleme
- **AutoML:** Otomatik model seçimi
- **Ensemble Methods:** Çoklu model birleştirme

### 📱 **Faz 3: Dashboard Geliştirmeleri**
- **Mobile App:** React Native
- **Multi-language:** 5 dil desteği
- **Push Notifications:** Anlık bildirimler
- **Offline Mode:** Çevrimdışı çalışma

### 🌐 **Faz 4: Veri Genişletme**
- **IoT Sensörler:** Gerçek zamanlı veri
- **Blockchain:** Şeffaf tedarik zinciri
- **50+ Ülke:** Genişletilmiş kapsam
- **Satellite Data:** Uzaktan algılama

### 💼 **Faz 5: İş Modeli Geliştirme**
- **SaaS Platformu:** Abonelik modeli
- **Kurumsal Entegrasyonlar:** API servisleri
- **Politika Danışmanlığı:** Uzman hizmetleri
- **Eğitim Programları:** Sertifika kursları

---

## 🔗 **CANLI DASHBOARD ERİŞİMİ**

<div align="center">

### 🌐 **[Ecolense Intelligence Dashboard](https://ecolense-intelligence.streamlit.app/)**

[![Streamlit](https://img.shields.io/badge/Streamlit-Cloud-blue?style=for-the-badge&logo=streamlit)](https://ecolense-intelligence.streamlit.app/)
[![Status](https://img.shields.io/badge/Status-Live-brightgreen?style=for-the-badge)](https://ecolense-intelligence.streamlit.app/)

</div>

---

## 🎯 **DASHBOARD ÖZELLİKLERİ**

### ✨ **Temel Özellikler**
- **🔄 Gerçek Zamanlı Güncelleme:** Anlık veri yenileme
- **📱 Responsive Tasarım:** Tüm cihazlarda uyumlu
- **🎨 Modern UI/UX:** Kullanıcı dostu arayüz
- **⚡ Hızlı Performans:** Optimize edilmiş kod

### 🤖 **AI Destekli Özellikler**
- **🧠 Akıllı Öneriler:** Model tabanlı tavsiyeler
- **🔮 Gelecek Tahminleri:** Makine öğrenmesi ile tahmin
- **📊 Otomatik Analiz:** Anlık içgörü üretimi
- **🎯 Kişiselleştirme:** Kullanıcı tercihlerine göre

### 📈 **Analitik Özellikler**
- **📊 İnteraktif Grafikler:** Plotly tabanlı görselleştirme
- **🔍 Detaylı Filtreleme:** Çoklu kriter seçimi
- **📋 Kapsamlı Raporlar:** PDF/Excel export
- **🔄 Karşılaştırmalı Analiz:** Çoklu veri karşılaştırması

---

## 👥 **PROJE EKİBİ**

<div align="center">

| **Üye** | **Rol** | **Katkı** |
|:--------|:--------|:----------|
| **Özge Güneş** | Data Scientist | Model geliştirme, analiz |
| **Kübra Saruhan** | Takım Arkadaşı | Veri analizi, dokümantasyon |

</div>

### 🎓 **Proje Bilgileri**
- **Kurum:** Miuul Data Scientist Bootcamp
- **Proje Türü:** Final Projesi
- **Dönem:** 2025
- **Teknoloji:** Python, Streamlit, Scikit-learn

---

## 📚 **REFERANSLAR**

### 📖 **Akademik Kaynaklar**
- **FAO (2021):** "The State of Food and Agriculture"
- **UNEP (2021):** "Food Waste Index Report"
- **World Bank (2022):** "Food Loss and Waste Database"
- **OECD (2023):** "Material Resources, Productivity and the Environment"

### 🌐 **Teknik Kaynaklar**
- **Scikit-learn Documentation:** Model seçimi ve optimizasyon
- **Streamlit Documentation:** Dashboard geliştirme
- **SHAP Documentation:** Model açıklanabilirliği
- **Plotly Documentation:** İnteraktif görselleştirme

---

<div align="center">

### 🌱 **Sürdürülebilir bir gelecek için veri odaklı çözümler**

[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/ozgunes91/ecolense-intelligence)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

</div> 