# Ecolense Intelligence Raporu

**Tarih:** 21 Mayis 2026  
**Canli dashboard:** [ecolense-intelligence.streamlit.app](https://ecolense-intelligence.streamlit.app)

## Yonetici Ozeti

Ecolense Intelligence, gida israfini yalnizca ton bazli bir kayip olarak degil; ekonomik maliyet, karbon etkisi, ulke profili ve kategori davranisi ile birlikte ele alan bir veri urunudur. Dashboard; 2010-2023 tarihsel verisini ve 2024-2030 projeksiyonlarini tek bir arayuzde birlestirir.

| Gosterge | Deger |
|---|---:|
| Ulke sayisi | 148 |
| Tarihsel donem | 2010-2023 |
| Tahmin ufku | 2024-2030 |
| Gozlem sayisi | 16.576 |
| Ortalama model test R2 | 0,9534 |

![2024-2030 Projeksiyon Ozeti](docs/assets/forecast_trends.png)

## Veri Seti

Veri seti ulke, yil ve gida kategorisi kiriliminda hazirlanmistir. Analizde gida israfi, ekonomik kayip, karbon ayak izi, nufus, kisi basi gelir, gida fiyat endeksi, malzeme ayak izi, gelir grubu ve bolge bilgileri birlikte kullanilir.

Baslica veri kaynaklari:

- UNEP Food Waste Index Report 2021
- FAO Food Price Index
- Gapminder GDP per capita serileri
- IMF WEO buyume varsayimlari
- Poore & Nemecek karbon katsayilari
- Ulke bolge, nufus ve ISO meta verileri

## Tarihsel Durum

2010-2023 toplaminda:

| Metrik | Deger |
|---|---:|
| Toplam gida israfi | 7.046,8 milyon ton |
| Ekonomik kayip | 27,18 trilyon USD |
| Karbon ayak izi | 43,57 trilyon kg CO2e |
| Ortalama surdurulebilirlik skoru | 83,1 / 100 |

2023 kategori dagilimi, toplam israfta ilk sirada **Fruits & Vegetables** kategorisinin yer aldigini gosterir. Bunu **Grains & Cereals**, **Dairy Products**, **Meat & Seafood** ve **Bakery Items** izler.

![2023 Kategori Bazli Israf](docs/assets/category_waste_2023.png)

## Modelleme

Modelleme uc hedef icin ayri yapilir:

- Total Waste (Tons)
- Economic Loss (Million $)
- Carbon_Footprint_kgCO2e

| Hedef | Test R2 | CV R2 | Overfit |
|---|---:|---:|---:|
| Total Waste (Tons) | 0,9674 | 0,9684 | 0,0195 |
| Economic Loss (Million $) | 0,9464 | 0,9458 | 0,0302 |
| Carbon_Footprint_kgCO2e | 0,9464 | 0,9609 | 0,0398 |

Model sonuclari, ulke ve kategori desenlerini guclu sekilde yakaladigini gosterir. Tahmin katmaninda model skoru, tarihsel ulke-kategori egilimi ve makro varsayimlar birlikte kullanilir.

## 2024-2030 Projeksiyonu

| Yil | Gida israfi | Ekonomik kayip | Karbon ayak izi | Ortalama skor |
|---:|---:|---:|---:|---:|
| 2024 | 545,7 milyon ton | 2,29 trilyon USD | 3,46 trilyon kg CO2e | 42,5 |
| 2025 | 554,7 milyon ton | 2,38 trilyon USD | 3,54 trilyon kg CO2e | 42,9 |
| 2026 | 566,0 milyon ton | 2,45 trilyon USD | 3,56 trilyon kg CO2e | 43,6 |
| 2027 | 571,3 milyon ton | 2,50 trilyon USD | 3,59 trilyon kg CO2e | 44,2 |
| 2028 | 578,2 milyon ton | 2,56 trilyon USD | 3,63 trilyon kg CO2e | 44,3 |
| 2029 | 583,2 milyon ton | 2,62 trilyon USD | 3,67 trilyon kg CO2e | 44,3 |
| 2030 | 590,5 milyon ton | 2,68 trilyon USD | 3,73 trilyon kg CO2e | 44,4 |

2024-2030 arasinda toplam gida israfi yaklasik **%8,2**, ekonomik kayip **%17,2**, karbon ayak izi **%7,8** artar. Surdurulebilirlik skorunda 0'a yapisan deger kullanilmaz; cok yuksek etki ureten ulkeler dusuk fakat okunabilir taban skorla temsil edilir.

## Dashboard Kullanim Akisi

1. Ana sayfada KPI kartlari ile genel tablo okunur.
2. Veri Analizi sayfasinda kategori ve degisken yapisi incelenir.
3. Model Performansi sayfasinda hedef bazli model kalitesi kontrol edilir.
4. Gelecek Tahminleri sayfasinda 2024-2030 ulke/metrik davranisi izlenir.
5. Hedef ve what-if modulleriyle politika senaryolari test edilir.
6. Rapor sayfasindan yonetici ozeti indirilebilir.

## Sonuc

Ecolense Intelligence, gida israfi kararlarini ulke, kategori, ekonomi ve karbon etkisi birlikte gorulecek sekilde tasarlar. Proje; veri kesfi, model performansi, ileri donem projeksiyonu ve raporlama islerini tek bir profesyonel dashboard akisi icinde toplar.
