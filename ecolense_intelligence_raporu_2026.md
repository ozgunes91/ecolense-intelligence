# Ecolense Intelligence Teknik Raporu

**Tarih:** 1 Haziran 2026<br>
**Canlı Dashboard:** [ecolense-intelligence.streamlit.app](https://ecolense-intelligence.streamlit.app)<br>
**İngilizce Rapor:** [ecolense_intelligence_report_2026_en.md](ecolense_intelligence_report_2026_en.md)<br>
**Hazırlayanlar:** Özge Güneş · Kübra Saruhan<br>
**Kurum:** Miuul Data Scientist Bootcamp

---

## Yönetici Özeti

Ecolense Intelligence, küresel gıda israfını çevresel ve ekonomik etkileriyle birlikte analiz eden bir sürdürülebilirlik karar destek platformudur. Proje; ülke, yıl ve gıda kategorisi kırılımlarını birleştirerek 2010-2023 tarihsel dönemini analiz eder ve 2024-2030 için projeksiyon üretir.

Dashboard, gıda israfını yalnızca toplam ton değeriyle değil; ekonomik kayıp, karbon ayak izi, sürdürülebilirlik skoru, ülke profili ve kategori kompozisyonu üzerinden birlikte yorumlar.

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

Veri seti ülke-yıl-gıda kategorisi seviyesinde hazırlanmıştır. Çalışmada gıda israfı, ekonomik kayıp, karbon ayak izi, nüfus, kişi başı gelir, materyal ayak izi, gıda fiyat endeksi, gelir grubu ve bölge bilgileri birlikte kullanılmıştır.

| Kaynak | İçerik |
|---|---|
| UNEP Food Waste Index Report | Ülke bazlı gıda atığı göstergeleri |
| FAO Food Price Index | Gıda fiyat endeksi ve dönemsel fiyat hareketleri |
| Gapminder GDP per capita | Gelir serileri |
| IMF WEO varsayımları | 2024-2030 makro projeksiyon girdileri |
| Poore & Nemecek karbon katsayıları | Gıda kategorilerine göre CO2e etkisi |
| Ülke meta verileri | Bölge, gelir grubu, ISO kodu ve nüfus bilgileri |

![2023 kategori dağılımı](docs/assets/category_waste_2023.png)

---

## Modelleme Yaklaşımı

Gradient Boosting Regressor, test performansı ve yorumlanabilirlik dengesi nedeniyle ana üretim modeli olarak seçilmiştir. Üç hedef ayrı ayrı modellenmiştir:

| Hedef | Test R² | CV R² | Aşırı öğrenme |
|---|---:|---:|---:|
| Toplam gıda israfı | 0,9674 | 0,9684 | 0,0195 |
| Ekonomik kayıp | 0,9464 | 0,9458 | 0,0302 |
| Karbon ayak izi | 0,9464 | 0,9609 | 0,0398 |
| Ortalama | 0,9534 | 0,9584 | 0,0300 |

![Model performansı](docs/assets/model_performance_summary.png)

---

## Açıklanabilirlik Analizi

Model açıklanabilirliği hedef bazlı özellik etkisi çıktılarıyla izlenmiştir. Bu çıktılar, karar süreçlerinde hangi değişkenlerin daha belirleyici olduğunu gösterir.

![SHAP ve özellik etkisi özeti](docs/assets/shap_feature_impact_overview.png)

![Toplam gıda israfı özellik etkisi](docs/assets/shap_total_waste.png)

![Ekonomik kayıp özellik etkisi](docs/assets/shap_economic_loss.png)

![Karbon ayak izi özellik etkisi](docs/assets/shap_carbon_footprint.png)

Analiz, kategori ve nüfus temelli değişkenlerin model kararlarında güçlü rol oynadığını gösterir. Bu nedenle politika yorumları yalnızca ülke toplamına değil, kategori kompozisyonuna da dayanır.

---

## 2024-2030 Projeksiyonu

Tahmin grafiği dört farklı metriği ayrı panellerde gösterir. Bu tercih, ekonomik kayıp ve karbon çizgilerinin farklı ölçek nedeniyle sıfıra yakınmış gibi görünmesini engeller.

![Tahmin trendleri](docs/assets/forecast_trends.png)

| Yıl | Gıda israfı | Ekonomik kayıp | Karbon ayak izi | Ortalama skor |
|---:|---:|---:|---:|---:|
| 2024 | 545,7 milyon ton | 2,29 trilyon USD | 3,46 trilyon kg CO2e | 42,5 |
| 2025 | 554,7 milyon ton | 2,38 trilyon USD | 3,54 trilyon kg CO2e | 42,9 |
| 2026 | 566,0 milyon ton | 2,45 trilyon USD | 3,56 trilyon kg CO2e | 43,6 |
| 2027 | 571,3 milyon ton | 2,50 trilyon USD | 3,59 trilyon kg CO2e | 44,2 |
| 2028 | 578,2 milyon ton | 2,56 trilyon USD | 3,63 trilyon kg CO2e | 44,3 |
| 2029 | 583,2 milyon ton | 2,62 trilyon USD | 3,67 trilyon kg CO2e | 44,3 |
| 2030 | 590,5 milyon ton | 2,68 trilyon USD | 3,73 trilyon kg CO2e | 44,4 |

---

## Dashboard Modülleri

| Modül | İşlev |
|---|---|
| Ana Sayfa | Ana KPI kartları, hızlı geçişler, veri chatbotu ve hikaye girişleri. |
| Veri Analizi | Veri kapsamı, kalite, dağılım, korelasyon ve kategori analizi. |
| Model Performansı | Test/CV metrikleri, hata ölçümleri ve hedef bazlı model kalitesi. |
| Gelecek Tahminleri | 2024-2030 ülke ve metrik tahminleri. |
| Hedef Bazlı Tahminler | Özel ülke/metrik hedeflerinin tahmin ufkunda takibi. |
| What-if | Varsayım değişikliklerinin çıktılar üzerindeki etkisi. |
| Country Deep Dive | Tek ülke için detaylı tarihsel ve tahminsel analiz. |
| Driver Sensitivity | Sürücü değişkenlerin metriklere etkisinin karşılaştırılması. |
| ROI / NPV | Azaltım senaryolarının finansal geri dönüş hesabı. |
| Benchmark & Lig | Ülkelerin karşılaştırmalı performans sıralaması. |
| Anomali & İzleme | Aykırı değer ve izleme sinyallerinin kontrolü. |
| Veri Hattı & Kalite | Kaynak, dosya, satır/sütun ve üretim akışı kontrolleri. |
| Karbon Akışları | Karbon yükünün kategori, ülke veya kıta dağılımı. |
| Model Karşılaştırma | Model sonuçları, hedef performansı ve özellik etkisi. |
| Politika Simülatörü | Atık azaltımı, karbon fiyatı ve teknoloji benimseme senaryoları. |
| İçgörü Paneli | Veri chatbotu, CAGR analizi, SHAP etkileri ve bağlamsal yanıtlar. |
| Risk & Fırsat | Ülkelerin risk ve fırsat eksenlerinde konumlandırılması. |
| Hedef Planlayıcı | 2030 hedefi için gerekli yıllık değişim oranı. |
| Rapor Oluşturucu | Rapor türüne göre farklı HTML/Markdown çıktılar. |
| Model Kartı | Metodoloji, performans, sınırlılıklar ve etik özet. |
| Adalet / Etki Paneli | Etkinin ülke, bölge ve gelir grubu kırılımında incelenmesi. |
| Story Mode | Başlığına uygun veri kesitlerinden üretilen özgün hikayeler. |

---

## Veri Chatbotu

Veri chatbotu, sabit cevap veren bir metin kutusu değildir. Soru metninden ülke, kategori, metrik, yıl ve niyet bilgisini ayıklar; ardından tarihsel veri, tahmin dosyası ve açıklanabilirlik çıktılarından ilgili kesiti okuyarak yanıt üretir. Yanıtın sonunda kullanılan veri dayanağı belirtilir.

---

## Sonuç

Ecolense Intelligence; gıda israfı, ekonomik kayıp ve karbon etkisini birlikte değerlendirerek sürdürülebilirlik ekipleri, araştırmacılar ve politika tasarımcıları için uygulanabilir bir karar destek katmanı sunar. Proje, model performansını açıklanabilirlik ve senaryo modülleriyle birlikte kullandığı için yalnızca tahmin üretmez; hangi alanlara odaklanılması gerektiğini de görünür hale getirir.

---

## Referanslar

- FAO. *The State of Food and Agriculture.*
- UNEP. *Food Waste Index Report.*
- Poore, J. & Nemecek, T. Reducing food's environmental impacts through producers and consumers. *Science.*
- IMF. *World Economic Outlook.*
- Lundberg, S. M. & Lee, S.-I. A Unified Approach to Interpreting Model Predictions. *NeurIPS.*

---

*Ecolense Intelligence, sürdürülebilir gıda sistemleri için veri odaklı karar desteği sunar.*
