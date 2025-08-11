#!/usr/bin/env python3
"""
Dashboard Otomatik Kurulum Scripti
"""

import pandas as pd
import json
import os

def auto_setup_dashboard():
    """Dashboard'ı otomatik olarak hazırla"""
    
    print("🚀 Dashboard otomatik kurulum başlıyor...")
    
    # 1. ISO kodlarını ekle
    print("\n1️⃣ ISO kodları ekleniyor...")
    add_iso_codes()
    
    # 2. Dashboard veri setini hazırla
    print("\n2️⃣ Dashboard veri seti hazırlanıyor...")
    prepare_dashboard_data()
    
    # 3. Kategori analizlerini oluştur
    print("\n3️⃣ Kategori analizleri oluşturuluyor...")
    create_category_analyses()
    
    # 4. Dashboard konfigürasyonunu güncelle
    print("\n4️⃣ Dashboard konfigürasyonu güncelleniyor...")
    update_dashboard_config()
    
    print("\n✅ Dashboard otomatik kurulum tamamlandı!")

def add_iso_codes():
    """ISO kodlarını ekle"""
    country_to_iso = {
        'Turkey': 'TUR', 'United States': 'USA', 'Germany': 'DEU', 'France': 'FRA',
        'United Kingdom': 'GBR', 'Italy': 'ITA', 'Spain': 'ESP', 'Netherlands': 'NLD',
        'Belgium': 'BEL', 'Sweden': 'SWE', 'Norway': 'NOR', 'Denmark': 'DNK',
        'Finland': 'FIN', 'Switzerland': 'CHE', 'Austria': 'AUT', 'Poland': 'POL',
        'Czech Republic': 'CZE', 'Hungary': 'HUN', 'Romania': 'ROU', 'Bulgaria': 'BGR'
    }
    
    df = pd.read_csv('data/ecolense_final_enriched_with_iso.csv')
    country_col = [col for col in df.columns if 'country' in col.lower()][0]
    df['ISO_Code'] = df[country_col].map(country_to_iso)
    df.to_csv('data/ecolense_final_enriched_with_iso.csv', index=False)
    print(f"✅ ISO kodları eklendi: {len(df)} satır")

def prepare_dashboard_data():
    """Dashboard için veri setini hazırla"""
    df = pd.read_csv('data/ecolense_final_enriched_with_iso.csv')
    
    # Kategori analizleri için gruplamalar
    category_analyses = {}
    
    # En yüksek israf kategorisi (ülke bazında)
    if 'Food Category' in df.columns and 'Total Waste (Tons)' in df.columns:
        country_waste = df.groupby(['Country', 'Food Category'])['Total Waste (Tons)'].sum().reset_index()
        top_categories = country_waste.loc[country_waste.groupby('Country')['Total Waste (Tons)'].idxmax()]
        category_analyses['top_waste_category'] = top_categories.to_dict('records')
    
    # Kategori bazında toplam değerler
    if 'Food Category' in df.columns:
        category_totals = df.groupby('Food Category').agg({
            'Total Waste (Tons)': 'sum',
            'Economic Loss (Million $)': 'sum',
            'Carbon_Footprint_kgCO2e': 'sum'
        }).reset_index()
        category_analyses['category_totals'] = category_totals.to_dict('records')
    
    # Kategori analizlerini kaydet
    with open('category_analyses.json', 'w', encoding='utf-8') as f:
        json.dump(category_analyses, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Kategori analizleri oluşturuldu: {len(category_analyses)} analiz")

def create_category_analyses():
    """Kategori analizlerini oluştur"""
    df = pd.read_csv('data/ecolense_final_enriched_with_iso.csv')
    
    analyses = {}
    
    # 1. Ülke bazında en çok israf kategorisi
    if 'Food Category' in df.columns and 'Total Waste (Tons)' in df.columns:
        country_category_waste = df.groupby(['Country', 'Food Category'])['Total Waste (Tons)'].sum().reset_index()
        top_categories = country_category_waste.loc[country_category_waste.groupby('Country')['Total Waste (Tons)'].idxmax()]
        analyses['country_top_waste_category'] = top_categories.to_dict('records')
    
    # 2. Kategori bazında toplam değerler
    if 'Food Category' in df.columns:
        category_summary = df.groupby('Food Category').agg({
            'Total Waste (Tons)': 'sum',
            'Economic Loss (Million $)': 'sum', 
            'Carbon_Footprint_kgCO2e': 'sum'
        }).reset_index()
        analyses['category_summary'] = category_summary.to_dict('records')
    
    # 3. En yüksek değerli kategoriler
    if 'Food Category' in df.columns:
        max_waste_category = df.groupby('Food Category')['Total Waste (Tons)'].sum().idxmax()
        max_economic_category = df.groupby('Food Category')['Economic Loss (Million $)'].sum().idxmax()
        max_carbon_category = df.groupby('Food Category')['Carbon_Footprint_kgCO2e'].sum().idxmax()
        
        analyses['top_categories'] = {
            'max_waste': max_waste_category,
            'max_economic': max_economic_category,
            'max_carbon': max_carbon_category
        }
    
    # Analizleri kaydet
    with open('dashboard_category_analyses.json', 'w', encoding='utf-8') as f:
        json.dump(analyses, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Kategori analizleri oluşturuldu")

def update_dashboard_config():
    """Dashboard konfigürasyonunu güncelle"""
    config = {
        'data_source': 'data/ecolense_final_enriched_with_iso.csv',
        'has_iso_codes': True,
        'has_category_analyses': True,
        'total_rows': 5000,
        'total_countries': 20,
        'total_years': 7,
        'prediction_years': '2025-2030'
    }
    
    with open('dashboard_config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print("✅ Dashboard konfigürasyonu güncellendi")

if __name__ == "__main__":
    auto_setup_dashboard() 