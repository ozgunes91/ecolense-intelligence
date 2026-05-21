# Ecolense Intelligence Raporu

**Tarih:** 21 Mayıs 2026  
**Canlı dashboard:** [ecolense-intelligence.streamlit.app](https://ecolense-intelligence.streamlit.app)

## Yönetici Özeti

Ecolense Intelligence, küresel gıda israfını ülke, yıl ve gıda kategorisi düzeyinde inceleyen bir sürdürülebilirlik analiz platformudur. Proje, israf miktarını tek başına ele almak yerine ekonomik kayıp, karbon ayak izi ve sürdürülebilirlik skoru ile birlikte değerlendirir.

Dashboard, 2010-2023 dönemindeki tarihsel görünümü ve 2024-2030 projeksiyonlarını aynı akışta sunar. Böylece kullanıcı, hangi ülkelerde ve hangi kategorilerde öncelik verilmesi gerektiğini hızlıca görebilir.

| Gösterge | Değer |
|---|---:|
| Ülke sayısı | 148 |
| Tarihsel dönem | 2010-2023 |
| Tahmin dönemi | 2024-2030 |
| Gözlem sayısı | 16.576 |
| Ortalama test R² | 0,9534 |

![2024-2030 projeksiyon özeti](docs/assets/forecast_trends.png)

## Veri Seti

Veri seti; ülke, yıl ve gıda kategorisi kırılımında hazırlanmıştır. Her satır, belirli bir ülkedeki belirli bir gıda kategorisinin ilgili yıldaki israf, maliyet ve karbon etkisini temsil eder.

Analizde kullanılan temel değişkenler şunlardır:

- Toplam gıda israfı
- Ekonomik kayıp
- Karbon ayak izi
- Nüfus
- Kişi başına gelir
- Gıda fiyat endeksi
- Gelir grubu ve bölge bilgisi
- Sürdürülebilirlik skoru

Veri kaynakları; UNEP Food Waste Index, FAO Food Price Index, Gapminder, IMF WEO, Poore & Nemecek karbon katsayıları ve ülke meta verilerinden oluşur.

![2023 kategori bazlı gıda israfı](docs/assets/category_waste_2023.png)

## Tarihsel Görünüm

2010-2023 döneminde toplam gıda israfı 7.046,8 milyon tona ulaşmıştır. Aynı dönemde ekonomik kayıp 27,18 trilyon USD, karbon ayak izi ise 43,57 trilyon kg CO2e düzeyindedir.

| Metrik | Değer |
|---|---:|
| Toplam gıda israfı | 7.046,8 milyon ton |
| Ekonomik kayıp | 27,18 trilyon USD |
| Karbon ayak izi | 43,57 trilyon kg CO2e |
| Ortalama sürdürülebilirlik skoru | 83,1 / 100 |

Kategori dağılımında meyve ve sebze grubu en yüksek israf hacmine sahiptir. Tahıl ürünleri, süt ürünleri, et-deniz ürünleri ve fırıncılık ürünleri de toplam etkinin önemli bölümünü oluşturur.

## Modelleme Yaklaşımı

Modelleme aşamasında üç hedef ayrı ayrı tahmin edilmiştir:

- Toplam gıda israfı
- Ekonomik kayıp
- Karbon ayak izi

Model, ülke ve kategori desenlerini yakalayabilmek için zaman, nüfus, gelir, fiyat endeksi, bölge ve kategori değişkenlerini birlikte kullanır. Performans değerlendirmesi test skoru, çapraz doğrulama skoru ve overfit kontrolü üzerinden yapılır.

![Model performansı özeti](docs/assets/model_performance_summary.png)

| Hedef | Test R² | CV R² | Overfit |
|---|---:|---:|---:|
| Toplam gıda israfı | 0,9674 | 0,9684 | 0,0195 |
| Ekonomik kayıp | 0,9464 | 0,9458 | 0,0302 |
| Karbon ayak izi | 0,9464 | 0,9609 | 0,0398 |

Sonuçlar, modelin üç hedefte de güçlü ve dengeli bir performans verdiğini göstermektedir.

## 2024-2030 Projeksiyonu

Projeksiyonlar, tarihsel ülke-kategori eğilimleri ile makro değişkenlerin birlikte okunmasıyla üretilir. Bu yapı, her yıl için aynı değeri tekrarlayan durağan bir tahmin yerine ülke, kategori ve yıl bazında değişen bir görünüm sağlar.

| Yıl | Gıda israfı | Ekonomik kayıp | Karbon ayak izi | Ortalama skor |
|---:|---:|---:|---:|---:|
| 2024 | 545,7 milyon ton | 2,29 trilyon USD | 3,46 trilyon kg CO2e | 42,5 |
| 2025 | 554,7 milyon ton | 2,38 trilyon USD | 3,54 trilyon kg CO2e | 42,9 |
| 2026 | 566,0 milyon ton | 2,45 trilyon USD | 3,56 trilyon kg CO2e | 43,6 |
| 2027 | 571,3 milyon ton | 2,50 trilyon USD | 3,59 trilyon kg CO2e | 44,2 |
| 2028 | 578,2 milyon ton | 2,56 trilyon USD | 3,63 trilyon kg CO2e | 44,3 |
| 2029 | 583,2 milyon ton | 2,62 trilyon USD | 3,67 trilyon kg CO2e | 44,3 |
| 2030 | 590,5 milyon ton | 2,68 trilyon USD | 3,73 trilyon kg CO2e | 44,4 |

2030'a doğru gıda israfı, ekonomik kayıp ve karbon ayak izi artış eğilimini korumaktadır. Bu nedenle en etkili müdahale alanları; yüksek hacimli ülkeler, yüksek karbon katsayısına sahip kategoriler ve ekonomik kaybın yoğunlaştığı ürün gruplarıdır.

## Dashboard Akışı

Dashboard, kullanıcının veriyi önce genel düzeyde görmesini, ardından ülke ve kategori ayrıntılarına inmesini sağlar.

| Modül | Amaç |
|---|---|
| Ana Sayfa | Genel KPI görünümü ve hızlı yönlendirme |
| Veri Analizi | Ülke, yıl ve kategori kırılımlarını inceleme |
| Model Performansı | Tahmin modelinin güvenilirliğini değerlendirme |
| Gelecek Tahminleri | 2024-2030 dönemini ülke ve metrik bazında izleme |
| What-if | Politika senaryolarını karşılaştırma |
| Risk & Fırsat | Ülkeleri risk ve fırsat alanlarına göre konumlandırma |
| Rapor Oluşturucu | Analiz çıktısını paylaşılabilir biçime getirme |

## Sonuç

Ecolense Intelligence, gıda israfını yalnızca çevresel bir sorun olarak değil, ekonomik ve operasyonel bir karar alanı olarak ele alır. Proje; veri analizi, modelleme, tahmin ve raporlama adımlarını tek bir dashboard deneyiminde birleştirir.

Bu yapı sayesinde kullanıcı, hangi ülkelerde, hangi gıda kategorilerinde ve hangi metriklerde öncelik verilmesi gerektiğini açık biçimde görebilir.
