<div align="center">

# Ecolense Intelligence

### Küresel Gıda Atığı Analizi ve Sürdürülebilirlik Karar Destek Platformu

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3+-orange.svg)](https://scikit-learn.org/)
[![Dashboard](https://img.shields.io/badge/Dashboard-Canlı-brightgreen.svg)](https://ecolense-intelligence.streamlit.app/)

[Canlı Dashboard](https://ecolense-intelligence.streamlit.app/) · [Teknik Rapor](ecolense_intelligence_raporu_2026.md)

</div>

---

## Projeye Genel Bakış

Ecolense Intelligence; küresel gıda atığını ton, ekonomik kayıp, karbon ayak izi ve sürdürülebilirlik skoru üzerinden birlikte inceleyen veri odaklı bir analiz platformudur. Proje; 148 ülke, 2010-2023 tarihsel dönem ve 2024-2030 projeksiyonlarını tek bir Streamlit dashboardunda birleştirir.

Platformun amacı, gıda israfını yalnızca geçmiş verilerle raporlamak değil; ülke, yıl ve kategori düzeyinde karar alınabilir içgörüler üretmektir. Bu nedenle veri hazırlama, modelleme, tahminleme, politika senaryosu ve raporlama modülleri aynı ürün akışı içinde tasarlanmıştır.

| Gösterge | Değer |
|---|---:|
| Ülke sayısı | 148 |
| Tarihsel dönem | 2010-2023 |
| Tahmin ufku | 2024-2030 |
| Toplam gözlem | 16.576 |
| Ortalama test R² | 0,9534 |
| Dashboard modülü | 22 |

---

## Görsel Özet

![Tahmin trendleri](docs/assets/forecast_trends.png)

![2023 kategori dağılımı](docs/assets/category_waste_2023.png)

![Model performansı](docs/assets/model_performance_summary.png)

![SHAP ve özellik etkisi özeti](docs/assets/shap_feature_impact_overview.png)

---

## Veri Seti ve Metodoloji

Veri seti; ülke, yıl ve gıda kategorisi kırılımında hazırlanmıştır. Analizde gıda israfı, ekonomik kayıp, karbon ayak izi, nüfus, kişi başı gelir, gıda fiyat endeksi, materyal ayak izi, gelir grubu ve bölge bilgileri birlikte kullanılır.

| Kaynak | Kullanım |
|---|---|
| UNEP Food Waste Index Report | Ülke bazlı gıda atığı göstergeleri |
| FAO Food Price Index | Gıda fiyat endeksi ve dönemsel fiyat hareketleri |
| Gapminder GDP per capita | Ülke bazlı gelir serileri |
| IMF WEO varsayımları | 2024-2030 makro projeksiyon girdileri |
| Poore & Nemecek katsayıları | Gıda kategorilerine göre karbon etkisi |
| Ülke meta verileri | Bölge, gelir grubu, ISO kodu ve nüfus bilgileri |

Veri hattı üç temel adımdan oluşur:

1. Kaynak verilerin ortak ülke-yıl-kategori seviyesinde hazırlanması
2. Model girdileri için oran, yoğunluk, etkileşim ve dönem değişkenlerinin üretilmesi
3. Tahmin çıktılarının dashboard ve rapor formatına dönüştürülmesi

---

## Modelleme

Modelleme üç ana hedef için ayrı ayrı yapılır:

| Hedef | Açıklama |
|---|---|
| `Total_Waste_Tons` | Toplam gıda israfı |
| `Economic_Loss_Million_USD` | Ekonomik kayıp |
| `Carbon_Footprint_kgCO2e` | Karbon ayak izi |

Gradient Boosting Regressor ana üretim modeli olarak kullanılmıştır. Model; kategori payı, nüfus, gelir, materyal ayak izi, fiyat endeksi ve tarihsel eğilim değişkenlerini birlikte değerlendirir.

| Hedef | Test R² | CV R² |
|---|---:|---:|
| Toplam gıda israfı | 0,9674 | 0,9684 |
| Ekonomik kayıp | 0,9464 | 0,9458 |
| Karbon ayak izi | 0,9464 | 0,9609 |
| Ortalama | 0,9534 | 0,9584 |

---

## Sürdürülebilirlik Skoru

Sürdürülebilirlik skoru, üç model çıktısından hesaplanan bileşik bir göstergedir:

```text
Skor = 0,40 x Atık_Skoru + 0,30 x Ekonomik_Skor + 0,30 x Karbon_Skoru
```

Bu tasarım sayesinde skor doğrudan denetlenebilir, ağırlıklar politika önceliklerine göre güncellenebilir ve her bileşenin etkisi ayrı ayrı izlenebilir. Tarihsel dönemde gerçek verilerden hesaplanan skor, tahmin döneminde model çıktıları üzerinden üretilir.

---

## Açıklanabilirlik Analizi

Model açıklanabilirliği, hedef bazlı SHAP/özellik etkisi çıktılarıyla takip edilir. Her hedef için modelin en çok dikkate aldığı değişkenler ayrı görselleştirilmiştir.

![Toplam gıda israfı özellik etkisi](docs/assets/shap_total_waste.png)

![Ekonomik kayıp özellik etkisi](docs/assets/shap_economic_loss.png)

![Karbon ayak izi özellik etkisi](docs/assets/shap_carbon_footprint.png)

Analiz sonuçları, gıda kategorisi ve nüfus temelli değişkenlerin tüm hedeflerde güçlü açıklayıcı rol üstlendiğini gösterir. Bu bulgu, müdahale planlarının ülke ölçeği kadar kategori kompozisyonunu da dikkate alması gerektiğini ortaya koyar.

---

## Dashboard Modülleri

Dashboard, analizden raporlamaya uzanan 22 modülden oluşur.

| Kategori | Modüller |
|---|---|
| Temel analiz | Ana Sayfa, Veri Analizi, Model Performansı, Gelecek Tahminleri, Story Mode |
| Karar destek | İçgörü Paneli, Politika Simülatörü, Hedef Planlayıcı, ROI / NPV |
| Derin analiz | Model Karşılaştırma, Hedef Bazlı Tahminler, What-if, Country Deep Dive, Driver Sensitivity, Benchmark & Lig |
| Raporlama | Rapor Oluşturucu, Model Kartı, Anomali & İzleme, Veri Hattı & Kalite |
| Etki analizi | Karbon Akışları, Risk & Fırsat, Adalet / Etki Paneli |

İçgörü Paneli; dashboarddaki ülke, kategori, hedef ve yıl seçimlerini kullanarak veri destekli özetler üretir. Yanıtlar sabit metinden ibaret değildir; seçilen bağlama göre metrikler, trendler ve karşılaştırmalar yeniden hesaplanır.

---

## Kurulum ve Çalıştırma

```bash
git clone https://github.com/ozgunes91/ecolense-intelligence.git
cd ecolense-intelligence

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

Tüm veri hattını ve model çıktılarını üretmek için:

```bash
python run_pipeline.py
```

Dashboardu başlatmak için:

```bash
streamlit run app.py
```

Modülleri ayrı ayrı çalıştırmak isteyenler için:

```bash
python 01_prepare_data.py
python 02_train_models.py
python 03_generate_forecasts.py
```

---

## Klasör Yapısı

```text
ecolense-intelligence/
├── data/
│   ├── global_food_waste_real_world.csv
│   ├── processed.csv
│   └── meta.json
├── docs/
│   └── assets/
│       ├── forecast_trends.png
│       ├── category_waste_2023.png
│       ├── model_performance_summary.png
│       ├── shap_feature_impact_overview.png
│       ├── shap_total_waste.png
│       ├── shap_economic_loss.png
│       └── shap_carbon_footprint.png
├── outputs/
│   ├── forecasts/
│   │   └── forecasts.csv
│   ├── metrics/
│   │   └── model_performance.json
│   └── explainability/
│       ├── shap_Total_Waste_Tons.csv
│       ├── shap_Economic_Loss_Million_USD.csv
│       └── shap_Carbon_Footprint_kgCO2e.csv
├── 01_prepare_data.py
├── 02_train_models.py
├── 03_generate_forecasts.py
├── run_pipeline.py
├── app.py
├── README.md
├── ecolense_intelligence_raporu_2026.md
└── requirements.txt
```

---

## Referanslar

- FAO (2021). *The State of Food and Agriculture.*
- UNEP (2021). *Food Waste Index Report.*
- Poore, J. & Nemecek, T. (2018). Reducing food's environmental impacts through producers and consumers. *Science.*
- IMF (2024). *World Economic Outlook.*
- Lundberg, S. M. & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. *NeurIPS.*

---

Ecolense Intelligence, sürdürülebilir gıda sistemleri için veri odaklı karar desteği sunar.
