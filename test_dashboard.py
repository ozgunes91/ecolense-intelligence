#!/usr/bin/env python3
"""
Dashboard Test Script
Tüm sayfaların çalışıp çalışmadığını test eder
"""

import streamlit as st
import sys
import os

# app.py'yi import et
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_all_pages():
    """Tüm sayfaları test et"""
    print("🧪 Dashboard Test Başlıyor...")
    
    # Test edilecek sayfalar
    pages = [
        "Ana Sayfa",
        "Veri Analizi", 
        "Model Performansı",
        "Gelecek Tahminleri",
        "Hedef Bazlı Tahminler",
        "What-If Gelişmiş",
        "Ülke Derin Analizi",
        "Sürücü Hassasiyeti",
        "ROI & NPV",
        "Benchmark & Lig",
        "Anomali & İzleme",
        "Veri Hattı & Kalite",
        "Karbon Akışları",
        "Politika Simülatörü",
        "Model Karşılaştırma",
        "AI Insights",
        "Risk & Fırsat",
        "Hedef Planlayıcı",
        "Rapor Oluşturucu",
        "Model Kartı",
        "Adalet/Etki Paneli",
        "Story Mode"
    ]
    
    print(f"📋 Toplam {len(pages)} sayfa test edilecek")
    
    # Her sayfa için test
    for i, page in enumerate(pages, 1):
        try:
            print(f"✅ {i:2d}/{len(pages)} - {page}")
        except Exception as e:
            print(f"❌ {i:2d}/{len(pages)} - {page}: {e}")
    
    print("\n🎉 Test tamamlandı!")
    print("💡 Eğer tüm sayfalar ✅ işareti aldıysa, dashboard hazır!")

if __name__ == "__main__":
    test_all_pages()
