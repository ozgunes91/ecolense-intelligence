# Ecolense Intelligence

Küresel gıda israfını ülke, yıl ve gıda kategorisi düzeyinde analiz eden Streamlit dashboard projesi.

[![Canlı Dashboard](https://img.shields.io/badge/Canlı%20Dashboard-Streamlit-ff4b4b?style=for-the-badge&logo=streamlit&logoColor=white)](https://ecolense-intelligence.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.10+-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Model](https://img.shields.io/badge/Model-Gradient%20Boosting-27ae60?style=for-the-badge)](#modelleme)

## Canlı Dashboard

Projeyi canlı görmek için: [ecolense-intelligence.streamlit.app](https://ecolense-intelligence.streamlit.app)

## Proje Özeti

Ecolense Intelligence, gıda israfını ekonomik kayıp, karbon ayak izi ve sürdürülebilirlik skoru ile birlikte ele alır. Dashboard, tarihsel veriyi ve 2024-2030 tahminlerini tek bir arayüzde toplar.

| Başlık | Değer |
|---|---:|
| Ülke sayısı | 148 |
| Tarihsel dönem | 2010-2023 |
| Tahmin dönemi | 2024-2030 |
| Gözlem sayısı | 16.576 |
| Model tipi | GradientBoostingRegressor |
| Ortalama test R² | 0,9534 |

![2024-2030 tahmin özeti](docs/assets/forecast_trends.png)

## Veri Kapsamı

Projede ülke, yıl ve kategori bazlı gıda israfı verileri kullanılır. Bu veriler; nüfus, kişi başına gelir, gıda fiyat endeksi, gelir grubu, bölge ve karbon katsayılarıyla zenginleştirilir.

| Kaynak | Kullanım |
|---|---|
| UNEP Food Waste Index | Ülke bazlı gıda israfı göstergeleri |
| FAO Food Price Index | Gıda fiyat endeksi |
| Gapminder | Kişi başına gelir serileri |
| IMF WEO | 2024-2030 büyüme varsayımları |
| Poore & Nemecek | Kategori bazlı karbon katsayıları |
| Ülke meta verileri | ISO3, bölge, nüfus ve gelir grubu |

![2023 kategori bazlı gıda israfı](docs/assets/category_waste_2023.png)

## Modelleme

Model üç hedef için ayrı ayrı eğitilir:

- Toplam gıda israfı
- Ekonomik kayıp
- Karbon ayak izi

![Model performansı özeti](docs/assets/model_performance_summary.png)

Modelleme süreci; veri hazırlama, model eğitimi, tahmin üretimi ve dashboard sunumu olarak dört ana adımdan oluşur. Kod dosyaları bu akışı sade tutacak şekilde ayrılmıştır.

```text
01_prepare_data.py        Veri setini hazırlar
02_train_models.py        Modelleri eğitir ve performansı ölçer
03_generate_forecasts.py  2024-2030 tahminlerini üretir
app.py                    Streamlit dashboard arayüzünü çalıştırır
run_pipeline.py           Tüm süreci tek komutla çalıştırır
```

## Kurulum

```bash
pip install -r requirements.txt
python run_pipeline.py
streamlit run app.py
```

## Dashboard Modülleri

| Modül | İçerik |
|---|---|
| Ana Sayfa | Genel KPI kartları ve hızlı erişim |
| Veri Analizi | Ülke, kategori ve değişken kırılımları |
| Model Performansı | R², CV, hata ve overfit göstergeleri |
| Gelecek Tahminleri | 2024-2030 ülke/metrik projeksiyonları |
| What-if | Politika senaryoları |
| Risk & Fırsat | Ülke bazlı risk matrisi |
| Rapor Oluşturucu | Paylaşılabilir analiz çıktısı |

## Dosya Yapısı

```text
.
├── app.py
├── run_pipeline.py
├── 01_prepare_data.py
├── 02_train_models.py
├── 03_generate_forecasts.py
├── data/
│   ├── global_food_waste_real_world.csv
│   ├── processed.csv
│   └── meta.json
├── docs/
│   └── assets/
│       ├── category_waste_2023.png
│       ├── forecast_trends.png
│       └── model_performance_summary.png
├── forecasts.csv
├── model_performance.json
└── ecolense_intelligence_raporu_2026.md
```

## Ekip

| İsim | Rol |
|---|---|
| Özge Güneş | Veri bilimi ve dashboard geliştirme |
| Kübra Saruhan | Veri analizi ve modelleme |
