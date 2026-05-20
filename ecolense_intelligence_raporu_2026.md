# ECOLENSE INTELLIGENCE - GERCEK VERI GUNCELLEME RAPORU

**Rapor tarihi:** 20 Mayis 2026  
**Veri araligi:** 2010-2023 gercek veri, 2024-2030 model tahmini  
**Kapsam:** 148 tekil ISO3 ulke, 8 gida kategorisi, 16.576 tarihsel gozlem  
**Model:** GradientBoostingRegressor, 3 hedef degisken

---

## 1. Yonetici Ozeti

Bu guncellemede eski 20 ulke / 5.000 satirlik sentetik gorunumlu veri yapisi yerine, UNEP Food Waste Index, FAO Food Price Index, Gapminder, IMF WEO, Poore & Nemecek LCA katsayilari ve ulke meta verileriyle zenginlestirilmis 2010-2023 veri seti kullanildi.

Onemli temizlik: `UK` / `United Kingdom` ve `UAE` / `United Arab Emirates` ayni ISO3 koduyla iki ayri ulke gibi sayiliyordu. Pipeline artik bu aliaslari tekillestiriyor; kapsam 150 gorunen ulkeden 148 tekil ISO3 ulkeye indi.

## 2. Veri Ozeti

| Metrik | Deger |
|---|---:|
| Tarihsel gozlem | 16.576 |
| Ulke | 148 |
| Yil | 2010-2023 |
| Kategori | 8 |
| Toplam gida atigi | 7.046,8 milyon ton |
| Ekonomik kayip | 27,18 trilyon USD |
| Karbon ayak izi | 43,57 trilyon kg CO2e |
| Ortalama surdurulebilirlik skoru | 83,1 / 100 |

## 3. Veri Kaynaklari ve Notlar

| Kaynak | Kullanim |
|---|---|
| UNEP Food Waste Index 2021 | Ulke bazli kisi basi gida atigi baz degerleri |
| FAO Food Price Index | Gida fiyat endeksi ve zaman etkisi |
| Gapminder Foundation | GDP per capita olcumleri |
| IMF World Economic Outlook | Gelecek donem buyume varsayimlari |
| Poore & Nemecek 2018 | Gida kategorisi karbon katsayilari |
| countryinfo / ulke meta verisi | ISO3, kita, bolge, nufus ve gelir grubu eslestirmeleri |

Not: Kategori kirilimlari, kaynaklardaki ulke-yil baz degerlerinin gida kategorilerine dagitilmasi ve LCA katsayilariyla zenginlestirilmesiyle modellemeye uygun hale getirilmistir. Bu nedenle rapor, kaynaklardan gelen olcumleri ve modelleme icin uretilen kategori dagilimlarini ayri degerlendirmelidir.

## 4. Model Performansi

Hedeflerden turetilmis rolling/share/per-capita kolonlari egitimden cikarildi. Boylece model performansi hala guclu, fakat onceki rapordaki gibi hedef sizintisiyla yapay olarak sisirilmis degil.

| Hedef | Test R2 | CV R2 | RMSE | Overfit |
|---|---:|---:|---:|---:|
| Total Waste (Tons) | 0,9979 | 0,9929 | 69.266,82 | 0,0012 |
| Economic Loss (Million $) | 0,9697 | 0,9632 | 1.136,09 | 0,0202 |
| Carbon_Footprint_kgCO2e | 0,9636 | 0,9797 | 2.442.792.337,66 | 0,0323 |

**Ortalama Test R2:** 0,9771  
**Ortalama overfit:** 0,0179

## 5. En Etkili Model Suruculeri

| Hedef | Ilk faktorler |
|---|---|
| Total Waste (Tons) | Pop_MatFP, GDP_Waste_PC, Population (Million), Population_Material_Interaction, Log_Population |
| Economic Loss (Million $) | Food Category_Enc, Waste_Per_Capita_kg, Pop_MatFP, Population (Million), Log_Population |
| Carbon_Footprint_kgCO2e | Food Category_Enc, Waste_Per_Capita_kg, Pop_MatFP, GDP_Waste_PC, Population (Million) |

## 6. Kategori Bazli Bulgular

| Kategori | Toplam atik (milyon ton) | Ekonomik kayip (milyon USD) | Karbon (trilyon kg CO2e) |
|---|---:|---:|---:|
| Fruits & Vegetables | 1.841,5 | 4.194.828 | 7,03 |
| Grains & Cereals | 1.337,4 | 936.252 | 1,87 |
| Dairy Products | 1.049,4 | 2.806.181 | 3,35 |
| Meat & Seafood | 984,9 | 12.075.090 | 26,46 |
| Bakery Items | 775,3 | 2.298.686 | 1,40 |

Meat & Seafood, toplam atik hacminde dorduncu sirada olmasina ragmen karbon etkisinde acik ara en kritik kategori.

## 7. 2024-2030 Tahminleri

| Yil | Toplam atik (milyon ton) | Ekonomik kayip (trilyon USD) | Karbon (trilyon kg CO2e) | Ortalama skor |
|---|---:|---:|---:|---:|
| 2024 | 523,3 | 2,21 | 3,27 | 47,3 |
| 2025 | 527,3 | 2,23 | 3,27 | 48,2 |
| 2026 | 531,3 | 2,19 | 3,29 | 49,8 |
| 2027 | 535,3 | 2,17 | 3,32 | 50,8 |
| 2028 | 541,5 | 2,18 | 3,34 | 51,2 |
| 2029 | 546,5 | 2,21 | 3,38 | 51,4 |
| 2030 | 549,9 | 2,21 | 3,41 | 51,7 |

2024-2030 arasinda model toplam atikta yaklasik %5,1, karbon ayak izinde yaklasik %4,3 artis ongoruyor. Ekonomik kayip toplamda yatay seyrediyor; bu kisim FAO fiyat endeksi ve GDP varsayimlarina duyarlidir.

## 8. Yapilan Duzeltmeler

| Eski sorun | Guncel durum |
|---|---|
| 20 ulke ve sentetik veri raporu | 148 ISO3 tekil ulke ve 2010-2023 gercek kaynakli veri ozeti |
| 2018-2024 kapsam iddiasi | Gercek tarihsel aralik 2010-2023 olarak duzeltildi |
| 2025-2030 tahmin iddiasi | Forecast dosyasi 2024-2030 olarak standardize edildi |
| Sabit `Sustainability_Score = 65` | Tahminlerde skor, kisi basi atik/kayip/karbon dagilimindan hesaplandi |
| Model performansinin sifir gorunmesi | Dashboard loader yeni JSON formatini `targets` ile okuyor |
| Raporun eski CSV yoluna gitmesi | Rapor olusturucu `data/processed.csv` ve guncel `model_performance.json` kullaniyor |
| Hedef sizintisi yapan feature'lar | Rolling/share/per-capita target turevleri egitimden cikarildi |
| UK/UAE alias tekrarları | ISO3 bazli tekillestirme eklendi |

## 9. Sonuc

Proje artik dashboard tasarimini koruyarak daha temiz bir veri hatti uzerinde calisiyor. Veri seti sentetik 20 ulke kurgusundan cikti; pipeline guncel dosyalari yeniden uretiyor, dashboard metrikleri dinamik okuyor, raporlar eski veri yoluna bagli kalmiyor ve forecast skorlamasi sabit deger yerine veri dagilimina dayaniyor.
