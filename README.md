<div align="center">

# 🌱 ECOLENSE INTELLIGENCE

### *Küresel Gıda Atığı Analizi ve Sürdürülebilirlik Platformu*

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3+-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Dashboard](https://img.shields.io/badge/Dashboard-Canlı-brightgreen.svg)](https://ecolense-intelligence.streamlit.app/)

**"İsrafı gözünden vuruyoruz."**

[🌐 Canlı Dashboard](https://ecolense-intelligence.streamlit.app/) · [📊 Teknik Rapor (TR)](ecolense_intelligence_raporu_2026.md) · [📄 Technical Report (EN)](ecolense_intelligence_report_2025.md)

</div>

---

## 🎯 Projeye Genel Bakış

Ecolense Intelligence; küresel gıda atığı krizini makine öğrenmesiyle ele alan, 148 ülkeye ait 16.576 gözlemi analiz eden ve 2024–2030 dönemi için güvenilir tahminler üreten veri odaklı bir sürdürülebilirlik platformudur. Platform; politika yapıcılara, araştırmacılara ve kurumsal sürdürülebilirlik profesyonellerine doğrudan eyleme dönüştürülebilir içgörüler sunar.

| Gösterge | Değer |
|---|---|
| **Kapsanan Ülke** | 148 |
| **Toplam Gözlem** | 16.576 |
| **Tarihsel Dönem** | 2010–2023 |
| **Tahmin Ufku** | 2024–2030 |
| **Ortalama Test R²** | 0,9534 |
| **Özellik Sayısı** | 37 |
| **Dashboard Modülü** | 22 |

---

## 📋 İçindekiler

1. [Problem Tanımı](#-problem-tanımı)
2. [Mimari ve Klasör Yapısı](#-mimari-ve-klasör-yapısı)
3. [Veri Seti ve Metodoloji](#-veri-seti-ve-metodoloji)
4. [Makine Öğrenmesi Modelleri](#-makine-öğrenmesi-modelleri)
5. [Sürdürülebilirlik Skoru — Tasarım Kararı](#-sürdürülebilirlik-skoru--tasarım-kararı)
6. [SHAP Analizi](#-shap-analizi)
7. [Dashboard — 22 Modül](#️-dashboard--22-modül)
8. [AI Insights Motoru](#-ai-insights-motoru)
9. [Kurulum ve Çalıştırma](#-kurulum-ve-çalıştırma)
10. [Bilinen Sorunlar ve Düzeltmeler](#-bilinen-sorunlar-ve-düzeltmeler)
11. [Gelecek Yol Haritası](#-gelecek-yol-haritası)
12. [Proje Ekibi](#-proje-ekibi)
13. [Referanslar](#-referanslar)

---

## 🌍 Problem Tanımı

Küresel gıda sistemleri, iklim, ekonomi ve toplumsal eşitlik üzerindeki en büyük baskılardan birini oluşturmaktadır:

- Dünya genelinde üretilen gıdanın **%33'ü** — 1,3 milyar ton — israf edilmektedir (FAO, 2021).
- Gıda atığı, küresel sera gazı emisyonlarının **%8–10'unu** oluşturmaktadır (UNEP, 2021).
- Yıllık ekonomik kayıp **1,2 trilyon USD** seviyesindedir.
- İsraf edilen gıdanın üretimi için yılda **250 km³** su tüketilmektedir.

Mevcut çözümler büyük ölçüde statik raporlara ve tek hedefli modellere dayanmaktadır. Ecolense Intelligence bu boşluğu kapatmak için: gerçek zamanlı analiz, çoklu hedef tahminleme ve veri destekli politika simülasyonunu tek bir platformda sunar.

---

## 🗂️ Mimari ve Klasör Yapısı

```
ecolense-intelligence/
│
├── data/
│   └── ecolense_final_enriched_with_iso.csv   # 16.576 satır, 37 değişken, 148 ülke
│
├── docs/
│   └── assets/                                # Grafik ve görsel çıktılar
│
├── .streamlit/
│   └── config.toml                            # Streamlit yapılandırması
│
├── 01_veri_hazirlama.py                       # Veri birleştirme ve özellik mühendisliği
├── 02_model_egitimi.py                        # Model eğitimi ve doğrulama
├── 03_model_karsilastirma_analizi.py          # 27 kombinasyon karşılaştırması
├── app.py                                     # Ana Streamlit uygulaması (22 modül)
├── storytelling.py                            # Story Mode modülü
│
├── ecolense_2025_2030_predictions_dashboard.csv
├── model_performance_dashboard.json
├── model_comparison_raporu.json
├── dashboard_category_analyses.json
│
├── shap_importance_Total_Waste_Tons.csv
├── shap_importance_Economic_Loss_Million_USD.csv
├── shap_importance_Carbon_Footprint_kgCO2e.csv
├── shap_summary_*.png
├── model_comparison_*.png
│
├── README.md                                  # Bu dosya (Türkçe)
├── README_EN.md                               # İngilizce açıklama
├── ecolense_intelligence_raporu_2026.md       # Detaylı teknik rapor (TR)
├── ecolense_intelligence_report_2025.md       # Technical report (EN)
│
└── requirements.txt
```

---

## 📊 Veri Seti ve Metodoloji

### Veri Kaynakları

| Kaynak | Kapsam | Kullanım |
|---|---|---|
| UNEP Food Waste Index Report 2021 | Ülke bazlı atık göstergeleri | Birincil hedef değişkenler |
| FAO Food Price Index | Gıda fiyat serileri | Ekonomik bağlam |
| Gapminder GDP per capita | 1950–2023 gelir serileri | Sosyoekonomik özellikler |
| IMF WEO büyüme varsayımları | 2024–2030 projeksiyonları | Tahmin katmanı makro girdileri |
| Poore & Nemecek karbon katsayıları | Kategori bazlı CO₂e faktörleri | Karbon hesaplamaları |
| Ülke meta verileri | Bölge, nüfus, ISO kodları | Coğrafi özellikler |

**Kapsam:** 148 ülke · 2010–2023 tarihsel dönem · 16.576 gözlem · 8 gıda kategorisi

### Özellik Mühendisliği — 29 Türetilmiş Değişken

```python
# Kişi başı metrikler (6 değişken)
df['Waste_Per_Capita_kg'] = df['Total_Waste_Tons'] * 1000 / df['Population_Million']

# Sürdürülebilirlik skoru — ağırlıklı bileşik formül
def calculate_sustainability_score(row):
    waste_score    = max(0, 1 - row['Waste_Per_Capita_kg']          / 150)
    economic_score = max(0, 1 - row['Economic_Loss_Per_Capita_USD'] /  40)
    carbon_score   = max(0, 1 - row['Carbon_Per_Capita_kgCO2e']     /   0.5)
    return max(0, min(100,
        (waste_score * 0.4 + economic_score * 0.3 + carbon_score * 0.3) * 100
    ))
```

| Kategori | Değişken Sayısı | Örnek |
|---|---|---|
| Kişi Başı Metrikler | 6 | `Waste_Per_Capita_kg` |
| Zamansal Özellikler | 8 | `Pandemic_Indicator`, `Year_Trend` |
| Coğrafi Değişkenler | 4 | `Continent`, `Hemisphere` |
| Türetilmiş Göstergeler | 6 | `Waste_Efficiency`, `Economic_Intensity` |
| Etkileşim Terimleri | 3 | `Population_Material_Interaction` |
| Kayan Ortalama Trendler | 2 | `Waste_Trend_3Y` |

---

## 🤖 Makine Öğrenmesi Modelleri

Modelleme üç hedef için ayrı ayrı yapılmıştır:

| Hedef | Test R² | CV R² | Aşırı Öğrenme |
|---|---|---|---|
| `Total_Waste_Tons` | 0,9674 | 0,9684 | 0,0195 |
| `Economic_Loss_Million_USD` | 0,9464 | 0,9458 | 0,0302 |
| `Carbon_Footprint_kgCO2e` | 0,9464 | 0,9609 | 0,0398 |
| **Ortalama** | **0,9534** | **0,9584** | **0,030** |

**Seçilen algoritma:** Gradient Boosting Regressor — 27 kombinasyon (3 algoritma × 3 özellik grubu × 3 hedef) içinden tutarlı biçimde en iyi performansı göstermiştir.

```python
GradientBoostingRegressor(
    n_estimators  = 100,
    max_depth     = 4,
    learning_rate = 0.05
)
```

Tahmin katmanında model skoru, tarihsel ülke–kategori eğilimi ve makro varsayımlar (IMF WEO) birlikte kullanılmaktadır.

---

## ♻️ Sürdürülebilirlik Skoru — Tasarım Kararı

**Neden ayrı bir model eğitilmiyor?**

Sürdürülebilirlik skoru, modelin zaten tahmin ettiği üç değişkenden (atık, ekonomik kayıp, karbon) deterministik formülle hesaplanan türetilmiş bir metriktir. Ayrı model eğitmek hem gereksiz hem de veri sızıntısına açık olurdu:

- Üç bileşen zaten yüksek doğrulukla modelleniyor (ort. R² 0,9534)
- Kural tabanlı formül tamamen yorumlanabilir ve denetlenebilir
- Ağırlıklar (0,4 / 0,3 / 0,3) politika kararlarına göre güncellenebilir

**Dashboard'da nasıl gösterilir:**

```
Tarihsel veri (2010–2023) → Gerçek hesaplanan skor doğrudan gösterilir
Tahmin (2024–2030)        → Model çıktılarından anlık formülle hesaplanır
Politika Simülatörü       → Senaryo değişikliklerini gerçek zamanlı yansıtır
```

> ⚠️ **Bilinen sorun:** Model sayfasında `Sustainability_Score` için SHAP bölümü boş görünmektedir. `shap_importance_Sustainability_Score.csv` dosyası mevcut değildir çünkü bu değişken için ayrı bir model eğitilmemiştir. Çözüm için [Bilinen Sorunlar](#-bilinen-sorunlar-ve-düzeltmeler) bölümüne bakınız.

---

## 🔍 SHAP Analizi

| Özellik | Total Waste | Economic Loss | Carbon Footprint |
|---|---|---|---|
| `Category_Waste_Share` | **%62,6** | — | **%62,6** |
| `Category_Economic_Share` | — | **%62,4** | — |
| `Population (Million)` | %10,4 | %10,2 | %10,4 |
| `Waste_Efficiency` | %8,8 | — | %8,7 |
| `Carbon_Per_Capita_kgCO2e` | %7,2 | — | %7,3 |

**Kritik bulgu:** Kategori payı değişkenleri tüm hedeflerde baskın belirleyicidir (~%62). Pandemi göstergeleri ise beklenenin aksine oldukça düşük etki göstermektedir (%0,1–0,3).

---

## 🖥️ Dashboard — 22 Modül

### 🏠 Temel Modüller (5)

| Modül | Açıklama |
|---|---|
| **Ana Sayfa** | KPI kartları, küresel özet, hızlı navigasyon |
| **Veri Analizi** | Kategori ve değişken yapısı, dağılım, korelasyon |
| **Model Performansı** | Hedef bazlı metrikler, SHAP görselleri |
| **Gelecek Tahminleri** | 2024–2030 ülke/metrik projeksiyonları |
| **Story Mode** | Veri destekli anlatı ve hikaye modu |

### 🤖 Yapay Zeka Destekli Modüller (4)

| Modül | Açıklama |
|---|---|
| **AI Insights** | Veri destekli dinamik içgörü motoru (aşağıya bakınız) |
| **Politika Simülatörü** | What-if senaryo analizi, müdahale etkisi |
| **Hedef Planlayıcı** | Hedefe ulaşmak için gerekli CAGR hesabı |
| **ROI / NPV** | Politika yatırımının finansal getiri analizi |

### 📈 Analitik Modüller (6)

| Modül | Açıklama |
|---|---|
| **Model Karşılaştırma** | 27 kombinasyon test sonuçları |
| **Hedef Bazlı Tahminler** | Özel hedeflere göre projeksiyon |
| **What-if (İleri)** | Nüfus, kategori, politika değişkeni senaryoları |
| **Country Deep Dive** | Ülke bazlı derinlemesine analiz |
| **Driver Sensitivity** | Tornado diyagramı, değişken duyarlılık |
| **Benchmark & Lig** | Ülke performans sıralaması ve karşılaştırma |

### 📄 Raporlama Modülleri (4)

| Modül | Açıklama |
|---|---|
| **Rapor Oluşturucu** | Otomatik yönetici özeti, indirilebilir çıktı |
| **Model Kartı** | Metodoloji, sınırlamalar, etik |
| **Anomali & İzleme** | Aykırı değer tespiti ve uyarı sistemi |
| **Veri Hattı & Kalite** | Kaynak izlenebilirliği, kalite metrikleri |

### 🌍 Etki Modülleri (3)

| Modül | Açıklama |
|---|---|
| **Karbon Akışları** | Ülke ve kategori bazlı CO₂e emisyon haritası |
| **Risk & Fırsat** | 2×2 eksen üzerinde ülke konumlandırma |
| **Adalet / Etki Paneli** | Sosyal eşitlik ve dağılımsal etki analizi |

---

## 🧠 AI Insights Motoru

AI Insights modülü, harici bir LLM API'si yerine **projenin kendi verilerinden ve model çıktılarından** beslenen bir dinamik içgörü sistemi olarak tasarlanmıştır.

### Nasıl Çalışır?

```
Kullanıcı sorusu / seçim
        ↓
Veri katmanı sorgusu (gerçek CSV + model çıktıları)
        ↓
Bağlama özgü istatistik hesaplama
        ↓
Şablonlu ama dinamik metin üretimi
        ↓
Ülke / yıl / kategori filtrelerine göre kişiselleştirilmiş yanıt
```

### Mevcut Özellikler

- Ülke veya kategori seçimine göre otomatik özet üretimi
- Model performans yorumlaması (R², aşırı öğrenme uyarıları)
- Trend tespiti ve anomali vurgulama
- Politika senaryosu karşılaştırması

### Gelecek: Gerçek RAG Entegrasyonu

Bir sonraki geliştirme fazında Anthropic Claude veya OpenAI API entegrasyonu planlanmaktadır. Bu yapıda veri seti embedding olarak indekslenecek; kullanıcı soruları önce bu indeksten ilgili bağlamı alacak (Retrieve), ardından LLM'e iletilecektir (Generate). Böylece sistem gerçek bir Retrieval-Augmented Generation mimarisine dönüşecektir.

---

## 🚀 Kurulum ve Çalıştırma

### Gereksinimler

```
Python 3.10+
streamlit>=1.28
pandas>=2.0
scikit-learn>=1.3
plotly>=5.15
shap>=0.42
numpy>=1.24
```

### Kurulum

```bash
# Depoyu klonla
git clone https://github.com/ozgunes91/ecolense-intelligence.git
cd ecolense-intelligence

# Sanal ortam oluştur
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate

# Bağımlılıkları yükle
pip install -r requirements.txt
```

### Çalıştırma Sırası

```bash
python 01_veri_hazirlama.py          # Veri hazırlama
python 02_model_egitimi.py           # Model eğitimi
python 03_model_karsilastirma_analizi.py   # Karşılaştırma (isteğe bağlı)
streamlit run app.py                 # Dashboard başlatma
```

### GitHub'a Yükleme

Dosyaları indirip reponuza eklemek için:

```bash
# Repoyu klonladıysanız
cd ecolense-intelligence

# Dosyaları kopyala (indirdiğiniz konuma göre güncelleyin)
cp ~/Downloads/README.md ./README.md
cp ~/Downloads/ecolense_intelligence_raporu_2026.md ./ecolense_intelligence_raporu_2026.md
cp ~/Downloads/Ecolense_Intelligence_Sunum.pptx ./docs/Ecolense_Intelligence_Sunum.pptx

# Değişiklikleri ekle ve gönder
git add README.md ecolense_intelligence_raporu_2026.md docs/Ecolense_Intelligence_Sunum.pptx
git commit -m "docs: README güncellendi, 2026 raporu ve sunum eklendi"
git push origin main
```

> `docs/` klasörü yoksa önce `mkdir docs` komutuyla oluşturun.

---

## ⚠️ Bilinen Sorunlar ve Düzeltmeler

### Model Sayfası — Sürdürülebilirlik Skoru SHAP Boş

**Sorun:** Model performans sayfasında `Sustainability_Score` sekmesi boş görünüyor.

**Neden:** `shap_importance_Sustainability_Score.csv` hiç üretilmedi — bu değişken için ayrı model eğitilmediğinden `02_model_egitimi.py` bu dosyayı oluşturmuyor.

**Hızlı düzeltme** (`app.py` içinde ilgili bölüme ekleyin):

```python
if selected_target == "Sustainability_Score":
    st.info(
        "Sürdürülebilirlik skoru, modelin tahmin ettiği üç bileşenden "
        "(atık, ekonomik kayıp, karbon) deterministik formülle hesaplanır. "
        "Bileşen SHAP analizleri için lütfen diğer sekmeleri inceleyiniz."
    )
    st.stop()
```

---

## 🗺️ Gelecek Yol Haritası

| Faz | Odak | Öne Çıkan Geliştirmeler |
|---|---|---|
| **Faz 2** | Model İyileştirme | LSTM, Transformer, AutoML, Ensemble yöntemleri |
| **Faz 3** | Gerçek RAG | Claude / OpenAI API, vektör veritabanı, embedding indeksi |
| **Faz 4** | Platform | Mobil uygulama, çok dilli destek, push bildirim |
| **Faz 5** | Veri Genişletme | IoT sensörleri, Blockchain, uydu verisi |
| **Faz 6** | İş Modeli | SaaS platform, kurumsal API, politika danışmanlığı |

---

## 👥 Proje Ekibi

| Üye | Rol | Sorumluluk |
|---|---|---|
| **Özge Güneş** | Kıdemli Veri Bilimci | Model geliştirme, SHAP analizi, dashboard mimarisi |
| **Kübra Saruhan** | Veri Bilimci | Veri hazırlama, özellik mühendisliği, dokümantasyon |

**Kurum:** Miuul Data Scientist Bootcamp · **Dönem:** 2025–2026

---

## 📚 Referanslar

- FAO (2021). *The State of Food and Agriculture.* Food and Agriculture Organization.
- UNEP (2021). *Food Waste Index Report 2021.* United Nations Environment Programme.
- Poore, J. & Nemecek, T. (2018). Reducing food's environmental impacts through producers and consumers. *Science, 360*(6392).
- IMF (2024). *World Economic Outlook.* International Monetary Fund.
- Lundberg, S. M. & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. *NeurIPS 2017.*
- Chen, T. & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System. *KDD 2016.*

---

<div align="center">

🌱 **Sürdürülebilir gelecek için veri odaklı çözümler**

[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)](https://github.com/ozgunes91/ecolense-intelligence)
[![Dashboard](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)](https://ecolense-intelligence.streamlit.app/)

</div>
