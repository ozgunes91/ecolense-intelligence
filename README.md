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
| **Global Food Wastage** | 8 | 5000 | 2018-2024 | Kaggle |
| **Material Footprint** | 32 | 197 | 1990-2021 | Kaggle |
| **Birleştirilmiş Veri** | 37 | 5000 | 2018-2024 | Inner Join |

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

#### **📊 Eksik Veri Analizi ve Doldurma**
| **Veri Türü** | **Eksik Sayı** | **Doldurma Metodu** | **Neden** |
|:--------------|:---------------|:-------------------|:----------|
| **Material Footprint** | 2514 gözlem | Median değer | Birleştirme sonrası eksik |
| **Continent/Hemisphere** | 20 ülke | Manuel atama | Coğrafi bilgi eksikliği |
| **Numeric Değerler** | Minimal | Median imputation | Veri tutarlılığı |

#### **🔧 Eksik Veri Doldurma Stratejisi**
```python
# Material Footprint eksik değerleri
footprint_median = merged_df['Material_Footprint_Per_Capita'].median()
merged_df['Material_Footprint_Per_Capita'].fillna(footprint_median, inplace=True)

# Manuel kıta ataması
country_continent_map = {
    'Turkey': 'Europe', 'USA': 'America', 'Germany': 'Europe',
    'France': 'Europe', 'UK': 'Europe', 'Italy': 'Europe',
    'Spain': 'Europe', 'Australia': 'Oceania', 'Indonesia': 'Asia',
    'India': 'Asia', 'China': 'Asia', 'South Africa': 'Africa',
    'Japan': 'Asia', 'Brazil': 'America', 'Canada': 'America',
    'Mexico': 'America', 'Russia': 'Europe', 'South Korea': 'Asia',
    'Saudi Arabia': 'Asia', 'Argentina': 'America'
}

# Numeric değerler için median
for col in numeric_cols:
    if merged_df[col].isnull().sum() > 0:
        median_val = merged_df[col].median()
        merged_df[col].fillna(median_val, inplace=True)
```

#### **📈 Diğer Veri Kalitesi İyileştirmeleri**
| **İşlem** | **Metod** | **Etki** |
|:----------|:----------|:---------|
| **Aykırı Değerler** | Winsorization (1%-99%) | %15 iyileştirme |
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

## **5. KÜRESEL SÜRDÜRÜLEBİLİRLİK ANALİZİ VE ÖNERİLER**

### **5.1 Küresel Çıkarımlar**

#### **5.1.1 Sosyal Sürdürülebilirlik Analizi**

Gıda israfı, küresel sosyal sürdürülebilirlik açısından kritik bir sorun teşkil etmektedir. FAO (2021) verilerine göre, dünyada üretilen gıdanın %33'ü israf edilmekte ve bu durum 1.3 milyar ton gıda kaybına neden olmaktadır. Analiz sonuçlarına göre, gelişmekte olan ülkelerde ev tipi israf daha yaygın görülürken, gelişmiş ülkelerde tedarik zinciri boyunca israf yaşanmaktadır. Bu durum, sosyal eşitsizlikleri artırmakta ve gıda güvenliğini tehdit etmektedir.

Eğitim ve bilinçlendirme programlarının bu sorunu çözmek için kritik önem taşıdığı tespit edilmiştir. Ayrıca, gıda israfının sağlık sistemleri üzerinde dolaylı etkileri bulunmakta ve bu durum toplumsal refahı olumsuz etkilemektedir.

#### **5.1.2 Ekonomik Sürdürülebilirlik Analizi**

Ekonomik açıdan, gıda israfı yıllık 1.2 trilyon USD ekonomik kayba neden olmaktadır. Bu miktar, dünya ekonomisinin önemli bir yükünü oluşturmaktadır. Yapılan analizler, tedarik zinciri optimizasyonu ile %15-20 oranında tasarruf sağlanabileceğini göstermektedir. Sürdürülebilir gıda sistemlerine yapılan yatırımların %25-30 oranında getiri sağladığı tespit edilmiştir.

Gıda fiyatlarındaki artış ve arz-talep dengesizliği, ekonomik istikrarı tehdit etmekte ve piyasa dengesizliklerine neden olmaktadır. Bu durum, özellikle gelişmekte olan ülkelerde ekonomik kırılganlığı artırmaktadır.

#### **5.1.3 Çevresel Sürdürülebilirlik Analizi**

Çevresel açıdan, gıda israfı küresel sera gazı emisyonlarının %8-10'unu oluşturmaktadır. Bu oran, iklim değişikliğinin ana nedenlerinden biri olarak kabul edilmektedir. İsraf edilen gıda için her yıl 250 km³ su kullanılmakta ve 1.4 milyar hektar tarım arazisi sadece israf edilecek gıda üretimi için kullanılmaktadır.

Bu durum, biyoçeşitliliği azaltmakta ve ekosistem üzerinde büyük baskı yaratmaktadır. Ayrıca, su kaynaklarının tükenmesi ve toprak bozulması gibi çevresel sorunlara da neden olmaktadır.

### **5.2 2030 Küresel Hedefleri ve Stratejiler**

#### **5.2.1 Sosyal Hedefler ve Stratejiler**

2030 yılına kadar gıda israfını %50 azaltma hedefi belirlenmiştir. Bu hedef, Birleşmiş Milletler'in Sürdürülebilir Kalkınma Hedefi 12.3 ile uyumlu olarak planlanmıştır. Ayrıca, 2 milyar insanın gıda güvenliğini sağlama ve 1 milyar kişiye sürdürülebilir gıda eğitimi verme hedefleri belirlenmiştir. Gıda erişimindeki eşitsizlikleri azaltarak sosyal adaleti güçlendirme stratejisi benimsenmiştir.

#### **5.2.2 Ekonomik Hedefler ve Stratejiler**

Ekonomik kayıpları azaltarak 600 milyar USD tasarruf sağlama hedefi belirlenmiştir. Sürdürülebilir gıda sektöründe 10 milyon yeni iş yaratma ve tedarik zinciri verimliliğini %30 artırma planları hazırlanmıştır. 500 milyar USD sürdürülebilir gıda yatırımı çekme stratejisi geliştirilmiştir.

#### **5.2.3 Çevresel Hedefler ve Stratejiler**

Gıda sektöründen 2.5 gigaton CO2 emisyonu azaltma hedefi belirlenmiştir. 125 km³ su tasarrufu sağlayarak su kaynaklarını koruma planı hazırlanmıştır. 700 milyon hektar arazi tasarrufu ile doğal alanları koruma ve %80 geri dönüşüm oranı ile döngüsel ekonomiye geçme stratejileri benimsenmiştir.

### **5.3 Paydaş Bazlı Aksiyon Önerileri**

#### **5.3.1 Politika Yapıcılar İçin Öneriler**

Politika yapıcılar için kategori bazlı stratejiler geliştirilmesi önerilmektedir. Ülke spesifik bölgesel çözümler ve teknoloji yatırımları (IoT ve blockchain) desteklenmelidir. Gıda israfı yasaları ve standartları oluşturulmalı, sürdürülebilir gıda üretimi için teşvik programları geliştirilmelidir.

#### **5.3.2 İş Dünyası İçin Öneriler**

İş dünyası için tedarik zinciri optimizasyonu ve müşteri eğitimi programları önerilmektedir. Teknoloji adopsiyonu ve akıllı sistemler entegrasyonu desteklenmelidir. Sürdürülebilir iş modeli ve döngüsel ekonomi yaklaşımı benimsenmelidir. Gıda bankaları ve bağış programları gibi sosyal sorumluluk projeleri geliştirilmelidir.

#### **5.3.3 Eğitim Kurumları İçin Öneriler**

Eğitim kurumları için sürdürülebilirlik odaklı müfredat güncellemeleri önerilmektedir. Veri odaklı araştırma çalışmaları ve öğrenci farkındalık programları geliştirilmelidir. Uygulamalı projeler ve gıda israfı önleme kampanyaları düzenlenmelidir. Uluslararası işbirlikleri ve küresel araştırma ağları kurulmalıdır.

#### **5.3.4 Sivil Toplum İçin Öneriler**

Sivil toplum için toplumsal bilinç artırıcı farkındalık kampanyaları önerilmektedir. Gönüllülük programları ve aktif katılım teşvik edilmelidir. İzleme sistemleri ve şeffaflık mekanizmaları geliştirilmelidir. Yerel gıda kurtarma programları ve dijital farkındalık kampanyaları düzenlenmelidir.

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
| **Kübra Saruhan** | Data Scientist | Veri analizi, dokümantasyon |

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
