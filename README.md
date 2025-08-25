# 🌱 **ECOLENSE INTELLIGENCE**
### *Premium Küresel Gıda Atığı Analizi ve Sürdürülebilir Çözümler Platformu*

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3+-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](https://ecolense-intelligence.streamlit.app/)

---

## 📊 **PROJE ÖZETİ**

<div align="center">

| 🎯 **Amaç** | 📈 **Kapsam** | 🤖 **Teknoloji** | 📊 **Performans** |
|:-------------:|:-------------:|:----------------:|:-----------------:|
| Küresel gıda atığı analizi | 20 ülke, 8 kategori | Gradient Boosting | %96.0 Test R² |
| Sürdürülebilirlik skorlama | 5000+ gözlem | SHAP Analizi | %0.8 Aşırı öğrenme |
| Politika önerileri | 37 değişken | Model Karşılaştırma | 22 Modül |

</div>

---

## 🌍 **PROBLEM TANIMI**

### 📈 **Küresel Gıda Atığı Krizi**

> **FAO Raporu (2021):** Dünya çapında üretilen gıdanın **%33'ü** israf ediliyor
> 
> **UNEP Çalışması:** Gıda atığı küresel sera gazı emisyonlarının **%8-10'unu** oluşturuyor
> 
> **Dünya Bankası Analizi:** Gelişmekte olan ülkelerde hane halkı atığı, gelişmiş ülkelerde tedarik zinciri atığı
> 
> **OECD Araştırması:** Kişi başı atık oranları ülke gelişim seviyesi ile ters orantılı

### 🎯 **Çözüm Yaklaşımımız**
- **Makine Öğrenmesi** ile proaktif analiz
- **AI Destekli** politika önerileri
- **Gerçek Zamanlı** dashboard platformu
- **Sürdürülebilirlik** odaklı çözümler

---

## 📚 **LİTERATÜR TARAMASI VE ARAŞTIRMA**

### 🔬 **Mevcut Çözümler ve Boşluklar**

| **Araştırma Alanı** | **Mevcut Durum** | **Boşluklar** | **Katkımız** |
|:-------------------|:-----------------|:----------------|:-------------------|
| **Veri Analizi** | Statik raporlar | Gerçek zamanlı analiz yok | Dinamik dashboard |
| **Modelleme** | Basit regresyon | Çoklu hedef yok | Gradient Boosting |
| **Görselleştirme** | Temel grafikler | Etkileşim yok | Plotly + Streamlit |
| **Öneriler** | Genel tavsiyeler | Kişiselleştirme yok | AI Asistan |

### 📖 **Referans Kaynakları**
- **FAO (Gıda ve Tarım Örgütü)** - Gıda güvenliği raporları
- **OECD (Ekonomik İşbirliği ve Kalkınma Örgütü)** - Ekonomik analizler
- **Dünya Bankası** - Kalkınma göstergeleri
- **BM Çevre Programı** - Çevresel etki değerlendirmeleri
- **Avrupa Çevre Ajansı** - Sürdürülebilirlik metrikleri

---

## 📊 **VERİ SETİ VE METODOLOJİ**

### 🗂️ **Veri Kaynakları**

<div align="center">

| **Veri Seti** | **Değişkenler** | **Gözlemler** | **Dönem** | **Kaynak** |
|:-------------:|:-------------------:|:-----------------:|:---------:|:----------:|
| **Küresel Gıda Atığı** | 8 | 5000 | 2018-2024 | Kaggle |
| **Materyal Ayak İzi** | 32 | 197 | 1990-2021 | Kaggle |
| **Birleştirilmiş Veri** | 37 | 5000 | 2018-2024 | Inner Join |

</div>

**📝 Veri Seti Notu:** Bu veri seti gerçek dünya verilerinin küçük ölçekli bir örneğidir. Toplam atık miktarı (125 milyon ton) gerçek dünya değerlerinin (1.3 milyar ton/yıl) çok küçük bir kısmını temsil eder. Bu nedenle, kişi başı değerler ve sürdürülebilirlik skorları bu veri seti için özel olarak hesaplanmıştır.

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
| **📊 Kişi Başı Metrikler** | Kişi başı hesaplamalar | 6 | `Waste_Per_Capita_kg` |
| **⏰ Zamansal Özellikler** | Zaman tabanlı değişkenler | 8 | `Pandemic_Indicator` |
| **🌍 Coğrafi Özellikler** | Kıta, yarıküre | 4 | `Continent`, `Hemisphere` |
| **📈 Türetilmiş Özellikler** | Verimlilik, yoğunluk | 6 | `Waste_Efficiency` |
| **🔄 Etkileşim Özellikleri** | Çapraz hesaplamalar | 3 | `Population_Material_Interaction` |
| **📊 Zaman Tabanlı Trendler** | Kayan ortalama | 2 | `Waste_Trend_3Y` |

#### **3. Sürdürülebilirlik Skoru Hesaplaması**
```python
def calculate_sustainability_score(row):
    # Gerçek dünya eşikleri (veri seti için ayarlandı)
    waste_threshold = 150  # kg/kişi/yıl (veri seti ortalaması: 109.5)
    economic_threshold = 40  # USD/kişi/yıl (veri seti ortalaması: 35.4)
    carbon_threshold = 0.5  # kg CO2e/kişi/yıl (veri seti ortalamasına dayalı)
    
    waste_score = max(0, 1 - (row['Waste_Per_Capita_kg'] / waste_threshold))
    economic_score = max(0, 1 - (row['Economic_Loss_Per_Capita_USD'] / economic_threshold))
    carbon_score = max(0, 1 - (row['Carbon_Per_Capita_kgCO2e'] / carbon_threshold))
    
    sustainability = (waste_score * 0.4 + economic_score * 0.3 + carbon_score * 0.3) * 100
    return max(0, min(100, sustainability))
```

### 🛠️ **Veri Kalitesi İyileştirmeleri**

#### **📊 Eksik Veri Analizi ve Doldurma**
| **Veri Türü** | **Eksik Sayı** | **Doldurma Yöntemi** | **Neden** |
|:--------------|:---------------|:-------------------|:----------|
| **Materyal Ayak İzi** | 2514 gözlem | Medyan değer | Birleştirme sonrası eksik |
| **Kıta/Yarıküre** | 20 ülke | Manuel atama | Coğrafi bilgi eksik |
| **Sayısal Değerler** | Minimal | Medyan doldurma | Veri tutarlılığı |

#### **🔧 Eksik Veri Doldurma Stratejisi**
```python
# Materyal Ayak İzi eksik değerleri
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

# Sayısal değerler için medyan
for col in numeric_cols:
    if merged_df[col].isnull().sum() > 0:
        median_val = merged_df[col].median()
        merged_df[col].fillna(median_val, inplace=True)
```

#### **📈 Diğer Veri Kalitesi İyileştirmeleri**
| **Süreç** | **Yöntem** | **Etki** |
|:----------|:----------|:---------|
| **Aykırı Değerler** | Winsorization (%1-%99) | %15 iyileştirme |
| **Kategorik Kodlama** | Label Encoding | Standardizasyon |
| **Ölçeklendirme** | StandardScaler | Model performansı |

---

## 🤖 **MAKİNE ÖĞRENMESİ MODELLERİ**

### 🎯 **Model Seçimi ve Performansı (02_model_egitimi.py'dan)**

#### **🏆 Ana Model: Gradient Boosting Regressor**
- **Algoritma:** Gradient Boosting
- **Hiperparametreler:** n_estimators=100, max_depth=4, learning_rate=0.05
- **Seçim Kriterleri:** Model Karşılaştırma Kazananı + CV R² + Aşırı Öğrenme Kontrolü

#### **🔄 Alternatif Modeller**
- **Random Forest:** Muhafazakar yaklaşım
- **Linear Regression:** Temel model
- **Ridge Regression:** Regularizasyon
- **Lasso Regression:** Özellik seçimi

#### **🎯 Çoklu Hedef Yaklaşımı**
- **Total Waste (Tons)**
- **Economic Loss (Million $)**
- **Carbon_Footprint_kgCO2e**

### 📊 **Model Performans Metrikleri**

<div align="center">

| **Metrik** | **Değer** | **Durum** |
|:-----------|:----------|:----------|
| **Test R² Skoru** | **%96.0** | 🟢 Mükemmel |
| **Çapraz Doğrulama R²** | **%95.8** | 🟢 Mükemmel |
| **Aşırı Öğrenme Farkı** | **%0.8** | 🟢 Çok İyi |
| **MAPE** | **%10.2** | 🟡 İyi |

</div>

### ✅ **Model Doğrulama**

| **Yöntem** | **Detaylar** | **Sonuç** |
|:-----------|:----------|:----------|
| **Train-Test Split** | %80/%20 | ✅ Geçerli |
| **Çapraz Doğrulama** | 3 katlı CV | ✅ Kararlı |
| **Model Karşılaştırma** | 27 kombinasyon | ✅ Optimize |
| **SHAP Analizi** | Model açıklanabilirliği | ✅ Şeffaf |

---

## 🧪 **MODEL KARŞILAŞTIRMA SONUÇLARI (03_model_karsilastirma_analizi.py'dan)**

### 📈 **Test Kapsamı**

| **Test Grubu** | **Kombinasyon** | **Sonuç** |
|:---------------|:----------------|:----------|
| **Model Türleri** | 3 farklı model | Gradient Boosting kazandı |
| **Özellik Grupları** | 6 farklı grup | Core + Efficiency en iyi |
| **Toplam Test** | 27 kombinasyon | %96.0 başarı |

### 🏆 **En İyi Performans Gösteren Kombinasyonlar**

| **Hedef** | **Model** | **Özellik Grubu** | **Test R²** | **Aşırı Öğrenme** |
|:----------|:----------|:------------------|:------------|:----------------|
| **Total Waste** | Gradient Boosting | Core + Efficiency | 0.960 | 0.008 |
| **Economic Loss** | Gradient Boosting | Core + Trends | 0.955 | 0.012 |
| **Carbon Footprint** | Gradient Boosting | Core + Efficiency | 0.960 | 0.008 |

---

## 🔍 **KRİTİK BULGULAR VE İÇGÖRÜLER**

### 🏆 **Sürdürülebilirlik Liderleri**

<div align="center">

| **Sıra** | **Ülke** | **Sürdürülebilirlik Skoru** | **Ana Özellik** |
|:--------:|:---------|:---------------------------|:----------------------|
| **🥇** | **UK** | **45.59** | Dengeli atık yönetimi |
| **🥈** | **Spain** | **44.30** | Verimli gıda yönetimi |
| **🥉** | **Russia** | **43.70** | Orta sürdürülebilirlik seviyesi |

</div>

### 🗑️ **En Düşük Sürdürülebilirlik Skoruna Sahip Ülkeler**

| **Sıra** | **Ülke** | **Sürdürülebilirlik Skoru** | **Ana Sorun** |
|:--------:|:---------|:---------------------------|:-------------|
| **1** | **Saudi Arabia** | **40.9** | Yüksek kişi başı atık |
| **2** | **France** | **41.0** | Verimsiz gıda yönetimi |
| **3** | **Italy** | **41.5** | Orta sürdürülebilirlik seviyesi |

### 🍎 **Kategoriye Göre Gıda Atığı (Veri Seti)**

| **Kategori** | **Toplam Atık (Milyon Ton)** | **Pay (%)** | **Ana Sorun** |
|:-------------|:-----------------------------|:------------|:-------------|
| **Prepared Food** | **17.9M** | **14.3%** | Son kullanma tarihi |
| **Beverages** | **16.4M** | **13.1%** | Ambalaj sorunları |
| **Bakery Items** | **15.6M** | **12.4%** | Taze ürün atığı |
| **Fruits & Vegetables** | **15.5M** | **12.4%** | Depolama sorunları |
| **Meat & Seafood** | **15.4M** | **12.3%** | Hijyen standartları |
| **Dairy Products** | **15.3M** | **12.2%** | Soğuk zincir |
| **Frozen Food** | **15.0M** | **12.0%** | Dondurma/çözme döngüsü |
| **Grains & Cereals** | **14.2M** | **11.3%** | En düşük atık |

### 🦠 **Pandemi Etki Analizi**

#### **Genel Etki**
- **Genel Atık:** Pandemi yılları (2020-2022) veri setinde mevcut
- **Ekonomik Kayıp:** Pandemi etkileri analiz edilebilir
- **Karbon Ayak İzi:** Pandemi dönemindeki değişiklikler gözlemlenebilir

#### **Veri Seti Kapsamı**
| **Dönem** | **Yıl Aralığı** | **Veri Mevcudiyeti** |
|:----------|:----------------|:---------------------|
| **Pandemi Öncesi** | 2018-2019 | ✅ Mevcut |
| **Pandemi Dönemi** | 2020-2022 | ✅ Mevcut |
| **Pandemi Sonrası** | 2023-2024 | ✅ Mevcut |

#### **Analiz Notu**
- Pandemi etki analizi dashboard'daki "Veri Analizi" sayfası kullanılarak yapılabilir
- Zaman serisi analizi trend değişikliklerini gözlemleyebilir

---

## 🧠 **SHAP ANALİZ SONUÇLARI**

### 📊 **En Önemli Özellikler (İlk 5)**

#### **Total Waste (Tons) Hedefi (SHAP Analizi)**
| **Özellik** | **SHAP Önem Skoru** | **Etki** |
|:------------|:-------------------|:---------|
| **Category_Waste_Share** | **%62.6** | 🟢 Çok Yüksek |
| **Population (Million)** | **%10.4** | 🟢 Yüksek |
| **Waste_Efficiency** | **%8.8** | 🟡 Orta |
| **Carbon_Per_Capita_kgCO2e** | **%7.2** | 🟡 Orta |
| **Waste_Trend** | **%2.3** | 🟡 Düşük |

#### **Economic Loss (Million $) Hedefi (SHAP Analizi)**
| **Özellik** | **SHAP Önem Skoru** | **Etki** |
|:------------|:-------------------|:---------|
| **Category_Economic_Share** | **%62.4** | 🟢 Çok Yüksek |
| **Population (Million)** | **%10.2** | 🟢 Yüksek |
| **Economic_Loss_Per_Capita_USD** | **%7.7** | 🟡 Orta |
| **GDP_Per_Capita_Proxy** | **%7.4** | 🟡 Orta |
| **Economic_Intensity** | **%2.6** | 🟡 Düşük |

#### **Carbon_Footprint_kgCO2e Hedefi (SHAP Analizi)**
| **Özellik** | **SHAP Önem Skoru** | **Etki** |
|:------------|:-------------------|:---------|
| **Category_Waste_Share** | **%62.6** | 🟢 Çok Yüksek |
| **Population (Million)** | **%10.4** | 🟢 Yüksek |
| **Waste_Efficiency** | **%8.7** | 🟡 Orta |
| **Carbon_Per_Capita_kgCO2e** | **%7.3** | 🟡 Orta |
| **Waste_Trend** | **%2.3** | 🟡 Düşük |

### 🔍 **Pandemi Etki Analizi**
- **Is_Pandemic_Year:** %0.2 etki (SHAP analizinde tespit edildi)
- **Year_Trend:** Zaman tabanlı artış trendi
- **Is_Post_Pandemic:** %0.02 etki (SHAP analizinde tespit edildi)
- **Pandemi etkisi tüm hedeflerde benzer düzeyde (%0.1-0.3 arası)**

---

## 🖥️ **DASHBOARD MODÜLLERİ**

### 📊 **22 Premium Modül**

<div align="center">

| **Modül Kategorisi** | **Modül Sayısı** | **Ana Özellikler** |
|:---------------------|:-----------------|:-------------------|
| **🏠 Temel Modüller** | 5 | Veri analizi, model performansı |
| **🤖 AI Destekli** | 4 | Tahminler, öneriler, simülasyon |
| **📈 Analitik** | 6 | SHAP, Model karşılaştırma, ROI |
| **📄 Raporlama** | 4 | Rapor oluşturucu, model kartı |
| **⚙️ Yardımcı** | 3 | Ayarlar, yardım, hakkında |

</div>

### 🎯 **Modül Detayları ve Faydaları**

#### **🏠 Temel Modüller**
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
| **Model Karşılaştırma** | Model karşılaştırma | Performans optimizasyonu | Test sonuçları |

#### **📈 Analitik Modüller**
| **Modül** | **Amaç** | **Faydalar** | **Kullanıcı Yetenekleri** |
|:----------|:---------|:-------------|:-------------------------|
| **SHAP Analizi** | Model açıklanabilirliği | Şeffaflık | Özellik önem analizi |
| **Kategori Analizi** | Kategori tabanlı analiz | Detaylı inceleme | Kategori karşılaştırması |
| **Ülke Karşılaştırması** | Ülke analizi | Benchmarking | Ülke performansı |
| **Trend Analizi** | Zaman serisi | Trend takibi | Zaman tabanlı analiz |
| **Korelasyon Matrisi** | İlişki analizi | Bağımlılık keşfi | Korelasyon incelemesi |
| **Veri Kalitesi** | Veri değerlendirme | Kalite kontrolü | Veri doğrulama |

#### **📄 Raporlama Modülleri**
| **Modül** | **Amaç** | **Faydalar** | **Kullanıcı Yetenekleri** |
|:----------|:---------|:-------------|:-------------------------|
| **Rapor Oluşturucu** | Otomatik raporlama | Zaman tasarrufu | Rapor indirme |
| **Model Kartı** | Model dokümantasyonu | Şeffaflık | Model detayları |
| **Performans Raporu** | Detaylı analiz | Kapsamlı değerlendirme | Performans takibi |
| **Veri Raporu** | Veri özeti | Hızlı bakış | Veri anlama |

### 🤖 **AI Asistan Sistemi**
- **Otomatik Akıllı Öneriler:** Model performansına dayalı öneriler
- **Gerçek Zamanlı İçgörüler:** Anında analiz ve tavsiye
- **Kişiselleştirilmiş Öneriler:** Kullanıcı ihtiyaçlarına göre özelleştirme

---

## 🎯 **SONUÇLAR VE ÖNERİLER**

### 🏆 **Kritik İçgörüler**

#### **1. Model Performansı**
- **%96.0 Test R²:** Mükemmel tahmin gücü
- **%0.8 Aşırı Öğrenme Farkı:** Çok iyi genelleme
- **%95.8 CV R²:** Kararlı performans

#### **2. Veri Kalitesi**
- **5000+ gözlem:** Kapsamlı veri seti
- **37 değişken:** Zengin özellik seti
- **20 ülke:** Küresel kapsam

#### **3. İş Değeri**
- **22 modül:** Kapsamlı platform
- **AI destekli:** Akıllı öneriler
- **Gerçek zamanlı:** Anında analiz

### 💡 **Küresel Sürdürülebilirlik İçgörüleri ve Aksiyon Önerileri**

#### **🌍 Küresel İçgörüler**

##### **📊 Sosyal Sürdürülebilirlik**
Dünya çapında üretilen gıdanın üçte biri israf ediliyor ve bu 1.3 milyar ton gıda kaybına neden oluyor. Gelişmekte olan ülkelerde hane halkı atığı daha yaygınken, gelişmiş ülkelerde tedarik zinciri boyunca atık oluşuyor. Bu durum sosyal eşitsizlikleri artırıyor ve gıda güvenliğini tehdit ediyor. Bu sorunu çözmek için eğitim ve farkındalık programları kritik öneme sahip. Ayrıca, gıda atığının sağlık sistemleri üzerinde dolaylı etkileri bulunuyor.

##### **💰 Ekonomik Sürdürülebilirlik**
Gıda atığı yıllık 1.2 trilyon USD ekonomik kayba neden oluyor. Bu, dünya ekonomisi için önemli bir yük. Tedarik zinciri optimizasyonu ile %15-20 tasarruf sağlanabilir. Sürdürülebilir gıda sistemlerine yapılan yatırımlar %25-30 yatırım getirisi sağlıyor. Artan gıda fiyatları ve arz-talep dengesizliği de ekonomik istikrarı tehdit ediyor.

##### **🌱 Çevresel Sürdürülebilirlik**
Gıda atığı küresel sera gazı emisyonlarının %8-10'unu oluşturuyor. Bu, iklim değişikliğinin ana nedenlerinden biri. İsraf edilen gıda için yıllık 250 km³ su kullanılıyor. 1.4 milyar hektar tarım arazisi sadece israf edilecek gıda üretimi için kullanılıyor. Bu durum biyolojik çeşitliliği azaltıyor ve ekosistemler üzerinde büyük baskı yaratıyor.

#### **🎯 Küresel Hedefler (2030)**

##### **📈 Sosyal Hedefler**
2030 yılına kadar gıda atığını %50 azaltmayı hedefliyoruz. Bu, Birleşmiş Milletler Sürdürülebilir Kalkınma Hedefi 12.3 ile uyumlu. 2 milyar insan için gıda güvenliği sağlamayı ve 1 milyar insana sürdürülebilir gıda eğitimi vermeyi planlıyoruz. Gıda erişimindeki eşitsizlikleri azaltarak sosyal adaleti güçlendirmeyi hedefliyoruz.

##### **💼 Ekonomik Hedefler**
Ekonomik kayıpları azaltarak 600 milyar USD tasarruf etmeyi hedefliyoruz. Sürdürülebilir gıda sektöründe 10 milyon yeni iş yaratmayı ve tedarik zinciri verimliliğini %30 artırmayı planlıyoruz. Sürdürülebilir gıda yatırımında 500 milyar USD çekmeyi hedefliyoruz.

##### **🌿 Çevresel Hedefler**
Gıda sektöründen 2.5 gigaton CO2 emisyonu azaltmayı hedefliyoruz. Su kaynaklarını korumak için 125 km³ su tasarruf etmeyi planlıyoruz. Doğal alanları korumak için 700 milyon hektar arazi tasarruf etmeyi ve %80 geri dönüşüm oranı ile döngüsel ekonomiye geçmeyi hedefliyoruz.

#### **🏛️ Politika Yapıcılar İçin**
- **Hedefli Politikalar:** Kategori tabanlı stratejiler
- **Ülkeye Özel:** Bölgesel çözümler
- **Teknoloji Yatırımı:** IoT ve blockchain
- **Düzenleme:** Gıda atığı yasaları ve standartları
- **Teşvik Programları:** Sürdürülebilir gıda üretimi desteği

#### **🏢 İşletmeler İçin**
- **Tedarik Zinciri:** Optimizasyon
- **Müşteri Eğitimi:** Farkındalık artırma
- **Teknoloji Benimseme:** Akıllı sistemler
- **Sürdürülebilir İş Modeli:** Döngüsel ekonomi yaklaşımı
- **Sosyal Sorumluluk:** Gıda bankaları ve bağış programları

#### **🏫 Eğitim Kurumları İçin**
- **Müfredat Güncelleme:** Sürdürülebilirlik odaklı
- **Araştırma Desteği:** Veri odaklı çalışmalar
- **Farkındalık Programları:** Öğrenci eğitimi
- **Uygulamalı Projeler:** Gıda atığı önleme kampanyaları
- **Uluslararası İşbirlikleri:** Küresel araştırma ağları

#### **🌍 Sivil Toplum İçin**
- **Farkındalık Kampanyaları:** Sosyal bilinç
- **Gönüllü Programları:** Aktif katılım
- **İzleme Sistemleri:** Şeffaflık
- **Topluluk Girişimleri:** Yerel gıda kurtarma programları
- **Sosyal Medya:** Dijital farkındalık kampanyaları

---

## 🚀 **GELECEK GELİŞTİRME ÖNERİLERİ**

### 📱 **Faz 2: Model İyileştirmeleri**
- **Derin Öğrenme Modelleri:** LSTM, Transformer
- **Gerçek Zamanlı API'ler:** Otomatik güncellemeler
- **AutoML:** Otomatik model seçimi
- **Ensemble Yöntemleri:** Çoklu model kombinasyonu

### 📱 **Faz 3: Dashboard İyileştirmeleri**
- **Mobil Uygulama:** React Native
- **Çoklu Dil:** 5 dil desteği
- **Push Bildirimleri:** Anında bildirimler
- **Çevrimdışı Mod:** Çevrimdışı çalışma

### 🌐 **Faz 4: Veri Genişletme**
- **IoT Sensörleri:** Gerçek zamanlı veri
- **Blockchain:** Şeffaf tedarik zinciri
- **50+ Ülke:** Genişletilmiş kapsam
- **Uydu Verisi:** Uzaktan algılama

### 💼 **Faz 5: İş Modeli Geliştirme**
- **SaaS Platformu:** Abonelik modeli
- **Kurumsal Entegrasyonlar:** API hizmetleri
- **Politika Danışmanlığı:** Uzman hizmetleri
- **Eğitim Programları:** Sertifikasyon kursları

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
- **🔄 Gerçek Zamanlı Güncellemeler:** Anında veri yenileme
- **📱 Duyarlı Tasarım:** Tüm cihazlarla uyumlu
- **🎨 Modern UI/UX:** Kullanıcı dostu arayüz
- **⚡ Hızlı Performans:** Optimize edilmiş kod

### 🤖 **AI Destekli Özellikler**
- **🧠 Akıllı Öneriler:** Model tabanlı tavsiyeler
- **🔮 Gelecek Tahminleri:** Makine öğrenmesi tahminleri
- **📊 Otomatik Analiz:** Anında içgörü üretimi
- **🎯 Kişiselleştirme:** Kullanıcı tercihlerine göre

### 📈 **Analitik Özellikler**
- **📊 İnteraktif Grafikler:** Plotly tabanlı görselleştirme
- **🔍 Detaylı Filtreleme:** Çoklu kriter seçimi
- **📋 Kapsamlı Raporlar:** PDF/Excel dışa aktarma
- **🔄 Karşılaştırmalı Analiz:** Çoklu veri karşılaştırması

---

## 👥 **PROJE EKİBİ**

<div align="center">

| **Üye** | **Rol** | **Katkı** |
|:--------|:--------|:----------|
| **Özge Güneş** | Veri Bilimci | Model geliştirme, analiz |
| **Kübra Saruhan** | Veri Bilimci | Veri analizi, dokümantasyon |

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
- **Scikit-learn Dokümantasyonu:** Model seçimi ve optimizasyon
- **Streamlit Dokümantasyonu:** Dashboard geliştirme
- **SHAP Dokümantasyonu:** Model açıklanabilirliği
- **Plotly Dokümantasyonu:** İnteraktif görselleştirme

---

<div align="center">

### 🌱 **Sürdürülebilir gelecek için veri odaklı çözümler**

[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/ozgunes91/ecolense-intelligence)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

</div> 
