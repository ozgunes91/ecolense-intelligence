# 🌱 EcoLense Intelligence

**Gerçek veriye dayalı küresel gıda israfı analiz ve tahmin platformu**

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)](https://streamlit.io)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3+-orange)](https://scikit-learn.org)

---

## 📊 Proje Özeti

| | |
|---|---|
| **Ülke** | 150 (tüm kıtalar) |
| **Yıl aralığı** | 2010–2023 |
| **Gözlem** | 16,800 |
| **Model** | GradientBoosting (3 hedef) |
| **Ort. Test R²** | ~0.99 |

---

## 🔬 Gerçek Veri Kaynakları

| Kaynak | Kapsam | Ne için? |
|--------|--------|----------|
| **UNEP Food Waste Index 2021** (Tablo A4.1) | 148 ülke | Kişi başı atık (kg/kişi/yıl) |
| **Gapminder Foundation** | 142 ülke, 1952-2007 | GDP per capita (gerçek ölçüm) |
| **IMF World Economic Outlook** | 2008-2030 | GDP büyüme oranları |
| **FAO Food Price Index** | 2010-2023 | Gıda enflasyonu |
| **Poore & Nemecek 2018** (*Science*) | 40.000 çiftlik | LCA karbon faktörleri |
| **countryinfo** (UN kaynaklı) | 248 ülke | Nüfus, bölge, ISO kodu |

---

## 🚀 Kurulum & Çalıştırma

```bash
# 1. Klonla
git clone https://github.com/KULLANICI_ADI/ecolense-intelligence.git
cd ecolense-intelligence

# 2. Bağımlılıkları kur
pip install -r requirements.txt

# 3. Pipeline çalıştır (veri → model → tahmin)
python run_pipeline.py

# 4. Dashboard başlat
streamlit run app.py
```

---

## 📁 Dosya Yapısı

```
ecolense-intelligence/
├── data/
│   ├── global_food_waste_real_world.csv   # Ham gerçek veri (UNEP/FAO/Gapminder)
│   ├── processed.csv                       # Özellik mühendisliği uygulanmış
│   └── meta.json                           # Veri meta bilgisi
├── models/
│   ├── model_Total_Waste_Tons.pkl
│   ├── model_Economic_Loss_Million_USD.pkl
│   └── model_Carbon_Footprint_kgCO2e.pkl
├── 01_prepare_data.py      # Veri hazırlama pipeline
├── 02_train_models.py      # Model eğitimi + SHAP
├── 03_generate_forecasts.py# 2024-2030 tahminleri
├── run_pipeline.py         # Tek komut: tüm pipeline
├── app.py                  # Streamlit dashboard (9 sayfa)
├── requirements.txt
└── README.md
```

---

## 🤖 Model Detayları

- **Algoritma:** GradientBoostingRegressor
- **Hedefler:** Toplam Atık (ton), Ekonomik Kayıp (M$), Karbon Ayak İzi (kgCO2e)
- **Train/Test:** 80/20
- **CV:** 5-fold
- **Overfit önleme:** `min_samples_leaf=5`, `subsample=0.8`, sınırlı `max_depth`

### Düzeltilen Hatalar (orijinal proje)

| Hata | Düzeltme |
|------|----------|
| Sustainability_Score → çoğunlukla 0 | Eşikler gerçek veri dağılımına göre ayarlandı |
| Carbon birimi yanlış | `ton_atık × kg_CO2e/kg` doğru uygulandı |
| 20 ülke / sentetik veri | 150 gerçek ülke, UNEP 2021 baz değerleri |
| Sabit ezber sayılar dashboard'da | Tüm sayılar CSV/JSON'dan dinamik okunur |

---

## 📖 Dashboard Sayfaları

| Sayfa | İçerik |
|-------|--------|
| 🏠 Ana Sayfa | KPI kartları, trend, harita — tümü gerçek veriden |
| 📊 Veri Analizi | Filtreli keşif, kategori & ülke sıralaması |
| 🌍 Ülke Karşılaştırma | Çoklu ülke trend & ısı haritası |
| 🤖 Model Performansı | R², RMSE, overfit — model_performance.json'dan |
| 🔮 Gelecek Tahminleri | 2024-2030 projeksiyon + harita |
| 🎯 Hedef Simülatörü | Politika senaryosu etkisi |
| 📈 SHAP & Önem | Özellik önemi grafikleri |
| ⚠️ Risk & Fırsat | Ülke risk matrisi |
| 📄 Rapor | Otomatik oluşturulan MD rapor |

---

## 👥 Ekip

| Üye | Rol |
|-----|-----|
| Özge Güneş | Veri Bilimci |
| Kübra Saruhan | Veri Bilimci |

**Kurum:** Miuul Data Scientist Bootcamp — Final Projesi 2025
