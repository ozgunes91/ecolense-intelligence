# Ecolense Intelligence Teknik Raporu

**Tarih:** 31 Mayıs 2026<br>
**Canlı Dashboard:** [ecolense-intelligence.streamlit.app](https://ecolense-intelligence.streamlit.app)<br>
**Hazırlayanlar:** Özge Güneş · Kübra Saruhan<br>
**Kurum:** Miuul Data Scientist Bootcamp

---

## Yönetici Özeti

Ecolense Intelligence, küresel gıda israfını çevresel ve ekonomik etkileriyle birlikte analiz eden bir sürdürülebilirlik karar destek platformudur. Proje; ülke, yıl ve gıda kategorisi kırılımlarını birleştirerek 2010-2023 tarihsel dönemini analiz eder ve 2024-2030 için projeksiyon üretir.

Dashboard, gıda israfını yalnızca toplam ton değeriyle değil; ekonomik kayıp, karbon ayak izi, sürdürülebilirlik skoru, ülke profili ve kategori kompozisyonu üzerinden birlikte yorumlar. Böylece kullanıcı, hangi ülkenin hangi kategoride daha yüksek etki yarattığını ve hangi politika senaryosunun daha güçlü sonuç verebileceğini aynı ekranda inceleyebilir.

| Gösterge | Değer |
|---|---:|
| Ülke sayısı | 148 |
| Tarihsel dönem | 2010-2023 |
| Tahmin ufku | 2024-2030 |
| Toplam gözlem | 16.576 |
| Ortalama test R² | 0,9534 |
| Dashboard modülü | 22 |

---

## Veri Seti

Veri seti; ülke, yıl ve gıda kategorisi seviyesinde hazırlanmıştır. Çalışmada gıda israfı, ekonomik kayıp, karbon ayak izi, nüfus, kişi başı gelir, materyal ayak izi, gıda fiyat endeksi, gelir grubu ve bölge bilgileri birlikte kullanılmıştır.

| Kaynak | İçerik |
|---|---|
| UNEP Food Waste Index Report | Ülke bazlı gıda atığı göstergeleri |
| FAO Food Price Index | Gıda fiyat endeksi ve dönemsel fiyat hareketleri |
| Gapminder GDP per capita | Gelir serileri |
| IMF WEO varsayımları | 2024-2030 makro projeksiyon girdileri |
| Poore & Nemecek karbon katsayıları | Gıda kategorilerine göre CO₂e etkisi |
| Ülke meta verileri | Bölge, gelir grubu, ISO kodu ve nüfus bilgileri |

Veri hazırlama sürecinde ülke adları ve ISO kodları standartlaştırılmış, kategori bazlı pay değişkenleri üretilmiş, nüfus ve materyal ayak izi gibi ölçek değişkenleri modelleme için uygun forma getirilmiştir.

---

## Tarihsel Görünüm

2010-2023 döneminde gıda israfı düzenli artış eğilimi göstermiştir. Bu artışta nüfus büyümesi, kentleşme, tüketim alışkanlıkları ve kategori kompozisyonu belirleyici olmuştur.

![2023 kategori dağılımı](docs/assets/category_waste_2023.png)

2023 görünümünde meyve-sebze, tahıl, süt ürünleri, et-deniz ürünleri ve fırın ürünleri yüksek etki yaratan ana kategoriler olarak öne çıkar. Kategori dağılımı, yalnızca toplam ülke nüfusuna bakmanın yeterli olmadığını; gıda sepetindeki ürün kompozisyonunun da politika tasarımında dikkate alınması gerektiğini gösterir.

---

## Modelleme Yaklaşımı

Modelleme üç ana hedef için ayrı ayrı yürütülmüştür:

| Hedef | Açıklama |
|---|---|
| `Total_Waste_Tons` | Toplam gıda israfı |
| `Economic_Loss_Million_USD` | Ekonomik kayıp |
| `Carbon_Footprint_kgCO2e` | Karbon ayak izi |

Gradient Boosting Regressor, test performansı ve yorumlanabilirlik dengesi nedeniyle ana üretim modeli olarak seçilmiştir. Model; kategori payı, nüfus, gelir, materyal ayak izi, fiyat endeksi ve tarihsel eğilim değişkenlerinden beslenir.

![Model performansı](docs/assets/model_performance_summary.png)

| Hedef | Test R² | CV R² | Aşırı Öğrenme |
|---|---:|---:|---:|
| Toplam gıda israfı | 0,9674 | 0,9684 | 0,0195 |
| Ekonomik kayıp | 0,9464 | 0,9458 | 0,0302 |
| Karbon ayak izi | 0,9464 | 0,9609 | 0,0398 |
| Ortalama | 0,9534 | 0,9584 | 0,0300 |

Sonuçlar, üç hedefte de güçlü genelleme performansı elde edildiğini göstermektedir. En yüksek açıklama gücü toplam gıda israfında görülürken, ekonomik kayıp ve karbon ayak izi hedeflerinde de dengeli sonuçlar alınmıştır.

---

## Sürdürülebilirlik Skoru

Sürdürülebilirlik skoru, modelin tahmin ettiği üç bileşenin ağırlıklı birleşimiyle hesaplanır:

```text
Skor = 0,40 x Atık_Skoru + 0,30 x Ekonomik_Skor + 0,30 x Karbon_Skoru
```

Bu tasarım, skorun şeffaf ve denetlenebilir kalmasını sağlar. Atık, ekonomik kayıp ve karbon ayak izi ayrı ayrı izlenebildiği için kullanıcı yalnızca toplam skoru değil, skorun hangi bileşenden etkilendiğini de görebilir. Ağırlıklar, farklı politika önceliklerine göre yeniden kalibre edilebilir.

---

## Açıklanabilirlik Analizi

Model açıklanabilirliği hedef bazlı SHAP/özellik etkisi çıktılarıyla izlenmiştir. Her hedef için en etkili değişkenler ayrı ayrı görselleştirilmiştir.

![SHAP ve özellik etkisi özeti](docs/assets/shap_feature_impact_overview.png)

![Toplam gıda israfı özellik etkisi](docs/assets/shap_total_waste.png)

![Ekonomik kayıp özellik etkisi](docs/assets/shap_economic_loss.png)

![Karbon ayak izi özellik etkisi](docs/assets/shap_carbon_footprint.png)

Analiz, kategori ve nüfus temelli değişkenlerin model kararlarında güçlü rol oynadığını gösterir. Toplam israf ve karbon ayak izi tarafında gıda kategorisi etkisi daha baskın görünürken, ekonomik kayıp hedefinde kategoriyle birlikte ölçek ve gelir göstergeleri de belirginleşir.

Bu sonuç, politika simülasyonlarının iki eksende okunmasını gerektirir: ülke ölçeği ve kategori kompozisyonu. Büyük nüfusa sahip ülkelerde toplam etki yükselirken, yüksek karbon yoğunluklu kategoriler karbon ayak izi üzerinde çarpan etkisi yaratır.

---

## 2024-2030 Projeksiyonu

![Tahmin trendleri](docs/assets/forecast_trends.png)

| Yıl | Gıda israfı | Ekonomik kayıp | Karbon ayak izi | Ortalama skor |
|---:|---:|---:|---:|---:|
| 2024 | 545,7 milyon ton | 2,29 trilyon USD | 3,46 trilyon kg CO₂e | 42,5 |
| 2025 | 554,7 milyon ton | 2,38 trilyon USD | 3,54 trilyon kg CO₂e | 42,9 |
| 2026 | 566,0 milyon ton | 2,45 trilyon USD | 3,56 trilyon kg CO₂e | 43,6 |
| 2027 | 571,3 milyon ton | 2,50 trilyon USD | 3,59 trilyon kg CO₂e | 44,2 |
| 2028 | 578,2 milyon ton | 2,56 trilyon USD | 3,63 trilyon kg CO₂e | 44,3 |
| 2029 | 583,2 milyon ton | 2,62 trilyon USD | 3,67 trilyon kg CO₂e | 44,3 |
| 2030 | 590,5 milyon ton | 2,68 trilyon USD | 3,73 trilyon kg CO₂e | 44,4 |

Projeksiyonlar, baz senaryoda gıda israfı ve ekonomik kaybın artış eğilimini koruduğunu göstermektedir. Bu nedenle azaltım stratejileri yalnızca toplam hacmi değil, kategori bazlı yüksek etkili alanları da hedeflemelidir.

---

## Dashboard Yapısı

Dashboard, analizden karar desteğine uzanan 22 modülden oluşur.

| Kategori | Modüller |
|---|---|
| Temel analiz | Ana Sayfa, Veri Analizi, Model Performansı, Gelecek Tahminleri, Story Mode |
| Karar destek | İçgörü Paneli, Politika Simülatörü, Hedef Planlayıcı, ROI / NPV |
| Derin analiz | Model Karşılaştırma, Hedef Bazlı Tahminler, What-if, Country Deep Dive, Driver Sensitivity, Benchmark & Lig |
| Raporlama | Rapor Oluşturucu, Model Kartı, Anomali & İzleme, Veri Hattı & Kalite |
| Etki analizi | Karbon Akışları, Risk & Fırsat, Adalet / Etki Paneli |

İçgörü Paneli, kullanıcının seçtiği ülke, hedef ve yıl bilgisine göre metrikleri yeniden hesaplar. Böylece tek tip yanıt üretmek yerine seçilen bağlama göre trend, sıralama, risk ve fırsat yorumları sunar.

---

## Sonuç

Ecolense Intelligence; gıda israfı, ekonomik kayıp ve karbon etkisini aynı analitik çatı altında birleştirir. Model performansı, açıklanabilirlik çıktıları ve senaryo modülleri birlikte değerlendirildiğinde proje; sürdürülebilirlik ekipleri, araştırmacılar ve politika tasarımcıları için uygulanabilir bir karar destek katmanı sunar.

Ana bulgular şunlardır:

- Kategori kompozisyonu, model kararlarında en güçlü belirleyicilerden biridir.
- Nüfus ve ölçek değişkenleri toplam etkiyi artıran temel faktörlerdir.
- Ekonomik kayıp tarafında kategori etkisiyle birlikte gelir ve fiyat göstergeleri daha görünür hale gelir.
- 2024-2030 projeksiyonları, güçlü azaltım politikaları olmadan SDG 12.3 hedefinden uzaklaşma riskini işaret eder.

---

## Gelişim Yol Haritası

| Faz | Odak |
|---|---|
| Faz 2 | Zaman serisi modelleri ve ensemble karşılaştırmaları |
| Faz 3 | Ülke/kategori bilgi kartları ve gelişmiş veri arama |
| Faz 4 | Mobil uyumlu karar destek ekranları |
| Faz 5 | Tedarik zinciri, uydu verisi ve sensör tabanlı veri genişletme |
| Faz 6 | Kurumsal API ve sürdürülebilirlik danışmanlığı kullanımları |

---

## Referanslar

- FAO (2021). *The State of Food and Agriculture.*
- UNEP (2021). *Food Waste Index Report.*
- Poore, J. & Nemecek, T. (2018). Reducing food's environmental impacts through producers and consumers. *Science.*
- IMF (2024). *World Economic Outlook.*
- Lundberg, S. M. & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. *NeurIPS.*

---

*Ecolense Intelligence — sürdürülebilir gıda sistemleri için veri odaklı karar desteği.*
