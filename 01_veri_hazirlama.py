#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01 - Veri Hazırlama (Dashboard için)
====================================

Bu script, dashboard için tüm veri hazırlık işlemlerini yapar:
1. Veri birleştirme ve zenginleştirme
2. ISO kodları ekleme
3. Sustainability_Score'ları düzeltme

Adımlar:
- Veri birleştirme
- Eksik değer analizi
- Aykırı değer tespiti
- Özellik mühendisliği
- Encoding
- ISO kodları ekleme
- Sustainability_Score düzeltme
- Dashboard için hazırlık
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import KNNImputer
import warnings
warnings.filterwarnings('ignore')

class VeriHazirlama:
    def __init__(self):
        self.foodwaste_df = None
        self.footprint_df = None
        self.merged_df = None
        self.final_df = None
        self.label_encoders = {}
        
    def veri_yukle(self):
        """Veri setlerini yükle"""
        print("📊 Veri setleri yükleniyor...")
        
        # Food waste veri seti
        self.foodwaste_df = pd.read_csv('data/global_food_wastage_dataset.csv')
        print(f"✅ Food waste: {self.foodwaste_df.shape}")
        print(f"   Sütunlar: {list(self.foodwaste_df.columns)}")
        
        # Material footprint veri seti  
        self.footprint_df = pd.read_csv('data/material_footprint.csv')
        print(f"✅ Material footprint: {self.footprint_df.shape}")
        print(f"   Sütunlar: {list(self.footprint_df.columns)}")
        
    def veri_analizi(self):
        """Veri setlerini analiz et"""
        print("\n🔍 Veri analizi yapılıyor...")
        
        # Food waste analizi
        print("\n📊 Food Waste Analizi:")
        print(f"   Satır sayısı: {len(self.foodwaste_df)}")
        print(f"   Sütun sayısı: {len(self.foodwaste_df.columns)}")
        print(f"   Benzersiz ülke: {self.foodwaste_df['Country'].nunique()}")
        print(f"   Benzersiz yıl: {self.foodwaste_df['Year'].nunique()}")
        print(f"   Benzersiz kategori: {self.foodwaste_df['Food Category'].nunique()}")
        
        # Veri tipleri
        print("\n📋 Veri tipleri:")
        print(self.foodwaste_df.dtypes)
        
        # Boş değerler
        print("\n🚨 Boş değerler:")
        null_counts = self.foodwaste_df.isnull().sum()
        print(null_counts[null_counts > 0])
        
        # Temel istatistikler
        print("\n📈 Temel istatistikler:")
        numeric_cols = ['Total Waste (Tons)', 'Economic Loss (Million $)', 'Population (Million)']
        print(self.foodwaste_df[numeric_cols].describe())
        
        # Material footprint analizi
        print("\n📊 Material Footprint Analizi:")
        print(f"   Satır sayısı: {len(self.footprint_df)}")
        print(f"   Sütun sayısı: {len(self.footprint_df.columns)}")
        print(f"   Benzersiz ülke: {self.footprint_df['Country'].nunique()}")
        
        # Yıl sütunları
        year_cols = [col for col in self.footprint_df.columns if any(str(year) in col for year in range(2018, 2025))]
        print(f"   Yıl sütunları: {len(year_cols)}")
        
    def veri_birlestir(self):
        """Veri setlerini birleştir"""
        print("\n🔗 Veri setleri birleştiriliyor...")
        
        # Material footprint'i long format'a çevir
        year_cols = [col for col in self.footprint_df.columns if any(str(year) in col for year in range(2018, 2025))]
        
        footprint_long = self.footprint_df.melt(
            id_vars=['ISO3', 'Country', 'Continent', 'Hemisphere', 'Human Development Groups', 
                    'UNDP Developing Regions', 'HDI Rank (2021)'],
            value_vars=year_cols,
            var_name='Year',
            value_name='Material_Footprint_Per_Capita'
        )
        
        # Year sütununu temizle
        footprint_long['Year'] = footprint_long['Year'].str.extract('(\d{4})').astype(int)
        
        print(f"✅ Material footprint long format: {footprint_long.shape}")
        
        # Veri setlerini birleştir
        self.merged_df = pd.merge(
            self.foodwaste_df,
            footprint_long[['Country', 'Year', 'Material_Footprint_Per_Capita', 'Continent', 'Hemisphere']],
            on=['Country', 'Year'],
            how='left'
        )
        
        print(f"✅ Birleştirilmiş veri: {self.merged_df.shape}")
        
        # Birleştirme kontrolü
        missing_footprint = self.merged_df['Material_Footprint_Per_Capita'].isnull().sum()
        print(f"⚠️ Eksik material footprint: {missing_footprint}")
        
    def eksik_degerleri_doldur(self):
        """Eksik değerleri doldur"""
        print("\n🔧 Eksik değerler dolduruluyor...")
        
        # Material footprint eksik değerleri
        footprint_median = self.merged_df['Material_Footprint_Per_Capita'].median()
        self.merged_df['Material_Footprint_Per_Capita'].fillna(footprint_median, inplace=True)
        
        # Continent ve Hemisphere eksik değerleri - Manuel kıta ataması
        country_continent_map = {
            'Turkey': 'Europe',
            'USA': 'America',
            'Germany': 'Europe',
            'France': 'Europe',
            'UK': 'Europe',
            'Italy': 'Europe',
            'Spain': 'Europe',
            'Australia': 'Oceania',
            'Indonesia': 'Asia',
            'India': 'Asia',
            'China': 'Asia',
            'South Africa': 'Africa',
            'Japan': 'Asia',
            'Brazil': 'America',
            'Canada': 'America',
            'Mexico': 'America',
            'Russia': 'Europe',
            'South Korea': 'Asia',
            'Saudi Arabia': 'Asia',
            'Argentina': 'America'
        }
        
        # Kıta bilgilerini manuel olarak düzelt
        for country, continent in country_continent_map.items():
            self.merged_df.loc[self.merged_df['Country'] == country, 'Continent'] = continent
        
        # Kalan eksik değerleri doldur
        self.merged_df['Continent'].fillna('Unknown', inplace=True)
        self.merged_df['Hemisphere'].fillna('Unknown', inplace=True)
        
        # Diğer eksik değerler
        numeric_cols = self.merged_df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if self.merged_df[col].isnull().sum() > 0:
                median_val = self.merged_df[col].median()
                self.merged_df[col].fillna(median_val, inplace=True)
                print(f"   {col}: {median_val:.2f} ile dolduruldu")
        
        print("✅ Eksik değerler dolduruldu")
        
    def ozellik_muhendisligi(self):
        """Özellik mühendisliği yap"""
        print("\n⚙️ Özellik mühendisliği yapılıyor...")
        
        # Per capita hesaplamaları (DÜZELTİLDİ)
        self.merged_df['Waste_Per_Capita_kg'] = self.merged_df['Avg Waste per Capita (Kg)']  # Orijinal veri zaten kg/kişi
        
        # Ekonomik kayıp per capita (DÜZELTİLDİ)
        # Economic Loss (Million $) zaten milyon USD cinsinde, nüfusa bölünce USD/kişi olur
        # Veri seti küçük ölçekte olduğu için gerçek dünya değerlerine uygun hale getiriyoruz
        self.merged_df['Economic_Loss_Per_Capita_USD'] = self.merged_df['Economic Loss (Million $)'] / self.merged_df['Population (Million)']
        
        # Carbon footprint hesaplama (DÜZELTİLDİ)
        # Gıda atığı kişi başına yıllık ~500-1000 kg CO2e yaratır (FAO, IPCC)
        # 1 ton gıda atığı ≈ 2.5 ton CO2e (daha gerçekçi)
        self.merged_df['Carbon_Footprint_kgCO2e'] = self.merged_df['Total Waste (Tons)'] * 2.5 * 1000  # kg CO2e per ton waste
        self.merged_df['Carbon_Per_Capita_kgCO2e'] = self.merged_df['Carbon_Footprint_kgCO2e'] / (self.merged_df['Population (Million)'] * 1000000)
        
        # Zaman özellikleri
        self.merged_df['Years_From_2018'] = self.merged_df['Year'] - 2018
        
        # Pandemi özellikleri
        self.merged_df['Is_Pandemic_Year'] = ((self.merged_df['Year'] >= 2020) & (self.merged_df['Year'] <= 2022)).astype(int)
        self.merged_df['Is_Post_Pandemic'] = (self.merged_df['Year'] >= 2023).astype(int)
        
        # Trend özellikleri
        self.merged_df['Year_Trend'] = self.merged_df['Year'] - 2018
        self.merged_df['Country_Trend'] = self.merged_df.groupby('Country')['Year'].rank()
        
        # Döngüsel özellikler
        self.merged_df['Year_Cycle'] = 2 * np.pi * self.merged_df['Year'] / 10
        self.merged_df['Year_Cycle_Cos'] = np.cos(self.merged_df['Year_Cycle'])
        
        # Etkileşim özellikleri (veri sızıntısı olmayan)
        self.merged_df['Population_Material_Interaction'] = self.merged_df['Population (Million)'] * self.merged_df['Material_Footprint_Per_Capita']
        self.merged_df['Year_Population_Interaction'] = self.merged_df['Years_From_2018'] * self.merged_df['Population (Million)']
        
        # Ekonomik ve sosyal özellikler
        self.merged_df['GDP_Per_Capita_Proxy'] = self.merged_df['Economic Loss (Million $)'] / self.merged_df['Population (Million)'] * 1000  # Proxy GDP
        self.merged_df['Waste_Efficiency'] = self.merged_df['Total Waste (Tons)'] / self.merged_df['Population (Million)']  # Waste per capita proxy
        self.merged_df['Economic_Intensity'] = self.merged_df['Economic Loss (Million $)'] / self.merged_df['Total Waste (Tons)']  # Economic loss per ton
        
        # Zaman bazlı trendler
        self.merged_df['Waste_Trend'] = self.merged_df.groupby('Country')['Total Waste (Tons)'].transform(lambda x: x.rolling(window=3, min_periods=1).mean())
        self.merged_df['Economic_Trend'] = self.merged_df.groupby('Country')['Economic Loss (Million $)'].transform(lambda x: x.rolling(window=3, min_periods=1).mean())
        
        # Kategori bazlı özellikler
        self.merged_df['Category_Waste_Share'] = self.merged_df.groupby(['Country', 'Year'])['Total Waste (Tons)'].transform(lambda x: x / x.sum())
        self.merged_df['Category_Economic_Share'] = self.merged_df.groupby(['Country', 'Year'])['Economic Loss (Million $)'].transform(lambda x: x / x.sum())
        
        # Sustainability Score hesaplama (gerçek dünya verilerine göre)
        def calculate_sustainability_score(row):
            # Gerçek dünya threshold'ları (veri setine göre ayarlandı)
            waste_threshold = 150  # kg/kişi/yıl (veri seti ortalaması: 109.5)
            economic_threshold = 40  # USD/kişi/yıl (veri seti ortalaması: 35.4)
            carbon_threshold = 0.5  # kg CO2e/kişi/yıl (veri seti ortalamasına göre)
            
            waste_score = max(0, 1 - (row['Waste_Per_Capita_kg'] / waste_threshold))
            economic_score = max(0, 1 - (row['Economic_Loss_Per_Capita_USD'] / economic_threshold))
            carbon_score = max(0, 1 - (row['Carbon_Per_Capita_kgCO2e'] / carbon_threshold))
            
            sustainability = (waste_score * 0.4 + economic_score * 0.3 + carbon_score * 0.3) * 100
            return max(0, min(100, sustainability))
        
        self.merged_df['Sustainability_Score'] = self.merged_df.apply(calculate_sustainability_score, axis=1)
        
        print("✅ Özellik mühendisliği tamamlandı")
        
    def aykiri_degerleri_isle(self):
        """Aykırı değerleri işle (winsorization)"""
        print("\n🔧 Aykırı değerler işleniyor...")
        
        # Aykırı değer işlenecek sütunlar
        outlier_cols = ['Waste_Per_Capita_kg', 'Economic_Loss_Per_Capita_USD', 'Carbon_Per_Capita_kgCO2e']
        
        for col in outlier_cols:
            if col in self.merged_df.columns:
                # 1. ve 99. percentile'ları hesapla
                p1 = self.merged_df[col].quantile(0.01)
                p99 = self.merged_df[col].quantile(0.99)
                
                # Aykırı değerleri kırp (winsorization)
                self.merged_df[col] = self.merged_df[col].clip(lower=p1, upper=p99)
                
                print(f"   {col}: %1-%99 aralığına kırpıldı ({p1:.6f} - {p99:.6f})")
        
        print("✅ Aykırı değerler işlendi")
        
    def aykiri_deger_tespiti(self):
        """Aykırı değerleri tespit et"""
        print("\n🔍 Aykırı değer tespiti yapılıyor...")
        
        # Aykırı değer raporu
        outlier_report = []
        
        numeric_cols = ['Total Waste (Tons)', 'Economic Loss (Million $)', 'Population (Million)', 
                       'Waste_Per_Capita_kg', 'Economic_Loss_Per_Capita_USD', 'Carbon_Per_Capita_kgCO2e']
        
        for col in numeric_cols:
            if col in self.merged_df.columns:
                Q1 = self.merged_df[col].quantile(0.25)
                Q3 = self.merged_df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = self.merged_df[(self.merged_df[col] < lower_bound) | (self.merged_df[col] > upper_bound)]
                
                outlier_report.append({
                    'Column': col,
                    'Outlier_Count': len(outliers),
                    'Percentage': len(outliers) / len(self.merged_df) * 100,
                    'Min_Outlier': outliers[col].min() if len(outliers) > 0 else None,
                    'Max_Outlier': outliers[col].max() if len(outliers) > 0 else None
                })
        
        # Raporu kaydet
        outlier_df = pd.DataFrame(outlier_report)
        outlier_df.to_csv('aykiri_deger_raporu.csv', index=False)
        print("✅ Aykırı değer raporu kaydedildi: aykiri_deger_raporu.csv")
        
        print("\n📊 Aykırı değer özeti:")
        print(outlier_df)
        
    def encoding_yap(self):
        """Kategorik değişkenleri encode et"""
        print("\n🔤 Encoding yapılıyor...")
        
        categorical_cols = ['Country', 'Food Category', 'Continent', 'Hemisphere']
        
        for col in categorical_cols:
            if col in self.merged_df.columns:
                le = LabelEncoder()
                self.merged_df[f'{col}_Encoded'] = le.fit_transform(self.merged_df[col])
                self.label_encoders[col] = le
                print(f"   {col}: {len(le.classes_)} kategori")
        
        print("✅ Encoding tamamlandı")
        
    def iso_kodlari_ekle(self):
        """ISO kodları ekle"""
        print("\n🌍 ISO kodları ekleniyor...")
        
        # Ülke isimlerini ISO kodlarına çeviren sözlük
        country_to_iso = {
            'Turkey': 'TUR',
            'USA': 'USA',
            'Germany': 'DEU',
            'France': 'FRA',
            'UK': 'GBR',
            'Italy': 'ITA',
            'Spain': 'ESP',
            'Australia': 'AUS',
            'Indonesia': 'IDN',
            'India': 'IND',
            'China': 'CHN',
            'South Africa': 'ZAF',
            'Japan': 'JPN',
            'Brazil': 'BRA',
            'Saudi Arabia': 'SAU',
            'Mexico': 'MEX',
            'Argentina': 'ARG',
            'Canada': 'CAN',
            'South Korea': 'KOR',
            'Russia': 'RUS'
        }
        
        # ISO kodları ekle
        self.merged_df['ISO_Code'] = self.merged_df['Country'].map(country_to_iso)
        
        # Eksik ISO kodları kontrol et
        missing_iso = self.merged_df[self.merged_df['ISO_Code'].isnull()]['Country'].unique()
        if len(missing_iso) > 0:
            print(f"⚠️ ISO kodu eksik ülkeler ({len(missing_iso)}):")
            for country in missing_iso:
                print(f"  - {country}")
        else:
            print("✅ Tüm ülkeler için ISO kodları mevcut")
        

        
    def dashboard_analizleri(self):
        """Dashboard için analizler yap"""
        print("\n📊 Dashboard analizleri yapılıyor...")
        
        # Kategori analizleri
        category_analyses = {}
        
        for category in self.merged_df['Food Category'].unique():
            cat_data = self.merged_df[self.merged_df['Food Category'] == category]
            
            analysis = {
                'total_waste': cat_data['Total Waste (Tons)'].sum(),
                'economic_loss': cat_data['Economic Loss (Million $)'].sum(),
                'carbon_footprint': cat_data['Carbon_Footprint_kgCO2e'].sum(),
                'avg_sustainability': cat_data['Sustainability_Score'].mean(),
                'country_count': cat_data['Country'].nunique(),
                'year_count': cat_data['Year'].nunique()
            }
            
            category_analyses[category] = analysis
        
        # JSON olarak kaydet
        import json
        with open('dashboard_category_analyses.json', 'w', encoding='utf-8') as f:
            json.dump(category_analyses, f, indent=2, ensure_ascii=False)
        
        print("✅ Kategori analizleri kaydedildi: dashboard_category_analyses.json")
        
        # Genel istatistikler
        general_stats = {
            'total_countries': self.merged_df['Country'].nunique(),
            'total_years': self.merged_df['Year'].nunique(),
            'total_categories': self.merged_df['Food Category'].nunique(),
            'total_records': len(self.merged_df),
            'avg_sustainability': self.merged_df['Sustainability_Score'].mean(),
            'total_waste': self.merged_df['Total Waste (Tons)'].sum(),
            'total_economic_loss': self.merged_df['Economic Loss (Million $)'].sum(),
            'total_carbon_footprint': self.merged_df['Carbon_Footprint_kgCO2e'].sum()
        }
        
        with open('dashboard_config.json', 'w', encoding='utf-8') as f:
            json.dump(general_stats, f, indent=2, ensure_ascii=False)
        
        print("✅ Genel istatistikler kaydedildi: dashboard_config.json")
        
    def kaydet(self):
        """Veri setini kaydet"""
        print("\n💾 Veri seti kaydediliyor...")
        
        # Ana veri setini kaydet
        self.merged_df.to_csv('data/ecolense_final_enriched_with_iso.csv', index=False)
        print("✅ Ana veri seti kaydedildi: data/ecolense_final_enriched_with_iso.csv")
        
        # Yedek olarak ISO'suz versiyonu da kaydet
        self.merged_df.to_csv('data/ecolense_final_enriched.csv', index=False)
        print("✅ Yedek veri seti kaydedildi: data/ecolense_final_enriched.csv")
        
        print(f"\n📊 Final veri seti özeti:")
        print(f"   Satır sayısı: {len(self.merged_df)}")
        print(f"   Sütun sayısı: {len(self.merged_df.columns)}")
        print(f"   Ülke sayısı: {self.merged_df['Country'].nunique()}")
        print(f"   Yıl aralığı: {self.merged_df['Year'].min()} - {self.merged_df['Year'].max()}")
        print(f"   Kategori sayısı: {self.merged_df['Food Category'].nunique()}")
        
    def calistir(self):
        """Tüm işlemleri çalıştır"""
        print("🚀 VERİ HAZIRLAMA BAŞLIYOR...")
        print("=" * 50)
        
        # 1. Veri yükleme
        self.veri_yukle()
        
        # 2. Veri analizi
        self.veri_analizi()
        
        # 3. Veri birleştirme
        self.veri_birlestir()
        
        # 4. Eksik değerleri doldur
        self.eksik_degerleri_doldur()
        
        # 5. Özellik mühendisliği
        self.ozellik_muhendisligi()
        
        # 6. Aykırı değerleri işle
        self.aykiri_degerleri_isle()
        
        # 7. Aykırı değer tespiti
        self.aykiri_deger_tespiti()
        
        # 8. Encoding
        self.encoding_yap()
        
        # 9. ISO kodları ekle
        self.iso_kodlari_ekle()
        
        # 10. Dashboard analizleri
        self.dashboard_analizleri()
        
        # 11. Kaydet
        self.kaydet()
        
        print("\n🎉 VERİ HAZIRLAMA TAMAMLANDI!")
        print("=" * 50)

if __name__ == "__main__":
    veri_hazirlama = VeriHazirlama()
    veri_hazirlama.calistir() 