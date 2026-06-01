<div align="center">

# Ecolense Intelligence

### Küresel Gıda Atığı Analizi ve Sürdürülebilirlik Karar Destek Platformu

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3+-orange.svg)](https://scikit-learn.org/)
[![Dashboard](https://img.shields.io/badge/Dashboard-Canlı-brightgreen.svg)](https://ecolense-intelligence.streamlit.app/)

[Canlı Dashboard](https://ecolense-intelligence.streamlit.app/) · [Teknik Rapor](ecolense_intelligence_raporu_2026.md) · [English README](README.en.md)

</div>

---

## Genel Bakış

Ecolense Intelligence, küresel gıda israfını ülke, yıl ve gıda kategorisi düzeyinde inceleyen veri odaklı bir karar destek platformudur. Dashboard; gıda israfı, ekonomik kayıp, karbon ayak izi ve sürdürülebilirlik skorunu aynı analitik çatı altında birleştirir.

| Gösterge | Değer |
|---|---:|
| Ülke sayısı | 148 |
| Tarihsel dönem | 2010-2023 |
| Tahmin ufku | 2024-2030 |
| Toplam gözlem | 16.576 |
| Ortalama test R² | 0,9534 |
| 2023 ortalama sürdürülebilirlik skoru | 82,7/100 |
| 2030 ortalama sürdürülebilirlik projeksiyonu | 77,9/100 |
| Dashboard modülü | 22 |

---

## Dashboard Önizleme

![Dashboard ana sayfa](docs/assets/dashboard_home.jpg)

![Model performansı sayfası](docs/assets/dashboard_model_performance.jpg)

![SHAP ve özellik etkisi bölümü](docs/assets/dashboard_shap_section.jpg)

---

## Analitik Görseller

Tahmin grafiği farklı ölçekleri aynı eksene sıkıştırmaz; israf, ekonomik kayıp, karbon ve skor ayrı panellerde gösterilir.

![Tahmin trendleri](docs/assets/forecast_trends.png)

![2023 kategori dağılımı](docs/assets/category_waste_2023.png)

![Model performansı](docs/assets/model_performance_summary.png)

![SHAP ve özellik etkisi özeti](docs/assets/shap_feature_impact_overview.png)

---

## Sürdürülebilirlik Skoru

Sürdürülebilirlik skoru, ülke düzeyinde kişi başı gıda israfı, kişi başı ekonomik kayıp ve kişi başı karbon baskısını birlikte okuyan 0-100 arası bileşik göstergedir. Yüksek skor, bu üç baskının aynı anda daha kontrollü olduğu bir profili gösterir.

2023 verisinde ortalama skor 82,7/100, ülke medyanı 82,9/100 seviyesindedir. En yüksek skorlar India, Russia, Romania, South Africa ve Lithuania tarafında yoğunlaşır. 2024-2030 projeksiyonunda skor 2023 ölçeğinden koparılmadan, aynı ülkenin kişi başı atık, ekonomik kayıp ve karbon baskısındaki değişime göre güncellenir.

---

## Veri Seti ve Metodoloji

Veri seti ülke-yıl-kategori kırılımında hazırlanmıştır. Analizde gıda israfı, ekonomik kayıp, karbon ayak izi, nüfus, kişi başı gelir, materyal ayak izi, gıda fiyat endeksi, gelir grubu ve bölge bilgileri birlikte kullanılır.

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
3. Tahmin, açıklanabilirlik ve rapor çıktılarının dashboard formatına dönüştürülmesi

---

## Modelleme

Modelleme üç hedef için ayrı ayrı yapılır:

| Hedef | Açıklama | Test R² | CV R² |
|---|---|---:|---:|
| `Total Waste (Tons)` | Toplam gıda israfı | 0,9674 | 0,9684 |
| `Economic Loss (Million $)` | Ekonomik kayıp | 0,9464 | 0,9458 |
| `Carbon_Footprint_kgCO2e` | Karbon ayak izi | 0,9464 | 0,9609 |

Gradient Boosting Regressor ana üretim modeli olarak kullanılır. Açıklanabilirlik çıktıları `outputs/explainability/` altında CSV olarak, rapor görselleri `docs/assets/` altında PNG olarak tutulur.

![Toplam gıda israfı özellik etkisi](docs/assets/shap_total_waste.png)

![Ekonomik kayıp özellik etkisi](docs/assets/shap_economic_loss.png)

![Karbon ayak izi özellik etkisi](docs/assets/shap_carbon_footprint.png)

---

## Dashboard Modülleri

| Modül | Ne işe yarar? |
|---|---|
| Ana Sayfa | Projenin ana KPI kartlarını, hızlı geçişleri, veri chatbotunu ve hikaye girişlerini sunar. |
| Veri Analizi | Veri kapsamını, eksik değerleri, dağılımları, korelasyonları ve kategori kırılımlarını inceler. |
| Model Performansı | Test R², CV R², hata metrikleri ve hedef bazlı model kalitesini gösterir. |
| Gelecek Tahminleri | 2024-2030 döneminde ülke ve metrik bazlı tahminleri görselleştirir. |
| Hedef Bazlı Tahminler | Seçilen ülke/metrik için hedef senaryolarını tahmin ufkunda takip eder. |
| What-if | Nüfus, kategori azaltımı ve politika varsayımlarının etkisini senaryo olarak hesaplar. |
| Country Deep Dive | Tek ülkenin tarihsel profilini, kategori etkisini ve tahmin seyrini detaylandırır. |
| Driver Sensitivity | Sürücü değişkenlerin hedef metrik üzerindeki duyarlılığını karşılaştırır. |
| ROI / NPV | Azaltım senaryolarının finansal geri dönüşünü ve net bugünkü değerini hesaplar. |
| Benchmark & Lig | Ülkeleri performans liginde sıralar ve karşılaştırmalı konumlarını gösterir. |
| Anomali & İzleme | Aykırı değerleri ve izleme sinyallerini kontrol eder. |
| Veri Hattı & Kalite | Dosya kaynaklarını, veri kapsamını, satır/sütun kalitesini ve üretim akışını özetler. |
| Karbon Akışları | Karbon yükünün kategori, ülke veya kıta üzerinden nasıl dağıldığını gösterir. |
| Model Karşılaştırma | Model sonuçlarını, hedef bazlı performansı ve özellik etkilerini birlikte değerlendirir. |
| Politika Simülatörü | Atık azaltımı, karbon fiyatı ve teknoloji benimsemesi gibi politika girdilerini test eder. |
| İçgörü Paneli | Veri chatbotu, CAGR analizi, SHAP etkileri ve seçilen ülke/metrik bağlamında yanıt üretir. |
| Risk & Fırsat | Ülkeleri risk ve fırsat eksenlerinde konumlandırır. |
| Hedef Planlayıcı | 2030 hedefine ulaşmak için gerekli yıllık değişim oranını hesaplar. |
| Rapor Oluşturucu | Seçilen rapor türüne göre farklı, veri kaynaklı HTML/Markdown rapor üretir. |
| Model Kartı | Model yaklaşımı, performans, sınırlılıklar ve etik notları tek sayfada toplar. |
| Adalet / Etki Paneli | Etkinin ülke, bölge ve gelir grubu kırılımında adil dağılımını inceler. |
| Story Mode | Başlığına uygun veri kesitlerinden bulgu, yorum ve önerilen aksiyon içeren veri hikayeleri sunar. |

---

## Veri Chatbotu

Dashboarddaki veri chatbotu sabit metin döndürmez. Soru metninden ülke, metrik, kategori, yıl ve niyet bilgisini yakalar; birden fazla soru varsa parçalayarak ayrı ayrı yanıtlar. Yanıtlar tarihsel veri, tahmin çıktısı ve açıklanabilirlik dosyalarından ilgili kesiti okuyarak üretilir; kullanılan veri dayanağı yanıtın sonunda belirtilir.

---

## Kurulum

```bash
git clone https://github.com/ozgunes91/ecolense-intelligence.git
cd ecolense-intelligence

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Tüm veri hattını çalıştırmak için:

```bash
python run_pipeline.py
```

Dashboardu başlatmak için:

```bash
streamlit run app.py
```

---

## Klasör Yapısı

```text
ecolense-intelligence/
├── data/
│   ├── global_food_waste_real_world.csv
│   ├── processed.csv
│   └── meta.json
├── docs/assets/
│   ├── dashboard_home.jpg
│   ├── dashboard_model_performance.jpg
│   ├── dashboard_shap_section.jpg
│   ├── forecast_trends.png
│   ├── category_waste_2023.png
│   ├── model_performance_summary.png
│   ├── shap_feature_impact_overview.png
│   ├── shap_total_waste.png
│   ├── shap_economic_loss.png
│   └── shap_carbon_footprint.png
├── outputs/
│   ├── forecasts/forecasts.csv
│   ├── metrics/model_performance.json
│   └── explainability/shap_*.csv
├── models/
├── 01_prepare_data.py
├── 02_train_models.py
├── 03_generate_forecasts.py
├── run_pipeline.py
└── app.py
```

---

## Referanslar

- FAO. *The State of Food and Agriculture.*
- UNEP. *Food Waste Index Report.*
- Poore, J. & Nemecek, T. Reducing food's environmental impacts through producers and consumers. *Science.*
- IMF. *World Economic Outlook.*
- Lundberg, S. M. & Lee, S.-I. A Unified Approach to Interpreting Model Predictions. *NeurIPS.*

---

Ecolense Intelligence, sürdürülebilir gıda sistemleri için veri odaklı karar desteği sunar.
