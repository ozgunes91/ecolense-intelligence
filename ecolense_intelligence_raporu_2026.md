# Ecolense Intelligence — Teknik Rapor

**Tarih:** 21 Mayıs 2026
**Canlı Dashboard:** [ecolense-intelligence.streamlit.app](https://ecolense-intelligence.streamlit.app)
**Hazırlayanlar:** Özge Güneş · Kübra Saruhan
**Kurum:** Miuul Data Scientist Bootcamp

---

## Yönetici Özeti

Ecolense Intelligence; gıda israfını yalnızca ton bazlı bir kayıp olarak değil, ekonomik maliyet, karbon etkisi, ülke profili ve kategori davranışı ile birlikte ele alan veri odaklı bir sürdürülebilirlik ürünüdür. Dashboard; 2010–2023 tarihsel verisini ve 2024–2030 projeksiyonlarını tek bir arayüzde birleştirir.

| Gösterge | Değer |
|---|---:|
| Ülke sayısı | 148 |
| Tarihsel dönem | 2010–2023 |
| Tahmin ufku | 2024–2030 |
| Gözlem sayısı | 16.576 |
| Ortalama model test R² | 0,9534 |
| Dashboard modülü | 22 |

---

## Veri Seti

Veri seti; ülke, yıl ve gıda kategorisi kırılımında hazırlanmıştır. Analizde gıda israfı, ekonomik kayıp, karbon ayak izi, nüfus, kişi başı gelir, gıda fiyat endeksi, materyal ayak izi, gelir grubu ve bölge bilgileri birlikte kullanılır.

**Başlıca veri kaynakları:**

| Kaynak | İçerik |
|---|---|
| UNEP Food Waste Index Report 2021 | Ülke bazlı atık göstergeleri |
| FAO Food Price Index | Gıda fiyat serileri |
| Gapminder GDP per capita | 1950–2023 gelir serileri |
| IMF WEO büyüme varsayımları | 2024–2030 makro projeksiyon girdileri |
| Poore & Nemecek karbon katsayıları | Kategori bazlı CO₂e faktörleri |
| Ülke meta verileri | Bölge, nüfus, ISO kodları |

---

## Tarihsel Durum (2010–2023)

| Metrik | Değer |
|---|---:|
| Toplam gıda israfı | 7.046,8 milyon ton |
| Ekonomik kayıp | 27,18 trilyon USD |
| Karbon ayak izi | 43,57 trilyon kg CO₂e |
| Ortalama sürdürülebilirlik skoru | 83,1 / 100 |

2023 kategori dağılımı, toplam israfta ilk sırada **Fruits & Vegetables** kategorisinin yer aldığını göstermektedir. Bunu **Grains & Cereals**, **Dairy Products**, **Meat & Seafood** ve **Bakery Items** izlemektedir.

### Yıllık Eğilimler

2010–2023 döneminde toplam gıda israfı yılda ortalama %2,4 artmıştır. Bu artış; nüfus büyümesi, kentleşme ve değişen tüketim alışkanlıklarından kaynaklanmaktadır. Pandemi döneminde (2020–2021) kısa vadeli bir yavaşlama gözlemlenmiş; ancak 2022 itibarıyla eğilim önceki seviyesine dönmüştür.

---

## Modelleme

Modelleme üç hedef için ayrı ayrı gerçekleştirilmiştir:

- `Total_Waste_Tons` — Toplam gıda israfı
- `Economic_Loss_Million_USD` — Ekonomik kayıp
- `Carbon_Footprint_kgCO2e` — Karbon ayak izi

### Model Performansı

| Hedef | Test R² | CV R² | Aşırı Öğrenme |
|---|---:|---:|---:|
| Total Waste (Tons) | 0,9674 | 0,9684 | 0,0195 |
| Economic Loss (Million USD) | 0,9464 | 0,9458 | 0,0302 |
| Carbon Footprint (kg CO₂e) | 0,9464 | 0,9609 | 0,0398 |
| **Ortalama** | **0,9534** | **0,9584** | **0,030** |

**Seçilen algoritma:** Gradient Boosting Regressor (`n_estimators=100`, `max_depth=4`, `learning_rate=0.05`). 27 kombinasyon (3 algoritma × 3 özellik grubu × 3 hedef) sistematik olarak test edilmiş; bu yapı tutarlı biçimde en iyi genelleme performansını vermiştir.

Tahmin katmanında model skoru, tarihsel ülke–kategori eğilimi ve IMF WEO makro varsayımları birlikte kullanılmaktadır.

### Sürdürülebilirlik Skoru — Tasarım Kararı

Sürdürülebilirlik skoru, modelin tahmin ettiği üç bileşenden (atık, ekonomik kayıp, karbon ayak izi) ağırlıklı formülle hesaplanan türetilmiş bir metriktir. Bu nedenle ayrı bir makine öğrenmesi modeli eğitilmemiştir:

```
Skor = 0,40 × Atık_Skoru + 0,30 × Ekonomik_Skoru + 0,30 × Karbon_Skoru
```

Her bileşen, veri setine özgü kalibre eşiklere göre 0–1 aralığına normalize edilir; ardından 0–100 ölçeğine çevrilir. Sıfıra yapışan değer kullanılmaz; çok yüksek etki üreten ülkeler düşük fakat okunabilir bir taban skorla temsil edilir.

Bu yaklaşımın avantajları:
- Bileşenler zaten yüksek doğrulukla modelleniyor (ort. R² 0,9534)
- Formül deterministik — sonuçlar tam yorumlanabilir ve denetlenebilir
- Ağırlıklar politika önceliklerine göre güncellenebilir
- Veri sızıntısı riski sıfır

### SHAP Analizi

SHAP değerleri modelin hangi değişkenlerden ne ölçüde etkilendiğini ortaya koymaktadır:

| Özellik | Total Waste | Economic Loss | Carbon Footprint |
|---|---:|---:|---:|
| Category_Waste/Economic_Share | ~%62,6 | ~%62,4 | ~%62,6 |
| Population (Million) | %10,4 | %10,2 | %10,4 |
| Waste_Efficiency | %8,8 | — | %8,7 |
| Carbon_Per_Capita_kgCO2e | %7,2 | — | %7,3 |
| GDP / Economic göstergeler | — | ~%15 | — |

**Kritik bulgu:** Kategori payı değişkenleri tüm hedeflerde baskın belirleyicidir (~%62). Pandemi göstergeleri beklenenin aksine oldukça düşük etki göstermektedir (%0,1–0,3).

---

## 2024–2030 Projeksiyonu

| Yıl | Gıda israfı | Ekonomik kayıp | Karbon ayak izi | Ort. skor |
|---:|---:|---:|---:|---:|
| 2024 | 545,7 milyon ton | 2,29 trilyon USD | 3,46 trilyon kg CO₂e | 42,5 |
| 2025 | 554,7 milyon ton | 2,38 trilyon USD | 3,54 trilyon kg CO₂e | 42,9 |
| 2026 | 566,0 milyon ton | 2,45 trilyon USD | 3,56 trilyon kg CO₂e | 43,6 |
| 2027 | 571,3 milyon ton | 2,50 trilyon USD | 3,59 trilyon kg CO₂e | 44,2 |
| 2028 | 578,2 milyon ton | 2,56 trilyon USD | 3,63 trilyon kg CO₂e | 44,3 |
| 2029 | 583,2 milyon ton | 2,62 trilyon USD | 3,67 trilyon kg CO₂e | 44,3 |
| 2030 | 590,5 milyon ton | 2,68 trilyon USD | 3,73 trilyon kg CO₂e | 44,4 |

2024–2030 arasında baz senaryoda toplam gıda israfı yaklaşık **%8,2**, ekonomik kayıp **%17,2**, karbon ayak izi **%7,8** artış göstermektedir. Bu eğilim, mevcut politikaların sürdürülmesi durumunda BM SDG 12.3 hedefine (2030'a kadar %50 azaltım) ulaşılamayacağına işaret etmektedir.

---

## Dashboard — 22 Modül

### Modül Kategorileri

| Kategori | Modüller |
|---|---|
| **Temel (5)** | Ana Sayfa · Veri Analizi · Model Performansı · Gelecek Tahminleri · Story Mode |
| **AI Destekli (4)** | AI Insights · Politika Simülatörü · Hedef Planlayıcı · ROI / NPV |
| **Analitik (6)** | Model Karşılaştırma · Hedef Bazlı Tahminler · What-if · Country Deep Dive · Driver Sensitivity · Benchmark & Lig |
| **Raporlama (4)** | Rapor Oluşturucu · Model Kartı · Anomali & İzleme · Veri Hattı & Kalite |
| **Etki (3)** | Karbon Akışları · Risk & Fırsat · Adalet / Etki Paneli |

### AI Insights Motoru

AI Insights modülü, harici bir LLM API'si yerine **projenin kendi verilerinden ve model çıktılarından** beslenen dinamik bir içgörü sistemidir. Kullanıcı seçimlerine göre bağlama özgü istatistikler hesaplanarak şablonlu ama veri destekli yanıtlar üretilir. Bu yaklaşım; harici bağımlılık gerektirmez, her zaman veriyle tutarlı yanıt verir ve yanlış üretim (halüsinasyon) riskini ortadan kaldırır.

Bir sonraki geliştirme fazında gerçek RAG (Retrieval-Augmented Generation) mimarisine geçiş planlanmaktadır: veri seti embedding olarak indekslenecek, kullanıcı soruları önce bu indeksten ilgili bağlamı alacak, ardından bir dil modeline iletilecektir.

---

## Dashboard Kullanım Akışı

1. **Ana Sayfa** — KPI kartlarıyla küresel tabloya bakış
2. **Veri Analizi** — Kategori ve değişken yapısını inceleyin
3. **Model Performansı** — Hedef bazlı model kalitesini kontrol edin
4. **Gelecek Tahminleri** — 2024–2030 ülke/metrik davranışını izleyin
5. **What-if & Politika Simülatörü** — Senaryo ve politika müdahalelerini test edin
6. **AI Insights** — Veri destekli otomatik içgörü alın
7. **Rapor Oluşturucu** — Yönetici özeti indirin

---

## Bilinen Sorunlar

**Model sayfası — Sürdürülebilirlik Skoru SHAP bölümü boş**

`shap_importance_Sustainability_Score.csv` dosyası mevcut değildir; bu değişken için ayrı bir model eğitilmediğinden bu dosya hiç üretilmemiştir. Hızlı düzeltme: ilgili sekmeye "Sürdürülebilirlik skoru türetilmiş bir metriktir, bileşen SHAP analizleri için diğer sekmeleri inceleyiniz" bilgi mesajı eklenmelidir.

---

## Gelecek Çalışmalar

| Faz | İçerik |
|---|---|
| Faz 2 | LSTM, Transformer ve AutoML modelleri |
| Faz 3 | Gerçek RAG entegrasyonu (Claude / OpenAI API + vektör veritabanı) |
| Faz 4 | Mobil uygulama, çok dilli destek |
| Faz 5 | IoT sensör verisi, Blockchain tedarik zinciri izleme |
| Faz 6 | SaaS platform, kurumsal API, politika danışmanlığı hizmetleri |

---

## Referanslar

- FAO (2021). *The State of Food and Agriculture.* Food and Agriculture Organization.
- UNEP (2021). *Food Waste Index Report 2021.* United Nations Environment Programme.
- Poore, J. & Nemecek, T. (2018). Reducing food's environmental impacts through producers and consumers. *Science, 360*(6392), 987–992.
- IMF (2024). *World Economic Outlook.* International Monetary Fund.
- Lundberg, S. M. & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. *NeurIPS 2017.*
- Chen, T. & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System. *KDD 2016.*

---

*Ecolense Intelligence — Sürdürülebilir gelecek için veri odaklı çözümler*
*© 2026 Özge Güneş & Kübra Saruhan · Miuul Data Scientist Bootcamp*
