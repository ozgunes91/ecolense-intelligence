#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard Pipeline Çalıştırma Scripti
=====================================

Bu script, dashboard için tam pipeline'ı çalıştırır:
1. Veri birleştirme ve analiz
2. Model eğitimi
3. Dashboard için hazırlık

Adımlar:
- İki veri setini birleştir
- Analiz et
- Boş değerleri doldur
- Özellik üret
- Zenginleştir
- Aykırı değer tespiti
- Encoding
- Model eğitimi
"""

import os
import sys
import subprocess
import time

def run_script(script_name, description):
    """Script çalıştırma fonksiyonu"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"📁 Script: {script_name}")
    print(f"{'='*60}")
    
    try:
        # Script'i çalıştır
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print(f"✅ {description} başarıyla tamamlandı!")
            print("\n📊 Çıktı:")
            print(result.stdout)
        else:
            print(f"❌ {description} başarısız!")
            print("\n🚨 Hata:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Script çalıştırma hatası: {e}")
        return False
    
    return True

def check_files():
    """Gerekli dosyaları kontrol et"""
    print("\n🔍 Gerekli dosyalar kontrol ediliyor...")
    
    required_files = [
        'data/global_food_wastage_dataset.csv',
        'data/material_footprint.csv'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Eksik dosyalar:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("✅ Tüm gerekli dosyalar mevcut!")
    return True

def main():
    """Ana çalıştırma fonksiyonu"""
    print("🚀 ECOLENSE DASHBOARD PIPELINE BAŞLIYOR...")
    print("=" * 70)
    print("📋 Pipeline Adımları:")
    print("   1. Veri hazırlama (birleştirme, analiz, encoding, ISO)")
    print("   2. Model eğitimi ve SHAP analizi")
    print("   3. A/B testing analizi")
    print("   4. Dashboard için hazırlık")
    print("=" * 70)
    
    # Dosya kontrolü
    if not check_files():
        print("\n❌ Pipeline başlatılamadı - eksik dosyalar!")
        return
    
    # Pipeline adımları
    pipeline_steps = [
        {
            'script': '01_veri_hazirlama.py',
            'description': 'Veri Hazırlama (Birleştirme, Analiz, Encoding, ISO)'
        },
        {
            'script': '02_model_egitimi.py',
            'description': 'Model Eğitimi ve SHAP Analizi'
        },
        {
            'script': '03_ab_testing_analizi.py',
            'description': 'A/B Testing Analizi'
        }
    ]
    
    # Her adımı çalıştır
    for i, step in enumerate(pipeline_steps, 1):
        print(f"\n📋 Adım {i}/{len(pipeline_steps)}: {step['description']}")
        
        if not run_script(step['script'], step['description']):
            print(f"\n❌ Pipeline adım {i} başarısız! Durduruluyor...")
            return
        
        # Kısa bekleme
        time.sleep(2)
    
    # Sonuç kontrolü
    print("\n🔍 Sonuç dosyaları kontrol ediliyor...")
    
    expected_files = [
        'data/ecolense_final_enriched_with_iso.csv',
        'data/ecolense_dashboard_data.csv',
        'ecolense_2025_2030_predictions_dashboard.csv',
        'model_performance_dashboard.json',
        'aykiri_deger_raporu.csv',
        'ab_testing_raporu.json',
        'ab_testing_sonuclari.csv'
    ]
    
    created_files = []
    for file_path in expected_files:
        if os.path.exists(file_path):
            created_files.append(file_path)
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} (eksik)")
    
    print(f"\n📊 Oluşturulan dosya sayısı: {len(created_files)}/{len(expected_files)}")
    
    if len(created_files) == len(expected_files):
        print("\n🎉 DASHBOARD PIPELINE BAŞARIYLA TAMAMLANDI!")
        print("=" * 70)
        print("📋 Oluşturulan Dosyalar:")
        for file_path in created_files:
            print(f"   ✅ {file_path}")
        
        print("\n🚀 Dashboard için hazır!")
        print("   - ecolense_dashboard_data.csv: Dashboard verisi")
        print("   - ecolense_2025_2030_predictions_dashboard.csv: Tahminler")
        print("   - model_performance_dashboard.json: Model raporu")
        print("   - aykiri_deger_raporu.csv: Aykırı değer raporu")
        print("   - ab_testing_raporu.json: A/B testing raporu")
        print("   - ab_testing_sonuclari.csv: A/B testing sonuçları")
        
        print("\n📊 Dashboard Entegrasyonu:")
        print("   1. ecolense_dashboard_data.csv dosyasını dashboard'a yükle")
        print("   2. ecolense_2025_2030_predictions_dashboard.csv tahminleri kullan")
        print("   3. Aykırı değer raporunu kontrol et")
        print("   4. Model performans raporunu incele")
        print("   5. A/B testing sonuçlarını analiz et")
        print("   6. SHAP analizlerini incele")
        
    else:
        print("\n⚠️ Pipeline tamamlandı ancak bazı dosyalar eksik!")
        print("Lütfen hata mesajlarını kontrol edin.")

if __name__ == "__main__":
    main() 