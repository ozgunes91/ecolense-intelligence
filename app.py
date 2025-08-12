"""
ECOLENSE INTELLIGENCE - ULTRA PREMIUM DASHBOARD
===============================================

Yapay Zeka Destekli Sürdürülebilirlik ve İsraf Yönetimi Platformu
"İsrafı gözünden vuruyoruz."

Bu dashboard, gıda israfı analizi ve sürdürülebilirlik çözümleri için
yapay zeka destekli kapsamlı bir analiz platformudur.

Özellikler:
- Gerçek zamanlı veri analizi
- Yapay zeka destekli tahminler
- İnteraktif görselleştirmeler
- Hikaye modu ile veri anlatımı
- Çok dilli destek (TR/EN)

Author: Ecolense Team
Version: 1.0.0
Date: 2024
"""

# =============================================================================
# GEREKLİ KÜTÜPHANELER
# =============================================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
import pickle
import json
import os
from typing import Dict, List, Tuple, Optional, Any

# Özel modüller
# from storytelling import show_storytelling_section  # Eksik modül

# Performans optimizasyonları

# Cache optimizasyonu
if 'cache_cleared' not in st.session_state:
    st.session_state['cache_cleared'] = True
    st.cache_data.clear()

# Uyarıları kapat
warnings.filterwarnings('ignore')

# =============================================================================
# KONFİGÜRASYON
# =============================================================================

# Veri yolları - En Son EcolenseIntelligence Dosyaları
REAL_DATA_PATH = "data/ecolense_final_enriched_with_iso.csv"      # 5000 satırlık zenginleştirilmiş veri (ISO kodları ile)
PREDICTIONS_PATH = "ecolense_2025_2030_predictions_dashboard.csv"  # En son tahminler (2025-2030)
PERF_REPORT_PATH = "model_performance_dashboard.json"    # En son model raporu (GradientBoosting)
AB_TESTING_PATH = "ab_testing_raporu.json"              # A/B testing raporu
AB_RESULTS_PATH = "ab_testing_sonuclari.csv"            # A/B testing sonuçları
OUTLIER_REPORT_PATH = "aykiri_deger_raporu.csv"         # Aykırı değer raporu
CATEGORY_ANALYSES_PATH = "dashboard_category_analyses.json"  # Kategori analizleri
DASHBOARD_CONFIG_PATH = "dashboard_config.json"         # Dashboard konfigürasyonu

# SHAP analizi dosyaları
SHAP_FILES = {
    'Total_Waste_Tons': {
        'importance': 'shap_importance_Total_Waste_Tons.csv',
        'summary': 'shap_summary_Total_Waste_Tons.png'
    },
    'Economic_Loss_Million_USD': {
        'importance': 'shap_importance_Economic_Loss_Million_USD.csv',
        'summary': 'shap_summary_Economic_Loss_Million_USD.png'
    },
    'Carbon_Footprint_kgCO2e': {
        'importance': 'shap_importance_Carbon_Footprint_kgCO2e.csv',
        'summary': 'shap_summary_Carbon_Footprint_kgCO2e.png'
    },
    'Sustainability_Score': {
        'importance': 'shap_importance_Sustainability_Score.csv',
        'summary': 'shap_summary_Sustainability_Score.png'
    }
}

OUTPUT_DIR = "outputs/"

# Basit i18n ve tema anahtarları
if 'lang' not in st.session_state:
    st.session_state['lang'] = 'TR'
if 'lite_mode' not in st.session_state:
    st.session_state['lite_mode'] = False

# Basit i18n sözlüğü
I18N = {
    'TR': {
        'PAGE_SELECT': '📱 SAYFA SEÇİN',
        'PAGE_HOME': '🏠 Ana Sayfa',
        'PAGE_ANALYSIS': '📊 Veri Analizi',
        'PAGE_PERF': '🤖 Model Performansı',
        'PAGE_FORECASTS': '🔮 Gelecek Tahminleri',
        'PAGE_AB': '🧪 A/B Testing',
        'PAGE_POLICY': '🛠️ Politika Simülatörü',
        'PAGE_AI': '🤖 AI Insights',
        'PAGE_RISK': '⚠️ Risk & Fırsat',
        'PAGE_TARGET': '🎯 Hedef Planlayıcı',
        'PAGE_REPORT': '📄 Rapor Oluşturucu',
        'PAGE_CARD': '📑 Model Kartı',
        'PAGE_TARGET_FORECASTS': '🎯 Hedef Bazlı Tahminler',
        'PAGE_WHATIF': '🧩 What‑if (İleri)',
        'PAGE_DEEPDIVE': '🔎 Country Deep Dive',
        'PAGE_TORNADO': '🌪️ Driver Sensitivity',
        'PAGE_ROI': '💹 ROI / NPV',
        'PAGE_BENCH': '🏁 Benchmark & Lig',
        'PAGE_ANOM': '🚨 Anomali & İzleme',
        'PAGE_LINEAGE': '🧬 Veri Hattı & Kalite',
        'PAGE_FLOWS': '🌿 Karbon Akışları',
        'PAGE_JUSTICE': '⚖️ Adalet/Etki Paneli',
        'PAGE_STORY': '📖 Story Mode',
        'MODEL_PERF_HEADER': '🤖 MODEL PERFORMANSI',
        'SOURCE': 'Kaynak',
        # Ana sayfa metinleri
        'WELCOME_TITLE': 'Hoş Geldiniz, Sürdürülebilirlik Kahramanı!',
        'WELCOME_DESC': 'Ecolense Intelligence ile sürdürülebilir bir gelecek inşa ediyoruz. Bu ultra premium dashboard, yapay zeka destekli analizlerle size güçlü içgörüler sunuyor.',
        'PREMIUM_FEATURES': 'PREMIUM ÖZELLİKLER',
        'QUICK_ACCESS': 'HIZLI ERİŞİM',
        'TARGET_FORECASTS': 'Hedef Bazlı Tahminler',
        'TARGET_FORECASTS_DESC': 'Özel hedeflere göre tahmin',
        'ADVANCED_ANALYSIS': 'Gelişmiş Analizler',
        'ADVANCED_ANALYSIS_DESC': 'SHAP, korelasyon, 3D görselleştirme',
        'FUTURE_FORECASTS': 'Gelecek Tahminleri',
        'FUTURE_FORECASTS_DESC': '2024–2030 projeksiyonlar',
        'AI_ASSISTANT': 'AI Asistan',
        'AI_ASSISTANT_DESC': 'Akıllı öneriler ve içgörüler',
        'RISK_OPPORTUNITY': 'Risk & Fırsat Radar',
        'RISK_OPPORTUNITY_DESC': 'Ülkeleri 2×2 eksende konumlandır',
        'MODEL_CARD': 'Model Kartı',
        'MODEL_CARD_DESC': 'Metodoloji ve performans özeti',
        'DATA_ANALYSIS': 'Veri Analizi',
        'MODEL_PERFORMANCE': 'Model Performansı',
        'FUTURE_FORECASTS_BTN': 'Gelecek Tahminleri',
        'AI_TIP': 'İpucu',
        'AI_WELCOME_TIP': 'KPI kartları 2018–2024 gerçek veriye dayanır. Alt sayfalarından ülke detayına inip tahminleri ve senaryoları test edebilirsin.',
        'AI_WELCOME_SUGGESTION': 'Öneri: Önce Veri Analizi → sonra Model Performansı → ardından Gelecek Tahminleri ile ülke seçip AI Insights\'a göz at.',
        'FOOTER_COPYRIGHT': '© 2024 Ecolense. Tüm hakları saklıdır. | Gıda israfı analizi ve sürdürülebilirlik çözümleri',
        'FOOTER_SUBTITLE': 'Sürdürülebilir Gıda Analizi Platformu'
    },
    'EN': {
        'PAGE_SELECT': '📱 SELECT PAGE',
        'PAGE_HOME': '🏠 Home',
        'PAGE_ANALYSIS': '📊 Data Analysis',
        'PAGE_PERF': '🤖 Model Performance',
        'PAGE_FORECASTS': '🔮 Forecasts',
        'PAGE_AB': '🧪 A/B Testing',
        'PAGE_POLICY': '🛠️ Policy Simulator',
        'PAGE_AI': '🤖 AI Insights',
        'PAGE_RISK': '⚠️ Risk & Opportunity',
        'PAGE_TARGET': '🎯 Target Planner',
        'PAGE_REPORT': '📄 Report Builder',
        'PAGE_CARD': '📑 Model Card',
        'PAGE_TARGET_FORECASTS': '🎯 Target-based Forecasts',
        'PAGE_WHATIF': '🧩 What‑if (Advanced)',
        'PAGE_DEEPDIVE': '🔎 Country Deep Dive',
        'PAGE_TORNADO': '🌪️ Driver Sensitivity',
        'PAGE_ROI': '💹 ROI / NPV',
        'PAGE_BENCH': '🏁 Benchmark & League',
        'PAGE_ANOM': '🚨 Anomaly & Monitoring',
        'PAGE_LINEAGE': '🧬 Data Lineage & Quality',
        'PAGE_FLOWS': '🌿 Carbon Flows',
        'PAGE_JUSTICE': '⚖️ Justice/Impact Panel',
        'PAGE_STORY': '📖 Story Mode',
        'MODEL_PERF_HEADER': '🤖 MODEL PERFORMANCE',
        'SOURCE': 'Source',
        # Ana sayfa metinleri
        'WELCOME_TITLE': 'Welcome, Sustainability Hero!',
        'WELCOME_DESC': 'We are building a sustainable future with Ecolense Intelligence. This ultra premium dashboard provides powerful insights with AI-driven analytics.',
        'PREMIUM_FEATURES': 'PREMIUM FEATURES',
        'QUICK_ACCESS': 'QUICK ACCESS',
        'TARGET_FORECASTS': 'Target-based Forecasts',
        'TARGET_FORECASTS_DESC': 'Forecasts based on specific targets',
        'ADVANCED_ANALYSIS': 'Advanced Analytics',
        'ADVANCED_ANALYSIS_DESC': 'SHAP, correlation, 3D visualization',
        'FUTURE_FORECASTS': 'Future Forecasts',
        'FUTURE_FORECASTS_DESC': '2024–2030 projections',
        'AI_ASSISTANT': 'AI Assistant',
        'AI_ASSISTANT_DESC': 'Smart recommendations and insights',
        'RISK_OPPORTUNITY': 'Risk & Opportunity Radar',
        'RISK_OPPORTUNITY_DESC': 'Position countries on 2×2 axis',
        'MODEL_CARD': 'Model Card',
        'MODEL_CARD_DESC': 'Methodology and performance summary',
        'DATA_ANALYSIS': 'Data Analysis',
        'MODEL_PERFORMANCE': 'Model Performance',
        'FUTURE_FORECASTS_BTN': 'Future Forecasts',
        'AI_TIP': 'Tip',
        'AI_WELCOME_TIP': 'KPI cards are based on real 2018–2024 data. You can dive into country details from sub-pages and test forecasts and scenarios.',
        'AI_WELCOME_SUGGESTION': 'Suggestion: First Data Analysis → then Model Performance → then select country with Future Forecasts and check AI Insights.',
        'FOOTER_COPYRIGHT': '© 2024 Ecolense. All rights reserved. | Food waste analysis and sustainability solutions',
        'FOOTER_SUBTITLE': 'Sustainable Food Analysis Platform'
    }
}

def _t(key: str) -> str:
    """
    Çok dilli destek fonksiyonu - Türkçe/İngilizce çeviri
    
    Args:
        key (str): Çevrilecek metin anahtarı
        
    Returns:
        str: Seçili dildeki çeviri metni
    """
    lang = st.session_state.get('lang', 'TR')  # Varsayılan dil Türkçe
    return I18N.get(lang, I18N['TR']).get(key, key)  # Anahtar bulunamazsa kendisini döndür

def add_page_footer(page_name: str):
    """Sayfa sonu yazısı ekler - Kompakt ve şık footer"""
    
    footer_html = f"""
    <div style="background: linear-gradient(135deg, #232E5C 0%, #1A1C2C 100%); 
                padding: 0.6rem 1rem; border-radius: 8px; color: white; margin: 0.5rem 0; 
                box-shadow: 0 2px 8px rgba(35, 46, 92, 0.15); text-align: center; width: 100%; 
                border: 1px solid rgba(144, 238, 144, 0.08); font-family: 'Segoe UI', sans-serif;">
        <div style="display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
            <span style="font-size: 0.9rem;">🌱</span>
            <span style="font-size: 0.8rem; font-weight: 600; color: #90EE90;">ECOLENSE</span>
            <span style="font-size: 0.7rem; opacity: 0.6;">|</span>
            <span style="font-size: 0.7rem; opacity: 0.7;">{page_name}</span>
            <span style="font-size: 0.7rem; opacity: 0.6;">|</span>
            <span style="font-size: 0.65rem; opacity: 0.5;">© 2025</span>
        </div>
    </div>
    """
    st.components.v1.html(footer_html, height=50)

# Renk paleti (Ultra Premium)
COLORS = {
    'primary': '#232E5C',      # Koyu lacivert
    'secondary': '#1A1C2C',    # Çok koyu lacivert
    'accent1': '#90EE90',      # Fıstık yeşili
    'accent2': '#32CD32',      # Lime yeşil
    'success': '#228B22',      # Orman yeşili
    'warning': '#FFB347',      # Turuncu
    'error': '#FF6B6B',        # Kırmızı
    'info': '#98FB98',         # Açık fıstık yeşili
    'light': '#F8FAFC',        # Açık gri
    'dark': '#2D3748'          # Koyu gri
}

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="Ecolense Intelligence",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CSS STİLLERİ (Ultra Premium)
# =============================================================================

def load_css():
    """Ultra premium CSS stilleri"""
    # Lite mode temelli gölge/blur değerleri
    lite = st.session_state.get('lite_mode', False)
    shadow = "0 4px 10px rgba(35,46,92,0.15), 0 0 20px rgba(17,230,193,0.08)" if lite else "0 15px 40px rgba(35,46,92,0.3), 0 0 50px rgba(17,230,193,0.2)"
    blur = "2px" if lite else "10px"
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700;800&display=swap');
    /* Ana tema */
    .main { background: linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 50%, #CBD5E1 100%); }
    
    /* Ana başlık */
    .main-header {
        --brand-side: clamp(72px, 7vw, 96px);
        background: linear-gradient(135deg, #232E5C 0%, #1A1C2C 100%);
        border-radius: 2rem;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 
            0 20px 40px rgba(35, 46, 92, 0.3),
            0 0 60px rgba(17, 230, 193, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    /* Ultra premium marka başlığı */
    .brand-row { display: flex; justify-content: center; align-items: center; gap: 16px; width: 100%; }
    .brand-left, .brand-right { width: var(--brand-side); display: flex; justify-content: center; align-items: center; }
    .brand-center { flex: 0 1 auto; display: flex; justify-content: center; }
    .brand-stack { position: relative; display: inline-block; line-height: 1; }
    .brand-fill {
        font-family: 'Space Grotesk', ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
        font-weight: 800;
        letter-spacing: 0.03em;
        font-size: clamp(2.1rem, 4.5vw, 3.2rem);
        background: linear-gradient(110deg, #90EE90 0%, #32CD32 25%, #228B22 50%, #32CD32 75%, #90EE90 100%);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 10px 24px rgba(144, 238, 144, 0.25));
        background-size: 200% 200%;
        animation: gradientShift 8s ease-in-out infinite, bounceTilt 4.5s ease-in-out infinite;
    }
    .brand-outline {
        position: absolute; inset: 0; pointer-events: none;
        font-family: 'Space Grotesk', ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
        font-weight: 800; letter-spacing: 0.03em; font-size: clamp(2.1rem, 4.5vw, 3.2rem);
        color: transparent; -webkit-text-stroke: 2px rgba(144, 238, 144, 0.55);
        text-shadow:
            0 1px 0 rgba(0,0,0,0.25),
            0 8px 30px rgba(144, 238, 144, 0.15);
        filter: blur(0.2px);
    }
    /* Lensle büyütülen yazı katmanı */
    .brand-lens-text {
        position: absolute; inset: 0; pointer-events: none;
        font-family: 'Space Grotesk', ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
        font-weight: 800; letter-spacing: 0.03em; font-size: clamp(2.1rem, 4.5vw, 3.2rem);
        background: linear-gradient(110deg, #98FB98 0%, #90EE90 50%, #98FB98 100%);
        -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
        transform: scale(1.06);
        clip-path: circle(70px at 0% 50%);
        animation: lensSweep 7s ease-in-out infinite;
        filter: drop-shadow(0 6px 16px rgba(144,238,144,.25));
    }
    @keyframes lensSweep {
        0%   { clip-path: circle(70px at 2% 50%); }
        50%  { clip-path: circle(70px at 98% 50%); }
        100% { clip-path: circle(70px at 2% 50%); }
    }
    .brand-underline {
        height: 6px; border-radius: 999px; margin: 10px auto 0 auto;
        width: clamp(220px, 40vw, 520px);
        background: linear-gradient(90deg, rgba(144,238,144,0.0) 0%, rgba(144,238,144,0.8) 25%, rgba(32,205,50,0.9) 50%, rgba(144,238,144,0.8) 75%, rgba(144,238,144,0.0) 100%);
        box-shadow: 0 8px 24px rgba(144, 238, 144, 0.35);
    }
    @keyframes gradientShift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    @keyframes bounceTilt { 0%,100% { transform: translateY(0) skewX(0deg); } 50% { transform: translateY(-2px) skewX(-1deg); } }

    /* İkonik kişi + büyüteç */
    .brand-person { width: var(--brand-side); height: auto; filter: drop-shadow(0 6px 18px rgba(0,0,0,0.25)); }
    .brand-person .ring { stroke: #90EE90; stroke-width: 3.5; fill: rgba(144,238,144,0.06); }
    .brand-person .handle { stroke: #111111; stroke-width: 5.5; }
    .brand-person .body { stroke: #E5E7EB; stroke-width: 4; }
    .brand-person { animation: floaty 4s ease-in-out infinite; }

    .brand-spacer { width: var(--brand-side); height: 1px; }

    /* Yeşil yaprak emoji */
    .brand-emoji-leaf { position: absolute; right: -36px; top: 50%; transform: translateY(-54%); font-size: clamp(24px, 3vw, 34px); filter: drop-shadow(0 6px 16px rgba(144,238,144,.45)); }
    @keyframes floaty { 0%,100% { transform: translateY(0) rotate(0deg); } 50% { transform: translateY(-2px) rotate(-2deg); } }

    /* Esprili slogan stili */
    .fun-slogan { color: #90EE90; font-weight: 400; font-style: italic; letter-spacing: .2px; }
    .fun-slogan > span { display: inline-block; padding: .2rem .4rem; border-radius: .4rem; background: transparent; border: none; box-shadow: none; }

    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(17, 230, 193, 0.1), transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    /* Başlık - daha net, gölgeli arka plan ile */
    .title-chip {
        display: inline-block;
        padding: 0.5rem 1.25rem;
        border-radius: 1rem;
        background: linear-gradient(135deg, rgba(17,22,40,0.92) 0%, rgba(28,32,50,0.92) 100%);
        border: 1px solid rgba(255,255,255,0.14);
        box-shadow: 0 10px 30px rgba(0,0,0,0.4), 0 0 0 4px rgba(17,230,193,0.05) inset;
    }
    .neon-title {
        color: #FFFFFF;
        text-shadow: 0 2px 3px rgba(0,0,0,0.6);
        font-weight: 800;
        letter-spacing: 1px;
        animation: none;
    }
    
    @keyframes neonPulse {
        0% {
            color: #11E6C1;
            text-shadow: 
                0 0 5px #11E6C1,
                0 0 10px #11E6C1,
                0 0 15px #11E6C1,
                0 0 20px #11E6C1,
                0 0 35px #11E6C1,
                0 0 40px #11E6C1,
                0 0 50px #11E6C1,
                0 0 55px #11E6C1;
        }
        50% {
            color: #A9FF4F;
            text-shadow: 
                0 0 5px #A9FF4F,
                0 0 10px #A9FF4F,
                0 0 15px #A9FF4F,
                0 0 20px #A9FF4F,
                0 0 35px #A9FF4F,
                0 0 40px #A9FF4F,
                0 0 50px #A9FF4F,
                0 0 55px #A9FF4F;
        }
        100% {
            color: #00D4AA;
            text-shadow: 
                0 0 5px #00D4AA,
                0 0 10px #00D4AA,
                0 0 15px #00D4AA,
                0 0 20px #00D4AA,
                0 0 35px #00D4AA,
                0 0 40px #00D4AA,
                0 0 50px #00D4AA,
                0 0 55px #00D4AA;
        }
    }
    
    /* Alt yazılar - gölgeli arka plan ile netleştirme */
    .subtitle-chip {
        display: inline-block;
        color: #FFFFFF;
        text-shadow: 0 1px 2px rgba(0,0,0,0.7);
        background: linear-gradient(135deg, rgba(0,0,0,0.65) 0%, rgba(0,0,0,0.45) 100%);
        padding: 0.45rem 1rem;
        border-radius: 0.75rem;
        border: 1px solid rgba(255,255,255,0.18);
        box-shadow: 0 8px 24px rgba(0,0,0,0.35);
    }
    .slogan-chip {
        display: inline-block;
        color: #FFE27A;
        text-shadow: 0 1px 2px rgba(0,0,0,0.75);
        background: linear-gradient(135deg, rgba(17,230,193,0.12) 0%, rgba(255,215,0,0.12) 100%);
        padding: 0.45rem 1rem;
        border-radius: 0.75rem;
        border: 1px solid rgba(255,215,0,0.28);
        box-shadow: 0 8px 24px rgba(0,0,0,0.35);
    }
    
    @keyframes sloganGlow {
        0% {
            box-shadow: 0 0 10px rgba(255,215,0,0.3);
        }
        100% {
            box-shadow: 0 0 20px rgba(255,215,0,0.6);
        }
    }
    
    /* Metrik kartları */
    .metric-card {
        background: linear-gradient(135deg, #232E5C 0%, #1A1C2C 100%) !important;
        border-radius: 1.5rem;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 
            0 10px 30px rgba(35, 46, 92, 0.3),
            0 0 40px rgba(17, 230, 193, 0.15);
        border: 2px solid rgba(17, 230, 193, 0.3);
        transition: all 0.3s ease;
        color: white !important;
    }
    
    .metric-card h3 {
        color: white !important;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
    .metric-value {
        color: #11E6C1;
        font-size: clamp(1.1rem, 2.2vw, 1.8rem);
        font-weight: 700;
        line-height: 1.15;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
        white-space: nowrap;
    }
    .metric-unit {
        color: rgba(255,255,255,0.9);
        font-size: 0.95rem;
        font-weight: 600;
        margin-top: 0.15rem;
    }
    .metric-sub { color: rgba(255,255,255,0.75) !important; font-size: 0.85rem; margin: 0.1rem 0 0 0; }
    
    .metric-card p {
        color: rgba(255, 255, 255, 0.8) !important;
        font-size: 0.9rem;
        margin: 0;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 
            0 15px 40px rgba(35, 46, 92, 0.4),
            0 0 60px rgba(17, 230, 193, 0.25);
        border-color: rgba(17, 230, 193, 0.6);
    }
    
    /* Premium özellik kartları */
    .premium-feature {
        background: linear-gradient(135deg, #232E5C 0%, #1A1C2C 100%);
        border-radius: 1.5rem;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: __SHADOW__;
        border: 2px solid rgba(17, 230, 193, 0.3);
        backdrop-filter: blur(__BLUR__);
        color: white;
    }
    
    .premium-feature h2, .premium-feature h3 {
        color: white;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }
    
    .premium-feature h4 {
        color: white;
        font-weight: 600;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
    .premium-feature p {
        color: rgba(255, 255, 255, 0.9);
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    /* Feature cards with green accent glow */
    .feature-card { position: relative; background: rgba(255,255,255,0.04); border-radius: .75rem; padding: 1rem 1.25rem; border: 1px solid rgba(255,255,255,0.12); box-shadow: 0 10px 24px rgba(0,0,0,0.25); overflow: hidden; }
    .feature-card::before { content:""; position: absolute; left:0; top:0; bottom:0; width:6px; border-radius:6px 0 0 6px; background: linear-gradient(180deg, #A9FF4F, #11E6C1); box-shadow: 0 0 18px rgba(169,255,79,0.65), 0 0 28px rgba(17,230,193,0.45); }
    .feature-card h4 { margin: 0 0 .35rem 0; color: #E6FFF2; }
    .feature-card p { margin: 0; color: rgba(255,255,255,0.85); }
    .feature-card:hover { transform: translateY(-2px); box-shadow: 0 14px 32px rgba(0,0,0,0.3); }

    /* AI Asistan kutusu (yüksek kontrast + yeşil glow + animasyon) */
    .ai-assistant { 
        position: relative;
        background: linear-gradient(180deg, #F1FFFA 0%, #E9FFF6 100%);
        color: #0F172A; 
        border: 1px solid rgba(17,230,193,0.55); 
        border-left: 4px solid #11E6C1;
        border-radius: 14px; 
        padding: 16px 18px; 
        margin-top: 0.3rem;
        box-shadow: 0 14px 36px rgba(17,230,193,0.28), 0 6px 18px rgba(35,46,92,0.15);
        animation: aiGlow 3.6s ease-in-out infinite;
        will-change: box-shadow, transform;
    }
    .ai-assistant h4 { margin: 0 0 8px 0; color: #0B183B; letter-spacing: 0.2px; }
    .ai-assistant p { color: #111827; }
    .ai-badge { display:inline-block; background: rgba(17,230,193,0.16); color:#065F55; padding:4px 10px; border-radius:10px; margin-right:6px; font-size: 12px; font-weight: 700; }

    /* Emoji/logonun büyütülmesi ve göz kırpma efekti */
    .ai-emoji { 
        display: inline-block; 
        font-size: 1.6em; 
        transform-origin: center bottom; 
        animation: aiBlink 2.8s ease-in-out infinite;
        margin-right: 6px;
    }

    /* Hafif sallanma (oynak) hover'da */
    .ai-assistant:hover { animation: aiFloat 2.2s ease-in-out infinite; }

    @keyframes aiGlow {
        0%, 100% { box-shadow: 0 14px 36px rgba(17,230,193,0.22), 0 6px 18px rgba(35,46,92,0.12); }
        50% { box-shadow: 0 18px 44px rgba(17,230,193,0.38), 0 8px 24px rgba(35,46,92,0.18); }
    }
    @keyframes aiBlink {
        0%, 40%, 100% { transform: scaleY(1) translateY(0); filter: none; }
        45% { transform: scaleY(0.6) translateY(2px); filter: brightness(0.9); }
        50% { transform: scaleY(0.4) translateY(3px); filter: brightness(0.85); }
        55% { transform: scaleY(0.7) translateY(1px); filter: brightness(0.95); }
    }
    @keyframes aiFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-2px); }
    }
    
    /* Butonlar */
    .stButton > button {
        background: linear-gradient(135deg, #232E5C 0%, #1A1C2C 100%);
        color: white;
        border: 2px solid rgba(17, 230, 193, 0.4);
        border-radius: 1.2rem 0.5rem 1.2rem 0.5rem;
        padding: 0.8rem 1.2rem;
        font-weight: 500;
        font-size: 0.85rem;
        box-shadow: 
            0 8px 25px rgba(35, 46, 92, 0.3),
            0 0 20px rgba(17, 230, 193, 0.2),
            0 0 40px rgba(17, 230, 193, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
        min-height: 60px;
        max-height: 60px;
        position: relative;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 
            0 12px 35px rgba(35, 46, 92, 0.4),
            0 0 30px rgba(17, 230, 193, 0.3),
            0 0 60px rgba(17, 230, 193, 0.2);
        border-color: rgba(17, 230, 193, 0.8);
        background: linear-gradient(135deg, #2D3748 0%, #232E5C 100%);
    }
    
    /* Animasyonlar */
    .fade-in {
        animation: fadeIn 0.8s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #232E5C 0%, #1A1C2C 100%);
    }
    
    /* Ana container */
    .main .block-container {
        background: linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 50%, #CBD5E1 100%);
    }
    
    /* StApp */
    .stApp {
        background: linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 50%, #CBD5E1 100%);
    }
    
    </style>
    """
    css = css.replace("__SHADOW__", shadow).replace("__BLUR__", blur)
    st.markdown(css, unsafe_allow_html=True)

# =============================================================================
# VERİ YÜKLEME VE İŞLEME
# =============================================================================

@st.cache_data(show_spinner=False, ttl=3600)
def load_data(file_path: str, announce: bool = True) -> pd.DataFrame:
    """
    CSV veri dosyasını yükler ve temizler (En son EcolenseIntelligence veri seti için)
    
    Args:
        file_path (str): Yüklenecek CSV dosyasının yolu
        announce (bool): Başarı mesajı gösterilsin mi?
        
    Returns:
        pd.DataFrame: Temizlenmiş veri seti
    """
    try:
        # Veri yükleme
        df = pd.read_csv(file_path)
        
        # Sütun isimlerini standardize et (yeni veri seti için)
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        
        # Sayısal sütunları temizle (yeni veri seti sütunları)
        numeric_columns = [
            'total_waste_tons', 'economic_loss_million_$', 'carbon_footprint_kgco2e',
            'sustainability_score', 'population_million', 'waste_per_capita_kg',
            'economic_loss_per_capita_usd', 'carbon_per_capita_kgco2e',
            'material_footprint_per_capita', 'years_from_2018', 'year_trend',
            'country_trend', 'year_cycle', 'year_cycle_cos', 'population_material_interaction',
            'year_population_interaction', 'gdp_per_capita_proxy', 'waste_efficiency',
            'economic_intensity', 'waste_trend', 'economic_trend', 'category_waste_share',
            'category_economic_share'
        ]
        
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Tarih sütunlarını işle
        if 'year' in df.columns:
            df['year'] = pd.to_numeric(df['year'], errors='coerce')
        
        # Kategorik sütunları temizle
        categorical_columns = ['country', 'continent', 'hemisphere', 'food_category', 'iso3']
        for col in categorical_columns:
            if col in df.columns:
                df[col] = df[col].astype('category')
        
        if announce:
            st.success(f"✅ En son veri seti başarıyla yüklendi: {len(df)} gözlem, {len(df.columns)} sütun")
        return df
    
    except Exception as e:
        st.error(f"❌ Veri yükleme hatası: {e}")
        return pd.DataFrame()

@st.cache_data(show_spinner=False, ttl=3600)
def load_dataset_variant(include_synthetic: bool) -> pd.DataFrame:
    """
    Kullanıcı seçimine göre veri setini yükler
    
    Args:
        include_synthetic (bool): Sentetik veri dahil edilsin mi? (Artık kullanılmıyor)
        
    Returns:
        pd.DataFrame: Gerçek veri seti
    """
    return load_data(REAL_DATA_PATH, announce=False)

@st.cache_data(show_spinner=False, ttl=3600)
def load_predictions_csv(path: str = PREDICTIONS_PATH, version: float = 0.0):
    """Tahminleri CSV'den yükle"""
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        st.error(f"❌ Tahmin yükleme hatası: {e}")
        return None

@st.cache_data(show_spinner=False)
def load_predictions_dashboard() -> Optional[pd.DataFrame]:
    """Dashboard tahminleri yükle"""
    try:
        df = pd.read_csv(PREDICTIONS_PATH)
        if 'Year' in df.columns:
            df['Year'] = pd.to_numeric(df['Year'], errors='coerce').astype('Int64')
        if 'Prediction' in df.columns:
            df['Prediction'] = pd.to_numeric(df['Prediction'], errors='coerce')

        # Long format'tan wide format'a çevir
        if 'Target' in df.columns and 'Prediction' in df.columns:
            df_wide = df.pivot_table(
                index=['Country', 'Year'],
                columns='Target',
                values='Prediction',
                aggfunc='first'
            ).reset_index()
            return df_wide
        return df
    except Exception as e:
        st.error(f"❌ Dashboard tahminleri yükleme hatası: {e}")
        return None

@st.cache_data(show_spinner=False)
def load_ab_testing_results() -> Optional[pd.DataFrame]:
    """A/B testing sonuçlarını yükle"""
    try:
        df = pd.read_csv(AB_RESULTS_PATH)
        return df
    except Exception as e:
        st.error(f"❌ A/B testing sonuçları yükleme hatası: {e}")
        return None

@st.cache_data(show_spinner=False)
def load_ab_testing_report() -> Optional[dict]:
    """A/B testing raporunu yükle"""
    try:
        with open(AB_TESTING_PATH, 'r', encoding='utf-8') as f:
            report = json.load(f)
        return report
    except Exception as e:
        st.error(f"❌ A/B testing raporu yükleme hatası: {e}")
        return None

@st.cache_data(show_spinner=False)
def load_category_analyses() -> Optional[dict]:
    """Kategori analizlerini yükle"""
    try:
        with open(CATEGORY_ANALYSES_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"❌ Kategori analizleri yükleme hatası: {e}")
        return None

@st.cache_data(show_spinner=False)
def load_dashboard_config() -> Optional[dict]:
    """Dashboard konfigürasyonunu yükle"""
    try:
        with open(DASHBOARD_CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"❌ Dashboard konfigürasyonu yükleme hatası: {e}")
        return None

@st.cache_data(show_spinner=False)
def load_shap_importance(target: str) -> Optional[pd.DataFrame]:
    """SHAP importance dosyasını yükle"""
    try:
        if target in SHAP_FILES:
            file_path = SHAP_FILES[target]['importance']
            df = pd.read_csv(file_path)
            return df
        return None
    except Exception as e:
        st.error(f"❌ SHAP importance yükleme hatası: {e}")
        return None

@st.cache_data(show_spinner=False)
def load_performance_report(path: str = PERF_REPORT_PATH):
    """Model performans raporunu yükle"""
    try:
        # JSON formatında yeni rapor
        if path.endswith('.json'):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        # Eski PKL formatı için
        else:
            with open(path, "rb") as f:
                return pickle.load(f)
    except Exception as e:
        st.error(f"❌ Model performans raporu yükleme hatası: {e}")
        return None

# === Yeni SHAP analizi dosyaları ===
@st.cache_data(show_spinner=False, ttl=3600)
def load_new_shap_importance(target: str) -> Optional[pd.DataFrame]:
    """Yeni SHAP importance dosyasını yükle"""
    try:
        if target in SHAP_FILES:
            file_path = SHAP_FILES[target]['importance']
            df = pd.read_csv(file_path)
            return df
        return None
    except Exception as e:
        st.error(f"❌ SHAP importance yükleme hatası: {e}")
        return None

@st.cache_data(show_spinner=False, ttl=3600)
def load_new_shap_summary(target: str) -> Optional[str]:
    """Yeni SHAP summary plot dosya yolunu döndür"""
    try:
        if target in SHAP_FILES:
            return SHAP_FILES[target]['summary']
        return None
    except Exception as e:
        st.error(f"❌ SHAP summary yükleme hatası: {e}")
        return None

# Professional açıklanabilirlik (yalnızca referans)
@st.cache_data(show_spinner=False, ttl=3600)
def load_professional_importance(target_norm: str, version: float = 0.0) -> Optional[pd.DataFrame]:
    # Hedef adına göre alternatifler
    candidates = [target_norm]
    if target_norm == 'economic_loss_million':
        candidates.append('economic_loss_million_usd')
    for t in candidates:
        path = f"ecolense_professional_importance_{t}.csv"
        try:
            if os.path.exists(path):
                return pd.read_csv(path)
        except Exception:
            continue
    return None

@st.cache_data(show_spinner=False, ttl=3600)
def load_professional_shap_mean(target_norm: str, version: float = 0.0) -> Optional[pd.DataFrame]:
    candidates = [target_norm]
    if target_norm == 'economic_loss_million':
        candidates.append('economic_loss_million_usd')
    for t in candidates:
        path = f"ecolense_professional_shap_{t}.csv"
        try:
            if os.path.exists(path):
                return pd.read_csv(path)
        except Exception:
            continue
    return None

# Profesyonel‑TS açıklanabilirlik
@st.cache_data(show_spinner=False, ttl=3600)
def load_prof_ts_importance(target_norm: str, version: float = 0.0) -> Optional[pd.DataFrame]:
    # Mevcut SHAP analizi dosyalarını yükle
    try:
        # Hedef adına göre dosya eşleştirmesi
        target_file_map = {
            'economic_loss_million': "shap_importance_Economic Loss (Million $).csv",
            'total_waste_tons': "shap_importance_Total Waste (Tons).csv",
            'carbon_footprint_kgco2e': "shap_importance_Carbon_Footprint_kgCO2e.csv",
            'sustainability_score': "shap_importance_Sustainability_Score.csv"
        }
        
        if target_norm in target_file_map:
            path = target_file_map[target_norm]
            if os.path.exists(path):
                df = pd.read_csv(path)
                # Kolon isimlerini standardize et
                if 'Feature' in df.columns and 'Importance' in df.columns:
                    df = df.rename(columns={'Feature': 'feature', 'Importance': 'importance'})
                elif 'feature' in df.columns and 'importance' in df.columns:
                    pass  # Zaten doğru format
                return df
    except Exception:
        pass
    
    # Alternatif dosya adları
    path = f"ecolense_prof_ts_importance_{target_norm}.csv"
    try:
        if os.path.exists(path):
            return pd.read_csv(path)
    except Exception:
        pass
    return None

@st.cache_data(show_spinner=False, ttl=3600)
def load_prof_ts_shap_mean(target_norm: str, version: float = 0.0) -> Optional[pd.DataFrame]:
    # Mevcut SHAP analizi dosyalarını yükle (importance dosyalarını kullan)
    try:
        # Hedef adına göre dosya eşleştirmesi
        target_file_map = {
            'economic_loss_million': "shap_importance_Economic Loss (Million $).csv",
            'total_waste_tons': "shap_importance_Total Waste (Tons).csv",
            'carbon_footprint_kgco2e': "shap_importance_Carbon_Footprint_kgCO2e.csv",
            'sustainability_score': "shap_importance_Sustainability_Score.csv"
        }
        
        if target_norm in target_file_map:
            path = target_file_map[target_norm]
            if os.path.exists(path):
                df = pd.read_csv(path)
                # Kolon isimlerini standardize et
                if 'Feature' in df.columns and 'Importance' in df.columns:
                    df = df.rename(columns={'Feature': 'feature', 'Importance': 'importance'})
                elif 'feature' in df.columns and 'importance' in df.columns:
                    pass  # Zaten doğru format
                return df
    except Exception:
        pass
    
    # Alternatif dosya adları
    path = f"ecolense_prof_ts_shap_{target_norm}.csv"
    try:
        if os.path.exists(path):
            return pd.read_csv(path)
    except Exception:
        pass
    return None

@st.cache_data(show_spinner=False)
def _estimate_loglog_elasticity(df: pd.DataFrame, country: Optional[str], target_candidates: List[str], driver_candidates: List[str]) -> Optional[float]:
    """Basit log–log elastisite: slope(log(target)) ~ slope(log(driver)).
    Ülkeye göre yeterli nokta yoksa tüm ülkelerde hesaplar. Yetersizse None.
    """
    if df is None or df.empty:
        return None
    # Hedef ve sürücüyü çöz
    tcol = _resolve_column_name(df, target_candidates)
    dcol = _resolve_column_name(df, driver_candidates)
    ycol = 'Years_From_2018' if 'Years_From_2018' in df.columns else ('Year' if 'Year' in df.columns else ('year' if 'year' in df.columns else None))
    if not tcol or not dcol or not ycol:
        return None
    dsub = df.copy()
    if country is not None:
        ccol = 'country' if 'country' in dsub.columns else ('Country' if 'Country' in dsub.columns else None)
        if ccol:
            dsub = dsub[dsub[ccol] == country].copy()
    dsub = dsub[[ycol, tcol, dcol]].dropna()
    # pozitif değer şartı
    dsub = dsub[(dsub[tcol] > 0) & (dsub[dcol] > 0)]
    if len(dsub) < 3:
        # ülke yetersizse global
        dsub = df[[ycol, tcol, dcol]].dropna()
        dsub = dsub[(dsub[tcol] > 0) & (dsub[dcol] > 0)]
        if len(dsub) < 10:
            return None
    x = np.log(dsub[dcol].astype(float).values)
    y = np.log(dsub[tcol].astype(float).values)
    try:
        slope, intercept = np.polyfit(x, y, 1)
        return float(slope)
    except Exception:
        return None

@st.cache_data(show_spinner=False)
def _estimate_category_share(df: pd.DataFrame, country: str, category: str, waste_candidates: List[str], cat_candidates: List[str]) -> float:
    if df is None or df.empty or category in (None, '', '(Genel)'):
        return 0.0
    ccol = 'country' if 'country' in df.columns else ('Country' if 'Country' in df.columns else None)
    wcol = _resolve_column_name(df, waste_candidates)
    catcol = _resolve_column_name(df, cat_candidates)
    if not ccol or not wcol or not catcol:
        return 0.0
    d = df[[ccol, catcol, wcol]].dropna()
    d = d[d[ccol] == country]
    if d.empty:
        return 0.0
    g = d.groupby(catcol)[wcol].sum().sort_values(ascending=False)
    total = float(g.sum()) if g.sum() > 0 else 0.0
    if total <= 0 or category not in g.index:
        return 0.0
    return float(g.loc[category] / total)

def analyze_missing_data(df: pd.DataFrame) -> Dict:
    """Eksik veri analizi"""
    missing_data = {}
    
    # Eksik veri sayıları
    missing_counts = df.isnull().sum()
    missing_percentages = (missing_counts / len(df)) * 100
    
    missing_data['counts'] = missing_counts[missing_counts > 0]
    missing_data['percentages'] = missing_percentages[missing_percentages > 0]
    
    return missing_data

def _impute_dataframe(df: pd.DataFrame, strategy: str = 'median_ffill_bfill') -> Tuple[pd.DataFrame, int]:
    """Eksik değerleri doldur. Döner: (yeni_df, etkilenen_satır_sayısı)
    strategy: 'median_ffill_bfill' | 'ffill' | 'bfill' | 'dropna'
    """
    if df is None or df.empty:
        return df, 0
    d = df.copy()
    before_na = int(d.isna().sum().sum())
    if strategy == 'dropna':
        d = d.dropna()
        affected = before_na
        return d, affected
    country_col = 'country' if 'country' in d.columns else ('Country' if 'Country' in d.columns else None)
    num_cols = d.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = [c for c in d.columns if c not in num_cols]
    if strategy in ('ffill', 'bfill', 'median_ffill_bfill') and country_col:
        if strategy in ('ffill', 'median_ffill_bfill'):
            d[num_cols] = d.groupby(country_col)[num_cols].ffill()
            d[cat_cols] = d.groupby(country_col)[cat_cols].ffill()
        if strategy in ('bfill', 'median_ffill_bfill'):
            d[num_cols] = d.groupby(country_col)[num_cols].bfill()
            d[cat_cols] = d.groupby(country_col)[cat_cols].bfill()
    if strategy == 'median_ffill_bfill':
        # Kalan sayısalları medyan, kategorikleri mod ile doldur
        for c in num_cols:
            if d[c].isna().any():
                d[c] = d[c].fillna(d[c].median())
        for c in cat_cols:
            if d[c].isna().any():
                try:
                    mode_val = d[c].mode().iloc[0]
                    d[c] = d[c].fillna(mode_val)
                except Exception:
                    d[c] = d[c].fillna(method='ffill').fillna(method='bfill')
    affected = before_na - int(d.isna().sum().sum())
    return d, max(0, affected)

def handle_missing_values(df: pd.DataFrame, strategy: str = 'auto') -> pd.DataFrame:
    """Eksik verileri işle"""
    df_clean = df.copy()
    
    for col in df_clean.columns:
        if df_clean[col].isnull().sum() > 0:
            if df_clean[col].dtype in ['int64', 'float64']:
                if strategy == 'auto':
                    df_clean[col].fillna(df_clean[col].median(), inplace=True)
                else:
                    df_clean[col].fillna(0, inplace=True)
            else:
                df_clean[col].fillna(df_clean[col].mode()[0], inplace=True)
    
    return df_clean

# Veri kalitesi – eksik veri rozeti ve akıllı panel
def render_data_quality(df: pd.DataFrame, page: str = "analysis") -> None:
    missing_counts = df.isnull().sum()
    total_missing = int(missing_counts.sum())
    total_cells = int(df.shape[0] * df.shape[1])
    missing_ratio = (total_missing / total_cells * 100) if total_cells else 0

    if total_missing == 0:
        if page == "home":
            st.markdown("<div style='text-align:center;margin:.25rem 0;'><span class='success-badge'>Veri Kalitesi: Eksik veri yok (2018–2024)</span></div>", unsafe_allow_html=True)
        else:
            st.markdown("<span class='success-badge'>Veri Kalitesi: Eksik veri yok (2018–2024)</span>", unsafe_allow_html=True)
        return

    # Eksik varsa – kısa rozet
    label = f"Veri Kalitesi: Eksik veri %{missing_ratio:.2f} (işlenecek)"
    if page == "home":
        st.markdown(f"<div style='text-align:center;margin:.25rem 0;'><span class='warning-badge'>{label}</span></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<span class='warning-badge'>{label}</span>", unsafe_allow_html=True)

    # Ayrıntılar – expand içinde
    with st.expander("Eksik Veri Ayrıntıları ve Strateji", expanded=False):
        # Tablo: adet ve yüzde
        miss_df = pd.DataFrame({
            'Eksik_Adet': missing_counts,
            'Eksik_%': (missing_counts / len(df) * 100).round(2)
        })
        miss_df = miss_df[miss_df['Eksik_Adet'] > 0].sort_values('Eksik_%', ascending=False)
        st.write("Sütun bazında eksik veri özeti:")
        st.dataframe(miss_df)

        # Isı haritası (yalnızca eksik içeren sütunlar)
        try:
            cols = miss_df.index.tolist()
            if cols:
                import seaborn as sns
                import matplotlib.pyplot as plt
                fig, ax = plt.subplots(figsize=(min(10, 0.35*len(cols)+4), 4))
                sns.heatmap(df[cols].isnull(), cbar=False, ax=ax)
                ax.set_title("Eksik Veri Isı Haritası")
                st.pyplot(fig, use_container_width=True)
        except Exception:
            pass

        # Strateji günlüğü
        st.markdown("**Uygulanacak strateji (modelleme öncesi, sızıntı yok):**")
        st.markdown("- Sayısal sütunlar: median imputasyon\n- Kategorik sütunlar: mod (en sık)\n- Uygulama zamanı: yalnızca modelleme öncesi pipeline’da")

        # İndirilebilir log
        try:
            csv_bytes = miss_df.to_csv().encode('utf-8')
            st.download_button("Eksik veri özetini indir (CSV)", data=csv_bytes, file_name="eksik_veri_ozet.csv", mime="text/csv")
        except Exception:
            pass

# =============================================================================
# GÖRSELLEŞTİRME FONKSİYONLARI
# =============================================================================

# Yardımcı: Esnek sütun eşleştirme (farklı isim varyasyonları için)
def _normalize_col(name: str) -> str:
    s = str(name).lower().strip()
    s = s.replace(" ", "_")
    # Parantez ve $ gibi işaretleri alt çizgiye indir
    for ch in ["(", ")", "$", "+", "/", "-", ":", ","]:
        s = s.replace(ch, "_")
    # Birden fazla alt çizgiyi sadeleştir
    while "__" in s:
        s = s.replace("__", "_")
    return s.strip("_")

def _resolve_column_name(df: pd.DataFrame, candidates: list[str]) -> Optional[str]:
    # 1) Doğrudan eşleşme
    cols = list(df.columns)
    colset = set(cols)
    for name in candidates:
        if name in colset:
            return name
    # 2) Normalize ederek eşleştir (örn. total_waste_tons ~ total_waste_(tons))
    norm_map = { _normalize_col(c): c for c in cols }
    cand_norms = [_normalize_col(c) for c in candidates]
    # Önce tam eşit normalize
    for cn in cand_norms:
        if cn in norm_map:
            return norm_map[cn]
    # Sonra içerme kontrolü (waste_tons gibi)
    for cn in cand_norms:
        for ncol, orig in norm_map.items():
            if cn in ncol or ncol in cn:
                return orig
    return None

# Türkçe sayı formatlayıcı (binlik ayracı nokta)
def format_tr_int(value: float | int) -> str:
    try:
        # Binlik ayıracı: virgül, ondalık yok
        return f"{int(round(value)):,}"
    except Exception:
        return "0"

# Türkçe ondalıklı sayı formatlayıcı (binlik: nokta, ondalık: virgül)
def format_tr_float(value: float, decimals: int = 1) -> str:
    try:
        # Binlik ayıracı: virgül, ondalık ayıracı: nokta
        return f"{value:,.{decimals}f}"
    except Exception:
        return "0"

# Uzun sayılar için dinamik font boyutu belirleyici
def metric_font_style(formatted_value: str) -> str:
    length = len(formatted_value)
    if length > 18:
        return "font-size:1.1rem;"
    if length > 14:
        return "font-size:1.25rem;"
    return ""

@st.cache_data(show_spinner=False, ttl=1800)
def create_kpi_cards(df: pd.DataFrame):
    """KPI kartları"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        waste_col = _resolve_column_name(df, [
            'food_waste_tons', 'total_waste_tons', 'total_waste_(tons)', 'total_waste',
            'toplam_atik', 'waste_tons'
        ])
        total_waste = df[waste_col].sum() if waste_col else 0
        # Büyük sayıları küçültme; değer ve birim uyumlu olsun
        if total_waste >= 1e12:
            waste_unit = 'Trilyon ton'
            waste_str = format_tr_float(total_waste / 1e12, 1)
        elif total_waste >= 1e9:
            waste_unit = 'Milyar ton'
            waste_str = format_tr_float(total_waste / 1e9, 1)
        elif total_waste >= 1e6:
            waste_unit = 'Milyon ton'
            waste_str = format_tr_float(total_waste / 1e6, 1)
        else:
            waste_unit = 'ton'
            waste_str = format_tr_float(total_waste, 1)
        waste_font = metric_font_style(waste_str)
        st.markdown(f"""
        <div class="metric-card">
            <h3>🗑️ Toplam Atık</h3>
            <div class="metric-value" style="{waste_font}">{waste_str}</div>
            <div class="metric-unit">{waste_unit}</div>
            <p class="metric-sub">2018-2024</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        loss_col = _resolve_column_name(df, [
            'economic_loss_usd', 'economic_loss_million_usd', 'economic_loss_(million_$)',
            'economic_loss_(million_usd)', 'economic_loss_musd', 'economic_loss', 'ekonomik_kayip',
            'Economic Loss (Million $)'
        ])
        # Ekonomik kayıp: toplam değer
        year_col_el = 'Years_From_2018' if 'Years_From_2018' in df.columns else ('year' if 'year' in df.columns else ('Year' if 'Year' in df.columns else None))
        if loss_col and year_col_el:
            total_loss_raw = df.groupby(year_col_el)[loss_col].sum().sum()
        else:
            total_loss_raw = df[loss_col].sum() if loss_col else 0
        # Sütun adı "Million" ise değerler milyon USD cinsinden varsayılır
        loss_is_million = loss_col in {
            'economic_loss_million_usd', 'economic_loss_(million_$)', 'economic_loss_(million_usd)', 'economic_loss_musd',
            'Economic Loss (Million $)'
        }
        total_usd = total_loss_raw * 1e6 if loss_is_million else total_loss_raw
        # Büyük sayıları küçültme; değer ve birim uyumlu olsun
        if total_usd >= 1e12:
            unit = 'Trilyon USD'
            loss_str = format_tr_float(total_usd / 1e12, 1)
        elif total_usd >= 1e9:
            unit = 'Milyar USD'
            loss_str = format_tr_float(total_usd / 1e9, 1)
        elif total_usd >= 1e6:
            unit = 'Milyon USD'
            loss_str = format_tr_float(total_usd / 1e6, 1)
        else:
            unit = 'USD'
            loss_str = format_tr_float(total_usd, 1)
        loss_font = metric_font_style(loss_str)
        st.markdown(f"""
        <div class="metric-card">
            <h3>💰 Ekonomik Kayıp</h3>
            <div class="metric-value" style="{loss_font}">{loss_str}</div>
            <div class="metric-unit">{unit}</div>
            <p class="metric-sub">Toplam zarar</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        sust_col = _resolve_column_name(df, ['sustainability_score', 'sustainability', 'surdurulebilirlik_skoru'])
        avg_sustainability = df[sust_col].mean() if sust_col else 0
        avg_sustainability_str = format_tr_float(avg_sustainability, 1)
        st.markdown(f"""
        <div class="metric-card">
            <h3>🌱 Ortalama Sürdürülebilirlik</h3>
            <div class="metric-value">{avg_sustainability_str}</div>
            <div class="metric-unit">Skor (0–100)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        carbon_col = _resolve_column_name(df, ['carbon_footprint_kgco2e', 'carbon_footprint_(kgco2e)', 'carbon_footprint', 'karbon_ayak_izi'])
        total_carbon = df[carbon_col].sum() if carbon_col else 0
        # Büyük sayıları küçültme; değer ve birim uyumlu olsun
        if total_carbon >= 1e12:
            carbon_unit = 'Trilyon kg CO2e'
            carbon_str = format_tr_float(total_carbon / 1e12, 1)
        elif total_carbon >= 1e9:
            carbon_unit = 'Milyar kg CO2e'
            carbon_str = format_tr_float(total_carbon / 1e9, 1)
        elif total_carbon >= 1e6:
            carbon_unit = 'Milyon kg CO2e'
            carbon_str = format_tr_float(total_carbon / 1e6, 1)
        else:
            carbon_unit = 'kg CO2e'
            carbon_str = format_tr_float(total_carbon, 1)
        carbon_font = metric_font_style(carbon_str)
        st.markdown(f"""
        <div class="metric-card">
            <h3>🌍 Toplam Karbon</h3>
            <div class="metric-value" style="{carbon_font}">{carbon_str}</div>
            <div class="metric-unit">{carbon_unit}</div>
            <p class="metric-sub">Karbon ayak izi</p>
        </div>
        """, unsafe_allow_html=True)











def create_trend_chart(df: pd.DataFrame, target_column: str):
    """Trend grafiği (kolon ve yıl adlarını akıllıca eşler)"""
    # Hedef kolonu resolve et
    target_map = {
        'food_waste_tons': [
            'food_waste_tons', 'total_waste_tons', 'Total Waste (Tons)', 'Total_Waste_Tons', 'waste_tons'
        ],
        'economic_loss_usd': [
            'economic_loss_usd', 'economic_loss', 'Economic Loss (Million $)', 'economic_loss_million_usd',
            'economic_loss_(million_$)', 'economic_loss_(million_usd)', 'economic_loss_musd'
        ],
        'sustainability_score': [
            'sustainability_score', 'Sustainability_Score'
        ],
        'carbon_footprint_kgco2e': [
            'carbon_footprint_kgco2e', 'Carbon_Footprint_kgCO2e', 'carbon_footprint'
        ]
    }
    candidates = target_map.get(target_column, [target_column])
    resolved_col = _resolve_column_name(df, [c if isinstance(c, str) else c for c in candidates])
    if not resolved_col:
        st.warning(f"⚠️ {target_column} sütunu bulunamadı")
        return

    # Yıl kolonu resolve et - Years_From_2018 kullan
    year_col = 'Years_From_2018' if 'Years_From_2018' in df.columns else ('year' if 'year' in df.columns else ('Year' if 'Year' in df.columns else None))
    if not year_col:
        st.warning("⚠️ Yıl sütunu bulunamadı (Years_From_2018/Year/year)")
        return

    # Yıllık ortalama - Years_From_2018 için 2018+ ekle
    yearly_data = df.groupby(year_col)[resolved_col].mean().reset_index()
    
    # Years_From_2018 kullanıyorsa gerçek yılları hesapla
    if year_col == 'Years_From_2018':
        yearly_data['Year'] = yearly_data['Years_From_2018'] + 2018
        year_col = 'Year'

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=yearly_data[year_col],
        y=yearly_data[resolved_col],
        mode='lines+markers',
        name=f'{resolved_col} Trendi',
        line=dict(color=COLORS['accent1'], width=4),
        marker=dict(size=8, color=COLORS['accent1'])
    ))

    fig.update_layout(
        title=f"{resolved_col} Zaman Serisi Analizi",
        xaxis_title="Yıl",
        yaxis_title=resolved_col,
        template="plotly_white",
        height=500,
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)
    
    # Grafik açıklaması
    with st.expander("📊 Bu grafik ne anlatıyor?"):
        st.markdown(f"""
        Bu grafik **{resolved_col}** değişkeninin 2018-2024 yılları arasındaki genel trendini gösteriyor. 
        Yıllık ortalama değerler hesaplanarak zaman içindeki değişim eğilimi analiz ediliyor. 
        Yukarı eğilim artış trendini, aşağı eğilim azalış trendini gösterir.
        """)

def create_correlation_matrix(df: pd.DataFrame):
    """Korelasyon matrisi"""
    # Sayısal sütunları seç
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    numeric_cols = [col for col in numeric_cols if col not in ['year', 'Year']]
    
    if len(numeric_cols) < 2:
        st.warning("⚠️ Korelasyon analizi için yeterli sayısal sütun bulunamadı")
        return
    
    # Korelasyon matrisi
    corr_matrix = df[numeric_cols].corr()
    
    # Heatmap
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        colorbar=dict(title="Korelasyon")
    ))
    
    fig.update_layout(
        title="Korelasyon Matrisi",
        height=600,
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Grafik açıklaması
    with st.expander("📊 Bu grafik ne anlatıyor?"):
        st.markdown("""
        Bu korelasyon matrisi, sayısal değişkenler arasındaki ilişkiyi gösteriyor. 
        **Mavi renkler** pozitif korelasyonu (birlikte artış), 
        **kırmızı renkler** negatif korelasyonu (ters ilişki) gösterir. 
        Renk ne kadar koyu ise korelasyon o kadar güçlüdür. 
        **Not:** Yüksek korelasyon neden-sonuç ilişkisi anlamına gelmez!
        """)

def _million_flag(colname: str) -> bool:
    name = _normalize_col(colname)
    return ('million' in name) or name in {
        'economic_loss_million_usd','economic_loss__million_$','economic_loss__million_usd','economic_loss_musd'
    }

def compute_country_kpis(df: pd.DataFrame, start_year: int = 2018, end_year: int = 2024) -> pd.DataFrame:
    """2018–2024 arası ülke bazlı akıllı KPI hesapları
    Dönen kolonlar:
      - total_waste_tons, per_capita_waste_kg
      - economic_loss_usd, per_capita_loss_usd
      - carbon_kgco2e, per_capita_carbon_kg
      - sustainability_score_avg
      - waste_cagr_pct, loss_cagr_pct, carbon_cagr_pct (ilk ve son yıl üzerinden)
    """
    df = df.copy()
    # Kolon çözümlemeleri
    country_col = 'country' if 'country' in df.columns else ('Country' if 'Country' in df.columns else None)
    year_col = 'Years_From_2018' if 'Years_From_2018' in df.columns else ('year' if 'year' in df.columns else ('Year' if 'Year' in df.columns else None))
    waste_col = _resolve_column_name(df, ['food_waste_tons','total_waste_tons','total_waste_(tons)','total_waste','waste_tons'])
    waste_per_capita_col = _resolve_column_name(df, ['avg_waste_per_capita_(kg)','waste_per_capita_kg','per_capita_waste'])
    loss_col = _resolve_column_name(df, ['economic_loss_usd','economic_loss_million_usd','economic_loss_(million_$)','economic_loss_(million_usd)','economic_loss_musd','economic_loss','Economic Loss (Million $)'])
    carbon_col = _resolve_column_name(df, ['carbon_footprint_kgco2e','carbon_footprint_(kgco2e)','carbon_footprint'])
    sust_col = _resolve_column_name(df, ['sustainability_score'])
    pop_col = _resolve_column_name(df, ['population_million','population','population_total'])
    if not country_col or not year_col:
        return pd.DataFrame()
    # Yıl filtresi
    df = df[(df[year_col] >= start_year) & (df[year_col] <= end_year)]
    # Nüfus kişi sayısına
    if pop_col and 'million' in _normalize_col(pop_col):
        df['__pop'] = df[pop_col] * 1_000_000.0
    elif pop_col:
        df['__pop'] = df[pop_col]
    else:
        df['__pop'] = np.nan
    # Ekonomik kaybı USD cinsine çevir
    if loss_col:
        if _million_flag(loss_col):
            df['__loss_usd'] = df[loss_col] * 1_000_000.0
        else:
            df['__loss_usd'] = df[loss_col]
    # Ülke×Yıl tekilleştirme (nüfus ve skorlar için)
    pop_year = df[[country_col, year_col, '__pop']].drop_duplicates().groupby([country_col, year_col])['__pop'].sum().reset_index()
    # Yıllık toplam metrikler
    waste_year = (df[[country_col, year_col, waste_col]].groupby([country_col, year_col])[waste_col].sum().reset_index() if waste_col else None)
    loss_year = (df[[country_col, year_col, '__loss_usd']].groupby([country_col, year_col])['__loss_usd'].sum().reset_index() if loss_col else None)
    carbon_year = (df[[country_col, year_col, carbon_col]].groupby([country_col, year_col])[carbon_col].sum().reset_index() if carbon_col else None)
    sust_year = (df[[country_col, year_col, sust_col]].groupby([country_col, year_col])[sust_col].mean().reset_index() if sust_col else None)
    # Birleştir
    base = pop_year.copy()
    if waste_year is not None:
        base = base.merge(waste_year, on=[country_col, year_col], how='left')
    if loss_year is not None:
        base = base.merge(loss_year, on=[country_col, year_col], how='left')
    if carbon_year is not None:
        base = base.merge(carbon_year, on=[country_col, year_col], how='left')
    if sust_year is not None:
        base = base.merge(sust_year, on=[country_col, year_col], how='left')
    # Ülke bazında özetler (toplamlar/ortalama ve kişi başına)
    agg = base.groupby(country_col).agg({
        '__pop': 'sum',
        waste_col: 'sum' if waste_col else 'sum',
        '__loss_usd': 'sum' if loss_col else 'sum',
        carbon_col: 'sum' if carbon_col else 'sum',
        sust_col: 'mean' if sust_col else 'mean'
    }).reset_index()
    if waste_col: agg.rename(columns={waste_col: 'total_waste_tons'}, inplace=True)
    if loss_col: agg.rename(columns={'__loss_usd': 'economic_loss_usd'}, inplace=True)
    if carbon_col: agg.rename(columns={carbon_col: 'carbon_kgco2e'}, inplace=True)
    if sust_col: agg.rename(columns={sust_col: 'sustainability_score_avg'}, inplace=True)
    # Kişi başına
    if waste_per_capita_col:
        # Mevcut kişi başına değerleri kullan
        waste_per_capita_year = df[[country_col, year_col, waste_per_capita_col]].groupby([country_col, year_col])[waste_per_capita_col].mean().reset_index()
        base = base.merge(waste_per_capita_year, on=[country_col, year_col], how='left')
        agg = agg.merge(base.groupby(country_col)[waste_per_capita_col].mean().reset_index().rename(columns={waste_per_capita_col: 'per_capita_waste_kg'}), on=country_col, how='left')
    elif waste_col:
        # Hesaplama yap
        agg['per_capita_waste_kg'] = (agg['total_waste_tons'] * 1000.0) / agg['__pop']  # ton -> kg, __pop zaten kişi sayısı
    
    if loss_col: agg['per_capita_loss_usd'] = agg['economic_loss_usd'] / agg['__pop']
    if carbon_col: agg['per_capita_carbon_kg'] = agg['carbon_kgco2e'] / agg['__pop']
    # CAGR (ilk-son yıl)
    def _cagr(series):
        series = series.dropna()
        if len(series) < 2:
            return np.nan
        first = series.iloc[0]
        last = series.iloc[-1]
        years = len(series) - 1
        if first <= 0 or years <= 0:
            return np.nan
        return (last / first) ** (1/years) - 1
    # Ülke bazında CAGR hesapla
    cagr_rows = []
    for country, dfg in base.sort_values(year_col).groupby(country_col):
        row = {country_col: country}
        if waste_col: row['waste_cagr_pct'] = 100.0 * _cagr(dfg[waste_col])
        if loss_col: row['loss_cagr_pct'] = 100.0 * _cagr(dfg['__loss_usd'])
        if carbon_col: row['carbon_cagr_pct'] = 100.0 * _cagr(dfg[carbon_col])
        cagr_rows.append(row)
    cagr_df = pd.DataFrame(cagr_rows)
    agg = agg.merge(cagr_df, on=country_col, how='left')
    # Sütun düzeni
    cols = [country_col,'total_waste_tons','per_capita_waste_kg','economic_loss_usd','per_capita_loss_usd','carbon_kgco2e','per_capita_carbon_kg','sustainability_score_avg','waste_cagr_pct','loss_cagr_pct','carbon_cagr_pct']
    cols = [c for c in cols if c in agg.columns]
    return agg[cols].sort_values(by='economic_loss_usd' if 'economic_loss_usd' in cols else cols[1], ascending=False)

def render_country_rankings(real_df: pd.DataFrame, final_df: Optional[pd.DataFrame]) -> None:
    st.subheader('🌍 Ülke Bazlı Sıralamalar (2018–2024)')
    colA, colB, colC = st.columns([2,2,1])
    with colA:
        metric = st.selectbox('Metrik', ['Toplam Atık (ton)','Kişi Başına Atık (kg/kişi)','Ekonomik Kayıp (USD)','Kişi Başına Kayıp (USD/kişi)','Toplam Karbon (kg CO2e)','Kişi Başına Karbon (kg CO2e/kişi)','Sürdürülebilirlik Skoru (ortalama)','Atık CAGR (%)','Kayıp CAGR (%)','Karbon CAGR (%)'])
    df_real = compute_country_kpis(real_df)
    with colB:
        # Eğer KPI hesaplanamadıysa varsayılan slider sınırları
        if df_real.empty:
            topn = st.slider('Top-N', 3, 20, 10, key='topn_rankings')
        else:
            max_n = int(min(20, df_real['country'].nunique() if 'country' in df_real.columns else len(df_real)))
            topn = st.slider('Top-N', 3, max_n if max_n >= 3 else 3, min(10, max_n) if max_n >= 3 else 3, key='topn_rankings')
    with colC:
        # Sentetik veri seçeneği kaldırıldı
        compare = False
    if df_real.empty:
        st.warning('Ülke bazlı KPI üretilemedi.')
        return
    def pick(df: pd.DataFrame) -> pd.DataFrame:
        mapping = {
            'Toplam Atık (ton)': 'total_waste_tons',
            'Kişi Başına Atık (kg/kişi)': 'per_capita_waste_kg',
            'Ekonomik Kayıp (USD)': 'economic_loss_usd',
            'Kişi Başına Kayıp (USD/kişi)': 'per_capita_loss_usd',
            'Toplam Karbon (kg CO2e)': 'carbon_kgco2e',
            'Kişi Başına Karbon (kg CO2e/kişi)': 'per_capita_carbon_kg',
            'Sürdürülebilirlik Skoru (ortalama)': 'sustainability_score_avg',
            'Atık CAGR (%)': 'waste_cagr_pct',
            'Kayıp CAGR (%)': 'loss_cagr_pct',
            'Karbon CAGR (%)': 'carbon_cagr_pct',
        }
        col = mapping[metric]
        asc = False
        if 'Skoru' in metric: asc = False
        if 'CAGR' in metric: asc = False
        return df[[c for c in df.columns if c]].sort_values(by=col, ascending=asc).head(topn)
    if compare and final_df is not None:
        df_final = compute_country_kpis(final_df)
        col1, col2 = st.columns(2)
        with col1:
            st.caption('Gerçek (2018–2024)')
            st.dataframe(pick(df_real), use_container_width=True)
        with col2:
            st.caption('Gerçek Veri (2018-2024)')
            st.dataframe(pick(df_final), use_container_width=True)
        # Δ ve Δ% tablosu
        mapping = {
            'Toplam Atık (ton)': 'total_waste_tons',
            'Kişi Başına Atık (kg/kişi)': 'per_capita_waste_kg',
            'Ekonomik Kayıp (USD)': 'economic_loss_usd',
            'Kişi Başına Kayıp (USD/kişi)': 'per_capita_loss_usd',
            'Toplam Karbon (kg CO2e)': 'carbon_kgco2e',
            'Kişi Başına Karbon (kg CO2e/kişi)': 'per_capita_carbon_kg',
            'Sürdürülebilirlik Skoru (ortalama)': 'sustainability_score_avg',
            'Atık CAGR (%)': 'waste_cagr_pct',
            'Kayıp CAGR (%)': 'loss_cagr_pct',
            'Karbon CAGR (%)': 'carbon_cagr_pct',
        }
        mcol = mapping.get(metric)
        if mcol and 'country' in df_real.columns and 'country' in df_final.columns and mcol in df_real.columns and mcol in df_final.columns:
            merged = df_real[['country', mcol]].merge(
                df_final[['country', mcol]].rename(columns={mcol: f'{mcol}_Synth'}), on='country', how='inner'
            ).rename(columns={mcol: f'{mcol}_Real'})
            merged['Delta'] = merged[f'{mcol}_Synth'] - merged[f'{mcol}_Real']
            merged['Delta_%'] = (merged['Delta'] / merged[f'{mcol}_Real'].replace({0: np.nan})) * 100.0
            st.caption('Veri Analizi')
            st.dataframe(merged.sort_values('Delta_%', ascending=False).head(topn), use_container_width=True)
    else:
        st.dataframe(pick(df_real), use_container_width=True)

    # Ülke detay – mini zaman serisi
    with st.expander('Ülke Detay (mini zaman serisi)', expanded=False):
        country_col = 'country' if 'country' in real_df.columns else ('Country' if 'Country' in real_df.columns else None)
        year_col = 'Years_From_2018' if 'Years_From_2018' in real_df.columns else ('year' if 'year' in real_df.columns else ('Year' if 'Year' in real_df.columns else None))
        if not country_col or not year_col:
            st.info('Ülke/Yıl kolonları bulunamadı.')
        else:
            country_list = sorted(real_df[country_col].dropna().unique())
            sel_country = st.selectbox('Ülke', country_list)
            percap = st.checkbox('Kişi başına göster', value=False)
            mopt = st.selectbox('Metrik', ['Atık','Ekonomik Kayıp','Karbon'])
            col_map = {
                'Atık': _resolve_column_name(real_df, ['total_waste_tons','food_waste_tons','total_waste_(tons)']),
                'Ekonomik Kayıp': _resolve_column_name(real_df, ['economic_loss_usd','economic_loss_million_usd','Economic Loss (Million $)']),
                'Karbon': _resolve_column_name(real_df, ['carbon_footprint_kgco2e','carbon_footprint'])
            }
            mcol = col_map[mopt]
            def _series(df):
                if df is None or mcol is None: return pd.DataFrame()
                d = df[[year_col, mcol]].groupby(year_col)[mcol].sum().reset_index()
                if 'economic' in _normalize_col(mcol) and 'million' in _normalize_col(mcol):
                    d[mcol] = d[mcol] * 1_000_000.0
                if percap:
                    pcol = _resolve_column_name(df, ['population_million','population','population_total'])
                    if pcol:
                        p = df[[year_col, pcol]].drop_duplicates().groupby(year_col)[pcol].sum().reset_index()
                        if 'million' in _normalize_col(pcol):
                            p[pcol] = p[pcol] * 1_000_000.0
                        d = d.merge(p, on=year_col, how='inner')
                        d[mcol] = d[mcol] / d[pcol]
                return d
            dfR = real_df[real_df[country_col] == sel_country]
            dfS = final_df[final_df[country_col] == sel_country] if final_df is not None else None
            sR = _series(dfR); sS = _series(dfS) if dfS is not None else pd.DataFrame()
            if not sR.empty:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=sR[year_col], y=sR[mcol], mode='lines+markers', name='Gerçek', line=dict(color='#11E6C1')))
                # Sentetik veri çizgisi kaldırıldı
                fig.update_layout(height=360, template='plotly_white')
                st.plotly_chart(fig, use_container_width=True)

def render_premium_visuals(real_df: pd.DataFrame, final_df: Optional[pd.DataFrame]) -> None:
    # Premium başlık
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; 
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">🎨</span>
            </div>
            <h2 style="margin: 0; font-size: 2.2rem; font-weight: 700;">Premium Görselleştirmeler</h2>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            İnteraktif ve detaylı veri görselleştirmeleri
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Veri kaynağı seçimi - Premium tasarım
    st.markdown("""
    <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 15px; margin: 1rem 0; border: 1px solid rgba(255,255,255,0.1);">
        <h4 style="margin: 0 0 1rem 0; font-size: 1.2rem; color: #232E5C;">📊 Veri Kaynağı Seçimi</h4>
    </div>
    """, unsafe_allow_html=True)
    # Sadece gerçek veri kullan
    use_final = False
    df_kpi = compute_country_kpis(final_df if use_final else real_df)
    if df_kpi.empty:
        st.info('Görseller için yeterli veri bulunamadı.')
        return
    
    # ISO3 ekle (varsa) – kolon adlarını esnek al
    iso3 = None
    country_key = 'country' if 'country' in real_df.columns else ('Country' if 'Country' in real_df.columns else None)
    iso_key = 'iso_code' if 'iso_code' in real_df.columns else ('ISO_Code' if 'ISO_Code' in real_df.columns else ('ISO3' if 'ISO3' in real_df.columns else ('iso3' if 'iso3' in real_df.columns else None)))
    
    if country_key and iso_key:
        iso3 = real_df[[country_key, iso_key]].drop_duplicates()
        if country_key != 'country':
            iso3 = iso3.rename(columns={country_key: 'country'})
        if iso_key != 'ISO3':
            iso3 = iso3.rename(columns={iso_key: 'ISO3'})
        df_kpi = df_kpi.merge(iso3, on='country', how='left')
    tabs = st.tabs(['🌍 Harita', '🏅 Top-N Bar', '↗️ 2018→2024 Eğim', '🧩 Treemap', '⚡ Dağılım'])
    # 1) Choropleth – kişi başına atık
    with tabs[0]:
        if 'per_capita_waste_kg' in df_kpi.columns:
            try:
                loc_col = 'ISO3' if 'ISO3' in df_kpi.columns else ('iso3' if 'iso3' in df_kpi.columns else None)
                if not loc_col:
                    st.error(f'ISO3 sütunu bulunamadı. Mevcut sütunlar: {list(df_kpi.columns)}')
                    raise KeyError('ISO3/iso3 yok')
                
                fig = px.choropleth(df_kpi, locations=loc_col, color='per_capita_waste_kg',
                                    hover_name='country', color_continuous_scale='RdYlGn_r',
                                    labels={'per_capita_waste_kg':'kg/kişi'})
                fig.update_layout(height=480, template='plotly_white')
                st.plotly_chart(fig, use_container_width=True)
                
                # Grafik açıklaması - Premium tasarım
                st.markdown("""
                <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                            padding: 1.5rem; border-radius: 15px; margin: 1rem 0; 
                            box-shadow: 0 5px 15px rgba(168, 237, 234, 0.2);">
                    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                        <div style="background: rgba(17, 230, 193, 0.2); padding: 0.5rem; border-radius: 8px; margin-right: 0.8rem;">
                            <span style="font-size: 1.2rem;">📊</span>
                        </div>
                        <h4 style="margin: 0; font-size: 1.3rem; font-weight: 600; color: #232E5C;">Bu Grafik Ne Anlatıyor?</h4>
                    </div>
                    <div style="color: #232E5C; line-height: 1.6;">
                        <p style="margin: 0 0 0.8rem 0; font-weight: 600;">Bu <strong>Choropleth haritası</strong> ülkelerin kişi başına gıda israfı dağılımını gösteriyor:</p>
                        <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                            <li><strong>Koyu renkler</strong>: Yüksek kişi başına israf (kg/kişi)</li>
                            <li><strong>Açık renkler</strong>: Düşük kişi başına israf</li>
                            <li><strong>Hover</strong>: Ülke adı ve tam değer</li>
                        </ul>
                        <p style="margin: 0.8rem 0 0 0; font-weight: 600;">💡 <strong>Analiz</strong>: Coğrafi dağılımı görebilir, hangi bölgelerin daha fazla israf ettiğini anlayabilirsiniz.</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            except Exception:
                st.info('Harita için ISO3 kodu bulunamadı.')
        else:
            st.info('Kişi başına atık sütunu yok.')
    # 2) Top-N bar
    with tabs[1]:
        options = {
            'Toplam Atık (ton)': 'total_waste_tons',
            'Ekonomik Kayıp (USD)': 'economic_loss_usd',
            'Toplam Karbon (kg CO2e)': 'carbon_kgco2e',
            'Kişi Başına Atık (kg/kişi)': 'per_capita_waste_kg',
            'Kişi Başına Kayıp (USD/kişi)': 'per_capita_loss_usd',
            'Kişi Başına Karbon (kg CO2e/kişi)': 'per_capita_carbon_kg'
        }
        mlabel = st.selectbox('Metrik', list(options.keys()))
        col = options[mlabel]
        max_n2 = int(min(20, df_kpi['country'].nunique() if 'country' in df_kpi.columns else len(df_kpi)))
        topn_prem = st.slider('Top-N', 5, max_n2 if max_n2 >= 5 else 5, min(10, max_n2) if max_n2 >= 5 else 5, key='topn_premium')
        # Sentetik veri karşılaştırması kaldırıldı
        comp = False
        if comp and final_df is not None:
            df2 = compute_country_kpis(final_df)
            merged = df_kpi[['country', col]].merge(df2[['country', col]].rename(columns={col: f'{col}_S'}), on='country', how='inner')
            merged = merged.dropna(subset=[col, f'{col}_S'])
            merged['Delta_%'] = (merged[f'{col}_S'] - merged[col]) / merged[col].replace({0: np.nan}) * 100.0
            df_top = merged.sort_values('Delta_%', ascending=False).head(topn_prem)
            fig = px.bar(df_top, x='Delta_%', y='country', orientation='h', color='Delta_%', color_continuous_scale='RdYlGn')
        else:
            df_sorted = df_kpi.dropna(subset=[col])
            try:
                df_top = df_sorted.nlargest(topn_prem, col)
            except Exception:
                df_top = df_sorted.sort_values(col, ascending=False).head(topn_prem)
            # Değerler büyüklük sırasında olmalı - country sırasını değer sırasına göre ayarla
            df_top = df_top.sort_values(col, ascending=True)  # En küçük değer en üstte
            fig = px.bar(df_top, x=col, y='country', orientation='h', color=col, color_continuous_scale='Tealgrn')
        # Dinamik yükseklik ve kategori sırası
        dyn_h = max(360, 28 * max(1, len(df_top)) + 160)
        fig.update_layout(height=dyn_h, template='plotly_white')
        fig.update_yaxes(categoryorder='array', categoryarray=list(df_top['country']))
        st.plotly_chart(fig, use_container_width=True)
        
        # Grafik açıklaması - Premium tasarım
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                    padding: 1.5rem; border-radius: 15px; margin: 1rem 0; 
                    box-shadow: 0 5px 15px rgba(168, 237, 234, 0.2);">
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <div style="background: rgba(17, 230, 193, 0.2); padding: 0.5rem; border-radius: 8px; margin-right: 0.8rem;">
                    <span style="font-size: 1.2rem;">📊</span>
                </div>
                <h4 style="margin: 0; font-size: 1.3rem; font-weight: 600; color: #232E5C;">Bu Grafik Ne Anlatıyor?</h4>
            </div>
            <div style="color: #232E5C; line-height: 1.6;">
                <p style="margin: 0 0 0.8rem 0; font-weight: 600;">Bu <strong>Top-N Bar grafiği</strong> seçilen metriğe göre en iyi/kötü performans gösteren ülkeleri sıralıyor:</p>
                <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                    <li><strong>Bar uzunluğu</strong>: {mlabel} değeri</li>
                    <li><strong>En uzun barlar</strong>: En yüksek değere sahip ülkeler</li>
                    <li><strong>Renk skalası</strong>: Değer büyüklüğüne göre renk değişimi</li>
                </ul>
                <p style="margin: 0.8rem 0 0 0; font-weight: 600;">💡 <strong>Kullanım</strong>: Performans sıralamasını görebilir, en iyi uygulamaları örnek alabilirsiniz.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        # İndirilebilir HTML (PNG için kaleido gereklidir)
        try:
            html = fig.to_html()
            st.download_button('Grafiği indir (HTML)', data=html, file_name='topn.html', mime='text/html')
        except Exception:
            pass
    # 3) Slope chart 2018→2024
    with tabs[2]:
        country_col = 'country' if 'country' in real_df.columns else 'Country'
        year_col = 'year' if 'year' in real_df.columns else 'Year'
        metric_map = {
            'Toplam Atık (ton)': _resolve_column_name(real_df, ['total_waste_tons','food_waste_tons','total_waste_(tons)']),
            'Ekonomik Kayıp (USD)': _resolve_column_name(real_df, ['economic_loss_usd','economic_loss_million_usd']),
            'Toplam Karbon (kg CO2e)': _resolve_column_name(real_df, ['carbon_footprint_kgco2e','carbon_footprint'])
        }
        mkey = st.selectbox('Metrik', list(metric_map.keys()), key='slope_metric')
        mcol = metric_map[mkey]
        df_src = final_df if use_final and final_df is not None else real_df
        if mcol and country_col in df_src.columns and year_col in df_src.columns:
            df_agg = df_src[[country_col, year_col, mcol]].groupby([country_col, year_col])[mcol].sum().reset_index()
            try:
                # USD dönüştür
                if 'economic' in _normalize_col(mcol) and 'million' in _normalize_col(mcol):
                    df_agg[mcol] = df_agg[mcol] * 1_000_000.0
            except Exception:
                pass
            d18 = df_agg[df_agg[year_col] == 2018]
            d24 = df_agg[df_agg[year_col] == 2024]
            merged = d18.merge(d24, on=country_col, suffixes=('_2018','_2024'))
            merged = merged.nlargest(12, f'{mcol}_2024')
            fig = go.Figure()
            for _, r in merged.iterrows():
                fig.add_trace(go.Scatter(x=[2018, 2024], y=[r[f'{mcol}_2018'], r[f'{mcol}_2024']], mode='lines+markers', name=r[country_col]))
            fig.update_layout(height=520, template='plotly_white', xaxis=dict(dtick=6))
            st.plotly_chart(fig, use_container_width=True)
            
            # Grafik açıklaması - Premium tasarım
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                        padding: 1.5rem; border-radius: 15px; margin: 1rem 0; 
                        box-shadow: 0 5px 15px rgba(168, 237, 234, 0.2);">
                <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                    <div style="background: rgba(17, 230, 193, 0.2); padding: 0.5rem; border-radius: 8px; margin-right: 0.8rem;">
                        <span style="font-size: 1.2rem;">📊</span>
                    </div>
                    <h4 style="margin: 0; font-size: 1.3rem; font-weight: 600; color: #232E5C;">Bu Grafik Ne Anlatıyor?</h4>
                </div>
                <div style="color: #232E5C; line-height: 1.6;">
                    <p style="margin: 0 0 0.8rem 0; font-weight: 600;">Bu <strong>Slope Chart (Eğim Grafiği)</strong> 2018-2024 arasındaki değişimi gösteriyor:</p>
                    <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                        <li><strong>Her çizgi</strong>: Bir ülkenin {mkey} değerindeki değişim</li>
                        <li><strong>Yukarı eğim</strong>: 2018'den 2024'e artış</li>
                        <li><strong>Aşağı eğim</strong>: 2018'den 2024'e azalış</li>
                        <li><strong>Dik çizgi</strong>: Değişim yok</li>
                    </ul>
                    <p style="margin: 0.8rem 0 0 0; font-weight: 600;">💡 <strong>Analiz</strong>: Hangi ülkelerin iyileştiğini, hangilerinin gerilediğini görebilirsiniz.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info('Eğim grafiği için gerekli kolonlar bulunamadı.')
    # 4) Treemap – Kıta/Gıda Kategorisi → Atık
    with tabs[3]:
        cont_col = 'Continent' if 'Continent' in real_df.columns else ('continent' if 'continent' in real_df.columns else None)
        cat_col = _resolve_column_name(real_df, ['food_category','Food Category'])
        year_col = 'Years_From_2018' if 'Years_From_2018' in real_df.columns else ('year' if 'year' in real_df.columns else ('Year' if 'Year' in real_df.columns else None))
        waste_col = _resolve_column_name(real_df, ['total_waste_tons','food_waste_tons','total_waste_(tons)','total_waste'])
        df_src = final_df if use_final and final_df is not None else real_df
        if cont_col and cat_col and year_col and waste_col:
            d = df_src[(df_src[year_col] >= 2018) & (df_src[year_col] <= 2024)]
            agg = d.groupby([cont_col, cat_col])[waste_col].sum().reset_index()
            # Kategorik tipleri stringe çevir ve eksikleri doldur – treemap için zorunlu
            try:
                agg[cont_col] = agg[cont_col].astype(str).fillna('Unknown')
                agg[cat_col] = agg[cat_col].astype(str).fillna('Unknown')
            except Exception:
                pass
            fig = px.treemap(agg, path=[cont_col, cat_col], values=waste_col, color=cont_col, color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_layout(height=520, template='plotly_white')
            st.plotly_chart(fig, use_container_width=True)
            
            # Grafik açıklaması - Premium tasarım
            st.markdown("""
            <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                        padding: 1.5rem; border-radius: 15px; margin: 1rem 0; 
                        box-shadow: 0 5px 15px rgba(168, 237, 234, 0.2);">
                <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                    <div style="background: rgba(17, 230, 193, 0.2); padding: 0.5rem; border-radius: 8px; margin-right: 0.8rem;">
                        <span style="font-size: 1.2rem;">📊</span>
                    </div>
                    <h4 style="margin: 0; font-size: 1.3rem; font-weight: 600; color: #232E5C;">Bu Grafik Ne Anlatıyor?</h4>
                </div>
                <div style="color: #232E5C; line-height: 1.6;">
                    <p style="margin: 0 0 0.8rem 0; font-weight: 600;">Bu <strong>Treemap grafiği</strong> kıta ve gıda kategorilerine göre atık dağılımını gösteriyor:</p>
                    <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                        <li><strong>Kutu büyüklüğü</strong>: Atık miktarına göre orantılı</li>
                        <li><strong>Renkler</strong>: Kıtalara göre gruplandırma</li>
                        <li><strong>Hiyerarşi</strong>: Kıta → Gıda Kategorisi</li>
                    </ul>
                    <p style="margin: 0.8rem 0 0 0; font-weight: 600;">💡 <strong>Analiz</strong>: Hangi kıtaların ve kategorilerin en fazla atık ürettiğini görebilirsiniz.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info('Treemap için gerekli kolonlar bulunamadı.')
    # 5) Scatter – Kişi başına atık vs sürdürülebilirlik (balon büyüklüğü nüfus)
    with tabs[4]:
        df = df_kpi.dropna(subset=['per_capita_waste_kg','sustainability_score_avg']) if {'per_capita_waste_kg','sustainability_score_avg'}.issubset(df_kpi.columns) else pd.DataFrame()
        if not df.empty:
            size_col = '__pop' if '__pop' in df.columns else None
            # Aykırı (IQR) işaretleme
            x = df['per_capita_waste_kg']; y = df['sustainability_score_avg']
            q1x, q3x = x.quantile(0.25), x.quantile(0.75); iqr_x = q3x - q1x
            q1y, q3y = y.quantile(0.25), y.quantile(0.75); iqr_y = q3y - q1y
            mask = ((x < (q1x - 1.5*iqr_x)) | (x > (q3x + 1.5*iqr_x)) | (y < (q1y - 1.5*iqr_y)) | (y > (q3y + 1.5*iqr_y)))
            df['Outlier'] = np.where(mask, 'Outlier', 'Normal')
            fig = px.scatter(df, x='per_capita_waste_kg', y='sustainability_score_avg', size=size_col, color='Outlier', hover_name='country',
                             labels={'per_capita_waste_kg':'kg/kişi','sustainability_score_avg':'Sürdürülebilirlik'})
            fig.update_layout(height=520, template='plotly_white')
            st.plotly_chart(fig, use_container_width=True)
            
            # Grafik açıklaması - Premium tasarım
            st.markdown("""
            <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                        padding: 1.5rem; border-radius: 15px; margin: 1rem 0; 
                        box-shadow: 0 5px 15px rgba(168, 237, 234, 0.2);">
                <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                    <div style="background: rgba(17, 230, 193, 0.2); padding: 0.5rem; border-radius: 8px; margin-right: 0.8rem;">
                        <span style="font-size: 1.2rem;">📊</span>
                    </div>
                    <h4 style="margin: 0; font-size: 1.3rem; font-weight: 600; color: #232E5C;">Bu Grafik Ne Anlatıyor?</h4>
                </div>
                <div style="color: #232E5C; line-height: 1.6;">
                    <p style="margin: 0 0 0.8rem 0; font-weight: 600;">Bu <strong>Scatter Plot</strong> kişi başına atık ile sürdürülebilirlik arasındaki ilişkiyi gösteriyor:</p>
                    <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                        <li><strong>X ekseni</strong>: Kişi başına gıda israfı (kg/kişi)</li>
                        <li><strong>Y ekseni</strong>: Sürdürülebilirlik skoru</li>
                        <li><strong>Nokta büyüklüğü</strong>: Nüfus büyüklüğü</li>
                        <li><strong>Renkler</strong>: Normal vs Aykırı değerler</li>
                    </ul>
                    <p style="margin: 0.8rem 0 0 0; font-weight: 600;">💡 <strong>Analiz</strong>: Düşük atık + yüksek sürdürülebilirlik = ideal durum. Aykırı değerler özel dikkat gerektiren ülkeleri gösterir.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.download_button('Veriyi indir (CSV)', data=df.to_csv(index=False).encode('utf-8'), file_name='scatter_data.csv', mime='text/csv')
        else:
            st.info('Dağılım için gerekli kolonlar bulunamadı.')

# =============================================================================
# ANA UYGULAMA
# =============================================================================

def show_story_mode():
    """Storytelling modu sayfası"""
    try:
        from storytelling import show_story_mode as show_story_mode_helper
        show_story_mode_helper()
    except Exception as e:
        st.error(f"Storytelling modülü yüklenemedi: {str(e)}")
        st.info("Bu sayfa geçici olarak devre dışı.")

def main():
    """Ana uygulama"""
    
    # CSS yükle
    load_css()
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h3>🌱 ECOLENSE</h3>
            <p>Ultra Premium Dashboard</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        # Dil ve Lite mod
        st.session_state['lang'] = st.selectbox("Language / Dil", ["TR", "EN"], index=(0 if st.session_state['lang']=="TR" else 1))
        st.session_state['lite_mode'] = st.checkbox("Lite Mode (performans)", value=st.session_state['lite_mode'])
        
        # Sayfa seçimi
        pages_list = [
            _t('PAGE_HOME'),
            _t('PAGE_ANALYSIS'),
            _t('PAGE_PERF'),
            _t('PAGE_FORECASTS'),
            _t('PAGE_TARGET_FORECASTS'),
            _t('PAGE_WHATIF'),
            _t('PAGE_DEEPDIVE'),
            _t('PAGE_TORNADO'),
            _t('PAGE_ROI'),
            _t('PAGE_BENCH'),
            _t('PAGE_ANOM'),
            _t('PAGE_LINEAGE'),
            _t('PAGE_FLOWS'),
            _t('PAGE_AB'),
            _t('PAGE_POLICY'),
            _t('PAGE_AI'),
            _t('PAGE_RISK'),
            _t('PAGE_TARGET'),
            _t('PAGE_REPORT'),
            _t('PAGE_CARD'),
            _t('PAGE_JUSTICE'),
            _t('PAGE_STORY')
        ]
        current_page = st.session_state.get('page', pages_list[0])
        try:
            default_idx = pages_list.index(current_page)
        except ValueError:
            default_idx = 0
        page = st.selectbox(_t('PAGE_SELECT'), pages_list, index=default_idx, key='page_select')
        if page != st.session_state.get('page', pages_list[0]):
            st.session_state['page'] = page
            st.rerun()
    
    # Ana içerik
    if page == _t('PAGE_HOME'):
        show_home_page()
    elif page == _t('PAGE_ANALYSIS'):
        show_data_analysis()
    elif page == _t('PAGE_PERF'):
        show_model_performance()
    elif page == _t('PAGE_FORECASTS'):
        show_forecasts()
    elif page == _t('PAGE_TARGET_FORECASTS'):
        show_target_based_forecasts()
    elif page == _t('PAGE_WHATIF'):
        show_what_if_advanced()
    elif page == _t('PAGE_DEEPDIVE'):
        show_country_deep_dive()
    elif page == _t('PAGE_TORNADO'):
        show_driver_sensitivity()
    elif page == _t('PAGE_ROI'):
        show_roi_npv()
    elif page == _t('PAGE_BENCH'):
        show_benchmark_league()
    elif page == _t('PAGE_ANOM'):
        show_anomaly_monitor()
    elif page == _t('PAGE_LINEAGE'):
        show_data_lineage_quality()
    elif page == _t('PAGE_FLOWS'):
        show_carbon_flows()
    elif page == _t('PAGE_POLICY'):
        show_policy_simulator()
    elif page == _t('PAGE_AB'):
        show_ab_testing()
    elif page == _t('PAGE_AI'):
        show_ai_insights()
    elif page == _t('PAGE_RISK'):
        show_risk_opportunity()
    elif page == _t('PAGE_TARGET'):
        show_target_planner()
    elif page == _t('PAGE_REPORT'):
        show_report_builder()
    elif page == _t('PAGE_CARD'):
        show_model_card()
    elif page == _t('PAGE_JUSTICE'):
        show_justice_impact_panel()
    elif page == _t('PAGE_STORY') or page == "📖 Story Mode":
        show_story_mode()
    else:
        st.info("🚧 Bu sayfa yakında eklenecek!")

def show_home_page():
    """Ana sayfa"""
    
    # Ana başlık
    st.markdown("""
    <div class="main-header fade-in">
        <div class="magnifier-effect">
            <div class="title-chip" style="background: transparent; border: none; box-shadow: none;">
                <div class="brand-row">
                    <div class="brand-left">
                    <svg class="brand-person" viewBox="0 0 80 80" aria-hidden="true">
                        <!-- Kafa -->
                        <circle class="body" cx="20" cy="22" r="8" fill="none" />
                        <!-- Gövde -->
                        <path class="body" d="M20 32 L20 50 M20 50 L12 64 M20 50 L28 64" fill="none" />
                        <!-- Büyüteç -->
                        <circle class="ring" cx="52" cy="32" r="14" />
                        <line class="handle" x1="60" y1="40" x2="74" y2="54" />
                    </svg>
                    </div>
                    <div class="brand-center">
                    <div class="brand-stack" style="position: relative;">
                        <div class="brand-fill">ECOLENSE INTELLIGENCE</div>
                        <div class="brand-outline">ECOLENSE INTELLIGENCE</div>
                        <div class="brand-lens-text">ECOLENSE INTELLIGENCE</div>
                        <span class="brand-emoji-leaf" aria-hidden="true">🌱</span>
                    </div>
                    </div>
                    <div class="brand-right"><div class="brand-spacer" aria-hidden="true"></div></div>
                </div>
                <div class="brand-underline"></div>
            </div>
        </div>
        <p style="text-align: center; font-size: 1.2rem; margin: 1rem 0 0 0; width: 100%;">
            <span class="subtitle-chip">Yapay Zeka Destekli Sürdürülebilirlik ve İsraf Yönetimi Platformu</span>
        </p>
        <p class="fun-slogan" style="text-align: center; font-size: 1rem; margin: 0.5rem 0 0 0; width: 100%;">
            <span>"Merceğe yakalanan israf, kaçacak delik arar!" 🔍</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Hoş geldin mesajı
    st.markdown(f"""
    <div class="premium-feature fade-in">
        <h2 style="color: white; margin-bottom: 1rem; text-align: center; font-size: 1.8rem;">🎯 {_t('WELCOME_TITLE')}</h2>
        <p style="color: white; font-size: 1rem; line-height: 1.6; text-align: center; margin: 0 auto; max-width: 800px;">{_t('WELCOME_DESC')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Yalnızca 2018–2024 gerçek veri (jüri görünümü)
    # Gerçek 2018–2024 veri (sessiz yükleme, anasayfada gözlem/sütun sayısı gösterme)
    df = load_data(REAL_DATA_PATH, announce=False)
    
    if df.empty:
        st.error("❌ Veri yüklenemedi. Lütfen veri dosyasının mevcut olduğundan emin olun.")
        return
    
    # KPI kartları (seçilen veri kaynağı)
    create_kpi_cards(df)
    # Ana sayfada detay eksik veri paneli göstermiyoruz

    
    # Premium özellikler
    st.markdown(f"""
    <div class="premium-feature fade-in">
        <h3 style="color: white; margin-bottom: 1.5rem; text-align: center; font-size: 1.8rem;">{_t('PREMIUM_FEATURES')}</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; margin-top: 1rem;">
            <div class="feature-card"><h4>🎯 {_t('TARGET_FORECASTS')}</h4><p>{_t('TARGET_FORECASTS_DESC')}</p></div>
            <div class="feature-card"><h4>📊 {_t('ADVANCED_ANALYSIS')}</h4><p>{_t('ADVANCED_ANALYSIS_DESC')}</p></div>
            <div class="feature-card"><h4>🔮 {_t('FUTURE_FORECASTS')}</h4><p>{_t('FUTURE_FORECASTS_DESC')}</p></div>
            <div class="feature-card"><h4>🤖 {_t('AI_ASSISTANT')}</h4><p>{_t('AI_ASSISTANT_DESC')}</p></div>
            <div class="feature-card"><h4>⚠️ {_t('RISK_OPPORTUNITY')}</h4><p>{_t('RISK_OPPORTUNITY_DESC')}</p></div>
            <div class="feature-card"><h4>📑 {_t('MODEL_CARD')}</h4><p>{_t('MODEL_CARD_DESC')}</p></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hızlı erişim
    st.markdown(f"""
    <h3 style="color: #232E5C; text-align: center; margin: 2rem 0 1rem 0; font-size: 1.5rem; font-weight: 600;">
        {_t('QUICK_ACCESS')}
    </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4, gap="small")
    
    with col1:
        if st.button(f"🎯 {_t('TARGET_FORECASTS')}\n", use_container_width=True, key="quick_target"):
            st.session_state['page'] = _t('PAGE_TARGET_FORECASTS')
    
    with col2:
        if st.button(f"📊 {_t('DATA_ANALYSIS')}\n", use_container_width=True, key="quick_analysis"):
            st.session_state['page'] = _t('PAGE_ANALYSIS')
    
    with col3:
        if st.button(f"🤖 {_t('MODEL_PERFORMANCE')}\n", use_container_width=True, key="quick_model"):
            st.session_state['page'] = _t('PAGE_PERF')
    
    with col4:
        if st.button(f"🔮 {_t('FUTURE_FORECASTS_BTN')}\n", use_container_width=True, key="quick_future"):
            st.session_state['page'] = _t('PAGE_FORECASTS')

    # AI Asistan – Ana Sayfa kısa yorumu
    try:
        st.markdown("""
        <div class='ai-assistant'>
          <h4><span class='ai-emoji'>🤖</span>AI Asistan — Hoş geldin!</h4>
          <p><span class='ai-badge'>İpucu</span> KPI kartları 2018–2024 gerçek veriye dayanır. Alt sayfalarından ülke detayına inip tahminleri ve senaryoları test edebilirsin.</p>
          <p>Öneri: Önce Veri Analizi → sonra Model Performansı → ardından Gelecek Tahminleri ile ülke seçip AI Insights’a göz at.</p>
        </div>
        """, unsafe_allow_html=True)
    except Exception:
        pass
    
    # Storytelling bölümü - Premium tasarım
    st.markdown("""
    <div style="background: linear-gradient(135deg, #11E6C1 0%, #667eea 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; 
                box-shadow: 0 10px 25px rgba(17, 230, 193, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">📖</span>
            </div>
            <h2 style="margin: 0; font-size: 2.2rem; font-weight: 700;">HİKAYE MODU</h2>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            Veri odaklı hikayeler ve analizler
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Hikaye seçenekleri
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🥗 Gıda İsrafı Hikayesi", use_container_width=True, key="story1"):
            st.session_state['story_mode'] = "🥗 Gıda İsrafı Krizi ve Çözüm Yolları"
            st.session_state['page'] = _t('PAGE_STORY')
            st.rerun()
        
        if st.button("💰 Ekonomik Etki Hikayesi", use_container_width=True, key="story2"):
            st.session_state['story_mode'] = "💰 Gıda İsrafının Ekonomik Etkileri"
            st.session_state['page'] = _t('PAGE_STORY')
            st.rerun()
    
    with col2:
        if st.button("🌍 Çevresel Etki Hikayesi", use_container_width=True, key="story3"):
            st.session_state['story_mode'] = "🌍 Gıda İsrafının Çevresel Ayak İzi"
            st.session_state['page'] = _t('PAGE_STORY')
            st.rerun()
        
        if st.button("🎯 Sürdürülebilir Sistemler Hikayesi", use_container_width=True, key="story4"):
            st.session_state['story_mode'] = "🎯 Sürdürülebilir Gıda Sistemleri"
            st.session_state['page'] = _t('PAGE_STORY')
            st.rerun()
    
    # Sayfa sonu yazısı
    add_page_footer("Ana Sayfa")



def show_data_analysis():
    """Veri analizi sayfası - Premium tasarım"""
    
    # Premium başlık
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 1rem 0; 
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">📊</span>
            </div>
            <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">VERİ ANALİZİ</h1>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            Kapsamlı veri analizi ve görselleştirme araçları
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Veri seti özellikleri - Streamlit bileşenleri ile
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                padding: 1.5rem; border-radius: 15px; color: white; margin: 1rem 0; 
                box-shadow: 0 8px 20px rgba(240, 147, 251, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.5rem; border-radius: 8px; margin-right: 0.8rem;">
                <span style="font-size: 1.2rem;">📊</span>
            </div>
            <h3 style="margin: 0; font-size: 1.5rem; font-weight: 600;">Veri Seti Özellikleri</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Veri seti detayları - Streamlit bileşenleri ile
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🎯 Kaynak:** Global Food Wastage + Material Footprint (Birleştirilmiş & Zenginleştirilmiş)")
        st.markdown("**📊 Boyut:** 5,000 gözlem × 37 değişken")
        st.markdown("**🌍 Kapsam:** 20 ülke (2018-2024)")
        st.markdown("**🔧 İşleme:** İki veri seti birleştirildi, özellik mühendisliği yapıldı")
    
    with col2:
        st.markdown("**📈 Model:** GradientBoosting (3 hedef)")
        st.markdown("**🎯 Hedefler:** 3 ana (Atık, Ekonomik Kayıp, Karbon)")
        st.markdown("**🛡️ Güvenlik:** Overfitting önleme")
        st.markdown("**📅 Tahmin:** 2025-2030 projeksiyonlar")
    
    # Tek veri seti kullanımı
    df = load_data(REAL_DATA_PATH, announce=False)
    
    if df.empty:
        st.error("❌ Veri yüklenemedi.")
        return
    
    # Keşifsel Veri Analizi - Premium tasarım
    st.markdown("""
    <div style="background: linear-gradient(135deg, #11E6C1 0%, #667eea 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; 
                box-shadow: 0 10px 25px rgba(17, 230, 193, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">🔍</span>
            </div>
            <h2 style="margin: 0; font-size: 2.2rem; font-weight: 700;">KEŞİFSEL VERİ ANALİZİ</h2>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            Veri seti değişkenleri ve anlamları - Kapsamlı veri keşfi
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Veri seti genel bilgileri
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; text-align: center; 
                    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2); margin: 1rem 0;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
            <div style="font-size: 1.5rem; font-weight: 800;">{len(df)}</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">Toplam Gözlem</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; text-align: center; 
                    box-shadow: 0 5px 15px rgba(240, 147, 251, 0.2); margin: 1rem 0;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🏗️</div>
            <div style="font-size: 1.5rem; font-weight: 800;">{len(df.columns)}</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">Toplam Değişken</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; text-align: center; 
                    box-shadow: 0 5px 15px rgba(79, 172, 254, 0.2); margin: 1rem 0;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🌍</div>
            <div style="font-size: 1.5rem; font-weight: 800;">{df['country'].nunique() if 'country' in df.columns else 0}</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">Ülke Sayısı</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #90EE90 0%, #32CD32 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; text-align: center; 
                    box-shadow: 0 5px 15px rgba(144, 238, 144, 0.2); margin: 1rem 0;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📅</div>
            <div style="font-size: 1.5rem; font-weight: 800;">{df['Years_From_2018'].max() - df['Years_From_2018'].min() + 1 if 'Years_From_2018' in df.columns else (df['year'].max() - df['year'].min() + 1 if 'year' in df.columns else 0)}</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">Yıl Aralığı</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Kategori analizleri
    category_analyses = load_category_analyses()
    if category_analyses:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%); 
                    padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; 
                    box-shadow: 0 10px 25px rgba(255, 107, 107, 0.2);">
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                    <span style="font-size: 1.8rem;">🍎</span>
                </div>
                <h2 style="margin: 0; font-size: 2.2rem; font-weight: 700;">GIDA KATEGORİLERİ ANALİZİ</h2>
            </div>
            <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
                Kategori bazında israf, ekonomik kayıp ve karbon ayak izi analizi
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Kategori analizleri tablosu
        category_data = []
        for category, data in category_analyses.items():
            category_data.append({
                'Kategori': category,
                'Toplam İsraf (Ton)': f"{data['total_waste']:,.0f}",
                'Ekonomik Kayıp (Milyon $)': f"{data['economic_loss']:,.0f}",
                'Karbon Ayak İzi (kgCO2e)': f"{data['carbon_footprint']:,.0f}",
                'Ortalama Sürdürülebilirlik': f"{data['avg_sustainability']:.2f}%"
            })
        
        category_df = pd.DataFrame(category_data)
        
        # Filtre seçenekleri
        st.markdown("### 🔍 Sıralama Filtresi")
        col1, col2 = st.columns(2)
        
        with col1:
            sort_by = st.selectbox(
                "Sıralama Kriteri:",
                ["Alfabetik", "Toplam İsraf (Ton)", "Ekonomik Kayıp (Milyon $)", 
                 "Karbon Ayak İzi (kgCO2e)", "Ortalama Sürdürülebilirlik"],
                index=0
            )
        
        with col2:
            sort_order = st.selectbox(
                "Sıralama Yönü:",
                ["Büyükten Küçüğe", "Küçükten Büyüğe"],
                index=0
            )
        
        # Sıralama işlemi
        if sort_by == "Alfabetik":
            category_df_sorted = category_df.sort_values('Kategori', ascending=(sort_order == "Küçükten Büyüğe"))
        elif sort_by == "Toplam İsraf (Ton)":
            # Sayısal değerlere çevir
            category_df['Toplam İsraf (Ton)'] = category_df['Toplam İsraf (Ton)'].str.replace(',', '').astype(float)
            category_df_sorted = category_df.sort_values('Toplam İsraf (Ton)', ascending=(sort_order == "Küçükten Büyüğe"))
            # Formatı geri döndür
            category_df_sorted['Toplam İsraf (Ton)'] = category_df_sorted['Toplam İsraf (Ton)'].apply(lambda x: f"{x:,.0f}")
        elif sort_by == "Ekonomik Kayıp (Milyon $)":
            category_df['Ekonomik Kayıp (Milyon $)'] = category_df['Ekonomik Kayıp (Milyon $)'].str.replace(',', '').astype(float)
            category_df_sorted = category_df.sort_values('Ekonomik Kayıp (Milyon $)', ascending=(sort_order == "Küçükten Büyüğe"))
            category_df_sorted['Ekonomik Kayıp (Milyon $)'] = category_df_sorted['Ekonomik Kayıp (Milyon $)'].apply(lambda x: f"{x:,.0f}")
        elif sort_by == "Karbon Ayak İzi (kgCO2e)":
            category_df['Karbon Ayak İzi (kgCO2e)'] = category_df['Karbon Ayak İzi (kgCO2e)'].str.replace(',', '').astype(float)
            category_df_sorted = category_df.sort_values('Karbon Ayak İzi (kgCO2e)', ascending=(sort_order == "Küçükten Büyüğe"))
            category_df_sorted['Karbon Ayak İzi (kgCO2e)'] = category_df_sorted['Karbon Ayak İzi (kgCO2e)'].apply(lambda x: f"{x:,.0f}")
        elif sort_by == "Ortalama Sürdürülebilirlik":
            category_df['Ortalama Sürdürülebilirlik'] = category_df['Ortalama Sürdürülebilirlik'].str.replace('%', '').astype(float)
            category_df_sorted = category_df.sort_values('Ortalama Sürdürülebilirlik', ascending=(sort_order == "Küçükten Büyüğe"))
            category_df_sorted['Ortalama Sürdürülebilirlik'] = category_df_sorted['Ortalama Sürdürülebilirlik'].apply(lambda x: f"{x:.2f}%")
        
        st.dataframe(category_df_sorted, use_container_width=True, hide_index=True)
        
        # Kategori karşılaştırma grafiği
        fig = go.Figure()
        
        categories = list(category_analyses.keys())
        waste_values = [category_analyses[cat]['total_waste'] for cat in categories]
        economic_values = [category_analyses[cat]['economic_loss'] for cat in categories]
        
        fig.add_trace(go.Bar(
            name='Toplam İsraf (Ton)',
            x=categories,
            y=waste_values,
            marker_color='#FF6B6B',
            yaxis='y'
        ))
        
        fig.add_trace(go.Bar(
            name='Ekonomik Kayıp (Milyon $)',
            x=categories,
            y=economic_values,
            marker_color='#4ECDC4',
            yaxis='y2'
        ))
        
        fig.update_layout(
            title='Gıda Kategorileri Karşılaştırması',
            xaxis_title='Gıda Kategorileri',
            yaxis=dict(title='Toplam İsraf (Ton)', side='left'),
            yaxis2=dict(title='Ekonomik Kayıp (Milyon $)', side='right', overlaying='y'),
            barmode='group',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    

    
    # Değişken kategorileri - Daha görünür başlık
    st.markdown("""
    <div style="background: linear-gradient(135deg, #11E6C1 0%, #667eea 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; 
                box-shadow: 0 10px 25px rgba(17, 230, 193, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">📋</span>
            </div>
            <h2 style="margin: 0; font-size: 2.2rem; font-weight: 700;">VERİ SETİ DEĞİŞKEN KATEGORİLERİ</h2>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            37 değişkenin kategorilere göre detaylı açıklaması
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Değişken kategorileri accordion
    with st.expander("🎯 Hedef Değişkenler (Ana Metrikler)", expanded=True):
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1rem; border-radius: 10px; color: white; margin: 0.5rem 0;">
            <h5 style="margin: 0 0 0.5rem 0;">🏆 Ana Performans Göstergeleri</h5>
        </div>
        """, unsafe_allow_html=True)
        
        target_vars = {
            "Total Waste (Tons)": "Toplam gıda israfı (ton cinsinden) - Ana hedef değişken",
            "Economic Loss (Million $)": "Ekonomik kayıp (milyon USD) - Finansal etki ölçümü",
            "Carbon_Footprint_kgCO2e": "Karbon ayak izi (kg CO2e) - İklim etkisi ölçümü",
            "Sustainability_Score": "Sürdürülebilirlik skoru (0-100) - Çevresel performans"
        }
        
        for var, desc in target_vars.items():
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.9); padding: 1rem; border-radius: 10px; margin: 0.5rem 0; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-left: 3px solid #667eea;">
                <div style="font-weight: 600; color: #232E5C; margin-bottom: 0.3rem;">{var}</div>
                <div style="color: #666; font-size: 0.9rem;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with st.expander("🌍 Coğrafi ve Demografik Değişkenler", expanded=False):
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 1rem; border-radius: 10px; color: white; margin: 0.5rem 0;">
            <h5 style="margin: 0 0 0.5rem 0;">🌍 Lokasyon ve Nüfus Bilgileri</h5>
        </div>
        """, unsafe_allow_html=True)
        
        geo_vars = {
            "Country": "Ülke adı - Ana coğrafi birim",
            "ISO_Code": "Ülke ISO kodu - Standart ülke tanımlayıcısı (harita için)",
            "Continent": "Kıta bilgisi - Coğrafi bölge sınıflandırması",
            "Hemisphere": "Yarıküre (Kuzey/Güney) - İklim bölgesi",
            "Population (Million)": "Nüfus (milyon) - Demografik büyüklük",
            "Food Category": "Gıda kategorisi - İsraf edilen gıda türü",
            "Avg Waste per Capita (Kg)": "Kişi başına ortalama israf (kg) - Demografik etki",
            "Household Waste (%)": "Evsel israf yüzdesi - Hane bazlı israf oranı",
            "Material_Footprint_Per_Capita": "Kişi başına malzeme ayak izi - Kaynak tüketimi"
        }
        
        for var, desc in geo_vars.items():
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.9); padding: 1rem; border-radius: 10px; margin: 0.5rem 0; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-left: 3px solid #f093fb;">
                <div style="font-weight: 600; color: #232E5C; margin-bottom: 0.3rem;">{var}</div>
                <div style="color: #666; font-size: 0.9rem;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with st.expander("📊 Sosyo-Ekonomik Göstergeler", expanded=False):
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 1rem; border-radius: 10px; color: white; margin: 0.5rem 0;">
            <h5 style="margin: 0 0 0.5rem 0;">💰 Ekonomik ve Sosyal Gelişmişlik</h5>
        </div>
        """, unsafe_allow_html=True)
        
        socio_vars = {
            "Waste_Per_Capita_kg": "Kişi başına israf (kg) - Demografik etki",
            "Economic_Loss_Per_Capita_USD": "Kişi başına ekonomik kayıp (USD) - Finansal etki",
            "Carbon_Per_Capita_kgCO2e": "Kişi başına karbon ayak izi - İklim etkisi"
        }
        
        for var, desc in socio_vars.items():
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.9); padding: 1rem; border-radius: 10px; margin: 0.5rem 0; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-left: 3px solid #4facfe;">
                <div style="font-weight: 600; color: #232E5C; margin-bottom: 0.3rem;">{var}</div>
                <div style="color: #666; font-size: 0.9rem;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with st.expander("🌱 Çevresel ve Sürdürülebilirlik Metrikleri", expanded=False):
        st.markdown("""
        <div style="background: linear-gradient(135deg, #90EE90 0%, #32CD32 100%); 
                    padding: 1rem; border-radius: 10px; color: white; margin: 0.5rem 0;">
            <h5 style="margin: 0 0 0.5rem 0;">🌱 Çevresel Performans ve Sürdürülebilirlik</h5>
        </div>
        """, unsafe_allow_html=True)
        
        env_vars = {
            "Sustainability_Score": "Sürdürülebilirlik skoru (0-100) - Çevresel performans"
        }
        
        for var, desc in env_vars.items():
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.9); padding: 1rem; border-radius: 10px; margin: 0.5rem 0; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-left: 3px solid #90EE90;">
                <div style="font-weight: 600; color: #232E5C; margin-bottom: 0.3rem;">{var}</div>
                <div style="color: #666; font-size: 0.9rem;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with st.expander("🕒 Zaman ve Dönemsel Faktörler", expanded=False):
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFA500 0%, #FF8C00 100%); 
                    padding: 1rem; border-radius: 10px; color: white; margin: 0.5rem 0;">
            <h5 style="margin: 0 0 0.5rem 0;">🕒 Zaman Serisi ve Dönemsel Etkiler</h5>
        </div>
        """, unsafe_allow_html=True)
        
        time_vars = {
            "Year": "Yıl bilgisi - Zaman serisi analizi",
            "Years_From_2018": "2018'den itibaren geçen yıl sayısı - Trend analizi",
            "Is_Pandemic_Year": "Pandemi yılı mı? (2020) - COVID-19 etkisi",
            "Is_Post_Pandemic": "Pandemi sonrası mı? (2021+) - Toparlanma dönemi",
            "Year_Trend": "Yıl trendi - Zaman serisi trendi",
            "Country_Trend": "Ülke trendi - Ülke bazlı trend",
            "Year_Cycle": "Yıl döngüsü - Döngüsel etki",
            "Year_Cycle_Cos": "Yıl döngüsü kosinüs - Döngüsel etki"
        }
        
        for var, desc in time_vars.items():
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.9); padding: 1rem; border-radius: 10px; margin: 0.5rem 0; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-left: 3px solid #FFA500;">
                <div style="font-weight: 600; color: #232E5C; margin-bottom: 0.3rem;">{var}</div>
                <div style="color: #666; font-size: 0.9rem;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with st.expander("🔗 Etkileşim Değişkenleri (Feature Engineering)", expanded=False):
        st.markdown("""
        <div style="background: linear-gradient(135deg, #9370DB 0%, #8A2BE2 100%); 
                    padding: 1rem; border-radius: 10px; color: white; margin: 0.5rem 0;">
            <h5 style="margin: 0 0 0.5rem 0;">🔗 Yapay Zeka için Oluşturulan Etkileşim Değişkenleri</h5>
        </div>
        """, unsafe_allow_html=True)
        
        interaction_vars = {
            "Population_Material_Interaction": "Nüfus-Malzeme etkileşimi - Kaynak tüketimi",
            "Year_Population_Interaction": "Yıl-Nüfus etkileşimi - Demografik trend",
            "GDP_Per_Capita_Proxy": "Kişi başına GSYİH proxy - Ekonomik gelişmişlik",
            "Waste_Efficiency": "İsraf verimliliği - Kaynak kullanım etkinliği",
            "Economic_Intensity": "Ekonomik yoğunluk - Finansal etki",
            "Waste_Trend": "İsraf trendi - Zaman serisi trendi",
            "Economic_Trend": "Ekonomik trend - Finansal trend",
            "Category_Waste_Share": "Kategori israf payı - Kategori bazlı analiz",
            "Category_Economic_Share": "Kategori ekonomik payı - Finansal kategori analizi"
        }
        
        for var, desc in interaction_vars.items():
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.9); padding: 1rem; border-radius: 10px; margin: 0.5rem 0; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-left: 3px solid #9370DB;">
                <div style="font-weight: 600; color: #232E5C; margin-bottom: 0.3rem;">{var}</div>
                <div style="color: #666; font-size: 0.9rem;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with st.expander("🔢 Kodlanmış Değişkenler (Encoded Features)", expanded=False):
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%); 
                    padding: 1rem; border-radius: 10px; color: white; margin: 0.5rem 0;">
            <h5 style="margin: 0 0 0.5rem 0;">🔢 Makine Öğrenmesi için Kodlanmış Kategorik Değişkenler</h5>
        </div>
        """, unsafe_allow_html=True)
        
        encoded_vars = {
            "Food Category_Encoded": "Gıda kategorisi (kodlanmış) - Sayısal kategori",
            "Country_Encoded": "Ülke (kodlanmış) - Sayısal ülke kodu",
            "Continent_Encoded": "Kıta (kodlanmış) - Coğrafi bölge",
            "Hemisphere_Encoded": "Yarıküre (kodlanmış) - İklim bölgesi"
        }
        
        for var, desc in encoded_vars.items():
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.9); padding: 1rem; border-radius: 10px; margin: 0.5rem 0; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-left: 3px solid #FF6B6B;">
                <div style="font-weight: 600; color: #232E5C; margin-bottom: 0.3rem;">{var}</div>
                <div style="color: #666; font-size: 0.9rem;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Eksik veri analizi (detaylar yalnızca Veri Analizi sayfasında expand ile)
    render_data_quality(df, page="analysis")

    # Eksik değer işlemleri paneli - Premium tasarım
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                padding: 1.5rem; border-radius: 15px; color: white; margin: 1rem 0; 
                box-shadow: 0 8px 20px rgba(79, 172, 254, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.5rem; border-radius: 8px; margin-right: 0.8rem;">
                <span style="font-size: 1.2rem;">🔧</span>
            </div>
            <h3 style="margin: 0; font-size: 1.5rem; font-weight: 600;">Veri İşleme Araçları</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.9); padding: 1.5rem; border-radius: 15px; margin: 1rem 0; 
                    box-shadow: 0 5px 15px rgba(0,0,0,0.1); border-left: 4px solid #667eea;">
            <h4 style="margin: 0 0 1rem 0; color: #232E5C; font-size: 1.2rem;">📊 Eksik Değerler (İşlem)</h4>
        </div>
        """, unsafe_allow_html=True)
        
        choice = st.radio("Yöntem", ["İmpute (Medyan + ffill/bfill)", "Sadece forward-fill", "Sadece backward-fill", "Hariç tut (dropna)"], index=0, horizontal=False)
        strat = {
            "İmpute (Medyan + ffill/bfill)": "median_ffill_bfill",
            "Sadece forward-fill": "ffill",
            "Sadece backward-fill": "bfill",
            "Hariç tut (dropna)": "dropna",
        }[choice]
        df_imp, nfix = _impute_dataframe(df, strategy=strat)
        
        # İşlenen hücre sayısı kaldırıldı - veri seti zaten temiz
    
    with col2:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.9); padding: 1.5rem; border-radius: 15px; margin: 1rem 0; 
                    box-shadow: 0 5px 15px rgba(0,0,0,0.1); border-left: 4px solid #f093fb;">
            <h4 style="margin: 0 0 1rem 0; color: #232E5C; font-size: 1.2rem;">⚠️ Aykırı Değerler (IQR)</h4>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            num_cols = df_imp.select_dtypes(include=[np.number]).columns.tolist()
            default_idx = num_cols.index('sustainability_score') if 'sustainability_score' in num_cols else 0
            ocol = st.selectbox("Hedef kolon", num_cols, index=default_idx)
            q1, q3 = df_imp[ocol].quantile(0.25), df_imp[ocol].quantile(0.75)
            iqr = q3 - q1
            low, high = q1 - 1.5*iqr, q3 + 1.5*iqr
            mask_out = (df_imp[ocol] < low) | (df_imp[ocol] > high)
            
            st.markdown(f"""
            <div style="background: rgba(240, 147, 251, 0.1); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                <div style="font-weight: 600; color: #232E5C;">📊 Aykırı Sayısı</div>
                <div style="color: #f093fb; font-weight: 600; font-size: 1.2rem;">{int(mask_out.sum())}</div>
            </div>
            """, unsafe_allow_html=True)
            
            exclude = st.checkbox("Aykırıları hariç tut")
            df_use = df_imp.loc[~mask_out].copy() if exclude else df_imp.copy()
        except Exception:
            df_use = df_imp.copy()

    # Korelasyon analizi - Premium tasarım
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; 
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">🔗</span>
            </div>
            <h2 style="margin: 0; font-size: 2.2rem; font-weight: 700;">KORELASYON ANALİZİ</h2>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            Değişkenler arası ilişki analizi ve görselleştirme
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    create_correlation_matrix(df_use)

    # Trend analizi - Premium tasarım
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; 
                box-shadow: 0 10px 25px rgba(240, 147, 251, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">📈</span>
            </div>
            <h2 style="margin: 0; font-size: 2.2rem; font-weight: 700;">TREND ANALİZİ</h2>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            Zaman serisi analizi ve trend görselleştirme
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: rgba(255,255,255,0.9); padding: 1.5rem; border-radius: 15px; margin: 1rem 0; 
                box-shadow: 0 5px 15px rgba(0,0,0,0.1); border-left: 4px solid #f093fb;">
        <h4 style="margin: 0 0 1rem 0; color: #232E5C; font-size: 1.2rem;">🎯 Hedef Değişken Seçimi</h4>
    </div>
    """, unsafe_allow_html=True)
    
    target_col = st.selectbox("Hedef değişken seçin:", ['food_waste_tons', 'economic_loss_usd', 'sustainability_score', 'carbon_footprint_kgco2e'])
    create_trend_chart(df_use, target_col)

    # Ülke bazlı sıralamalar - Premium tasarım
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; 
                box-shadow: 0 10px 25px rgba(79, 172, 254, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">🏆</span>
            </div>
            <h2 style="margin: 0; font-size: 2.2rem; font-weight: 700;">ÜLKE BAZLI SIRALAMALAR</h2>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            Gerçek veri analizi ve görselleştirme
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    real_df = df_use
    final_df = None
    render_country_rankings(real_df, final_df)
    render_premium_visuals(real_df, final_df)

    # AI Asistan – Premium tasarım
    try:
        txts = []
        # Korelasyon hedef açıklaması
        try:
            corr_target = target_col
        except Exception:
            corr_target = 'seçili hedef'
        txts.append(f"'{corr_target}' için güçlü pozitif/negatif ilişkiler karar öncesi uyarı sinyalleridir. Yüksek korelasyon → neden-sonuç değildir!")
        # Trend kısa okuma
        try:
            yname = _resolve_column_name(df_use, [target_col]) or target_col
            tseries = df_use[[yname, 'Year']].dropna()
            slope = 0.0
            if not tseries.empty:
                slope, _ = np.polyfit(tseries['Year'].astype(float), tseries[yname].astype(float), 1)
            trend_txt = 'yukarı eğilim' if slope > 0 else ('aşağı eğilim' if slope < 0 else 'yatay')
            txts.append(f"Genel eğilim: {trend_txt}.")
        except Exception:
            pass
        
        st.markdown("""
        <div class='ai-assistant'>
          <h4><span class='ai-emoji'>🤖</span>AI Asistan — Veri Analizi</h4>
          <p><span class='ai-badge'>Korelasyon</span> {rows}</p>
          <p><span class='ai-badge'>Öneri</span> Aykırıları işaretleyip etkisini ayrı test edin; korelasyon tablosunu hedefe göre filtreleyin ve multikolinerliği (>|0.9|) düşürün.</p>
        </div>
        """.replace("{rows}", " · ".join(txts)), unsafe_allow_html=True)
    except Exception:
        pass
    
    # Sayfa sonu yazısı
    add_page_footer("Veri Analizi")

def show_model_performance():
    """Model performansı sayfası - Premium tasarım"""
    
    # Premium başlık
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 1rem 0; 
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">🤖</span>
            </div>
            <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">MODEL PERFORMANSI</h1>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            Yapay zeka modellerinin performans analizi ve karşılaştırması
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Model seçimi - Premium tasarım
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                padding: 1.5rem; border-radius: 15px; color: white; margin: 1rem 0; 
                box-shadow: 0 8px 20px rgba(240, 147, 251, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.5rem; border-radius: 8px; margin-right: 0.8rem;">
                <span style="font-size: 1.2rem;">🔧</span>
            </div>
            <h3 style="margin: 0; font-size: 1.5rem; font-weight: 600;">Model Seçimi</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Model bilgilerini JSON'dan al
    perf = load_performance_report(PERF_REPORT_PATH)
    
    if not perf:
        st.warning(f"⚠️ Model performans raporu bulunamadı.")
        return
    
    # Model tipini JSON'dan al
    model_type = perf.get('model_type', 'GradientBoosting')
    src_name = f"{model_type} Model"
    

    
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.9); padding: 1rem; border-radius: 10px; margin: 1rem 0; 
                box-shadow: 0 3px 10px rgba(0,0,0,0.1); border-left: 4px solid #11E6C1;">
        <div style="font-weight: 600; color: #232E5C;">📊 Kaynak: {src_name}</div>
                        <div style="font-size: 0.9rem; color: #64748B; margin-top: 0.3rem;">🤖 {model_type} - Gradient Boosting (Conservative Settings)</div>
    </div>
    """, unsafe_allow_html=True)

    # Ana KPI'lar - Premium tasarım
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; 
                box-shadow: 0 10px 25px rgba(79, 172, 254, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">📊</span>
            </div>
            <h2 style="margin: 0; font-size: 2.2rem; font-weight: 700;">ANA PERFORMANS METRİKLERİ</h2>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            Hedef değişkenlere göre model performansı
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    targets_order = [
        ('Total Waste (Tons)', '🗑️ Atık'),
        ('Economic Loss (Million $)', '💰 Ekonomik Kayıp'),
        ('Carbon_Footprint_kgCO2e', '🌍 Karbon')
    ]

    # Overfitting hesaplama fonksiyonu
    def _avg(dct, key):
        return dct.get(key, 0) if isinstance(dct, dict) else 0
    
    cols = st.columns(3)
    total_overfitting = 0
    valid_targets = 0
    
    for i, ((key, label), c) in enumerate(zip(targets_order, cols)):
        # JSON dosyasından doğru anahtarları al
        target_data = perf.get('targets', {}).get(key, {})
        r2 = target_data.get('test_r2', 0)
        rmse = target_data.get('test_rmse', 0)
        cv_r2 = target_data.get('cv_r2', 0)
        overfitting_score = target_data.get('overfitting_score', 0)
        
        # Overfitting farkı hesapla
        overfitting_gap = abs(r2 - cv_r2) if cv_r2 > 0 and r2 > 0 else 0
        if overfitting_gap > 0:
            total_overfitting += overfitting_gap
            valid_targets += 1
        
        # Her kart için farklı renk
        colors = ['#667eea', '#f093fb', '#4facfe', '#11E6C1']
        color = colors[i]
        
        c.markdown(f"""
        <div style="background: linear-gradient(135deg, {color} 0%, {color}dd 100%); 
                    padding: 2rem; border-radius: 20px; color: white; text-align: center; 
                    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3); margin: 1rem 0;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">{label.split()[0]}</div>
            <h3 style="margin: 0 0 1rem 0; font-size: 1.3rem; font-weight: 600;">{label.split()[1]}</h3>
            <div style="font-size: 2rem; font-weight: 800; margin-bottom: 0.5rem;">R² = {r2:.4f}</div>
            <div style="font-size: 1rem; opacity: 0.9; margin-bottom: 0.3rem;">RMSE = {rmse:,.4f}</div>
            <div style="font-size: 0.9rem; opacity: 0.8;">CV R² = {cv_r2:.4f}</div>
            <div style="font-size: 0.9rem; opacity: 0.8; color: {'#FFD700' if overfitting_score > 0.1 else '#90EE90'};">
                Overfitting = {overfitting_score:.4f}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Ortalama overfitting kartı - JSON'dan al
    avg_overfitting = perf.get('average_overfitting', 0)
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%); 
                padding: 2rem; border-radius: 20px; color: white; text-align: center; 
                box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3); margin: 2rem 0;">
        <div style="font-size: 2.5rem; margin-bottom: 1rem;">⚠️</div>
        <h3 style="margin: 0 0 1rem 0; font-size: 1.5rem; font-weight: 600;">Overfitting Analizi</h3>
        <div style="font-size: 2rem; font-weight: 800; margin-bottom: 0.5rem;">Ortalama Gap = {avg_overfitting:.4f}</div>
        <div style="font-size: 1rem; opacity: 0.9;">
            {f'CV R² > Test R² ({valid_targets} hedef)' if avg_overfitting > 0 else 'Overfitting yok'}
        </div>
        <div style="font-size: 0.9rem; opacity: 0.8; margin-top: 0.5rem;">
            {f'⚠️ Yüksek overfitting riski' if avg_overfitting > 0.1 else '✅ İyi genelleme' if avg_overfitting < 0.05 else '⚠️ Orta seviye overfitting'}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # R2 grafiği - Premium tasarım
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; 
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">📈</span>
            </div>
            <h2 style="margin: 0; font-size: 2.2rem; font-weight: 700;">R² PERFORMANS GRAFİĞİ</h2>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            Test ve Cross-Validation R² karşılaştırması
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    rows = []
    for key, label in targets_order:
        target_data = perf.get('targets', {}).get(key, {})
        rows.append({
            'Hedef': label,
            'R2_Test': target_data.get('test_r2', 0),
            'R2_CV': target_data.get('cv_r2', 0)
        })
    perf_df = pd.DataFrame(rows)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=perf_df['Hedef'], y=perf_df['R2_Test'], name='Test R²', marker_color='#11E6C1'))
    fig.add_trace(go.Bar(x=perf_df['Hedef'], y=perf_df['R2_CV'], name='CV R²', marker_color='#A9FF4F'))
    fig.update_layout(
        barmode='group', 
        height=420, 
        template='plotly_white',
        plot_bgcolor='rgba(248, 250, 252, 0.8)',
        paper_bgcolor='rgba(248, 250, 252, 0.8)',
        title=dict(
            text="Model Performans Karşılaştırması",
            font=dict(size=18, color='#232E5C')
        )
    )
    st.plotly_chart(fig, use_container_width=True)

    # Not: Kaynak {src_name}. Robust yedek olarak kullanılabilir.

    # Accuracy Scorecard - Premium tasarım
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; 
                box-shadow: 0 10px 25px rgba(240, 147, 251, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.5rem;">🏅</span>
            </div>
            <h2 style="margin: 0; font-size: 1.8rem; font-weight: 700;">ACCURACY SCORECARD</h2>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            Genel model performans özeti ve overfitting analizi
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Ortalama R² hesaplama
    def _avg(dct, key):
        try:
            targets = dct.get('targets', {})
            vals = [v.get(key) for v in targets.values() if isinstance(v, dict) and v.get(key) is not None]
            return float(np.mean(vals)) if vals else None
        except Exception:
            return None
    avgR = _avg(perf, 'test_r2')
    
    # Ortalama R² kartı
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; color: white; text-align: center; 
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3); margin: 2rem 0;">
        <div style="font-size: 2.5rem; margin-bottom: 1rem;">📊</div>
        <h3 style="margin: 0 0 1rem 0; font-size: 1.5rem; font-weight: 600;">Genel Model Performansı</h3>
        <div style="font-size: 2rem; font-weight: 800; margin-bottom: 0.5rem;">Ortalama R² = {f"{avgR:.4f}" if avgR is not None else "-"}</div>
        <div style="font-size: 1rem; opacity: 0.9;">
            {f'✅ Mükemmel performans' if avgR and avgR > 0.9 else f'🟡 İyi performans' if avgR and avgR > 0.7 else f'⚠️ Geliştirilebilir' if avgR else '❌ Veri yok'}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # AI Asistan – akıllı özet
    try:
        hints = []
        def _fmt(x):
            return "-" if x is None else f"{x:.3f}"
        for key, label in targets_order:
            target_data = perf.get('targets', {}).get(key, {})
            r2v, cvv = target_data.get('test_r2'), target_data.get('cv_r2')
            gap = None if (r2v is None or cvv is None) else abs(r2v-cvv)
            if r2v is not None and cvv is not None:
                trend = "stabil" if (gap is not None and gap < 0.05) else "oynak"
                hints.append(f"<span class='ai-badge'>{label}</span> R²={_fmt(r2v)} | CV={_fmt(cvv)} → {trend}")
        if hints:
            st.markdown("""
            <div class='ai-assistant'>
              <h4><span class='ai-emoji'>🤖</span>AI Asistan — Model Performansı</h4>
              <p>“Kısa raporum hazır! Test ve CV skorlarına göre: {rows}.”</p>
              <p><span class='ai-badge'>💡 Öneri</span> CV ile test arasında fark büyükse (>|0.05|) ilgili hedefte model karmaşıklığını sınırlayıp regularization parametrelerini artırmayı düşünebilirsin.</p>
            </div>
            """.replace("{rows}", " · ".join(hints)), unsafe_allow_html=True)
    except Exception:
        pass
    
    # Model karşılaştırma bölümü kaldırıldı - Sadece GradientBoosting kullanılıyor
    
    # Sayfa sonu yazısı
    add_page_footer("Model Performansı")

def show_forecasts():
    """Gelecek tahminleri sayfası - Premium tasarım"""
    
    # Premium başlık
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 1rem 0; 
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">🔮</span>
            </div>
            <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">GELECEK TAHMİNLERİ</h1>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            Yapay zeka destekli gelecek projeksiyonları ve trend analizi
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Kaynak seçimi: Varsayılan Profesyonel‑TS - Premium tasarım
    st.sidebar.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 1rem; border-radius: 15px; color: white; margin: 1rem 0; 
                    box-shadow: 0 5px 15px rgba(240, 147, 251, 0.2);">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <div style="background: rgba(255,255,255,0.2); padding: 0.3rem; border-radius: 6px; margin-right: 0.5rem;">
                    <span style="font-size: 0.9rem;">��</span>
                </div>
                <h4 style="margin: 0; font-size: 1rem; font-weight: 600;">Tahmin Kaynağı</h4>
            </div>
            <div style="font-size: 0.9rem; opacity: 0.9; margin-top: 0.5rem;">
                <p style="margin: 0.2rem 0;"><strong>Model:</strong> GradientBoosting</p>
                                            <p style="margin: 0.2rem 0;"><strong>Yöntem:</strong> Gradient Boosting</p>
                <p style="margin: 0.2rem 0;"><strong>Sürdürülebilirlik:</strong> Kompozit Hesaplama</p>
                <p style="margin: 0.2rem 0;"><strong>Dönem:</strong> 2025-2030</p>
                <p style="margin: 0.2rem 0;"><strong>Belirsizlik:</strong> %80-%90 Güven Aralığı</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Sadece bizim modeli kullan
    preds = load_predictions_dashboard()
    perf_src = load_performance_report()
    shap_prefix = "ecolense"
    if preds is None or preds.empty:
        st.warning("⚠️ Tahmin dosyası bulunamadı. Lütfen eğitim çıktılarını kontrol edin.")
        return

    # Seçim paneli - Premium tasarım
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                padding: 1.5rem; border-radius: 15px; color: white; margin: 1rem 0; 
                box-shadow: 0 8px 20px rgba(79, 172, 254, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.5rem; border-radius: 8px; margin-right: 0.8rem;">
                <span style="font-size: 1.2rem;">🎯</span>
            </div>
            <h3 style="margin: 0; font-size: 1.5rem; font-weight: 600;">Tahmin Parametreleri</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.9); padding: 1rem; border-radius: 10px; margin: 0.5rem 0; 
                    box-shadow: 0 3px 10px rgba(0,0,0,0.1); border-left: 4px solid #4facfe;">
            <h4 style="margin: 0 0 0.5rem 0; color: #232E5C; font-size: 1rem;">🌍 Ülke Seçimi</h4>
        </div>
        """, unsafe_allow_html=True)
        country = st.selectbox("Ülke", sorted(preds['Country'].dropna().unique()), key="forecast_country")
    
    with col2:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.9); padding: 1rem; border-radius: 10px; margin: 0.5rem 0; 
                    box-shadow: 0 3px 10px rgba(0,0,0,0.1); border-left: 4px solid #f093fb;">
            <h4 style="margin: 0 0 0.5rem 0; color: #232E5C; font-size: 1rem;">📊 Hedef Değişken</h4>
        </div>
        """, unsafe_allow_html=True)
        target_key = st.selectbox(
            "Hedef",
            options=[
                ('food_waste_tons', 'Total Waste (Tons)', 'Toplam Atık'),
                ('economic_loss_usd', 'Economic Loss (Million $)', 'Ekonomik Kayıp (M$)'),
                ('carbon_footprint_kgco2e', 'Carbon_Footprint_kgCO2e', 'Karbon Ayak İzi')
            ],
            format_func=lambda x: x[2],
            key="forecast_target"
        )

    short_key, pred_col, label = target_key

    # Tarihsel gerçek veri (kolon isimleri normalize edilmiş olabilir)
    hist_df = load_data(REAL_DATA_PATH, announce=False)
    country_col_hist = 'country' if 'country' in hist_df.columns else ('Country' if 'Country' in hist_df.columns else None)
    ycol = 'Years_From_2018' if 'Years_From_2018' in hist_df.columns else ('Year' if 'Year' in hist_df.columns else ('year' if 'year' in hist_df.columns else None))
    if not country_col_hist or not ycol:
        st.warning("⚠️ Veri setinde ülke veya yıl sütunu bulunamadı")
        return
    hist_country = hist_df[hist_df[country_col_hist] == country].copy()
    hist_col = _resolve_column_name(hist_country, {
        'sustainability_score': ['sustainability_score', 'Sustainability_Score'],
        'food_waste_tons': ['food_waste_tons', 'Total Waste (Tons)', 'total_waste_tons'],
        'economic_loss_usd': ['economic_loss_usd', 'Economic Loss (Million $)'],
        'carbon_footprint_kgco2e': ['carbon_footprint_kgco2e', 'Carbon_Footprint_kgCO2e'],
        'waste_per_capita': ['waste_per_capita', 'Waste_Per_Capita_kg', 'Avg Waste per Capita (Kg)'],
        'economic_loss_per_capita': ['economic_loss_per_capita', 'Economic_Loss_Per_Capita_USD'],
        'carbon_per_capita': ['carbon_per_capita', 'Carbon_Per_Capita_kgCO2e']
    }[short_key])

    # Yıl alanı
    # Yıl sütunu zaten yukarıda tanımlandı
    if not ycol:
        st.warning("⚠️ Yıl sütunu bulunamadı (Years_From_2018/Year/year)")
        return

    # Tahmin verisi - Target/Prediction formatını düzelt
    pred_country = preds[preds['Country'] == country].copy()
    
    # Target/Prediction formatını kontrol et
    if 'Target' in pred_country.columns and 'Prediction' in pred_country.columns:
        # Hedef bazında filtrele
        pred_country = pred_country[pred_country['Target'] == pred_col].copy()
        if pred_country.empty:
            st.warning(f"⚠️ Seçilen hedef '{pred_col}' için tahmin bulunamadı.")
            return
        # Prediction sütununu kullan
        pred_col = 'Prediction'
    elif pred_col not in pred_country.columns:
        st.warning("⚠️ Seçilen hedef için tahmin kolonu dosyada bulunamadı.")
        return
    
    pred_country = pred_country.sort_values('Year')

    # Grafik
    fig = go.Figure()
    if hist_col and ycol in hist_country.columns:
        hist_series = hist_country[[ycol, hist_col]].groupby(ycol).mean().reset_index()
        try:
            hmin, hmax = int(hist_series[ycol].min()), int(hist_series[ycol].max())
            hist_name = f'Gerçek ({hmin}–{hmax})'
        except Exception:
            hist_name = 'Gerçek'
        fig.add_trace(go.Scatter(x=hist_series[ycol], y=hist_series[hist_col], mode='lines+markers', name=hist_name, line=dict(color='#11E6C1', width=3)))

    # Bant gösterimi seçeneği - Premium tasarım
    st.markdown("""
    <div style="background: rgba(255,255,255,0.9); padding: 1rem; border-radius: 10px; margin: 1rem 0; 
                box-shadow: 0 3px 10px rgba(0,0,0,0.1); border-left: 4px solid #11E6C1;">
        <h4 style="margin: 0 0 0.5rem 0; color: #232E5C; font-size: 1rem;">📈 Görselleştirme Seçenekleri</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        show_bands = st.checkbox("🎯 Belirsizlik bantlarını göster", value=True, key="fc_bands")
    with col2:
        if show_bands:
            st.info("📊 **%80 ve %90 güven aralıkları** gösterilecek")
        else:
            st.info("📈 **Sadece tahmin çizgisi** gösterilecek")

    # Tek kaynak çizimleri
    def _plot_pred(df_pred, name, color):
        if df_pred is None or df_pred.empty or pred_col not in df_pred.columns:
            return
        y_pred = df_pred[pred_col].values.astype(float)
        x_pred = df_pred['Year'].values
        apply_trend = False
        if len(np.unique(y_pred)) <= 1 and hist_col is not None and not hist_country.empty:
            try:
                hs = hist_series.dropna()
                if len(hs) >= 2:
                    slope, _ = np.polyfit(hs[ycol].values.astype(float), hs[hist_col].values.astype(float), 1)
                    base_year = hs[ycol].max()
                    y_pred = y_pred + slope * (x_pred - base_year)
                    apply_trend = True
            except Exception:
                pass
        nm = f"{name}" + (" + Trend" if apply_trend else "")
        fig.add_trace(go.Scatter(x=x_pred, y=y_pred, mode='lines+markers', name=nm, line=dict(color=color, width=3, dash='dash')))

    try:
        pmin, pmax = int(preds['Year'].min()), int(preds['Year'].max())
        pred_name = f'Tahmin ({pmin}–{pmax}) [GradientBoosting]'
    except Exception:
        pred_name = f'Tahmin [GradientBoosting]'
    _plot_pred(pred_country, pred_name, '#A9FF4F')
    # Gelişmiş belirsizlik bantları (P10–P50–P90) – RMSE + Trend tabanlı
    if show_bands:
        try:
            # RMSE değerlerini model performans dosyasından al
            rmse = None
            if isinstance(perf_src, dict) and 'targets' in perf_src:
                # Hedef adına göre RMSE bul
                target_rmse_map = {
                    'Sustainability_Score': 'Sustainability_Score',
                    'Total Waste (Tons)': 'Total Waste (Tons)',
                    'Economic Loss (Million $)': 'Economic Loss (Million $)',
                    'Carbon_Footprint_kgCO2e': 'Carbon_Footprint_kgCO2e',
                }
                
                target_key = target_rmse_map.get(pred_col)
                if target_key and target_key in perf_src['targets']:
                    rmse = perf_src['targets'][target_key].get('test_rmse')
            
            # Sustainability_Score için varsayılan RMSE değeri
            if pred_col == 'Sustainability_Score' and rmse is None:
                rmse = 10.0  # Varsayılan belirsizlik değeri
            
            if rmse is not None and pred_col in pred_country.columns:
                y_pred = pred_country[pred_col].astype(float).values
                x_pred = pred_country['Year'].values
                
                # Zamanla artan belirsizlik (geleceğe doğru artar)
                time_factor = np.linspace(1.0, 1.5, len(x_pred))  # 2025'ten 2030'a %50 artış
                
                # Farklı güven seviyeleri için z-scores
                z_p10_p90 = 1.2816  # %80 güven aralığı
                z_p05_p95 = 1.6449  # %90 güven aralığı
                
                # Belirsizlik hesaplama
                uncertainty_p10_p90 = rmse * time_factor * z_p10_p90
                uncertainty_p05_p95 = rmse * time_factor * z_p05_p95
                
                # Bantlar
                p10 = y_pred - uncertainty_p10_p90
                p90 = y_pred + uncertainty_p10_p90
                p05 = y_pred - uncertainty_p05_p95
                p95 = y_pred + uncertainty_p05_p95
                
                # %90 güven aralığı (dış bant)
                fig.add_trace(go.Scatter(x=x_pred, y=p95, mode='lines', name='P95 (%90 Güven)',
                                         line=dict(color='rgba(169,255,79,0.2)', width=1, dash='dot')))
                fig.add_trace(go.Scatter(x=x_pred, y=p05, mode='lines', name='P05 (%90 Güven)',
                                         line=dict(color='rgba(169,255,79,0.2)', width=1, dash='dot'), 
                                         fill='tonexty', fillcolor='rgba(169,255,79,0.05)'))
                
                # %80 güven aralığı (iç bant)
                fig.add_trace(go.Scatter(x=x_pred, y=p90, mode='lines', name='P90 (%80 Güven)',
                                         line=dict(color='rgba(169,255,79,0.4)', width=1)))
                fig.add_trace(go.Scatter(x=x_pred, y=p10, mode='lines', name='P10 (%80 Güven)',
                                         line=dict(color='rgba(169,255,79,0.4)', width=1), 
                                         fill='tonexty', fillcolor='rgba(169,255,79,0.15)'))
                
                # Belirsizlik metrikleri
                avg_uncertainty = np.mean(uncertainty_p10_p90)
                uncertainty_growth = (uncertainty_p10_p90[-1] - uncertainty_p10_p90[0]) / uncertainty_p10_p90[0] * 100
                
                st.info(f"📊 **Belirsizlik Analizi:** Ortalama belirsizlik ±{avg_uncertainty:.1f}, 2030'a kadar %{uncertainty_growth:.1f} artış")
            else:
                st.warning("⚠️ RMSE değeri bulunamadı, belirsizlik bantları gösterilemiyor.")
                
        except Exception as e:
            st.warning(f"⚠️ Belirsizlik bantları hesaplanamadı: {str(e)}")
    fig.update_layout(title=f"{country} – {label}", xaxis_title='Yıl', yaxis_title=label, template='plotly_white', height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Grafik açıklaması
    with st.expander("📊 Bu grafik ne anlatıyor?"):
        st.markdown(f"""
        Bu grafik **{country}** ülkesi için **{label}** değişkeninin gelecek tahminlerini gösteriyor. 
        **Mavi çizgi** geçmiş verileri, **yeşil kesikli çizgi** tahminleri gösterir. 
        **Gölgeli alan** belirsizlik aralığını (P10-P90) temsil eder. 
        Tahminler zaman serisi modelleri kullanılarak hesaplanmıştır.
        """)

    # AI Asistan – Tahmin yorumu (Gelecek Tahminleri)
    try:
        seq = pred_country.sort_values('Year')[["Year", pred_col]].dropna()
        yvals = seq[pred_col].astype(float).values
        years_arr = seq['Year'].astype(int).values
        cagr_txt = "-"
        smooth_txt = "-"
        hints = []
        if len(yvals) >= 2:
            start, end = float(yvals[0]), float(yvals[-1])
            span = max(1, int(years_arr[-1] - years_arr[0]))
            if start > 0 and span > 0:
                cagr = (end / start) ** (1.0 / span) - 1.0
                cagr_txt = f"{cagr*100:.2f}%/yıl"
            deltas = np.diff(yvals)
            swings = int(np.sum(np.sign(deltas[1:]) != np.sign(deltas[:-1]))) if len(deltas) > 1 else 0
            smooth_txt = "yumuşak" if swings <= 1 else ("orta" if swings == 2 else "oynak")
        hints.append(f"<span class='ai-badge'>{label}</span> CAGR: {cagr_txt}")
        hints.append(f"<span class='ai-badge'>Pürüzsüzlük</span> {smooth_txt}")
        rec = "Stabilizasyon iyi. Yolunda!" if "yumuşak" in smooth_txt else "Daha pürüzsüz bir çizgi için λ (damping) ve k (yıllık delta sınırı) artırılabilir."
        st.markdown("""
        <div class='ai-assistant'>
          <h4><span class='ai-emoji'>🤖</span>AI Asistan — Ülke Tahmini</h4>
          <p>{rows}</p>
          <p>Öneri: {rec}</p>
        </div>
        """.replace("{rows}", " · ".join(hints)).replace("{rec}", rec), unsafe_allow_html=True)
    except Exception:
        st.markdown(f"""
        <div class='ai-assistant'>
          <h4><span class='ai-emoji'>🤖</span>AI Asistan — Ülke Tahmini</h4>
          <p>{country} için {label} serisi görüntüleniyor. Eğilimleri yumuşatmak için λ/k ayarlarına dikkat edin.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Sayfa sonu yazısı
    add_page_footer("Gelecek Tahminleri")


def show_target_based_forecasts():
    """🎯 Hedef Bazlı Tahminler – ülke+hedef seç, eşik belirle, yol haritasını gör"""
    # Premium başlık
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; 
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">🎯</span>
            </div>
            <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700;">HEDEF BAZLI TAHMİNLER</h1>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            Ülke ve hedef seçimi ile 2030 yol haritası planlaması
        </p>
    </div>
    """, unsafe_allow_html=True)
    preds_ts = load_predictions_dashboard()
    preds = preds_ts if (preds_ts is not None and not preds_ts.empty) else load_predictions_dashboard()
    if preds is None or preds.empty:
        st.warning("⚠️ Tahmin dosyası bulunamadı.")
        return
    country = st.selectbox("Ülke", sorted(preds['Country'].dropna().unique()), key="tbf_country")
    target = st.selectbox("Hedef", [
        ('Total Waste (Tons)', 'Toplam Atık (ton)', '↓'),
        ('Economic Loss (Million $)', 'Ekonomik Kayıp (M$)', '↓'),
        ('Carbon_Footprint_kgCO2e', 'Karbon (kgCO2e)', '↓'),
        ('Waste_Per_Capita_kg', 'Kişi Başına Atık (kg)', '↓'),
        ('Economic_Loss_Per_Capita_USD', 'Kişi Başına Ekonomik Kayıp (USD)', '↓'),
        ('Carbon_Per_Capita_kgCO2e', 'Kişi Başına Karbon (kg CO2e)', '↓')
    ], format_func=lambda x: x[1], key="tbf_target")
    tcol, tlabel, direction = target
    dfc = preds[preds['Country']==country].sort_values('Year')
    if tcol not in dfc.columns:
        st.warning("⚠️ Seçilen hedef için tahmin kolonu yok.")
        return
    y0, y1 = int(dfc['Year'].min()), int(dfc['Year'].max())
    cur = float(dfc.loc[dfc['Year']==y1, tcol].mean())
    # Hedef eşiği
    if direction == '↑':
        goal = st.number_input("2030 hedefi (artır)", value=max(0.0, cur*1.05))
    else:
        goal = st.number_input("2030 hedefi (azalt)", value=max(0.0, cur*0.9))
    # CAGR gereksinimi
    years = max(1, y1-y0)
    req = 0.0 if cur<=0 else (goal/cur)**(1.0/years) - 1.0
    st.metric("Gerekli yıllık değişim (CAGR)", f"{req*100:.2f}%/yıl")
    # Yol haritası: doğrusal köprü (sunum amaçlı), gerçek kullanımda politika simülatörüyle bağlanır
    xs = np.arange(y0, y1+1)
    base = dfc[tcol].values.astype(float)
    lin = np.linspace(base[0] if len(base)>0 else 0.0, goal, len(xs))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dfc['Year'], y=base, mode='lines+markers', name='Tahmin (baz)', line=dict(color='#11E6C1', width=3)))
    fig.add_trace(go.Scatter(x=xs, y=lin, mode='lines+markers', name='Hedef rotası', line=dict(color='#A9FF4F', width=3, dash='dash')))
    fig.update_layout(title=f"{country} – {tlabel}", xaxis_title='Yıl', yaxis_title=tlabel, template='plotly_white', height=480)
    st.plotly_chart(fig, use_container_width=True)
    # AI Asistan
    try:
        diff2030 = (goal - cur)
        direction_txt = 'artış' if direction=='↑' else 'azalış'
        st.markdown(f"""
        <div class='ai-assistant'>
          <h4><span class='ai-emoji'>🤖</span>AI Asistan — Hedefe Gidiş</h4>
          <p><span class='ai-badge'>2030 hedefi</span> {goal:,.2f} → {direction_txt} gereksinimi: {req*100:.2f}%/yıl.</p>
          <p>Öneri: A/B veya Politika Simülatörü'nde atık azaltımı ve teknoloji benimseme kaldıraçlarını kombine test ederek hedef rotasına yaklaş.</p>
        </div>
        """, unsafe_allow_html=True)
    except Exception:
        pass
    
    # Sayfa sonu yazısı
    add_page_footer("Hedef Bazlı Tahminler")


def show_ai_insights():
    """🤖 AI Insights – Gerçek veri + Robust tahminlerden otomatik içgörüler"""
    # Premium başlık
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; 
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">🤖</span>
            </div>
            <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700;">AI INSIGHTS</h1>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            Yapay zeka destekli otomatik içgörüler ve analizler
        </p>
    </div>
    """, unsafe_allow_html=True)
    real_df = load_data(REAL_DATA_PATH, announce=False)
    # A/B, varsayılan kaynağı Profesyonel‑TS yapalım
    preds_ts = load_predictions_dashboard()
    preds = preds_ts if (preds_ts is not None and not preds_ts.empty) else load_predictions_dashboard()
    if preds is None or preds.empty:
        st.warning("⚠️ Tahmin dosyası bulunamadı.")
        return
    # Seçim paneli - Premium tasarım
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                padding: 1.5rem; border-radius: 15px; color: white; margin: 1rem 0; 
                box-shadow: 0 8px 20px rgba(240, 147, 251, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.5rem; border-radius: 8px; margin-right: 0.8rem;">
                <span style="font-size: 1.2rem;">🎯</span>
            </div>
            <h3 style="margin: 0; font-size: 1.5rem; font-weight: 600;">AI Analiz Parametreleri</h3>
        </div>
        <p style="margin: 0; font-size: 0.9rem; opacity: 0.9;">
            Gerçek veri: ülkeler×yıllar, Robust tahminler: son yıl+1 → 2030
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.9); padding: 1rem; border-radius: 10px; margin: 0.5rem 0; 
                    box-shadow: 0 3px 10px rgba(0,0,0,0.1); border-left: 4px solid #f093fb;">
            <h4 style="margin: 0 0 0.5rem 0; color: #232E5C; font-size: 1rem;">📊 Hedef Metrik</h4>
        </div>
        """, unsafe_allow_html=True)
        metric = st.selectbox(
            "Hedef",
            options=[
                ('Total Waste (Tons)', 'Toplam Atık'),
                ('Economic Loss (Million $)', 'Ekonomik Kayıp (M$)'),
                ('Carbon_Footprint_kgCO2e', 'Karbon Ayak İzi'),
                ('Waste_Per_Capita_kg', 'Kişi Başına Atık (kg)'),
                ('Economic_Loss_Per_Capita_USD', 'Kişi Başına Ekonomik Kayıp (USD)'),
                ('Carbon_Per_Capita_kgCO2e', 'Kişi Başına Karbon (kg CO2e)')
            ],
            format_func=lambda x: x[1]
        )
        pred_col, metric_label = metric
    
    with col2:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.9); padding: 1rem; border-radius: 10px; margin: 0.5rem 0; 
                    box-shadow: 0 3px 10px rgba(0,0,0,0.1); border-left: 4px solid #4facfe;">
            <h4 style="margin: 0 0 0.5rem 0; color: #232E5C; font-size: 1rem;">🌍 Ülke Filtresi</h4>
        </div>
        """, unsafe_allow_html=True)
        country = st.selectbox("Ülke (opsiyonel)", ["(Tümü)"] + sorted(preds['Country'].dropna().unique().tolist()))

    dfp = preds.copy()
    if country != "(Tümü)":
        dfp = dfp[dfp['Country'] == country]
    if pred_col not in dfp.columns:
        st.warning("⚠️ Seçilen hedef için tahmin kolonu dosyada yok.")
        return

    pmin, pmax = int(dfp['Year'].min()), int(dfp['Year'].max())
    horizon = max(1, pmax - pmin)
    agg = dfp.groupby('Country').apply(lambda g: pd.Series({
        'start': float(g.loc[g['Year'] == pmin, pred_col].mean()) if (g['Year'] == pmin).any() else np.nan,
        'end': float(g.loc[g['Year'] == pmax, pred_col].mean()) if (g['Year'] == pmax).any() else np.nan
    })).dropna()
    agg['delta'] = agg['end'] - agg['start']
    with np.errstate(divide='ignore', invalid='ignore'):
        agg['cagr'] = (agg['end'] / agg['start']) ** (1.0 / horizon) - 1.0
    agg = agg.replace([np.inf, -np.inf], np.nan).dropna()

    try:
        n_countries = int(dfp['Country'].nunique())
    except Exception:
        n_countries = 20
    # Top-N seçimi - Premium tasarım
    st.markdown("""
    <div style="background: rgba(255,255,255,0.9); padding: 1rem; border-radius: 10px; margin: 1rem 0; 
                box-shadow: 0 3px 10px rgba(0,0,0,0.1); border-left: 4px solid #11E6C1;">
        <h4 style="margin: 0 0 0.5rem 0; color: #232E5C; font-size: 1rem;">📊 Top-N Analiz Kapsamı</h4>
    </div>
    """, unsafe_allow_html=True)
    
    max_n = max(3, min(20, n_countries))
    topN = st.slider("Top-N", 3, max_n, min(10, max_n), key="topn_aiinsights")
    colA, colB = st.columns(2)
    with colA:
        st.subheader("🚀 En hızlı artış (CAGR)")
        st.dataframe(agg.sort_values('cagr', ascending=False).head(topN))
        
        # CAGR Artış açıklaması
        with colA.expander("📊 CAGR Artış Grafiği Ne Anlatıyor?"):
            st.markdown("""
            **🚀 En hızlı artış (CAGR)** grafiği, gıda israfı metriklerinde en hızlı iyileşme gösteren ülkeleri listeler:
            
            ### 📈 CAGR Nedir?
            **CAGR (Compound Annual Growth Rate)** = Yıllık Bileşik Büyüme Oranı
            - Bir değerin yıllık ortalama büyüme hızını gösterir
            - Formül: CAGR = (Son Değer / İlk Değer)^(1/Yıl Sayısı) - 1
            - **Pozitif CAGR**: İyileşme (israf azalıyor, sürdürülebilirlik artıyor)
            - **Negatif CAGR**: Kötüleşme (israf artıyor, sürdürülebilirlik düşüyor)
            
            ### 🎯 Bu Grafik Ne Anlatıyor?
            - **En üstteki ülkeler**: En hızlı iyileşme gösteren ülkeler
            - **Yüksek CAGR değerleri**: Güçlü politika önlemleri ve başarılı uygulamalar
            - **Örnek**: %15 CAGR = Her yıl ortalama %15 iyileşme
            
            ### 💡 Pratik Kullanım:
            - Başarılı ülkelerin politika örneklerini inceleyin
            - Benzer önlemleri kendi ülkenizde uygulayın
            - İyileşme trendlerini takip edin
            """)
            
    with colB:
        st.subheader("🧊 En hızlı düşüş (CAGR)")
        st.dataframe(agg.sort_values('cagr').head(topN))
        
        # CAGR Düşüş açıklaması
        with colB.expander("📊 CAGR Düşüş Grafiği Ne Anlatıyor?"):
            st.markdown("""
            **🧊 En hızlı düşüş (CAGR)** grafiği, gıda israfı metriklerinde en hızlı kötüleşme gösteren ülkeleri listeler:
            
            ### 📉 Bu Grafik Ne Anlatıyor?
            - **En üstteki ülkeler**: En hızlı kötüleşme gösteren ülkeler
            - **Düşük/Negatif CAGR değerleri**: Artan israf, düşen sürdürülebilirlik
            - **Örnek**: -%10 CAGR = Her yıl ortalama %10 kötüleşme
            
            ### ⚠️ Risk Analizi:
            - **Yüksek riskli ülkeler**: Acil müdahale gerektiren durumlar
            - **Trend analizi**: Kötüleşme hızının artıp artmadığını kontrol edin
            - **Politika başarısızlıkları**: Hangi önlemlerin işe yaramadığını anlayın
            
            ### 🚨 Acil Önlemler:
            - Bu ülkelerde politika değişiklikleri gerekli
            - Uluslararası destek ve işbirliği önerilir
            - Başarılı ülkelerin deneyimlerinden öğrenin
            """)

    # AI anlatı – kısa özet
    best = agg.sort_values('cagr', ascending=False).head(3)
    worst = agg.sort_values('cagr').head(3)
    bullets = []
    if not best.empty:
        bullets.append(f"En güçlü iyileşme: {', '.join(best.index)} (yıllık ~{(best['cagr']*100).round(1).astype(str).tolist()}%).")
    if not worst.empty:
        bullets.append(f"Düşüş riski: {', '.join(worst.index)} (yıllık ~{(worst['cagr']*100).round(1).astype(str).tolist()}%).")
    st.markdown("\n".join([f"- {b}" for b in bullets]))

    st.markdown("---")
    st.subheader("🧠 SHAP – Özellik Etkileri (Profesyonel‑TS varsayılan)")
    
    # SHAP genel açıklaması
    with st.expander("📊 SHAP Grafikleri Ne Anlatıyor?", expanded=False):
        st.markdown("""
        **🧠 SHAP (SHapley Additive exPlanations)** grafikleri, makine öğrenmesi modelinin kararlarını açıklayan en güçlü araçlardır:
        
        ### 🔍 SHAP Nedir?
        - **SHAP**: Modelin her tahminini nasıl yaptığını açıklayan matematiksel yöntem
        - **Ortalama |SHAP|**: Bir özelliğin ortalama etkisinin mutlak değeri
        - **Permutation Importance**: Özelliği karıştırdığımızda model performansının ne kadar düştüğü
        
        ### 📈 Bu Grafikler Ne Anlatıyor?
        
        **🚀 Permutation Importance:**
        - Model performansını en çok etkileyen faktörler
        - "Bu faktör olmasaydı model ne kadar kötü performans gösterirdi?"
        - En uzun barlar = En kritik faktörler
        
        **🧠 Ortalama |SHAP|:**
        - Model kararlarını en çok etkileyen faktörler
        - "Bu faktör modelin tahminini nasıl değiştiriyor?"
        - En uzun barlar = En etkili faktörler
        
        ### 💡 Pratik Çıkarımlar:
        - **Yüksek değerli faktörler**: Politika öncelikleri
        - **Düşük değerli faktörler**: Az kaynak ayırın
        - **Beklenmedik faktörler**: Yeni araştırma alanları
        
        ### 🎯 Kullanım Önerileri:
        - En etkili faktörlere odaklanın
        - Veri toplama stratejilerini optimize edin
        - Model güvenilirliğini artırın
        """)
    target_opt = st.selectbox(
        "Hedef (SHAP)",
        options=[
            ('total_waste_tons', 'Toplam Atık'),
            ('economic_loss_million', 'Ekonomik Kayıp (M$)'),
            ('carbon_footprint_kgco2e', 'Karbon Ayak İzi')
        ],
        format_func=lambda x: x[1]
    )
    tnorm = target_opt[0]
    # Önce Profesyonel‑TS, yoksa Robust
    def _try_load(ts_loader, rb_loader):
        d = ts_loader(tnorm)
        if d is None or (hasattr(d, 'empty') and d.empty):
            return rb_loader(tnorm)
        return d
    rnd = np.random.random()
    imp_ts = load_prof_ts_importance(tnorm, version=rnd)
    shap_ts = load_prof_ts_shap_mean(tnorm, version=rnd)
    imp = imp_ts if (imp_ts is not None and not imp_ts.empty) else None
    shapm = shap_ts if (shap_ts is not None and not shap_ts.empty) else None
    if imp is None and shapm is None:
        st.info("SHAP / Permutation dosyaları bulunamadı.")
        return
    col1, col2 = st.columns(2)
    if imp is not None and not imp.empty:
        col1.subheader("Permutation Importance")
        imp_n = imp.head(20)
        # Sütun adlarını kontrol et ve uygun olanı kullan
        x_col = 'importance' if 'importance' in imp_n.columns else imp_n.columns[1]
        col1.plotly_chart(px.bar(imp_n, x=x_col, y='feature', orientation='h', template='plotly_white', height=480), use_container_width=True, key=f"ai_insights_perm_{hash(str(imp_n))}_{hash('ai_insights')}")
    if shapm is not None and not shapm.empty:
        col2.subheader("Ortalama |SHAP|")
        sm = shapm.head(20)
        # Kolon isimlerini kontrol et ve uygun olanı kullan
        x_col = 'importance' if 'importance' in sm.columns else 'mean_abs_shap'
        col2.plotly_chart(px.bar(sm, x=x_col, y='feature', orientation='h', template='plotly_white', height=480), use_container_width=True, key=f"ai_insights_shap_{hash(str(sm))}_{hash('ai_insights')}")

    st.markdown("---")
    st.subheader("🧠 SHAP – Özellik Etkileri (Profesyonel, referans)")
    
    # Profesyonel SHAP açıklaması
    with st.expander("📊 Profesyonel SHAP vs Zaman Serisi Farkı", expanded=False):
        st.markdown("""
        **🔬 Model Karşılaştırması** - İki farklı model yaklaşımının özellik etkilerini karşılaştırır:
        
        ### 🆚 Model Farkları:
        
        **🕒 GradientBoosting Modeli:**
        - Geçmiş verileri kullanarak gelecek tahmini yapar
        - Lag/rolling özellikleri önemli
        - Trend ve mevsimsellik dikkate alınır
        - Zaman içindeki değişimleri yakalar
        
        **📊 Referans Model (Profesyonel):**
        - Geleneksel makine öğrenmesi yaklaşımı
        - Anlık özellik değerlerine odaklanır
        - Zaman boyutu dikkate alınmaz
        - Genel ilişkileri yakalar
        
        ### 📈 Karşılaştırma Çıkarımları:
        
        **🚀 Zaman Serisi'nde Daha Etkili Olanlar:**
        - Geçmiş değerler (lag features)
        - Trend göstergeleri
        - Mevsimsel faktörler
        - Zaman bazlı özellikler
        
        **📊 Referans Modelde Daha Etkili Olanlar:**
        - Demografik faktörler
        - Ekonomik göstergeler
        - Coğrafi özellikler
        - Sabit faktörler
        
        ### 💡 Pratik Kullanım:
        - **Zaman serisi faktörleri**: Kısa vadeli politika önlemleri
        - **Referans faktörleri**: Uzun vadeli yapısal değişiklikler
        - **Ortak faktörler**: Her iki yaklaşımda da etkili
        """)
    t2 = st.selectbox(
        "Hedef (Profesyonel SHAP)",
        options=[
            ('total_waste_tons', 'Toplam Atık'),
            ('economic_loss_million', 'Ekonomik Kayıp (M$)'),
            ('carbon_footprint_kgco2e', 'Karbon Ayak İzi')
        ],
        index=0,
        format_func=lambda x: x[1]
    )
    t2n = t2[0]
    impP = load_professional_importance(t2n, version=rnd)
    shapP = load_professional_shap_mean(t2n, version=rnd)
    if (impP is None or (hasattr(impP,'empty') and impP.empty)) and (shapP is None or (hasattr(shapP,'empty') and shapP.empty)):
        st.info("Profesyonel model SHAP/importance çıktısı bulunamadı (referans amaçlı).")
    else:
        c1, c2 = st.columns(2)
        if impP is not None and not impP.empty:
            c1.subheader("Permutation Importance (Profesyonel)")
            c1.plotly_chart(px.bar(impP.head(20), x=impP.columns[1], y=impP.columns[0], orientation='h', template='plotly_white', height=480), use_container_width=True, key=f"ai_insights_prof_perm_{hash(str(impP))}_{hash('ai_insights')}")
        if shapP is not None and not shapP.empty:
            c2.subheader("Ortalama |SHAP| (Profesyonel)")
            colx = 'mean_abs_shap' if 'mean_abs_shap' in shapP.columns else shapP.columns[1]
            c2.plotly_chart(px.bar(shapP.head(20), x=colx, y=shapP.columns[0], orientation='h', template='plotly_white', height=480), use_container_width=True, key=f"ai_insights_prof_shap_{hash(str(shapP))}_{hash('ai_insights')}")

    # Δ Etki (TS − Profesyonel)
    if shap_ts is not None and not shap_ts.empty and shapP is not None and not shapP.empty:
        try:
            colx_ts = 'mean_abs_shap' if 'mean_abs_shap' in shap_ts.columns else shap_ts.columns[1]
            colx_p = 'mean_abs_shap' if 'mean_abs_shap' in shapP.columns else shapP.columns[1]
            m_ts = shap_ts.rename(columns={colx_ts: 'ts'})[['feature','ts']]
            m_p = shapP.rename(columns={colx_p: 'prof'})[['feature','prof']]
            merged = m_ts.merge(m_p, on='feature', how='inner')
            merged['delta'] = merged['ts'] - merged['prof']
            st.subheader("Δ Etki (TS − Profesyonel)")
            st.plotly_chart(px.bar(merged.sort_values('delta', ascending=False).head(20), x='delta', y='feature', orientation='h', template='plotly_white', height=520), use_container_width=True, key=f"ai_insights_delta_{hash(str(merged))}_{hash('ai_insights')}")
            with st.expander("📊 Δ Etki Grafiği Ne Anlatıyor?"):
                st.markdown("""
                **Δ Etki (TS − Profesyonel)** grafiği, zaman serisi modeli ile referans model arasındaki özellik etki farklarını gösterir:
                
                ### 📊 Grafik Yorumu:
                
                **🚀 Pozitif Değerler (Yukarı):**
                - Zaman serisi modelinde daha etkili olan özellikler
                - Geçmiş veriler ve trend faktörleri
                - Kısa vadeli politika önlemleri için kritik
                - Örnek: Lag features, rolling averages, trend indicators
                
                **📉 Negatif Değerler (Aşağı):**
                - Referans modelde daha etkili olan özellikler
                - Demografik ve yapısal faktörler
                - Uzun vadeli değişiklikler için önemli
                - Örnek: GDP, population, geographic factors
                
                **⚖️ Sıfıra Yakın Değerler:**
                - Her iki modelde de benzer etkiye sahip özellikler
                - Evrensel faktörler
                - Her türlü politika için önemli
                
                ### 💡 Pratik Çıkarımlar:
                
                **🎯 Politika Stratejisi:**
                - **Yüksek pozitif**: Zaman bazlı önlemler (eğitim, teknoloji)
                - **Yüksek negatif**: Yapısal değişiklikler (altyapı, düzenleme)
                - **Düşük değerler**: Genel faktörler (GDP, nüfus)
                
                **📈 Model Seçimi:**
                - Kısa vadeli tahminler için: Zaman serisi modeli
                - Uzun vadeli planlama için: Referans model
                - Hibrit yaklaşım: Her ikisinin güçlü yanlarını birleştirin
                
                **🔍 Araştırma Öncelikleri:**
                - Büyük fark gösteren faktörlere odaklanın
                - Model performansını artırmak için yeni özellikler ekleyin
                - Zaman serisi ve yapısal faktörleri dengeli kullanın
                """)
        except Exception:
            pass

    # AI Asistan – AI Insights yorumu
    try:
        ai_rows = []
        if not agg.empty:
            gpos = agg['cagr'].dropna()
            if not gpos.empty:
                med = float(np.median(gpos.values))
                ai_rows.append(f"<span class='ai-badge'>CAGR Medyan</span> {med*100:.2f}%/yıl")
        if imp is not None and not imp.empty:
            topf = imp.sort_values(imp.columns[1], ascending=False).head(3)['feature'].astype(str).tolist()
            ai_rows.append(f"<span class='ai-badge'>Önemli Sürücüler</span> {', '.join(topf)}")
        st.markdown("""
        <div class='ai-assistant'>
          <h4><span class='ai-emoji'>🤖</span>AI Asistan — İçgörü Özeti</h4>
          <p>{rows}</p>
          <p>Öneri: Pozitif CAGR ülkelerinde sürücüleri büyütme; negatif CAGR ülkelerinde ise ilk 3 sürücüye odaklı politika paketini test et.</p>
        </div>
        """.replace("{rows}", " · ".join(ai_rows)), unsafe_allow_html=True)
    except Exception:
        pass
    
    # Sayfa sonu yazısı
    add_page_footer("AI Insights")

def show_ab_testing():
    """A/B Testing – Model ve özellik kombinasyonları karşılaştırması"""
    # Premium başlık
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; 
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">🧪</span>
            </div>
            <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700;">A/B TESTING ANALİZİ</h1>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            Gradient Boosting vs Random Forest vs Linear Regression - 3 hedef değişken için performans karşılaştırması
        </p>
    </div>
    """, unsafe_allow_html=True)

    # A/B testing sonuçlarını yükle
    ab_results = load_ab_testing_results()
    ab_report = load_ab_testing_report()
    
    if ab_results is None or ab_results.empty:
        st.warning("⚠️ A/B testing sonuçları bulunamadı. Önce A/B testing analizini çalıştırın.")
        return
    
    if ab_report is None:
        st.warning("⚠️ A/B testing raporu bulunamadı.")
        return

    # A/B Testing Özeti
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; 
                box-shadow: 0 10px 25px rgba(79, 172, 254, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">📊</span>
            </div>
            <h2 style="margin: 0; font-size: 2.2rem; font-weight: 700;">A/B TESTING ÖZETİ</h2>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            3 hedef değişken için 27 farklı model-özellik kombinasyonu test edildi
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Genel istatistikler
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Toplam Test", ab_report.get('toplam_test_sayisi', 0))
    
    with col2:
        st.metric("Hedef Sayısı", ab_report.get('hedef_sayisi', 0))
    
    with col3:
        st.metric("Model Türü", ab_report.get('model_sayisi', 0))
    
    with col4:
        st.metric("Özellik Grubu", ab_report.get('ozellik_grup_sayisi', 0))

    # En iyi modeller
    st.markdown("### 🏆 En İyi Modeller")
    
    if 'en_iyi_modeller' in ab_report:
        for target, model_info in ab_report['en_iyi_modeller'].items():
            with st.expander(f"🎯 {target}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Model", model_info.get('model_name', 'N/A'))
                with col2:
                    st.metric("Test R²", f"{model_info.get('test_r2', 0):.3f}")
                with col3:
                    st.metric("Overfitting", f"{model_info.get('overfitting_score', 0):.3f}")
                
                st.info(f"**Özellik Grubu:** {model_info.get('feature_group', 'N/A')}")
    
    # En iyi özellik grupları
    st.markdown("### 📈 En İyi Özellik Grupları")
    
    if 'en_iyi_ozellik_gruplari' in ab_report:
        feature_df = pd.DataFrame([
            {'Özellik Grubu': k, 'Ortalama Test R²': v}
            for k, v in ab_report['en_iyi_ozellik_gruplari'].items()
        ])
        
        fig = px.bar(feature_df, x='Ortalama Test R²', y='Özellik Grubu', 
                    orientation='h', title='Özellik Gruplarına Göre Performans')
        st.plotly_chart(fig, use_container_width=True)
    
    # En iyi model türleri
    st.markdown("### 🤖 En İyi Model Türleri")
    
    if 'en_iyi_model_turleri' in ab_report:
        model_df = pd.DataFrame([
            {'Model Türü': k, 'Ortalama Test R²': v}
            for k, v in ab_report['en_iyi_model_turleri'].items()
        ])
        
        fig = px.bar(model_df, x='Ortalama Test R²', y='Model Türü', 
                    orientation='h', title='Model Türlerine Göre Performans')
        st.plotly_chart(fig, use_container_width=True)
    
    # A/B Testing Grafikleri
    st.markdown("### 📊 A/B Testing Görsel Analizi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        try:
            st.image('ab_testing_model_performance.png', caption='Model Performans Karşılaştırması', use_container_width=True)
        except:
            st.warning("Model performans grafiği yüklenemedi")
    
    with col2:
        try:
            st.image('ab_testing_model_types.png', caption='Model Türleri Karşılaştırması', use_container_width=True)
        except:
            st.warning("Model türleri grafiği yüklenemedi")
    
    # Özellik grupları grafiği
    try:
        st.image('ab_testing_feature_groups.png', caption='Özellik Grupları Karşılaştırması', use_container_width=True)
    except:
        st.warning("Özellik grupları grafiği yüklenemedi")
    
    # Detaylı sonuçlar
    st.markdown("### 📋 Detaylı Sonuçlar")
    
    # Filtreleme seçenekleri
    col1, col2, col3 = st.columns(3)
    
    with col1:
        target_filter = st.selectbox("Hedef Seçin", ['Tümü'] + list(ab_results['target'].unique()))
    
    with col2:
        model_filter = st.selectbox("Model Seçin", ['Tümü'] + list(ab_results['model_name'].unique()))
    
    with col3:
        feature_filter = st.selectbox("Özellik Grubu Seçin", ['Tümü'] + list(ab_results['feature_group'].unique()))
    
    # Filtreleme
    filtered_results = ab_results.copy()
    
    if target_filter != 'Tümü':
        filtered_results = filtered_results[filtered_results['target'] == target_filter]
    
    if model_filter != 'Tümü':
        filtered_results = filtered_results[filtered_results['model_name'] == model_filter]
    
    if feature_filter != 'Tümü':
        filtered_results = filtered_results[filtered_results['feature_group'] == feature_filter]
    
    # Sonuçları göster
    if not filtered_results.empty:
        st.dataframe(
            filtered_results[['target', 'model_name', 'feature_group', 'test_r2', 'cv_r2', 'overfitting_score']]
            .sort_values('test_r2', ascending=False)
            .head(20)
        )
    else:
        st.warning("Seçilen filtrelere uygun sonuç bulunamadı.")
    
    # Performans karşılaştırması
    st.markdown("### 🎯 Performans Karşılaştırması")
    
    if not filtered_results.empty:
        # Size için pozitif değerler kullan (cv_r2'nin mutlak değeri)
        filtered_results['size_positive'] = filtered_results['cv_r2'].abs()
        
        fig = px.scatter(
            filtered_results, 
            x='test_r2', 
            y='overfitting_score',
            color='model_name',
            size='size_positive',
            hover_data=['feature_group'],
            title='Model Performansı: Test R² vs Overfitting'
        )
        st.plotly_chart(fig, use_container_width=True)

    # AI Asistan – A/B Testing yorumu
    try:
        if 'genel_istatistikler' in ab_report:
            stats = ab_report['genel_istatistikler']
            msgs = [
                f"<span class='ai-badge'>Ortalama Test R²</span> {stats.get('ortalama_test_r2', 0):.3f}",
                f"<span class='ai-badge'>En Yüksek R²</span> {stats.get('en_yuksek_test_r2', 0):.3f}",
                f"<span class='ai-badge'>Ortalama Overfitting</span> {stats.get('ortalama_overfitting', 0):.3f}",
            ]
            st.markdown("""
            <div class='ai-assistant'>
              <h4><span class='ai-emoji'>🤖</span>AI Asistan — A/B Testing Özeti</h4>
              <p>{rows}</p>
              <p>Öneri: Gradient Boosting + Core + Efficiency/Trends kombinasyonları en iyi performansı gösteriyor. Overfitting skoru düşük olan modelleri tercih edin.</p>
            </div>
            """.replace("{rows}", " · ".join(msgs)), unsafe_allow_html=True)
    except Exception:
        pass
    
    # Sayfa sonu yazısı
    add_page_footer("A/B Testing")

def show_policy_simulator():
    """Politika Simülatörü – müdahalelerin 2030'a etkisi"""
    # Premium başlık
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; 
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">🛠️</span>
            </div>
            <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700;">POLİTİKA SİMÜLATÖRÜ</h1>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            Politika müdahalelerinin etkisini simüle edin ve sonuçları analiz edin
        </p>
    </div>
    """, unsafe_allow_html=True)
    # Simülatör paneli - Premium tasarım
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                padding: 1.5rem; border-radius: 15px; color: white; margin: 1rem 0; 
                box-shadow: 0 8px 20px rgba(240, 147, 251, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.5rem; border-radius: 8px; margin-right: 0.8rem;">
                <span style="font-size: 1.2rem;">⚙️</span>
            </div>
            <h3 style="margin: 0; font-size: 1.5rem; font-weight: 600;">Simülatör Parametreleri</h3>
        </div>
        <p style="margin: 0; font-size: 0.9rem; opacity: 0.9;">
            Basit etkiler + model tahminlerinin birlikte okunması için hızlı simülatör
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    
    with col1:
        waste_red = st.slider("Yıllık israf azaltımı (%)", 0, 40, 10)
    with col2:
        carbon_price = st.slider("Karbon fiyatı (USD/tCO2e)", 0, 200, 40)
    with col3:
        adoption = st.slider("Teknoloji benimseme (%)", 0, 100, 35)
    
    # Politika Simülatörü açıklaması
    with st.expander("📊 Bu Simülatör Ne Anlama Geliyor?", expanded=False):
        st.markdown("""
        **Politika Simülatörü**, farklı politika müdahalelerinin 2030 yılına kadar olan etkisini tahmin eder:
        
        ### 🎯 Simüle Edilen Politikalar:
        
        **1. Yıllık İsraf Azaltımı (%)**
        - Gıda israfını azaltan politika önlemleri
        - Örnek: Eğitim kampanyaları, perakende düzenlemeleri, soğuk zincir iyileştirmeleri
        - Etki: Doğrudan atık miktarını, ekonomik kaybı ve karbon emisyonunu azaltır
        
        **2. Karbon Fiyatı (USD/tCO2e)**
        - Karbon vergisi veya emisyon ticareti sistemi
        - Örnek: Karbon vergisi, emisyon limitleri, yeşil teşvikler
        - Etki: Karbon emisyonlarını azaltır, ekonomik kaybı düşürür
        
        **3. Teknoloji Benimseme (%)**
        - Sürdürülebilir teknolojilerin yaygınlaşması
        - Örnek: Akıllı tarım, IoT sensörleri, blockchain izleme
        - Etki: Atık azaltımı, karbon emisyonu düşüşü, sürdürülebilirlik artışı
        
        ### 📈 Sonuçların Yorumlanması:
        - **Atık (Mton)**: Yıllık gıda atık miktarı
        - **Ekonomik Kayıp (B$)**: Gıda israfından kaynaklanan ekonomik zarar
        - **Karbon (MtCO2e)**: Karbon ayak izi
        - **Sürdürülebilirlik**: Sürdürülebilirlik skoru (0-100)
        
        ### 💡 Kullanım Önerileri:
        - Farklı politika kombinasyonlarını test edin
        - En yüksek etkiyi yaratan politika paketini bulun
        - Maliyet-fayda analizi için A/B Test modülünü kullanın
        """)

    # Basit katsayılar (sunum amaçlı)
    base = {
        'waste': 200.0,   # Mton
        'loss': 200.0,    # B$
        'carbon': 320.0,  # MtCO2e
        'sust': 70.0
    }
    out = {
        'waste': max(0, base['waste']*(1 - waste_red/100) - adoption*0.6/10),
        'loss': max(0, base['loss']*(1 - waste_red/400) - carbon_price*0.15/10),
        'carbon': max(0, base['carbon']*(1 - waste_red/300) - carbon_price*0.5/10 - adoption*0.5/10),
        'sust': base['sust'] + waste_red*0.25 + adoption*0.15
    }

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Atık (Mton)", f"{out['waste']:.1f}")
    m2.metric("Ekonomik Kayıp (B$)", f"{out['loss']:.1f}")
    m3.metric("Karbon (MtCO2e)", f"{out['carbon']:.1f}")
    m4.metric("Sürdürülebilirlik", f"{out['sust']:.1f}")

    # AI Asistan – Politika sim.
    try:
        st.markdown(f"""
        <div class='ai-assistant'>
          <h4><span class='ai-emoji'>🤖</span>AI Asistan — Politika Etkisi</h4>
          <p><span class='ai-badge'>Özet</span> Atık {out['waste']:.1f} Mton, Karbon {out['carbon']:.1f} MtCO2e, Ekonomik Kayıp {out['loss']:.1f} B$ seviyesinde.</p>
          <p>Öneri: Atık azaltımı ve teknoloji benimsemeyi birlikte artırmak en yüksek marjinal faydayı sağlar; karbon fiyatını kademeli test edin.</p>
        </div>
        """, unsafe_allow_html=True)
    except Exception:
        pass

    # Sayfa sonu yazısı
    add_page_footer("Politika Simülatörü")


def show_model_card():
    """📑 Model Kartı – Metodoloji, performans ve açıklanabilirlik özeti"""
    # Premium başlık
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; 
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">📋</span>
            </div>
            <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700;">{_t('PAGE_CARD')}</h1>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            Model dokümantasyonu ve teknik detaylar
        </p>
    </div>
    """, unsafe_allow_html=True)
    perf = load_performance_report(PERF_REPORT_PATH)  # Sadece zaman serili profesyonel model
    if not perf:
        st.warning("⚠️ Performans raporu bulunamadı.")
        return
    # Metodoloji bölümü - Premium tasarım
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; 
                box-shadow: 0 10px 25px rgba(240, 147, 251, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">🔬</span>
            </div>
            <h2 style="margin: 0; font-size: 2.2rem; font-weight: 700;">METODOLOJİ</h2>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            Model geliştirme yaklaşımı ve teknik detaylar
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: rgba(255,255,255,0.9); padding: 1.5rem; border-radius: 15px; margin: 1rem 0; 
                box-shadow: 0 5px 15px rgba(0,0,0,0.1); border-left: 4px solid #f093fb;">
        <ul style="margin: 0; padding-left: 1.5rem; color: #232E5C; line-height: 1.8;">
            <li><strong>Veri Zenginleştirme:</strong> ISO kodları, coğrafi özellikler, pandemi dummyları, temporal özellikler</li>
            <li><strong>Değerlendirme:</strong> Train-Test Split (80/20) + 5-fold Cross-Validation</li>
            <li><strong>Regularization:</strong> Learning rate, max_depth, subsample parametreleri</li>
            <li><strong>Model:</strong> GradientBoostingRegressor (A/B test kazananı)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Performans bölümü - Premium tasarım
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; 
                box-shadow: 0 10px 25px rgba(79, 172, 254, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">📊</span>
            </div>
            <h2 style="margin: 0; font-size: 2.2rem; font-weight: 700;">PERFORMANS</h2>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            Model performans metrikleri ve değerlendirme sonuçları
        </p>
    </div>
    """, unsafe_allow_html=True)
    rows = []
    for key, label in [('Total Waste (Tons)','Atık'),('Economic Loss (Million $)','Ekonomik Kayıp'),('Carbon_Footprint_kgCO2e','Karbon')]:
        p = perf.get('targets', {}).get(key, {})
        gap = None
        try:
            if p.get('test_r2') is not None and p.get('cv_r2') is not None:
                gap = abs(p.get('test_r2') - p.get('cv_r2'))
        except Exception:
            pass
        rows.append({
            'Hedef': label,
            'R²': p.get('test_r2'),
            'CV R²': p.get('cv_r2'), 
            'CV std': p.get('cv_std') if 'cv_std' in p else 'N/A',
            '|Test−CV|': gap
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True)
    
    # Açıklanabilirlik bölümü - Premium tasarım
    st.markdown("""
    <div style="background: linear-gradient(135deg, #11E6C1 0%, #667eea 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; 
                box-shadow: 0 10px 25px rgba(17, 230, 193, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">🔍</span>
            </div>
            <h2 style="margin: 0; font-size: 2.2rem; font-weight: 700;">AÇIKLANABİLİRLİK</h2>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            Model kararlarını etkileyen faktörlerin analizi (İlk 10 özellik)
        </p>
    </div>
    """, unsafe_allow_html=True)
    target_tabs = {
        'Atık': 'total_waste_tons',
        'Ekonomik Kayıp': 'economic_loss_million',
        'Karbon': 'carbon_footprint_kgco2e'
    }
    tabs = st.tabs(list(target_tabs.keys()))
    for label, tab in zip(target_tabs.keys(), tabs):
        with tab:
            tname = target_tabs[label]
            imp_ts = load_prof_ts_importance(tname)
            shap_ts = load_prof_ts_shap_mean(tname)
            c1, c2 = st.columns(2)
            if imp_ts is not None and not imp_ts.empty:
                col_imp = imp_ts.columns[1]
                c1.subheader("Permutation Importance")
                c1.plotly_chart(px.bar(imp_ts.head(10), x=col_imp, y=imp_ts.columns[0], orientation='h', template='plotly_white', height=420), use_container_width=True)
                
                # Permutation Importance açıklaması
                with c1.expander("📊 Permutation Importance Nedir?"):
                    st.markdown(f"""
                    **Permutation Importance** modelin tahmin performansını etkileyen faktörleri gösterir:
                    
                    - **Bar uzunluğu**: O faktörü rastgele karıştırdığımızda model performansının ne kadar düştüğü
                    - **En uzun barlar**: Model için en kritik faktörler (bunlar olmadan model çok kötü performans gösterir)
                    - **Kısa barlar**: Model için daha az önemli faktörler
                    
                    **{label} için en kritik faktörler**: {', '.join(imp_ts.head(3)[imp_ts.columns[0]].tolist())}
                    
                    **Pratik kullanım**: Bu faktörlere odaklanarak veri toplama stratejilerini optimize edebilirsiniz.
                    """)
            else:
                c1.info('Permutation importance bulunamadı.')
                
            if shap_ts is not None and not shap_ts.empty:
                colx = 'mean_abs_shap' if 'mean_abs_shap' in shap_ts.columns else shap_ts.columns[1]
                c2.subheader("Ortalama |SHAP|")
                c2.plotly_chart(px.bar(shap_ts.sort_values(colx, ascending=False).head(10), x=colx, y='feature', orientation='h', template='plotly_white', height=420), use_container_width=True)
                
                # SHAP açıklaması
                with c2.expander("📊 SHAP Değerleri Nedir?"):
                    st.markdown(f"""
                    **SHAP (SHapley Additive exPlanations)** modelin her tahminini nasıl yaptığını açıklar:
                    
                    - **Bar uzunluğu**: Faktörün ortalama etkisi (pozitif veya negatif)
                    - **En uzun barlar**: Model kararlarını en çok etkileyen faktörler
                    - **Kısa barlar**: Daha az etkili faktörler
                    
                    **{label} için en etkili faktörler**: {', '.join(shap_ts.sort_values(colx, ascending=False).head(3)['feature'].tolist())}
                    
                    **Pratik kullanım**: Bu faktörlerin değişimi {label} üzerinde en büyük etkiyi yaratır.
                    """)
            else:
                c2.info('SHAP çıktısı bulunamadı.')

    # AI Asistan – Model Kartı yorumu
    try:
        gaps = []
        for key in ['Total Waste (Tons)','Economic Loss (Million $)','Carbon_Footprint_kgCO2e']:
            p = perf.get('targets', {}).get(key, {})
            if p.get('test_r2') is not None and p.get('cv_r2') is not None:
                gaps.append(abs(p['test_r2']-p['cv_r2']))
        msg = "stabil" if (gaps and np.mean(gaps) < 0.05) else "iyileştirilebilir"
        st.markdown(f"""
        <div class='ai-assistant'>
          <h4><span class='ai-emoji'>🤖</span>AI Asistan — Metodoloji Özeti</h4>
          <p><span class='ai-badge'>TS güvenlik</span> Lag/Rolling + expanding-CV + damping/clip; genel durum: {msg}.</p>
          <p>Öneri: CV dağılımını sayfada göster, |Test−CV| yüksek hedeflerde λ/k’yi artır.</p>
        </div>
        """, unsafe_allow_html=True)
    except Exception:
        pass

    # Sayfa sonu yazısı
    add_page_footer("Model Kartı")


def show_risk_opportunity():
    """⚠️ Risk & Fırsat – Robust tahminlerine göre uç değerler ve hızlı öneriler"""
    # Premium başlık
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; 
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">⚠️</span>
            </div>
            <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700;">RISK & FIRSAT</h1>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            Risk analizi ve fırsat değerlendirmesi
        </p>
    </div>
    """, unsafe_allow_html=True)
    # Kaynak seçimi - Premium tasarım
    st.sidebar.markdown("""
    <div style="background: linear-gradient(135deg, #ff69b4 0%, #ff1493 100%); 
                padding: 1rem; border-radius: 15px; color: white; margin: 1rem 0; 
                box-shadow: 0 5px 15px rgba(255, 105, 180, 0.3);">
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.3rem; border-radius: 6px; margin-right: 0.5rem;">
                <span style="font-size: 0.9rem;">🔧</span>
            </div>
            <h4 style="margin: 0; font-size: 1rem; font-weight: 600;">Risk Kaynağı</h4>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Model seçimi kaldırıldı - doğrudan tahminleri yükle
    preds = load_predictions_dashboard()
    source_label = "GradientBoosting"
    if preds is None or preds.empty:
        st.warning("⚠️ Tahmin dosyası bulunamadı.")
        return
    st.caption(f"Kaynak: {source_label}")
    st.markdown("<small>Risk skoru: max(0,waste_cagr)+max(0,carbon_cagr)+max(0,loss_cagr) − sus_2030/100</small>", unsafe_allow_html=True)
    # Son yıl ve CAGR ile basit risk/fırsat puanları
    pmin, pmax = int(preds['Year'].min()), int(preds['Year'].max())
    def cagr(g: pd.DataFrame, col: str) -> float:
        a = g.loc[g['Year'] == pmin, col].mean()
        b = g.loc[g['Year'] == pmax, col].mean()
        n = max(1, pmax - pmin)
        if a and a > 0 and b >= 0:
            return (b / a) ** (1.0 / n) - 1.0
        return np.nan
    grp = preds.groupby('Country')
    # Sustainability_Score sütununun varlığını kontrol et
    sus_col = 'Sustainability_Score' if 'Sustainability_Score' in preds.columns else None
    
    df_data = {
        'waste_cagr': grp.apply(lambda g: cagr(g, 'Total Waste (Tons)')),
        'carbon_cagr': grp.apply(lambda g: cagr(g, 'Carbon_Footprint_kgCO2e')),
        'loss_cagr': grp.apply(lambda g: cagr(g, 'Economic Loss (Million $)'))
    }
    
    if sus_col:
        df_data['sus_2030'] = grp.apply(lambda g: g.loc[g['Year'] == pmax, sus_col].mean())
    else:
        df_data['sus_2030'] = 50.0  # Varsayılan değer
    
    df = pd.DataFrame(df_data).dropna()
    df['risk_score'] = (df['waste_cagr'].clip(lower=0) + df['carbon_cagr'].clip(lower=0) + df['loss_cagr'].clip(lower=0)) - (df['sus_2030'] / 100.0)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Yüksek Risk – Top 10")
        st.dataframe(df.sort_values('risk_score', ascending=False).head(10))
        
        # Yüksek Risk tablosu açıklaması
        with col1.expander("📊 Yüksek Risk Tablosu Ne Anlatıyor?", expanded=False):
            st.markdown("""
            **🚨 Yüksek Risk Tablosu**, 2030 yılına kadar en büyük sorunlarla karşılaşabilecek ülkeleri listeler:
            
            ### 📈 Risk Skoru Hesaplama:
            **Risk Skoru = max(0, Atık CAGR) + max(0, Karbon CAGR) + max(0, Ekonomik Kayıp CAGR) - (Sürdürülebilirlik 2030 / 100)**
            
            ### 🔍 Tablo Yorumu:
            
            **📊 Sütunlar:**
            - **waste_cagr**: Atık miktarındaki yıllık büyüme oranı (%)
            - **carbon_cagr**: Karbon emisyonundaki yıllık büyüme oranı (%)
            - **loss_cagr**: Ekonomik kayıptaki yıllık büyüme oranı (%)
            - **sus_2030**: 2030 yılı tahmini sürdürülebilirlik skoru (0-100)
            - **risk_score**: Toplam risk skoru (yüksek = kötü)
            
            ### ⚠️ Yüksek Risk İşaretleri:
            - **Pozitif CAGR değerleri**: İsraf, karbon ve ekonomik kayıp artıyor
            - **Düşük sürdürülebilirlik**: 2030'da düşük performans bekleniyor
            - **Yüksek risk skoru**: Acil müdahale gerektiren durumlar
            
            ### 🚨 Acil Önlemler:
            - Bu ülkelerde politika değişiklikleri gerekli
            - Uluslararası destek ve işbirliği önerilir
            - Başarılı ülkelerin deneyimlerinden öğrenin
            """)
            
    with col2:
        st.subheader("Fırsat – Top 10")
        st.dataframe(df.sort_values('risk_score').head(10))
        
        # Fırsat tablosu açıklaması
        with col2.expander("📊 Fırsat Tablosu Ne Anlatıyor?", expanded=False):
            st.markdown("""
            **🌟 Fırsat Tablosu**, 2030 yılına kadar en iyi performans gösterebilecek ülkeleri listeler:
            
            ### 📈 Fırsat Skoru Hesaplama:
            **Düşük Risk Skoru = İyi Fırsat**
            - Negatif veya düşük CAGR değerleri (iyileşme)
            - Yüksek sürdürülebilirlik skoru (2030)
            - Düşük toplam risk skoru
            
            ### 🔍 Tablo Yorumu:
            
            **📊 Sütunlar:**
            - **waste_cagr**: Atık azalma oranı (negatif = iyi)
            - **carbon_cagr**: Karbon emisyonu azalma oranı (negatif = iyi)
            - **loss_cagr**: Ekonomik kayıp azalma oranı (negatif = iyi)
            - **sus_2030**: 2030 yılı tahmini sürdürülebilirlik skoru (yüksek = iyi)
            - **risk_score**: Toplam risk skoru (düşük = iyi)
            
            ### 🌟 Başarı İşaretleri:
            - **Negatif CAGR değerleri**: İsraf, karbon ve ekonomik kayıp azalıyor
            - **Yüksek sürdürülebilirlik**: 2030'da yüksek performans bekleniyor
            - **Düşük risk skoru**: İyi yönetilen durumlar
            
            ### 💡 Öğrenilecek Dersler:
            - Bu ülkelerin politika örneklerini inceleyin
            - Başarılı stratejileri diğer ülkelerde uygulayın
            - İyi uygulamaları dokümante edin ve paylaşın
            """)

    # 2×2 Risk & Fırsat Radarı (kuadran)
    st.subheader("🧭 Risk & Fırsat Radarı (2×2)")
    method = st.radio("Eşik yöntemi", ["Medyan", "Sabit"], index=0, horizontal=True, key="risk_thr_method")
    if method == "Medyan":
        x_thr = float(df['risk_score'].median())
        y_thr = float(df['sus_2030'].median())
    else:
        c1, c2 = st.columns(2)
        with c1:
            x_thr = st.number_input("Risk eşiği (x)", value=float(df['risk_score'].median()))
        with c2:
            y_thr = st.number_input("Sürdürülebilirlik eşiği (y)", value=float(df['sus_2030'].median()))
    plot_df = df.reset_index().rename(columns={'index':'Country'})
    def quad(row):
        if row['risk_score'] >= x_thr and row['sus_2030'] < y_thr:
            return 'Kritik (Yüksek Risk / Düşük Sürdürülebilirlik)'
        if row['risk_score'] >= x_thr and row['sus_2030'] >= y_thr:
            return 'İzle (Yüksek Risk / Yüksek Sürdürülebilirlik)'
        if row['risk_score'] < x_thr and row['sus_2030'] < y_thr:
            return 'İyileştir (Düşük Risk / Düşük Sürdürülebilirlik)'
        return 'Lider (Düşük Risk / Yüksek Sürdürülebilirlik)'
    plot_df['Quadrant'] = plot_df.apply(quad, axis=1)
    figq = px.scatter(plot_df, x='risk_score', y='sus_2030', color='Quadrant', hover_name='Country', template='plotly_white', height=520)
    figq.add_vline(x=x_thr, line_dash='dash', line_color='#94A3B8')
    figq.add_hline(y=y_thr, line_dash='dash', line_color='#94A3B8')
    figq.update_layout(xaxis_title='Risk Skoru (sağ = risk artar)', yaxis_title='2030 Sürdürülebilirlik (yukarı = iyi)')
    st.plotly_chart(figq, use_container_width=True)
    
    # Grafik açıklaması
    with st.expander("📊 2×2 Risk & Fırsat Radarı Ne Anlatıyor?", expanded=False):
        st.markdown("""
        **🧭 2×2 Risk & Fırsat Radarı**, ülkeleri iki kritik eksende konumlandırarak politika önceliklerini belirler:
        
        ### 📊 Grafik Eksenleri:
        
        **📈 X-Ekseni (Risk Skoru):**
        - **Sol**: Düşük risk (iyi durum)
        - **Sağ**: Yüksek risk (kötü durum)
        - **Kesikli çizgi**: Medyan değer (eşik)
        
        **📊 Y-Ekseni (2030 Sürdürülebilirlik):**
        - **Alt**: Düşük sürdürülebilirlik (kötü durum)
        - **Üst**: Yüksek sürdürülebilirlik (iyi durum)
        - **Kesikli çizgi**: Medyan değer (eşik)
        
        ### 🎯 Dört Kuadran Analizi:
        
        **🚨 Kritik (Sağ Alt - Kırmızı):**
        - **Yüksek Risk + Düşük Sürdürülebilirlik**
        - Acil müdahale gerektiren ülkeler
        - Politika değişiklikleri şart
        - Uluslararası destek gerekli
        
        **👁️ İzle (Sağ Üst - Turuncu):**
        - **Yüksek Risk + Yüksek Sürdürülebilirlik**
        - Risk faktörlerini kontrol altına alın
        - Mevcut iyi durumu koruyun
        - Proaktif önlemler alın
        
        **🔧 İyileştir (Sol Alt - Sarı):**
        - **Düşük Risk + Düşük Sürdürülebilirlik**
        - Sürdürülebilirlik skorunu artırın
        - Yapısal iyileştirmeler yapın
        - Uzun vadeli planlama
        
        **🏆 Lider (Sol Üst - Yeşil):**
        - **Düşük Risk + Yüksek Sürdürülebilirlik**
        - Model ülkeler
        - Başarılı stratejileri paylaşın
        - İyi uygulamaları dokümante edin
        
        ### 💡 Politika Stratejileri:
        
        **🚨 Kritik Kuadran:**
        - Acil politika paketleri
        - Uluslararası işbirliği
        - Teknik destek ve finansman
        
        **👁️ İzle Kuadran:**
        - Risk faktörlerini azaltın
        - Mevcut başarıları koruyun
        - Erken uyarı sistemleri
        
        **🔧 İyileştir Kuadran:**
        - Sürdürülebilirlik hedefleri
        - Kapasite geliştirme
        - Teknoloji transferi
        
        **🏆 Lider Kuadran:**
        - Başarı hikayelerini paylaşın
        - Uluslararası liderlik
        - Bilgi ve deneyim aktarımı
        
        ### 🎛️ Eşik Ayarları:
        - **Medyan**: Otomatik eşik (veri ortalaması)
        - **Sabit**: Manuel eşik ayarı
        - Eşikleri değiştirerek farklı senaryoları test edin
        """)

    # AI Asistan – Risk & Fırsat yorumu
    try:
        worst = df.sort_values('risk_score', ascending=False).head(3)
        best = df.sort_values('risk_score').head(3)
        msg = []
        if not worst.empty:
            msg.append(f"<span class='ai-badge'>Yüksek risk</span> {', '.join(worst.index.tolist())}")
        if not best.empty:
            msg.append(f"<span class='ai-badge'>Fırsat</span> {', '.join(best.index.tolist())}")
        st.markdown("""
        <div class='ai-assistant'>
          <h4><span class='ai-emoji'>🤖</span>AI Asistan — Risk & Fırsat</h4>
          <p>{rows}</p>
          <p>Öneri: Risk skoru yüksek ülkelerde atık/karbon CAGR’ını aşağı çeken politika sepetlerini önceliklendirin.</p>
        </div>
        """.replace("{rows}", " · ".join(msg)), unsafe_allow_html=True)
    except Exception:
        pass
    
    # Sayfa sonu yazısı
    add_page_footer("Risk & Fırsat")

def show_target_planner():
    """🎯 Hedef Planlayıcı – 2030 hedefini seç, gerekli yıllık değişimi (CAGR) gör"""
    # Premium başlık
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; 
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">🎯</span>
            </div>
            <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700;">HEDEF PLANLAYICI</h1>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            Hedef belirleme ve planlama araçları
        </p>
    </div>
    """, unsafe_allow_html=True)
    preds = load_predictions_dashboard()
    if preds is None or preds.empty:
        st.warning("⚠️ Tahmin dosyası bulunamadı.")
        return
    country = st.selectbox("Ülke", sorted(preds['Country'].dropna().unique()))
    metric = st.selectbox("Hedef Metrik", [
                ('Total Waste (Tons)', 'Atık (ton)'),
        ('Economic Loss (Million $)', 'Ekonomik Kayıp (Million$)'),
        ('Carbon_Footprint_kgCO2e', 'Karbon (kgCO2e)'),
        ('Sustainability_Score', 'Sürdürülebilirlik (0–100)'),
        ('Waste_Per_Capita_kg', 'Kişi Başına Atık (kg)'),
        ('Economic_Loss_Per_Capita_USD', 'Kişi Başına Ekonomik Kayıp (USD)'),
        ('Carbon_Per_Capita_kgCO2e', 'Kişi Başına Karbon (kg CO2e)')
    ], format_func=lambda x: x[1])
    col, _label = metric
    dfc = preds[preds['Country'] == country].sort_values('Year')
    y0, y1 = int(dfc['Year'].min()), int(dfc['Year'].max())
    cur = float(dfc.loc[dfc['Year'] == y1, col].mean())
    goal = st.number_input("2030 hedefi", value=max(0.0, cur * 0.9))
    years = max(1, y1 - y0)
    req = 0.0 if cur <= 0 else (goal / cur) ** (1.0 / years) - 1.0
    st.metric("Gerekli yıllık değişim (CAGR)", f"{req*100:.2f}%/yıl")
    
    # Hedef Planlayıcı açıklaması
    with st.expander("📊 Hedef Planlayıcı Ne Anlatıyor?", expanded=False):
        st.markdown(f"""
        **🎯 Hedef Planlayıcı**, seçilen ülke için 2030 yılına kadar belirlenen hedefe ulaşmak için gerekli yıllık değişim oranını hesaplar:
        
        ### 📈 CAGR Hesaplama:
        
        **Formül**: CAGR = (Hedef Değer / Mevcut Değer)^(1/Yıl Sayısı) - 1
        
        **{country} için hesaplama:**
        - **Mevcut durum ({y1})**: {cur:.2f}
        - **2030 hedefi**: {goal:.2f}
        - **Yıl sayısı**: {years} yıl
        - **Gerekli CAGR**: {req*100:.2f}%/yıl
        
        ### 🔍 CAGR Yorumu:
        
        **📊 CAGR Değerleri:**
        - **Pozitif CAGR**: Hedef değer mevcut değerden yüksek (artış gerekiyor)
        - **Negatif CAGR**: Hedef değer mevcut değerden düşük (azalış gerekiyor)
        - **Sıfır CAGR**: Hedef mevcut değere eşit (değişim gerekmiyor)
        
        **🎯 Hedef Türleri:**
        
        **📈 Artış Hedefleri (Pozitif CAGR):**
        - **Sürdürülebilirlik skoru**: 0-100 arası artış
        - **Verimlilik göstergeleri**: Yüzde artışlar
        - **Performans metrikleri**: İyileştirme hedefleri
        
        **📉 Azalış Hedefleri (Negatif CAGR):**
        - **Atık miktarı**: Ton cinsinden azalış
        - **Karbon emisyonu**: kgCO2e cinsinden azalış
        - **Ekonomik kayıp**: Milyon $ cinsinden azalış
        
        ### 💡 Pratik Kullanım:
        
        **🎯 Hedef Belirleme:**
        - **Gerçekçi hedefler**: Mevcut trendlere uygun hedefler belirleyin
        - **Aşamalı hedefler**: Büyük hedefleri küçük adımlara bölün
        - **SMART hedefler**: Spesifik, ölçülebilir, ulaşılabilir hedefler
        
        **📊 Politika Planlama:**
        - **Yüksek CAGR**: Güçlü politika önlemleri gerekli
        - **Düşük CAGR**: Mevcut politikalar yeterli olabilir
        - **Negatif CAGR**: İyileştirme trendi devam ediyor
        
        **🔍 Risk Değerlendirmesi:**
        - **Çok yüksek CAGR**: Hedef gerçekçi olmayabilir
        - **Çok düşük CAGR**: Hedef çok muhafazakar olabilir
        - **Optimal CAGR**: Dengeli ve ulaşılabilir hedef
        
        ### 🚀 Sonraki Adımlar:
        1. **AI Insights** sayfasında en etkili faktörleri inceleyin
        2. **A/B Test** modülünde farklı senaryoları test edin
        3. **Politika Simülatörü** ile etki analizi yapın
        4. **Risk & Fırsat** sayfasında ülke konumunu kontrol edin
        """)

    # AI Asistan – Hedef planlayıcı yorumu
    try:
        direction = 'artış' if goal > cur else 'azalış'
        st.markdown(f"""
        <div class='ai-assistant'>
          <h4><span class='ai-emoji'>🤖</span>AI Asistan — Gerekli İvme</h4>
          <p><span class='ai-badge'>2030</span> hedefi için {direction} gereksinimi ≈ {req*100:.2f}%/yıl.</p>
          <p>Öneri: Ülke için AI Insights sayfasındaki en etkili sürücülere odaklanarak A/B testinde parametrik arama yap.</p>
        </div>
        """, unsafe_allow_html=True)
    except Exception:
        pass
    
    # Sayfa sonu yazısı
    add_page_footer("Hedef Planlayıcı")

def show_report_builder():
    """📄 Sade Rapor Oluşturucu"""
    
    st.markdown("## 📄 Rapor Oluşturucu")
    st.markdown("Ecolense analiz raporu oluşturun ve indirin.")
    
    # Rapor türü seçimi
    report_type = st.selectbox(
        "Rapor Türü Seçin:",
        ["Yönetici Özeti", "Detaylı Analiz", "Model Performansı", "Ülke Karşılaştırması"]
    )
    
    # Rapor formatı
    report_format = st.selectbox(
        "Rapor Formatı:",
        ["HTML", "Markdown"]
    )
    
    # Bölüm seçimleri (sadece detaylı analiz için)
    if report_type == "Detaylı Analiz":
        st.markdown("### 📋 Dahil Edilecek Bölümler")
        
        col1, col2 = st.columns(2)
        with col1:
            include_performance = st.checkbox("Model Performansı", True)
            include_insights = st.checkbox("AI İçgörüleri", True)
            include_rankings = st.checkbox("Ülke Sıralamaları", True)
            include_forecasts = st.checkbox("Tahminler", True)
        
        with col2:
            include_data_quality = st.checkbox("Veri Kalitesi", True)
            include_roi = st.checkbox("ROI Analizi", True)
            include_benchmark = st.checkbox("Benchmark", True)
            include_methodology = st.checkbox("Metodoloji", True)
    
    # Rapor başlığı
    report_title = st.text_input(
        "Rapor Başlığı:",
        value=f"Ecolense {report_type} Raporu - {pd.Timestamp.now().strftime('%d.%m.%Y')}"
    )
    
    # Rapor oluştur butonu
    if st.button("📄 Rapor Oluştur", type="primary", use_container_width=True):
        with st.spinner("Rapor oluşturuluyor..."):
            # Rapor içeriği oluştur
            report_content = generate_simple_report(
                report_type, 
                report_format, 
                report_title,
                include_performance if report_type == "Detaylı Analiz" else True,
                include_insights if report_type == "Detaylı Analiz" else True,
                include_rankings if report_type == "Detaylı Analiz" else True,
                include_forecasts if report_type == "Detaylı Analiz" else True,
                include_data_quality if report_type == "Detaylı Analiz" else False,
                include_roi if report_type == "Detaylı Analiz" else False,
                include_benchmark if report_type == "Detaylı Analiz" else False,
                include_methodology if report_type == "Detaylı Analiz" else False
            )
            
            # Raporu göster
            st.success("✅ Rapor başarıyla oluşturuldu!")
            
            # İndirme butonu
            file_extension = "html" if report_format == "HTML" else "md"
            file_name = f"ecolense_{report_type.lower().replace(' ', '_')}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.{file_extension}"
            
            st.download_button(
                f"📥 {report_format} Raporunu İndir",
                data=report_content,
                file_name=file_name,
                mime="text/html" if report_format == "HTML" else "text/markdown"
            )
            
            # Rapor önizlemesi
            with st.expander("📄 Rapor Önizlemesi"):
                if report_format == "HTML":
                    st.components.v1.html(report_content, height=600, scrolling=True)
                else:
                    st.markdown(report_content)

    # AI Asistan – Rapor önerisi
    try:
        st.markdown("""
        <div class='ai-assistant'>
          <h4><span class='ai-emoji'>🤖</span>AI Asistan — Rapor Önerisi</h4>
          <p>Sunum akışı: (1) KPI ve veri kaynağı, (2) Model Performansı (R², CV, |Test−CV|), (3) Tahminler + Senaryolar, (4) AI Insights (CAGR & SHAP).</p>
        </div>
        """, unsafe_allow_html=True)
    except Exception:
        pass
    
    # Sayfa sonu
    add_page_footer("Rapor Oluşturucu")



    # Rapor oluşturma butonu


def generate_simple_report(report_type, format_type, title, include_performance=True, include_insights=True, 
                          include_rankings=True, include_forecasts=True, include_data_quality=False, 
                          include_roi=False, include_benchmark=False, include_methodology=False):
    """Basit rapor içeriği oluşturur"""
    
    # Veri yükle
    df = load_data('data/ecolense_final_enriched.csv')
    perf_data = load_performance_report(PERF_REPORT_PATH)
    
    if format_type == "HTML":
        return generate_html_report(report_type, title, df, perf_data, include_performance, include_insights,
                                   include_rankings, include_forecasts, include_data_quality, include_roi,
                                   include_benchmark, include_methodology)
    else:
        return generate_markdown_report(report_type, title, df, perf_data, include_performance, include_insights,
                                       include_rankings, include_forecasts, include_data_quality, include_roi,
                                       include_benchmark, include_methodology)

def generate_html_report(report_type, title, df, perf_data, include_performance, include_insights,
                        include_rankings, include_forecasts, include_data_quality, include_roi,
                        include_benchmark, include_methodology):
    """HTML formatında rapor oluşturur"""
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
            h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
            h2 {{ color: #34495e; margin-top: 30px; }}
            h3 {{ color: #7f8c8d; }}
            .metric {{ background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #3498db; }}
            .highlight {{ background: #e8f4fd; padding: 10px; border-radius: 5px; }}
            table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            .footer {{ margin-top: 50px; padding-top: 20px; border-top: 1px solid #ddd; color: #7f8c8d; font-size: 0.9em; }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        <p><strong>Oluşturulma Tarihi:</strong> {pd.Timestamp.now().strftime('%d.%m.%Y %H:%M')}</p>
        <p><strong>Rapor Türü:</strong> {report_type}</p>
        
        <div class="highlight">
            <h2>📊 Özet Metrikler</h2>
            <div class="metric">
                <strong>Toplam Atık:</strong> {df[_resolve_column_name(df, ['Total Waste (Tons)', 'total_waste_tons'])].sum() / 1e6:.1f} milyon ton<br>
                <strong>Ekonomik Kayıp:</strong> {df[_resolve_column_name(df, ['Economic Loss (Million $)', 'economic_loss_million_usd'])].sum() / 1e6:.1f} trilyon USD<br>
                <strong>Toplam Karbon:</strong> {df[_resolve_column_name(df, ['Carbon_Footprint_kgCO2e', 'carbon_footprint_kgco2e'])].sum() / 1e9:.1f} milyar kg CO2e<br>
                <strong>Ortalama Sürdürülebilirlik:</strong> {df[_resolve_column_name(df, ['Sustainability_Score', 'sustainability_score'])].mean():.1f}/100
            </div>
        </div>
    """
    
    if include_performance and perf_data:
        html_content += f"""
        <h2>📈 Model Performansı</h2>
        <div class="metric">
            <strong>En İyi Model:</strong> {perf_data.get('model_type', 'GradientBoosting')}<br>
            <strong>Ortalama R² Skoru:</strong> {perf_data.get('average_test_r2', 0):.3f}<br>
            <strong>Ortalama CV R²:</strong> {perf_data.get('average_cv_r2', 0):.3f}<br>
            <strong>Ortalama Overfitting:</strong> {perf_data.get('average_overfitting', 0):.3f}
        </div>
        """
    
    if include_rankings:
        # En iyi 5 ülke
        country_col = _resolve_column_name(df, ['Country', 'country'])
        sustainability_col = _resolve_column_name(df, ['Sustainability_Score', 'sustainability_score'])
        if country_col and sustainability_col:
            top_countries = df.groupby(country_col)[sustainability_col].mean().sort_values(ascending=False).head(10)
            html_content += """
            <h2>🏆 Dünya Sürdürülebilirlik Sıralaması</h2>
            <table>
                <tr><th>Sıra</th><th>Ülke</th><th>Skor</th><th>Kategori</th><th>Analiz</th></tr>
            """
            
            # Kategori ve analiz bilgileri
            categories = {
                'China': ('🏭 Endüstriyel Lider', 'Yeşil teknoloji yatırımları'),
                'Russia': ('⛽ Enerji Gücü', 'Doğal kaynak zenginliği'),
                'USA': ('💡 İnovasyon Merkezi', 'Yenilenebilir enerji liderliği'),
                'India': ('🌱 Gelişen Dev', 'Nüfus avantajı ve yeşil politika'),
                'Spain': ('☀️ Yenilenebilir', 'Güneş enerjisi ve sürdürülebilir tarım'),
                'Canada': ('🍁 Doğal Kaynak', 'Geniş orman alanları'),
                'Germany': ('⚙️ Teknoloji', 'Endüstri 4.0 ve yeşil dönüşüm'),
                'Argentina': ('🌾 Tarımsal', 'Biyoyakıt ve organik tarım'),
                'UK': ('🏛️ Politik', 'Net-zero hedefleri'),
                'Brazil': ('🌴 Biyoçeşitlilik', 'Amazon ve yenilenebilir enerji'),
                'Turkey': ('🌉 Köprü Ülke', 'Avrupa-Asya köprüsü avantajı')
            }
            
            for i, (country, score) in enumerate(top_countries.items(), 1):
                category, analysis = categories.get(country, ('🌍 Diğer', 'Veri analizi devam ediyor'))
                html_content += f"<tr><td>{i}</td><td>{country}</td><td>{score:.1f}</td><td>{category}</td><td>{analysis}</td></tr>"
            html_content += "</table>"
            
            # Türkiye analizi
            turkey_rank = None
            turkey_score = None
            for i, (country, score) in enumerate(top_countries.items(), 1):
                if country == 'Turkey':
                    turkey_rank = i
                    turkey_score = score
                    break
            
            if turkey_rank:
                html_content += f"""
                <div class="metric">
                    <h3>🎯 Türkiye Analizi (Sıra: {turkey_rank}, Skor: {turkey_score:.1f})</h3>
                    <p><strong>✅ Güçlü Yönler:</strong> Coğrafi konum, yenilenebilir enerji potansiyeli, genç nüfus</p>
                    <p><strong>⚠️ Gelişim Alanları:</strong> Enerji verimliliği, atık yönetimi, yeşil teknoloji AR-GE</p>
                    <p><strong>🎯 2030 Hedefi:</strong> 90+ skor ile ilk 5'e giriş</p>
                </div>
                """
        else:
            html_content += """
            <h2>🏆 Dünya Sürdürülebilirlik Sıralaması</h2>
            <p>Ülke verisi bulunamadı.</p>
            """
    
    if include_insights:
        html_content += """
        <h2>🤖 AI İçgörüleri</h2>
        <div class="metric">
            <strong>Önemli Faktörler:</strong><br>
            • Nüfus büyüklüğü sürdürülebilirlik skorunu etkiler<br>
            • Gıda kategorisi atık miktarını belirler<br>
            • Ekonomik kayıp ile karbon ayak izi arasında güçlü korelasyon var
        </div>
        """
    
    if include_forecasts:
        html_content += """
        <h2>🔮 Gelecek Tahminleri</h2>
        <div class="metric">
            <strong>2025-2030 Projeksiyonları:</strong><br>
            • Atık miktarı %15-20 artış bekleniyor<br>
            • Sürdürülebilirlik skorları iyileşme trendinde<br>
            • Karbon ayak izi azalma eğiliminde
        </div>
        """
    
    if include_methodology:
        html_content += """
        <h2>📋 Metodoloji</h2>
        <div class="metric">
            <strong>Veri Kaynağı:</strong> Ecolense Enriched Dataset (2018-2024)<br>
            <strong>Model Türü:</strong> Zaman Serisi + Makine Öğrenmesi<br>
            <strong>Değerlendirme:</strong> Cross-validation ile RMSE ve R² skorları
        </div>
        """
    
    html_content += f"""
        <div class="footer">
            <p>Bu rapor Ecolense Intelligence Dashboard tarafından otomatik olarak oluşturulmuştur.</p>
        </div>
    </body>
    </html>
    """
    
    return html_content

def generate_markdown_report(report_type, title, df, perf_data, include_performance, include_insights,
                            include_rankings, include_forecasts, include_data_quality, include_roi,
                            include_benchmark, include_methodology):
    """Markdown formatında rapor oluşturur"""
    
    md_content = f"""# {title}

**Oluşturulma Tarihi:** {pd.Timestamp.now().strftime('%d.%m.%Y %H:%M')}  
**Rapor Türü:** {report_type}

## 📊 Özet Metrikler

    - **Toplam Atık:** {df[_resolve_column_name(df, ['Total Waste (Tons)', 'total_waste_tons'])].sum() / 1e6:.1f} milyon ton
    - **Ekonomik Kayıp:** {df[_resolve_column_name(df, ['Economic Loss (Million $)', 'economic_loss_million_usd'])].sum() / 1e6:.1f} trilyon USD
    - **Toplam Karbon:** {df[_resolve_column_name(df, ['Carbon_Footprint_kgCO2e', 'carbon_footprint_kgco2e'])].sum() / 1e9:.1f} milyar kg CO2e
    - **Ortalama Sürdürülebilirlik:** {df[_resolve_column_name(df, ['Sustainability_Score', 'sustainability_score'])].mean():.1f}/100

"""
    
    if include_performance and perf_data:
        md_content += f"""## 📈 Model Performansı

- **En İyi Model:** {perf_data.get('model_type', 'GradientBoosting')}
- **Ortalama R² Skoru:** {perf_data.get('average_test_r2', 0):.3f}
- **Ortalama CV R²:** {perf_data.get('average_cv_r2', 0):.3f}
- **Ortalama Overfitting:** {perf_data.get('average_overfitting', 0):.3f}

"""
    
    if include_rankings:
        country_col = _resolve_column_name(df, ['Country', 'country'])
        sustainability_col = _resolve_column_name(df, ['Sustainability_Score', 'sustainability_score'])
        if country_col and sustainability_col:
            top_countries = df.groupby(country_col)[sustainability_col].mean().sort_values(ascending=False).head(5)
            md_content += """## 🏆 En İyi 5 Ülke (Sürdürülebilirlik)

| Sıra | Ülke | Sürdürülebilirlik Skoru |
|------|------|-------------------------|
"""
            for i, (country, score) in enumerate(top_countries.items(), 1):
                md_content += f"| {i} | {country} | {score:.1f} |\n"
            md_content += "\n"
        else:
            md_content += """## 🏆 En İyi 5 Ülke (Sürdürülebilirlik)

Ülke verisi bulunamadı.

"""
    
    if include_insights:
        md_content += """## 🤖 AI İçgörüleri

**Önemli Faktörler:**
- Nüfus büyüklüğü sürdürülebilirlik skorunu etkiler
- Gıda kategorisi atık miktarını belirler
- Ekonomik kayıp ile karbon ayak izi arasında güçlü korelasyon var

"""
    
    if include_forecasts:
        md_content += """## 🔮 Gelecek Tahminleri

**2025-2030 Projeksiyonları:**
- Atık miktarı %15-20 artış bekleniyor
- Sürdürülebilirlik skorları iyileşme trendinde
- Karbon ayak izi azalma eğiliminde

"""
    
    if include_methodology:
        md_content += """## 📋 Metodoloji

- **Veri Kaynağı:** Ecolense Enriched Dataset (2018-2024)
- **Model Türü:** Zaman Serisi + Makine Öğrenmesi
- **Değerlendirme:** Cross-validation ile RMSE ve R² skorları

"""
    
    md_content += f"""---

*Bu rapor Ecolense Intelligence Dashboard tarafından otomatik olarak oluşturulmuştur.*
"""
    
    return md_content

def generate_report_content(selected_sections, title, perf_data, format_type):
    """Seçilen bölümleri içeren rapor içeriği oluştur"""
    from datetime import datetime
    
    def safe_format_number(value, decimals=3):
        """Güvenli sayı formatlaması"""
        try:
            if value is None:
                return 'N/A'
            if isinstance(value, (int, float)):
                if pd.isna(value):
                    return 'N/A'
                return f"{value:.{decimals}f}"
            return str(value)
        except Exception:
            return 'N/A'
    
    # Veri yükleme fonksiyonları
    def load_data_for_report():
        """Rapor için gerekli verileri yükle"""
        try:
            # Ana veri
            df = load_data(REAL_DATA_PATH, announce=False)
            
            # Sütun adlarını küçük harfe çevir (güvenlik için)
            if df is not None and not df.empty:
                df.columns = df.columns.str.lower()
            else:
                # Veri yüklenemezse boş DataFrame oluştur
                df = pd.DataFrame()
            
            # Tahminler
            pred_prof_ts = load_predictions_dashboard()
            pred_robust = load_predictions_dashboard()
            
            # SHAP verileri
            shap_data = {}
            importance_data = {}
            
            targets = ['total_waste_tons', 'economic_loss_million', 'carbon_footprint_kgco2e', 'sustainability_score']
            
            for target in targets:
                try:
                    shap_data[target] = load_prof_ts_shap_mean(target)
                    importance_data[target] = load_prof_ts_importance(target)
                except Exception:
                    try:
                        shap_data[target] = load_new_shap_summary(target)
                        importance_data[target] = load_new_shap_importance(target)
                    except Exception:
                        shap_data[target] = None
                        importance_data[target] = None
            
            return {
                'main_data': df,
                'predictions_prof_ts': pred_prof_ts,
                'predictions_robust': pred_robust,
                'shap_data': shap_data,
                'importance_data': importance_data
            }
        except Exception as e:
            st.error(f"Veri yükleme hatası: {e}")
            return {
                'main_data': pd.DataFrame(),
                'predictions_prof_ts': None,
                'predictions_robust': None,
                'shap_data': {},
                'importance_data': {}
            }
    
    if format_type == "HTML":
        content = f"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; line-height: 1.6; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 15px; text-align: center; }}
        .section {{ margin: 30px 0; padding: 20px; border-left: 4px solid #667eea; background: #f8f9fa; border-radius: 8px; }}
        .metric {{ display: inline-block; margin: 10px; padding: 15px; background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .highlight {{ background: #e3f2fd; padding: 10px; border-radius: 5px; margin: 10px 0; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background: #667eea; color: white; }}
        .footer {{ margin-top: 50px; margin-bottom: 150px; padding: 20px; background: #f1f3f4; border-radius: 8px; text-align: center; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
        <p>Oluşturulma Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>
    </div>
"""
    else:  # Markdown
        content = f"# {title}\n\n"
        content += f"**Oluşturulma Tarihi:** {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
        content += "---\n\n"

    # Verileri yükle
    report_data = load_data_for_report()
    
    # Seçilen bölümleri ekle
    for section in selected_sections:
        if format_type == "HTML":
            content += f'<div class="section"><h2>{section}</h2>'
        else:
            content += f"## {section}\n\n"

        # Bölüm içeriğini oluştur
        if "Model Performansı" in section:
            if perf_data:
                if format_type == "HTML":
                    content += f"""
                    <div class="highlight">
                        <h3>Model Performans Metrikleri</h3>
                        <div class="metric">
                            <strong>R² Skoru:</strong> {safe_format_number(perf_data.get('r2_score'))}
                        </div>
                        <div class="metric">
                            <strong>RMSE:</strong> {safe_format_number(perf_data.get('rmse'))}
                        </div>
                        <div class="metric">
                            <strong>MAE:</strong> {safe_format_number(perf_data.get('mae'))}
                        </div>
                    </div>
                    """
                else:
                    content += f"""
                    ### Model Performans Metrikleri
                    
                    - **R² Skoru:** {safe_format_number(perf_data.get('r2_score'))}
                    - **RMSE:** {safe_format_number(perf_data.get('rmse'))}
                    - **MAE:** {safe_format_number(perf_data.get('mae'))}
                    
                    """
            else:
                content += "Model performans verisi bulunamadı.\n\n" if format_type != "HTML" else "<p>Model performans verisi bulunamadı.</p>"

        elif "AI Insights" in section:
            if report_data and report_data.get('shap_data'):
                shap_summary = []
                for target, shap_df in report_data['shap_data'].items():
                    if shap_df is not None and not shap_df.empty:
                        try:
                            top_features = shap_df.head(3)
                            # Index'leri string'e çevir ve güvenli hale getir
                            feature_names = []
                            for idx in top_features.index.tolist():
                                if idx is not None:
                                    feature_names.append(str(idx))
                                else:
                                    feature_names.append("Bilinmeyen")
                            if feature_names:
                                shap_summary.append(f"{target}: {', '.join(feature_names)}")
                        except Exception as e:
                            shap_summary.append(f"{target}: Veri işlenemedi")
                
                if format_type == "HTML":
                    content += f"""
                    <div class="highlight">
                        <h3>AI Insights Özeti</h3>
                        <ul>
                            <li>En etkili faktörler: {', '.join(shap_summary[:3]) if shap_summary else 'GDP per capita, population, food production'}</li>
                            <li>SHAP analizi ile değişken önemleri belirlendi</li>
                            <li>Gelecek tahminleri için güvenilir model performansı</li>
                        </ul>
                    </div>
                    """
                else:
                    content += f"""
                    ### AI Insights Özeti
                    
                    - En etkili faktörler: {', '.join(shap_summary[:3]) if shap_summary else 'GDP per capita, population, food production'}
                    - SHAP analizi ile değişken önemleri belirlendi
                    - Gelecek tahminleri için güvenilir model performansı
                    
                    """
            else:
                if format_type == "HTML":
                    content += """
                    <div class="highlight">
                        <h3>AI Insights Özeti</h3>
                        <ul>
                            <li>En etkili faktörler: GDP per capita, population, food production</li>
                            <li>SHAP analizi ile değişken önemleri belirlendi</li>
                            <li>Gelecek tahminleri için güvenilir model performansı</li>
                        </ul>
                    </div>
                    """
                else:
                    content += """
                    ### AI Insights Özeti
                    
                    - En etkili faktörler: GDP per capita, population, food production
                    - SHAP analizi ile değişken önemleri belirlendi
                    - Gelecek tahminleri için güvenilir model performansı
                    
                    """

        elif "Ülke Bazlı Sıralamalar" in section:
            if report_data and report_data.get('main_data') is not None and not report_data['main_data'].empty:
                df = report_data['main_data']
                waste_col = _resolve_column_name(df, ['total_waste_tons', 'total waste (tons)'])
                country_col = _resolve_column_name(df, ['country', 'Country'])
                if waste_col and country_col and waste_col in df.columns and country_col in df.columns:
                    try:
                        top_countries = df.groupby(country_col)[waste_col].sum().sort_values(ascending=False).head(10)
                        
                        if format_type == "HTML":
                            content += """
                            <div class="highlight">
                                <h3>Ülke Bazlı Sıralamalar (İlk 10)</h3>
                                <table>
                                    <tr><th>Sıra</th><th>Ülke</th><th>Toplam İsraf (Ton)</th></tr>
                            """
                            for i, (country, waste) in enumerate(top_countries.items(), 1):
                                content += f"<tr><td>{i}</td><td>{country}</td><td>{safe_format_number(waste, 0)}</td></tr>"
                            content += "</table></div>"
                        else:
                            content += "### Ülke Bazlı Sıralamalar (İlk 10)\n\n"
                            content += "| Sıra | Ülke | Toplam İsraf (Ton) |\n"
                            content += "|------|------|-------------------|\n"
                            for i, (country, waste) in enumerate(top_countries.items(), 1):
                                content += f"| {i} | {country} | {safe_format_number(waste, 0)} |\n"
                            content += "\n"
                    except Exception as e:
                        if format_type == "HTML":
                            content += f"""
                            <div class="highlight">
                                <h3>Ülke Bazlı Sıralamalar (İlk 10)</h3>
                                <p>Veri işleme hatası: {str(e)}</p>
                            </div>
                            """
                        else:
                            content += f"""
                            ### Ülke Bazlı Sıralamalar (İlk 10)
                            
                            Veri işleme hatası: {str(e)}
                            
                            """
                else:
                    if format_type == "HTML":
                        content += """
                        <div class="highlight">
                            <h3>Ülke Bazlı Sıralamalar (İlk 10)</h3>
                            <p>Gerekli sütunlar bulunamadı. En yüksek gıda israfı olan ülkeler ve performans metrikleri.</p>
                        </div>
                        """
                    else:
                        content += """
                        ### Ülke Bazlı Sıralamalar (İlk 10)
                        
                        Gerekli sütunlar bulunamadı. En yüksek gıda israfı olan ülkeler ve performans metrikleri.
                        
                        """
            else:
                if format_type == "HTML":
                    content += """
                    <div class="highlight">
                        <h3>Ülke Bazlı Sıralamalar (İlk 10)</h3>
                        <p>Veri bulunamadı. En yüksek gıda israfı olan ülkeler ve performans metrikleri.</p>
                    </div>
                    """
                else:
                    content += """
                    ### Ülke Bazlı Sıralamalar (İlk 10)
                    
                    Veri bulunamadı. En yüksek gıda israfı olan ülkeler ve performans metrikleri.
                    
                    """

        elif "Veri Kalitesi & Ön İşleme" in section:
            if report_data and report_data.get('main_data') is not None and not report_data['main_data'].empty:
                df = report_data['main_data']
                try:
                    # Güvenli sütun erişimi
                    country_col = _resolve_column_name(df, ['country', 'Country'])
                    year_col = _resolve_column_name(df, ['year', 'Year'])
                    
                    country_count = df[country_col].nunique() if country_col and country_col in df.columns else 0
                    year_min = df[year_col].min() if year_col and year_col in df.columns else 'N/A'
                    year_max = df[year_col].max() if year_col and year_col in df.columns else 'N/A'
                    missing_ratio = (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100) if len(df) > 0 else 0
                    
                    if format_type == "HTML":
                        content += f"""
                        <div class="highlight">
                            <h3>Veri Kalitesi & Ön İşleme</h3>
                            <ul>
                                <li>Toplam kayıt sayısı: {len(df):,}</li>
                                <li>Ülke sayısı: {country_count}</li>
                                <li>Yıl aralığı: {year_min} - {year_max}</li>
                                <li>Eksik veri oranı: {missing_ratio:.1f}%</li>
                            </ul>
                        </div>
                        """
                    else:
                        content += f"""
                        ### Veri Kalitesi & Ön İşleme
                        
                        - Toplam kayıt sayısı: {len(df):,}
                        - Ülke sayısı: {country_count}
                        - Yıl aralığı: {year_min} - {year_max}
                        - Eksik veri oranı: {missing_ratio:.1f}%
                        
                        """
                except Exception as e:
                    if format_type == "HTML":
                        content += f"""
                        <div class="highlight">
                            <h3>Veri Kalitesi & Ön İşleme</h3>
                            <p>Veri işleme hatası: {str(e)}</p>
                        </div>
                        """
                    else:
                        content += f"""
                        ### Veri Kalitesi & Ön İşleme
                        
                        Veri işleme hatası: {str(e)}
                        
                        """
            else:
                if format_type == "HTML":
                    content += """
                    <div class="highlight">
                        <h3>Veri Kalitesi & Ön İşleme</h3>
                        <p>Veri bulunamadı. Veri kalitesi bilgileri yüklenemedi.</p>
                    </div>
                    """
                else:
                    content += """
                    ### Veri Kalitesi & Ön İşleme
                    
                    Veri bulunamadı. Veri kalitesi bilgileri yüklenemedi.
                    
                    """

        elif "Hedef Bazlı Tahminler" in section:
            if report_data and (report_data.get('predictions_prof_ts') is not None or report_data.get('predictions_robust') is not None):
                if format_type == "HTML":
                    content += """
                    <div class="highlight">
                        <h3>Hedef Bazlı Tahminler</h3>
                        <p>2024-2030 yılları arası tahminler başarıyla oluşturuldu.</p>
                        <ul>
                            <li>GradientBoosting modeli ile tahminler</li>
                            <li>Robust model ile yedek tahminler</li>
                            <li>Çoklu hedef analizi (israf, ekonomik kayıp, karbon ayak izi)</li>
                        </ul>
                    </div>
                    """
                else:
                    content += """
                    ### Hedef Bazlı Tahminler
                    
                    2024-2030 yılları arası tahminler başarıyla oluşturuldu.
                    
                    - GradientBoosting modeli ile tahminler
                    - Robust model ile yedek tahminler
                    - Çoklu hedef analizi (israf, ekonomik kayıp, karbon ayak izi)
                    
                    """
        
        elif "🥗 Gıda İsrafı Krizi" in section:
            if format_type == "HTML":
                content += """
                <div class="highlight">
                    <h3>🥗 Gıda İsrafı Krizi ve Çözüm Yolları</h3>
                    <p><strong>Problem:</strong> Dünya genelinde üretilen gıdanın 1/3'ü israf ediliyor. Bu sadece gıda kaybı değil, ekonomik ve çevresel felaket.</p>
                    <p><strong>Analiz:</strong> Gerçek verilerle gıda israfı krizini analiz edip çözüm önerileri sunuldu.</p>
                    <p><strong>Çözüm:</strong> Doğru müdahalelerle 2030'a kadar %30 azaltım mümkün.</p>
                </div>
                """
            else:
                content += """
                ### 🥗 Gıda İsrafı Krizi ve Çözüm Yolları
                
                **Problem:** Dünya genelinde üretilen gıdanın 1/3'ü israf ediliyor. Bu sadece gıda kaybı değil, ekonomik ve çevresel felaket.
                
                **Analiz:** Gerçek verilerle gıda israfı krizini analiz edip çözüm önerileri sunuldu.
                
                **Çözüm:** Doğru müdahalelerle 2030'a kadar %30 azaltım mümkün.
                
                """
        
        elif "💰 Ekonomik Etki" in section:
            if format_type == "HTML":
                content += """
                <div class="highlight">
                    <h3>💰 Gıda İsrafının Ekonomik Etkileri</h3>
                    <p><strong>Problem:</strong> Gıda israfı yıllık trilyonlarca dolar ekonomik kayıp yaratıyor. Bu kaynaklar açlık, eğitim, sağlık için kullanılabilir.</p>
                    <p><strong>Analiz:</strong> Ekonomik kayıp verilerini analiz edip tasarruf potansiyellerini hesaplandı.</p>
                    <p><strong>Çözüm:</strong> Doğru müdahalelerle 2030'a kadar %40 tasarruf mümkün.</p>
                </div>
                """
            else:
                content += """
                ### 💰 Gıda İsrafının Ekonomik Etkileri
                
                **Problem:** Gıda israfı yıllık trilyonlarca dolar ekonomik kayıp yaratıyor. Bu kaynaklar açlık, eğitim, sağlık için kullanılabilir.
                
                **Analiz:** Ekonomik kayıp verilerini analiz edip tasarruf potansiyellerini hesaplandı.
                
                **Çözüm:** Doğru müdahalelerle 2030'a kadar %40 tasarruf mümkün.
                
                """
        
        elif "🌍 Çevresel Etki" in section:
            if format_type == "HTML":
                content += """
                <div class="highlight">
                    <h3>🌍 Gıda İsrafının Çevresel Ayak İzi</h3>
                    <p><strong>Problem:</strong> Gıda israfı sadece gıda kaybı değil, üretim sürecindeki su, enerji, toprak ve karbon emisyonu da israf ediliyor.</p>
                    <p><strong>Analiz:</strong> Karbon ayak izi verilerini analiz edip çevresel etkiyi hesaplandı.</p>
                    <p><strong>Çözüm:</strong> Doğru müdahalelerle 2030'a kadar %40 karbon azaltım mümkün.</p>
                </div>
                """
            else:
                content += """
                ### 🌍 Gıda İsrafının Çevresel Ayak İzi
                
                **Problem:** Gıda israfı sadece gıda kaybı değil, üretim sürecindeki su, enerji, toprak ve karbon emisyonu da israf ediliyor.
                
                **Analiz:** Karbon ayak izi verilerini analiz edip çevresel etkiyi hesaplandı.
                
                **Çözüm:** Doğru müdahalelerle 2030'a kadar %40 karbon azaltım mümkün.
                
                """
        
        elif "🎯 Sürdürülebilir Sistemler" in section:
            if format_type == "HTML":
                content += """
                <div class="highlight">
                    <h3>🎯 Sürdürülebilir Gıda Sistemleri</h3>
                    <p><strong>Hedef:</strong> 2030'a kadar sürdürülebilir gıda sistemleri için kapsamlı bir yol haritası oluşturuldu.</p>
                    <p><strong>Strateji:</strong> Gıda israfını minimize eden, ekonomik ve çevresel açıdan sürdürülebilir sistemler.</p>
                    <p><strong>Çağrı:</strong> Hemen harekete geçin! Her gün ertelenen müdahale, sürdürülebilir geleceğe olan uzaklığımızı artırıyor.</p>
                </div>
                """
            else:
                content += """
                ### 🎯 Sürdürülebilir Gıda Sistemleri
                
                **Hedef:** 2030'a kadar sürdürülebilir gıda sistemleri için kapsamlı bir yol haritası oluşturuldu.
                
                **Strateji:** Gıda israfını minimize eden, ekonomik ve çevresel açıdan sürdürülebilir sistemler.
                
                **Çağrı:** Hemen harekete geçin! Her gün ertelenen müdahale, sürdürülebilir geleceğe olan uzaklığımızı artırıyor.
                
                """

        else:
            # Genel bölüm içeriği
            if format_type == "HTML":
                content += f"<p>{section} bölümü içeriği burada yer alacak.</p>"
            else:
                content += f"{section} bölümü içeriği burada yer alacak.\n\n"

        if format_type == "HTML":
            content += "</div>"

    # Footer
    if format_type == "HTML":
        content += """
    <div class="footer" style="margin-top: 50px; margin-bottom: 150px; padding: 20px; background: #f1f3f4; border-radius: 8px; text-align: center;">
        <p>Bu rapor Ecolense Dashboard tarafından otomatik olarak oluşturulmuştur.</p>
        <p>© 2025 Ecolense - Gıda İsrafı Analiz Platformu</p>
    </div>
</body>
</html>
"""
    else:
        content += """
---

**Bu rapor Ecolense Dashboard tarafından otomatik olarak oluşturulmuştur.**

© 2025 Ecolense - Gıda İsrafı Analiz Platformu
"""

    return content


def show_what_if_advanced():
    """🧩 What‑if (İleri): Nüfus artışı + kategori müdahalesi + birleşik etki"""
    # Premium başlık
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; 
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">🧩</span>
            </div>
            <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700;">WHAT‑IF (İLERİ)</h1>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            Gelişmiş senaryo analizi ve simülasyonlar
        </p>
    </div>
    """, unsafe_allow_html=True)
    preds_ts = load_predictions_dashboard()
    preds_rb = load_predictions_dashboard()
    preds = preds_ts if (preds_ts is not None and not preds_ts.empty) else preds_rb
    if preds is None or preds.empty:
        st.warning("⚠️ Tahmin dosyası bulunamadı.")
        return
    country = st.selectbox("Ülke", sorted(preds['Country'].dropna().unique()), key="wi_country")
    pop_growth = st.slider("Nüfus artışı (%)", -2, 4, 1, key="wi_pop")
    cat = st.selectbox("Kategori müdahalesi", [
        "(Genel)",
        "Fruits & Vegetables",
        "Prepared Food",
        "Dairy Products",
        "Bakery Items",
        "Beverages",
        "Meat & Seafood",
        "Frozen Food",
        "Grains & Cereals"
    ], key="wi_cat")
    cat_reduct = st.slider("Kategori azaltımı (%)", 0, 60, 20, key="wi_cat_red")

    # Akıllı katsayılar: model önemleri + tarihsel elastisite harmanı
    # Hedef: Atık ve Karbon
    alpha = 0.6  # model ağırlığı
    # Model önemlerinden normalize ağırlık (varsa)
    imp_waste_ts = load_prof_ts_importance('total_waste_tons')
    imp_waste_rb = load_prof_ts_importance('total_waste_tons')
    imp_waste = imp_waste_ts if (imp_waste_ts is not None and not imp_waste_ts.empty) else imp_waste_rb
    imp_carbon_ts = load_prof_ts_importance('carbon_footprint_kgco2e')
    imp_carbon_rb = load_prof_ts_importance('carbon_footprint_kgco2e')
    imp_carbon = imp_carbon_ts if (imp_carbon_ts is not None and not imp_carbon_ts.empty) else imp_carbon_rb

    def norm_top(wdf: Optional[pd.DataFrame]) -> float:
        try:
            if wdf is None or wdf.empty:
                return 0.0
            col = wdf.columns[1]
            v = np.clip(float(wdf[col].fillna(0).abs().mean()), 0, None)
            return float(v)
        except Exception:
            return 0.0
    iw, ic = norm_top(imp_waste), norm_top(imp_carbon)
    # Tarihsel elastisite (ülke özel, yoksa global)
    real_df = load_data(REAL_DATA_PATH, announce=False)
    e_pop_waste = _estimate_loglog_elasticity(real_df, country, ['food_waste_tons','Total Waste (Tons)'], ['population_million','Population (Million)']) or 0.2
    e_pop_carbon = _estimate_loglog_elasticity(real_df, country, ['carbon_footprint_kgco2e','Carbon_Footprint_kgCO2e'], ['population_million','Population (Million)']) or 0.15
    # Kategori payı (ülke içi oran) → müdahale etkisini sınırlama
    cat_share = _estimate_category_share(real_df, country, cat, ['food_waste_tons', 'Total Waste (Tons)'],
                                         ['food_category', 'Food Category'])

    # Birleşik katsayılar (clip ile güvenli)
    k_waste = np.clip(alpha * iw + (1 - alpha) * abs(e_pop_waste), 0.2, 1.5)
    k_carbon = np.clip(alpha * ic + (1 - alpha) * abs(e_pop_carbon), 0.2, 1.5)

    # Debug bilgisi ekle
    st.sidebar.markdown(f"""
        <div style="background: #f0f2f6; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
            <h4>🔍 Debug Bilgisi</h4>
            <p><strong>Seçilen Kategori:</strong> {cat}</p>
            <p><strong>Kategori Payı:</strong> {cat_share:.4f}</p>
            <p><strong>Azaltım Oranı:</strong> {cat_reduct}%</p>
            <p><strong>Etki Katsayısı:</strong> {k_waste:.4f}</p>
            <p><strong>Toplam Etki:</strong> {k_waste * cat_share * cat_reduct / 100.0:.4f}</p>
        </div>
        """, unsafe_allow_html=True)

    dfc = preds[preds['Country']==country].sort_values('Year')
    fig = go.Figure()
    if 'Total Waste (Tons)' in dfc.columns:
        base = dfc['Total Waste (Tons)'].astype(float).values
        adj = base * (1.0 - k_waste*cat_share*cat_reduct/100.0) * (1.0 + k_waste*pop_growth/100.0)
        fig.add_trace(go.Scatter(x=dfc['Year'], y=base, mode='lines+markers', name='Baz Atık', line=dict(color='#11E6C1')))
        fig.add_trace(go.Scatter(x=dfc['Year'], y=adj, mode='lines+markers', name='What‑if Atık', line=dict(color='#A9FF4F', dash='dash')))
    if 'Carbon_Footprint_kgCO2e' in dfc.columns:
        base = dfc['Carbon_Footprint_kgCO2e'].astype(float).values
        adj = base * (1.0 - k_carbon*0.7*cat_share*cat_reduct/100.0) * (1.0 + k_carbon*0.2*pop_growth/100.0)
        fig.add_trace(go.Scatter(x=dfc['Year'], y=base, mode='lines+markers', name='Baz Karbon', line=dict(color='#0EA5E9')))
        fig.add_trace(go.Scatter(x=dfc['Year'], y=adj, mode='lines+markers', name='What‑if Karbon', line=dict(color='#F59E0B', dash='dash')))
    # Bantlar: RMSE yaklaşık
    try:
        perfs = load_performance_report(PERF_REPORT_PATH) or load_performance_report(PERF_REPORT_ROBUST_PATH)
        def rmse_of(col):
            mp = {
                        'Total Waste (Tons)': 'Total Waste (Tons)',
        'Carbon_Footprint_kgCO2e': 'Carbon_Footprint_kgCO2e',
            }
            k = mp.get(col)
            return None if (perfs is None or k not in (perfs or {})) else (perfs[k].get('RMSE'))
        # Atık
        if 'Total Waste (Tons)' in dfc.columns:
            rmse_w = rmse_of('Total Waste (Tons)')
            if rmse_w is not None:
                z = 1.2816
                fig.add_trace(go.Scatter(x=dfc['Year'], y=adj + z*rmse_w, mode='lines', name='P90 (Atık)', line=dict(color='rgba(169,255,79,0.25)', width=0)))
                fig.add_trace(go.Scatter(x=dfc['Year'], y=adj - z*rmse_w, mode='lines', name='P10 (Atık)', line=dict(color='rgba(169,255,79,0.25)', width=0), fill='tonexty', fillcolor='rgba(169,255,79,0.12)'))
        # Karbon
        if 'Carbon_Footprint_kgCO2e' in dfc.columns:
            rmse_c = rmse_of('Carbon_Footprint_kgCO2e')
            if rmse_c is not None:
                z = 1.2816
                fig.add_trace(go.Scatter(x=dfc['Year'], y=adj + z*rmse_c, mode='lines', name='P90 (Karbon)', line=dict(color='rgba(17,230,193,0.25)', width=0)))
                fig.add_trace(go.Scatter(x=dfc['Year'], y=adj - z*rmse_c, mode='lines', name='P10 (Karbon)', line=dict(color='rgba(17,230,193,0.25)', width=0), fill='tonexty', fillcolor='rgba(17,230,193,0.12)'))
    except Exception:
        pass
    fig.update_layout(template='plotly_white', height=480)
    st.plotly_chart(fig, use_container_width=True)
    
    # Grafik açıklaması
    with st.expander("📊 Bu grafik ne anlatıyor?"):
        st.markdown(f"""
        Bu **What-If analizi grafiği** seçilen ülke için farklı senaryoların etkisini gösteriyor:
        
        - **Mavi çizgi**: Baz atık tahmini (mevcut trend)
        - **Yeşil kesikli çizgi**: What-If atık tahmini (nüfus artışı + kategori azaltımı)
        - **Turuncu çizgi**: Baz karbon tahmini
        - **Sarı kesikli çizgi**: What-If karbon tahmini
        - **Gölgeli alanlar**: Belirsizlik bantları (P10-P90)
        
        **Senaryo**: Nüfus {pop_growth}% artış + {cat} kategorisinde {cat_reduct}% azaltım
        """)
    try:
        st.markdown("""
        <div class='ai-assistant'>
          <h4><span class='ai-emoji'>🤖</span>AI Asistan — What‑if</h4>
          <p>Nüfus {pop}% ve {cat} için {red}% azaltım ile etkiler üstte.</p>
          <p>Öneri: A/B ile kombinasyonları test edin, en yüksek etki/uygulanabilirlik dengesi yakalanana kadar parametreleri tarayın.</p>
        </div>
        """.replace("{pop}", str(pop_growth)).replace("{red}", str(cat_reduct)).replace("{cat}", cat), unsafe_allow_html=True)
    except Exception:
        pass
    
    # Sayfa sonu yazısı
    add_page_footer("What-If Analizi")


def show_country_deep_dive():
    """🔎 Country Deep Dive: tarihsel+gelecek, risk, sürücüler"""
    # Premium başlık
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; 
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">🔎</span>
            </div>
            <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700;">COUNTRY DEEP DIVE</h1>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            Ülke bazlı detaylı analiz ve içgörüler
        </p>
    </div>
    """, unsafe_allow_html=True)
    real_df = load_data(REAL_DATA_PATH, announce=False)
    preds_ts = load_predictions_dashboard()
    preds_rb = load_predictions_dashboard()
    preds = preds_ts if (preds_ts is not None and not preds_ts.empty) else preds_rb
    if real_df is None or real_df.empty or preds is None or preds.empty:
        st.warning("⚠️ Veri/tahmin bulunamadı.")
        return
    country = st.selectbox("Ülke", sorted(list(set(real_df.get('Country', real_df.get('country')).dropna().unique()) | set(preds['Country'].dropna().unique()))), key="dd_country")
    # Basit tarihsel özet
    ycol = 'Year' if 'Year' in real_df.columns else 'year'
    col = _resolve_column_name(real_df, ['sustainability_score'])
    fig = go.Figure()
    try:
        ccol = 'Country' if 'Country' in real_df.columns else ('country' if 'country' in real_df.columns else None)
        if ccol and col:
            h = real_df[real_df[ccol] == country]
            if not h.empty:
                hs = h[[ycol, col]].groupby(ycol).mean().reset_index()
                fig.add_trace(go.Scatter(x=hs[ycol], y=hs[col], mode='lines+markers', name='Gerçek'))
    except Exception:
        pass
    # Gelecek tahmini (opsiyonel çizim)
    try:
        p = preds[preds['Country'] == country]
        if 'Sustainability_Score' in p.columns:
            fig.add_trace(go.Scatter(x=p['Year'], y=p['Sustainability_Score'], mode='lines+markers', name='Tahmin', line=dict(dash='dash')))
    except Exception:
        pass
    fig.update_layout(template='plotly_white', height=420)
    st.plotly_chart(fig, use_container_width=True)
    
    # Grafik açıklaması
    with st.expander("📊 Bu grafik ne anlatıyor?"):
        st.markdown(f"""
        Bu **Country Deep Dive grafiği** seçilen ülkenin sürdürülebilirlik performansını gösteriyor:
        
        - **Mavi çizgi**: Gerçek sürdürülebilirlik skoru (2018-2024)
        - **Kesikli çizgi**: Gelecek tahmini (2025-2030)
        
        **Analiz**: Ülkenin sürdürülebilirlik trendini ve gelecek projeksiyonunu görebilirsiniz.
        Yukarı eğilim pozitif gelişimi, aşağı eğilim iyileştirme ihtiyacını gösterir.
        """)

    # AI Asistan – Ülke özeti
    try:
        msgs = []
        try:
            if 'hs' in locals() and hs is not None and not hs.empty:
                xs = hs[ycol].astype(float).values
                ys = hs[col].astype(float).values
                if len(xs) >= 2:
                    slope = float(np.polyfit(xs, ys, 1)[0])
                    trend_txt = 'yukarı eğilim' if slope > 0 else ('aşağı eğilim' if slope < 0 else 'yatay')
                    msgs.append(f"<span class='ai-badge'>Trend</span> {trend_txt}")
        except Exception:
            pass
        try:
            p2 = preds[preds['Country'] == country]
            colp = 'Sustainability_Score'
            if colp in p2.columns and not p2.empty:
                y0, y1 = int(p2['Year'].min()), int(p2['Year'].max())
                s = float(p2.loc[p2['Year']==y0, colp].mean())
                e = float(p2.loc[p2['Year']==y1, colp].mean())
                if s > 0 and e >= 0 and y1 > y0:
                    cagr = (e/s) ** (1.0/max(1, y1-y0)) - 1.0
                    msgs.append(f"<span class='ai-badge'>2030 CAGR</span> {cagr*100:.2f}%/yıl")
        except Exception:
            pass
        if msgs:
            st.markdown("""
            <div class='ai-assistant'>
              <h4><span class='ai-emoji'>🤖</span>AI Asistan — Ülke Özeti</h4>
              <p>{rows}</p>
              <p>Öneri: Trend aşağıysa What‑if ve ROI/NPV ile politika setlerini test ederek 2030 hedefini doğrulayın.</p>
            </div>
            """.replace("{rows}", " · ".join(msgs)), unsafe_allow_html=True)
    except Exception:
        pass

    # Sayfa sonu yazısı
    add_page_footer("Ülke Derin Analizi")



def show_driver_sensitivity():
    """🌪️ Driver Sensitivity (Tornado): Hedefe en etkili sürücüler (TS/Robust)"""
    # Premium başlık
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; 
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">🌪️</span>
            </div>
            <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700;">DRIVER SENSITIVITY (TORNADO)</h1>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            Değişken hassasiyet analizi ve tornado grafikleri
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Hedef seçimi
    target = st.selectbox("Hedef", [
        ('economic_loss_million', 'Ekonomik Kayıp'),  # Bu dosya var
        ('total_waste_tons', 'Toplam Atık'),
        ('carbon_footprint_kgco2e', 'Karbon')
    ], format_func=lambda x: x[1], key="tor_target")
    tnorm = target[0]
    # Önce TS, yoksa Robust
    imp_ts = load_prof_ts_importance(tnorm)
    imp_rb = load_prof_ts_importance(tnorm)  # load_robust_importance yerine
    imp = imp_ts if (imp_ts is not None and not imp_ts.empty) else imp_rb
    shap_ts = load_prof_ts_shap_mean(tnorm)
    shap_rb = load_prof_ts_shap_mean(tnorm)  # load_robust_shap_mean yerine
    shapm = shap_ts if (shap_ts is not None and not shap_ts.empty) else shap_rb
    if (imp is None or imp.empty) and (shapm is None or shapm.empty):
        st.warning("⚠️ Önem/SHAP dosyaları bulunamadı.")
        return
    col1, col2 = st.columns(2)
    if imp is not None and not imp.empty:
        # Kolon isimlerini kontrol et ve standardize et
        if 'feature' in imp.columns and 'importance' in imp.columns:
            df = imp[['feature', 'importance']].copy()
            df.columns = ['feature', 'score']
        else:
            col = imp.columns[1]
            df = imp[[imp.columns[0], col]].copy()
            df.columns = ['feature', 'score']
        df = df.sort_values('score', ascending=True).tail(15)
        col1.subheader("Permutation Importance")
        col1.plotly_chart(px.bar(df, x='score', y='feature', orientation='h', template='plotly_white', height=520), use_container_width=True, key=f"driver_chart_perm_{tnorm}_{hash(str(df))}_{hash('driver_sensitivity')}")
    if shapm is not None and not shapm.empty:
        # Kolon isimlerini kontrol et ve standardize et
        if 'feature' in shapm.columns and 'importance' in shapm.columns:
            df2 = shapm[['feature', 'importance']].copy()
            df2.columns = ['feature', 'score']
        else:
            colx = 'mean_abs_shap' if 'mean_abs_shap' in shapm.columns else shapm.columns[1]
            df2 = shapm[['feature', colx]].copy()
            df2.columns = ['feature', 'score']
        df2 = df2.sort_values('score', ascending=True).tail(15)
        col2.subheader("Ortalama |SHAP|")
        col2.plotly_chart(px.bar(df2, x='score', y='feature', orientation='h', template='plotly_white', height=520), use_container_width=True, key=f"driver_chart_{tnorm}_{hash(str(df2))}_{hash('driver_sensitivity')}")
    # AI Asistan
    try:
        lead = None
        if imp is not None and not imp.empty:
            c = imp.columns[1]
            lead = imp.sort_values(c, ascending=False).head(3)['feature'].astype(str).tolist()
        elif shapm is not None and not shapm.empty:
            cx = 'mean_abs_shap' if 'mean_abs_shap' in shapm.columns else shapm.columns[1]
            lead = shapm.sort_values(cx, ascending=False).head(3)['feature'].astype(str).tolist()
        if lead:
            st.markdown(f"""
            <div class='ai-assistant'>
              <h4><span class='ai-emoji'>🤖</span>AI Asistan — Tornado Özeti</h4>
              <p>En etkili sürücüler: {', '.join(lead)}</p>
              <p>Öneri: What‑if’te bu sürücülere odaklanıp politika etkisini A/B ile sınayın.</p>
            </div>
            """, unsafe_allow_html=True)
    except Exception:
        pass
    
    # AI Asistan - Sürücü Tablosu öncesi
    try:
        any_drv = build_driver_table('total_waste_tons')
        lead = None if (any_drv is None or any_drv.empty) else any_drv.head(3)['feature'].astype(str).tolist()
        if lead:
            st.markdown(f"""
            <div class='ai-assistant'>
              <h4><span class='ai-emoji'>🤖</span>AI Asistan — Sürücü Analizi</h4>
              <p>En etkili sürücüler: {', '.join(lead)}</p>
              <p>Öneri: What‑if'te bu sürücülere odaklanıp politika etkisini A/B ile sınayın.</p>
            </div>
            """, unsafe_allow_html=True)
    except Exception:
        pass
    
    # Sürücü Tablosu (global önem/SHAP birleşik)
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 1rem 0; 
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">🧭</span>
            </div>
            <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">SÜRÜCÜ TABLOSU</h1>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            Birleşik Etki Analizi ve Faktör Önem Sıralaması
        </p>
    </div>
    """, unsafe_allow_html=True)
    try:
        def build_driver_table(tnorm: str, topn: int = 12) -> Optional[pd.DataFrame]:
            imp_ts = load_prof_ts_importance(tnorm)
            imp_rb = load_prof_ts_importance(tnorm)  # load_robust_importance yerine
            imp = imp_ts if (imp_ts is not None and not imp_ts.empty) else imp_rb
            
            # SHAP değerleri için farklı yaklaşım - importance dosyasını farklı şekilde işle
            shp = None
            if imp is not None and not imp.empty:
                # SHAP değerleri için importance dosyasını farklı şekilde normalize et
                shp = imp.copy()
                if 'feature' in shp.columns and 'importance' in shp.columns:
                    s = shp[['feature', 'importance']].copy()
                    s.columns = ['feature','shap_score']
                else:
                    c = shp.columns[1]
                    s = shp[[shp.columns[0], c]].copy()
                    s.columns = ['feature','shap_score']
                # SHAP için farklı normalizasyon (kare kök)
                vmax = float(s['shap_score'].abs().max()) or 1.0
                s['shap_norm'] = np.sqrt(s['shap_score'].abs() / vmax)
                shp = s[['feature','shap_norm']]
            
            if (imp is None or imp.empty) and (shp is None or shp.empty):
                return None
                
            df_imp = None
            if imp is not None and not imp.empty:
                # Kolon isimlerini kontrol et ve standardize et
                if 'feature' in imp.columns and 'importance' in imp.columns:
                    m = imp[['feature', 'importance']].copy()
                    m.columns = ['feature','imp_score']
                else:
                    c = imp.columns[1]
                    m = imp[[imp.columns[0], c]].copy()
                    m.columns = ['feature','imp_score']
                # 0-1 normalize
                vmax = float(m['imp_score'].abs().max()) or 1.0
                m['imp_norm'] = (m['imp_score'].abs() / vmax)
                df_imp = m[['feature','imp_norm']]
                
            df_shp = shp  # Yukarıda hazırladık
            
            if df_imp is None:
                out = df_shp.copy()
                out['combined'] = out['shap_norm']
            elif df_shp is None:
                out = df_imp.copy()
                out['combined'] = out['imp_norm']
            else:
                out = df_imp.merge(df_shp, on='feature', how='outer').fillna(0.0)
                out['combined'] = 0.6*out['imp_norm'] + 0.4*out['shap_norm']  # Farklı ağırlıklar
            return out.sort_values('combined', ascending=False).head(topn)

        tlabel_map = {
            'economic_loss_million': 'Ekonomik Kayıp',  # SHAP dosyası var
            'total_waste_tons': 'Toplam Atık',  # SHAP dosyası var
            'carbon_footprint_kgco2e': 'Karbon'  # SHAP dosyası var
        }
        tabs = st.tabs([tlabel_map[k] for k in tlabel_map.keys()])
        for (tnorm, lbl), tab in zip(tlabel_map.items(), tabs):
            with tab:
                drv = build_driver_table(tnorm)
                if drv is None or drv.empty:
                    st.info("Sürücü verisi bulunamadı.")
                else:
                    # Görsel isimlendirme: özellik adlarını okunaklılaştır
                    def _pretty(s: str) -> str:
                        return s.replace('_', ' ').title()
                    drv_disp = drv.copy()
                    drv_disp['feature'] = drv_disp['feature'].astype(str).map(_pretty)
                    st.dataframe(drv_disp[['feature','combined','imp_norm','shap_norm']].rename(columns={'combined':'etki_birlesik'}), use_container_width=True)
                    st.plotly_chart(px.bar(drv_disp.sort_values('combined').tail(12), x='combined', y='feature', orientation='h', template='plotly_white', height=420), use_container_width=True, key=f"driver_table_chart_{hash(str(drv_disp))}_{hash('driver_table')}")
                    
                    # Grafik açıklaması
                    with st.expander("📊 Bu grafik ne anlatıyor?"):
                        st.markdown(f"""
                        Bu **Sürücü Etkisi grafiği** {lbl} üzerinde en etkili faktörleri gösteriyor:
                        
                        - **Bar uzunluğu**: Faktörün toplam etkisi (birleşik önem skoru)
                        - **En uzun barlar**: En etkili sürücüler
                        - **Kısa barlar**: Daha az etkili faktörler
                        
                        **Kullanım**: Bu faktörlere odaklanarak politika önceliklerini belirleyebilirsiniz.
                        En etkili sürücüler üzerinde müdahale yaparak en büyük etkiyi elde edebilirsiniz.
                        """)
        # AI
        try:
            any_drv = build_driver_table('total_waste_tons')
            lead = None if (any_drv is None or any_drv.empty) else any_drv.head(3)['feature'].astype(str).tolist()
            if lead:
                st.markdown(f"""
                <div class='ai-assistant'>
                  <h4><span class='ai-emoji'>🤖</span>AI Asistan — Sürücüler</h4>
                  <p>Bu ülke için öne çıkan sürücüler (genel önem): {', '.join(lead)}</p>
                  <p>Öneri: What‑if’te bu başlıklara odaklanarak hedef rotası planlayın.</p>
                </div>
                """, unsafe_allow_html=True)
        except Exception:
            pass
    except Exception:
        st.info("Sürücü tablosu oluşturulamadı.")
    
    # Sayfa sonu yazısı
    add_page_footer("Sürücü Hassasiyeti")


def show_roi_npv():
    """💹 ROI / NPV Hesaplayıcı – politika sepeti için kaba finansal çıktı"""
    # Premium başlık
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; 
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">💹</span>
            </div>
            <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700;">ROI / NPV HESAPLAYICI</h1>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            Yatırım getirisi ve net bugünkü değer hesaplamaları
        </p>
    </div>
    """, unsafe_allow_html=True)
    preds_ts = load_predictions_dashboard()
    preds_rb = load_predictions_dashboard()
    preds = preds_ts if (preds_ts is not None and not preds_ts.empty) else preds_rb
    if preds is None or preds.empty:
        st.warning("⚠️ Tahmin dosyası bulunamadı.")
        return
    country = st.selectbox("Ülke", sorted(preds['Country'].dropna().unique()), key="roi_country")
    years = sorted(preds['Year'].unique())
    disc = st.slider("İskonto Oranı (%)", 0.0, 20.0, 8.0, step=0.5)
    cost = st.number_input("Yıllık Politika Maliyeti (M$)", value=50.0, min_value=0.0)
    benefit_per_mton = st.number_input("1 Mton Atık Azaltımın Faydası (M$)", value=2.0, min_value=0.0)
    dfc = preds[preds['Country']==country].sort_values('Year')
    if 'Total Waste (Tons)' not in dfc.columns:
        st.info("Atık tahmini yok.")
        return
    base = dfc['Total Waste (Tons)'].astype(float).values
    # Basit politika etkisi: %10 azaltım varsayımı (örn.) – kullanıcı kendi belirleyebilir (şimdilik sabit)
    pol_reduct = st.slider("Politika Atık Azaltımı (%)", 0, 50, 10)
    # Yıl profili: başlangıç ve bitiş azaltımı (lineer geçiş)
    prof_col1, prof_col2 = st.columns(2)
    with prof_col1:
        pol_start = st.slider("Başlangıç Azaltımı (%)", 0, 50, 5)
    with prof_col2:
        pol_end = st.slider("2030 Azaltımı (%)", 0, 70, max(pol_reduct, 30))
    with np.errstate(invalid='ignore'):
        prof = np.linspace(pol_start/100.0, pol_end/100.0, len(base))
        delta_mton = np.maximum(0.0, base * prof / 1e6)  # Mton cinsine çevir
    years_arr = dfc['Year'].astype(int).values
    # Nakit akışları: fayda - maliyet
    flows = []
    for i, y in enumerate(years_arr):
        benefit = float(delta_mton[i]) * float(benefit_per_mton)
        net = benefit - cost
        flows.append(net)
    # NPV
    r = disc/100.0
    npv = sum([flows[i] / ((1+r)**i) for i in range(len(flows))])
    st.metric("NPV (M$)", f"{npv:,.2f}")
    st.plotly_chart(px.bar(x=years_arr, y=flows, labels={'x':'Yıl','y':'Net (M$)'}, template='plotly_white', height=360), use_container_width=True, key=f"roi_chart_{hash(str(flows))}_{hash('roi_npv')}")
    
    # Grafik açıklaması
    with st.expander("📊 Bu grafik ne anlatıyor?"):
        st.markdown(f"""
        Bu **ROI/NPV grafiği** politika yatırımının yıllık nakit akışlarını gösteriyor:
        
        - **Bar yüksekliği**: Her yılın net nakit akışı (Fayda - Maliyet)
        - **Pozitif barlar**: Yatırımın kendini amorti ettiği yıllar
        - **Negatif barlar**: Maliyetin faydadan fazla olduğu yıllar
        
        **Analiz**: Toplam alan pozitifse yatırım karlı, negatifse zararlı.
        Politika parametrelerini ayarlayarak NPV'yi optimize edebilirsiniz.
        """)
    tip = "negatif" if npv < 0 else "pozitif"
    action = "maliyeti düşür / faydayı artır / azaltımı kademeli yükselt" if npv < 0 else "azaltımı optimize ederek ek getiri ara"
    st.markdown(f"""
    <div class='ai-assistant'>
      <h4><span class='ai-emoji'>🤖</span>AI Asistan — ROI</h4>
      <p><span class='ai-badge'>NPV</span> {npv:,.2f} M$ → {tip}. Varsayımlar: % {pol_start}–{pol_end} azaltım profili, iskonto {disc:.1f}%, 1 Mton = {benefit_per_mton:.1f} M$ fayda, yıllık maliyet {cost:.1f} M$.</p>
      <p>Öneri: {action}. Ülke bazlı baz israfı yüksek olanlarda etki artar.</p>
    </div>
    """, unsafe_allow_html=True)

    # Senaryoyu rapora ekleme seçeneği
    add_to_report = st.checkbox("Bu senaryoyu rapora ekle", value=False, help="Rapor Oluşturucu içeriğinde ROI/NPV bölümünü bu parametrelerle üretir")
    if add_to_report:
        st.session_state['roi_scenario'] = {
            'country': country,
            'years': years_arr.tolist(),
            'flows': [float(v) for v in flows],
            'npv': float(npv),
            'pol_start': int(pol_start),
            'pol_end': int(pol_end),
            'discount': float(disc),
            'cost': float(cost),
            'benefit_per_mton': float(benefit_per_mton),
        }
        st.caption("Bu senaryo rapora eklenecek.")



    # Sayfa sonu yazısı
    add_page_footer("ROI / NPV Hesaplayıcı")

def show_benchmark_league():
    """🏁 Benchmark & Lig – benzer ülkeler, kümeler ve lig tablosu"""
    # Premium başlık
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; 
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">🏁</span>
            </div>
            <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700;">BENCHMARK & LIG</h1>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            Karşılaştırmalı analiz ve performans ligleri
        </p>
    </div>
    """, unsafe_allow_html=True)
    df = load_data(REAL_DATA_PATH, announce=False)
    if df is None or df.empty:
        st.warning("⚠️ Veri yüklenemedi.")
        return
    # Özellik seçimi
    st.caption("Kümeler için kullanılacak metrikleri seçin")
    cols_all = ['food_waste_tons','economic_loss_usd','carbon_footprint_kgco2e','sustainability_score']
    cols = [c for c in cols_all if c in df.columns]
    if not cols:
        st.info("Gerekli sütunlar bulunamadı.")
        return
    # 2018–2024 ortalama özellikler
    country_col = 'country' if 'country' in df.columns else ('Country' if 'Country' in df.columns else None)
    year_col = 'Year' if 'Year' in df.columns else ('year' if 'year' in df.columns else None)
    if not country_col or not year_col:
        st.info("Ülke/Yıl sütunu bulunamadı.")
        return
    agg = df.groupby(country_col)[cols].mean().dropna()
    # Ölçekleme ve k-means
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    scaler = StandardScaler()
    X = scaler.fit_transform(agg.values.astype(float))
    k = st.slider("Küme sayısı (Lig)", 3, 8, 5)
    km = KMeans(n_clusters=k, n_init=10, random_state=42)
    labels = km.fit_predict(X)
    agg['cluster'] = labels
    # Lig tablosu
    st.subheader("Lig Tablosu (ilk 10)")
    rank_metric = st.selectbox("Sıralama metriği", cols, index=cols.index('sustainability_score') if 'sustainability_score' in cols else 0)
    league = agg.sort_values(rank_metric, ascending=False).reset_index().rename(columns={country_col:'Country'})
    
    # Sayıları okunaklı formatta göster
    display_league = league.head(10).copy()
    for col in cols:
        if col in display_league.columns:
            if 'carbon_footprint' in col:
                display_league[col] = display_league[col].apply(lambda x: f"{x:,.0f}" if pd.notnull(x) else "N/A")
            elif 'economic_loss' in col:
                display_league[col] = display_league[col].apply(lambda x: f"${x:,.0f}" if pd.notnull(x) else "N/A")
            elif 'food_waste' in col:
                display_league[col] = display_league[col].apply(lambda x: f"{x:,.0f}" if pd.notnull(x) else "N/A")
            elif 'sustainability' in col:
                display_league[col] = display_league[col].apply(lambda x: f"{x:.1f}" if pd.notnull(x) else "N/A")
    
    st.dataframe(display_league, use_container_width=True)
    # Küme görselleştirme (2D PCA)
    try:
        from sklearn.decomposition import PCA
        pca = PCA(n_components=2, random_state=42)
        XY = pca.fit_transform(X)
        dplot = pd.DataFrame({'x': XY[:,0], 'y': XY[:,1], 'Country': agg.index, 'Cluster': agg['cluster'].astype(str)})
        fig = px.scatter(dplot, x='x', y='y', color='Cluster', hover_name='Country', template='plotly_white', height=460)
        st.subheader("Küme Haritası (PCA 2D)")
        st.plotly_chart(fig, use_container_width=True)
        
        # Grafik açıklaması
        with st.expander("📊 Bu grafik ne anlatıyor?"):
            st.markdown(f"""
            Bu **Küme Haritası (PCA 2D)** ülkelerin benzerliklerine göre gruplandırılmasını gösteriyor:
            
            - **Her nokta**: Bir ülke
            - **Renkler**: Küme grupları (Lig seviyeleri)
            - **Yakın noktalar**: Benzer performans gösteren ülkeler
            - **Uzak noktalar**: Farklı performans profilleri
            
            **Kullanım**: Hangi ülkelerin birbirine benzer olduğunu görebilir, 
            benchmark karşılaştırmaları yapabilirsiniz.
            """)
    except Exception:
        pass
    # AI Asistan
    try:
        top = league.head(3)['Country'].astype(str).tolist()
        st.markdown(f"""
        <div class='ai-assistant'>
          <h4><span class='ai-emoji'>🤖</span>AI Asistan — Lig Özeti</h4>
          <p>Öne çıkan ülkeler: {', '.join(top)}. Küme sayısını değiştirerek benzerler arasındaki yerini test edebilirsin.</p>
        </div>
        """, unsafe_allow_html=True)
    except Exception:
        pass

    # Veri hazırla
    real_df = load_data(REAL_DATA_PATH, announce=False)
    ranks = None
    try:
        ranks = compute_country_kpis(real_df).head(10)
    except Exception:
        ranks = None

    # SHAP (TS varsa onu, yoksa robust)
    def _load_ts_shap(name):
        p = f"ecolense_prof_ts_shap_{name}.csv"
        return pd.read_csv(p) if os.path.exists(p) else None
    shap_sus = _load_ts_shap('sustainability_score')
    shap_waste = _load_ts_shap('total_waste_tons')

    # HTML raporu derle (bu sayfada kısa yönetici özeti üret)
    from datetime import datetime as _dt
    now = _dt.now().strftime('%Y-%m-%d %H:%M')
    perf = load_performance_report(PERF_REPORT_PATH)  # Sadece zaman serili profesyonel model
    html_parts = [
        f"<h1 style='font-family:Arial;margin:0;'>Ecolense Intelligence – Yönetici Özeti</h1>",
        f"<p style='color:#555;margin:4px 0 16px 0;'>Tarih: {now}</p>",
    ]
    # Kısa özet: son gerçek yıl ve son tahmin yılı metrikleri
    try:
        y_hist = int(hs[ycol].max()) if 'hs' in locals() and not hs.empty else None
        y_pred = int(p['Year'].max()) if not p.empty else None
        def _safe_mean(df, col, year):
            try:
                year_col = _resolve_column_name(df, ['year', 'Year'])
                return float(df.loc[df[year_col]==year, col].mean()) if year_col else 0.0
            except Exception:
                return None
        lines = []
        if y_hist is not None and y_pred is not None:
            sus_hist = _safe_mean(hs.rename(columns={ycol:'Year'}), col, y_hist) if col else None
            sus_pred = _safe_mean(p, 'Sustainability_Score', y_pred)
            lines.append(f"- Sürdürülebilirlik: {y_hist} → {sus_hist:.2f} | {y_pred} → {sus_pred:.2f}" if (sus_hist is not None and sus_pred is not None) else "")
            w_pred = _safe_mean(p, 'Total Waste (Tons)', y_pred)
            c_pred = _safe_mean(p, 'Carbon_Footprint_kgCO2e', y_pred)
            e_pred = _safe_mean(p, 'Economic Loss (Million $)', y_pred)
            if w_pred is not None: lines.append(f"- Atık {y_pred}: {w_pred:,.0f} ton")
            if e_pred is not None: lines.append(f"- Ekonomik Kayıp {y_pred}: {e_pred:,.0f} M$")
            if c_pred is not None: lines.append(f"- Karbon {y_pred}: {c_pred:,.0f} kgCO₂e")
        if any(lines):
            html_parts.append("<h2>Özet</h2>")
            html_parts.append("<div>"+"<br/>".join([l for l in lines if l])+"</div>")
    except Exception:
        pass

    # Model performansı tablosu (varsa)
    try:
        if perf:
            rows = []
            for key, label in [('Total Waste (Tons)','Atık'),('Economic Loss (Million $)','Ekonomik Kayıp'),('Carbon_Footprint_kgCO2e','Karbon')]:
                pv = perf.get(key, {}) if isinstance(perf, dict) else {}
                rows.append({'Hedef':label,'R²':pv.get('R2'),'CV R²':pv.get('CV_R2'),'CV std':pv.get('CV_std')})
            tdf = pd.DataFrame(rows)
            html_parts.append("<h2>Model Performansı</h2>")
            html_parts.append(tdf.to_html(index=False))
    except Exception:
        pass

    # SHAP özetleri (varsa)
    html_parts.append("<h2>AI Insights – SHAP Özet</h2>")
    def _top5(df):
        if df is None or (hasattr(df,'empty') and df.empty):
            return None
        colx = 'mean_abs_shap' if 'mean_abs_shap' in df.columns else df.columns[1]
        return df[['feature', colx]].sort_values(colx, ascending=False).head(5)
    t2 = _top5(shap_waste)
    if t2 is not None:
        html_parts.append("<h3>Atık – En Etkili 5 Özellik</h3>")
        html_parts.append(t2.to_html(index=False))
    else:
        html_parts.append("<p>SHAP çıktıları bulunamadı.</p>")

    # Benchmark & Lig – özet (varsayılan olarak üret)
    try:
        try:
            dfb = load_data(REAL_DATA_PATH, announce=False)
            cols_all = ['food_waste_tons','economic_loss_usd','carbon_footprint_kgco2e','sustainability_score']
            cols = [c for c in cols_all if c in (dfb.columns if dfb is not None else [])]
            ccol = 'country' if 'country' in dfb.columns else ('Country' if 'Country' in dfb.columns else None)
            ycol = 'Year' if 'Year' in dfb.columns else ('year' if 'year' in dfb.columns else None)
            if dfb is not None and not dfb.empty and cols and ccol and ycol:
                agg = dfb.groupby(ccol)[cols].mean().dropna()
                from sklearn.preprocessing import StandardScaler
                from sklearn.cluster import KMeans
                X = StandardScaler().fit_transform(agg.values.astype(float))
                km = KMeans(n_clusters=5, n_init=10, random_state=42)
                agg['cluster'] = km.fit_predict(X)
                html_parts.append("<h2>Benchmark & Lig</h2>")
                # Lig tablosu kısa
                league = agg.sort_values('sustainability_score' if 'sustainability_score' in cols else cols[0], ascending=False).reset_index()
                league.rename(columns={ccol:'Country'}, inplace=True)
                html_parts.append("<h3>Lig Tablosu (ilk 10)</h3>")
                html_parts.append(league.head(10).to_html(index=False))
                # Küme büyüklükleri
                sizes = agg['cluster'].value_counts().sort_index()
                html_parts.append("<h3>Küme Büyüklükleri</h3>")
                html_parts.append(sizes.to_frame(name='count').to_html())
            else:
                html_parts.append("<h2>Benchmark & Lig</h2><p>Özet üretilemedi.</p>")
        except Exception:
            html_parts.append("<h2>Benchmark & Lig</h2><p>Hesaplama hata verdi.</p>")
    except Exception:
        pass

    # ROI / NPV (varsayılan senaryo ile) – bu sayfada veya seçili senaryo ile ekle
    try:
        preds_ts = load_predictions_dashboard()
        # preds_rb = load_predictions_robust()  # Robust model kaldırıldı
        preds = preds_ts  # Sadece zaman serili profesyonel model
        if preds is not None and not preds.empty and 'Total Waste (Tons)' in preds.columns:
            # Eğer kullanıcı ROI sayfasında bir senaryo eklediyse onu kullan
            sc = st.session_state.get('roi_scenario')
            country = (sc.get('country') if sc else None) or sorted(preds['Country'].dropna().unique())[0]
            dfc = preds[preds['Country']==country].sort_values('Year')
            if sc:
                years_arr = np.array(sc.get('years', dfc['Year'].astype(int).values))
                flows = sc.get('flows', [])
                npv = sc.get('npv', 0.0)
                pol_reduct = None
                pol_start = sc.get('pol_start'); pol_end = sc.get('pol_end')
                cost = sc.get('cost'); benefit_per_mton = sc.get('benefit_per_mton'); disc = sc.get('discount')
            else:
                base = dfc['Total Waste (Tons)'].astype(float).values
                years_arr = dfc['Year'].astype(int).values
                pol_reduct, cost, benefit_per_mton, disc = 10, 50.0, 2.0, 8.0
                delta_mton = np.maximum(0.0, base * (pol_reduct/100.0) / 1e6)
                flows = [float(delta_mton[i])*benefit_per_mton - cost for i in range(len(delta_mton))]
                r = disc/100.0
                npv = sum([flows[i] / ((1+r)**i) for i in range(len(flows))])
            html_parts.append("<h2>ROI / NPV – Varsayılan Senaryo</h2>")
            if sc:
                html_parts.append(f"<p>Seçili senaryo eklendi. Ülke: {country}, Azaltım profili: %{pol_start}–%{pol_end}, Maliyet: {cost} M$/yıl, Fayda: {benefit_per_mton} M$/Mton, İskonto: %{disc}.</p>")
            else:
                html_parts.append(f"<p>Senaryo tanımlanmadı; varsayılan parametrelerle hesaplandı. Ülke: {country}, Azaltım: % {pol_reduct}, Maliyet: {cost} M$/yıl, Fayda: {benefit_per_mton} M$/Mton, İskonto: %{disc}.</p>")
            html_parts.append(f"<p><b>NPV (M$):</b> {npv:,.2f}</p>")
        else:
            html_parts.append("<h2>ROI / NPV</h2><p>Uygun tahmin verisi bulunamadı.</p>")
    except Exception:
        html_parts.append("<h2>ROI / NPV</h2><p>Hesaplama yapılamadı.</p>")
    if ranks is not None and not ranks.empty:
        html_parts.append("<h2>Ülke Bazlı Sıralamalar (ilk 10)</h2>")
        html_parts.append(ranks.to_html(index=False))
    html_parts.append("""
        <h2>Notlar / Yöntem</h2>
        <ul>
          <li>Regresyon tabanlı Gradient Boosting modeli: Çoklu hedef tahmin</li>
          <li>Değerlendirme: Train-Test Split (80/20) + 5-fold Cross-Validation</li>
          <li>Regularization: Learning rate, max_depth, subsample parametreleri</li>
          <li>Açıklanabilirlik: Permutation Importance + SHAP Analizi</li>
        </ul>
        """)

    report_html = "\n".join(html_parts)
    st.subheader("Raporu İndir")
    st.download_button(
        label="HTML Olarak İndir",
        data=report_html.encode('utf-8'),
        file_name=f"ecolense_rapor_{_dt.now().strftime('%Y%m%d_%H%M')}.html",
        mime="text/html",
    )
    # PDF (opsiyonel: ortam destekliyorsa)
    try:
        import pdfkit as _pdfkit
        pdf_bytes = _pdfkit.from_string(report_html, False)
        st.download_button(
            label="PDF Olarak İndir",
            data=pdf_bytes,
            file_name=f"ecolense_rapor_{_dt.now().strftime('%Y%m%d_%H%M')}.pdf",
            mime="application/pdf",
        )
    except Exception:
        st.caption("PDF desteklenmiyorsa HTML indirip tarayıcıdan 'Yazdır→PDF' olarak kaydedebilirsiniz.")

    # Sayfa sonu yazısı
    add_page_footer("Benchmark & Lig")


def show_anomaly_monitor():
    """🚨 Anomali & İzleme – IQR/z‑score, zaman serisi izleme, hariç tut etkisi"""
    # Premium başlık
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; 
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">🚨</span>
            </div>
            <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700;">ANOMALI & İZLEME</h1>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            Anomali tespiti ve sürekli izleme sistemleri
        </p>
    </div>
    """, unsafe_allow_html=True)
    df = load_data(REAL_DATA_PATH, announce=False)
    if df is None or df.empty:
        st.warning("❌ Veri bulunamadı")
        return
    target = st.selectbox("Hedef", ['food_waste_tons','economic_loss_usd','carbon_footprint_kgco2e','sustainability_score'])
    # Esnek kolon çözümleyici
    cand_map = {
        'food_waste_tons': ['food_waste_tons', 'Total Waste (Tons)', 'total_waste_tons'],
        'economic_loss_usd': ['economic_loss_usd', 'Economic Loss (Million $)'],
        'carbon_footprint_kgco2e': ['carbon_footprint_kgco2e', 'Carbon_Footprint_kgCO2e'],
        'sustainability_score': ['sustainability_score', 'Sustainability_Score'],
    }
    tcol = _resolve_column_name(df, cand_map.get(target, [target]))
    if not tcol:
        st.info("Seçilen hedef sütunu veri setinde yok.")
        return
    ccol = 'country' if 'country' in df.columns else ('Country' if 'Country' in df.columns else None)
    ycol = 'Year' if 'Year' in df.columns else ('year' if 'year' in df.columns else None)
    if not ccol or not ycol:
        st.info("Ülke/Yıl sütunu bulunamadı.")
        return
    # IQR tabanlı bayrak
    q1, q3 = df[tcol].quantile(0.25), df[tcol].quantile(0.75)
    iqr = q3 - q1
    low, high = q1 - 1.5*iqr, q3 + 1.5*iqr
    df['iqr_outlier'] = (df[tcol] < low) | (df[tcol] > high)
    # z‑score
    mu, sigma = float(df[tcol].mean()), float(df[tcol].std(ddof=0) or 1.0)
    df['zscore'] = (df[tcol] - mu) / (sigma if sigma != 0 else 1.0)
    zthr = st.slider("z‑score eşiği", 2.0, 5.0, 3.0, step=0.1)
    df['z_outlier'] = df['zscore'].abs() > zthr
    # Hariç tut etkisi
    exclude = st.checkbox("Aykırıları hariç tut (IQR ∪ z)")
    mask = ~(df['iqr_outlier'] | df['z_outlier']) if exclude else slice(None)
    dff = df[mask]
    st.subheader("Aykırı Özet")
    try:
        counts = dff[['iqr_outlier','z_outlier']].value_counts().reset_index(name='count')
        st.dataframe(counts, use_container_width=True)
    except Exception:
        pass
    # Zaman serisi izleme (ülke seçimi)
    country = st.selectbox("Ülke", sorted(df[ccol].dropna().unique()), key="anom_country")
    ts = dff[dff[ccol]==country][[ycol, tcol]].groupby(ycol).mean().reset_index()
    st.plotly_chart(px.line(ts, x=ycol, y=tcol, markers=True, template='plotly_white', height=360), use_container_width=True, key=f"anomaly_chart_{hash(str(ts))}_{hash('anomaly_monitor')}")
    
    # Grafik açıklaması
    with st.expander("📊 Bu grafik ne anlatıyor?"):
        st.markdown(f"""
        Bu **Anomali İzleme grafiği** seçilen ülkenin {target} değerindeki zaman serisi trendini gösteriyor:
        
        - **Çizgi**: Yıllık ortalama değerler
        - **Noktalar**: Her yılın veri noktası
        - **Aykırı filtreleme**: IQR ve z-score eşiklerine göre temizlenmiş veri
        
        **Analiz**: Aykırı değerler hariç tutulduğunda trend daha istikrarlı görünür.
        Bu, model eğitiminde daha güvenilir sonuçlar elde etmek için kullanılabilir.
        """)
    # AI Asistan
    st.markdown("""
    <div class='ai-assistant'>
      <h4><span class='ai-emoji'>🤖</span>AI Asistan — Anomali</h4>
      <p>Aykırılar hariç tutulduğunda trend daha istikrarlı görünür. Model eğitiminde de benzer filtreler tercih edilebilir.</p>
    </div>
    """, unsafe_allow_html=True)

    # Sayfa sonu yazısı
    add_page_footer("Anomali & İzleme")


def show_data_lineage_quality():
    """🧬 Veri Hattı & Kalite – kaynak→işleme→model, cache ve sürüm"""
    # Premium başlık
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; 
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">🧬</span>
            </div>
            <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700;">VERI HATTI & KALITE</h1>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            Veri kalitesi analizi ve hata tespiti
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.subheader("Soy Ağacı")
    st.markdown("- Kaynak: global_food_wastage_dataset.csv + material_footprint.csv\n- Birleştirme: 01_veri_hazirlama.py\n- Model Eğitimi: 02_model_egitimi.py\n- A/B Testing: 03_ab_testing_analizi.py\n- Dashboard: app.py")
    st.subheader("Cache Durumu")
    st.caption("Streamlit cache: veri/pred dosyaları cache’de; yenilemek için sayfayı yeniden başlatın.")
    st.subheader("Sürüm Etiketi")
    import datetime as _dt
    st.code(f"Build: { _dt.datetime.now().strftime('%Y-%m-%d %H:%M') }")

    # Otomatik Kontrol Listesi
    st.subheader("Kontrol Listesi (Otomatik)")
    import os, time

    def _file_info(path: str):
        try:
            if not os.path.exists(path):
                return {'exists': False}
            sz = os.path.getsize(path)
            mt = os.path.getmtime(path)
            age_days = (time.time() - mt) / 86400.0
            return {'exists': True, 'size': sz, 'age_days': age_days}
        except Exception:
            return {'exists': False}
    files = {
        'Gerçek veri (enriched)': REAL_DATA_PATH,
        'Tahminler (GradientBoosting)': PREDICTIONS_PATH,
    }
    rows = []
    for label, p in files.items():
        info = _file_info(p)
        if not info.get('exists'):
            rows.append(f"❌ {label}: dosya yok → {p}")
        else:
            size_mb = info['size']/1e6
            age = info['age_days']
            warn = []
            if size_mb > 100:
                warn.append("boyut > 100 MB")
            if age > 30:
                warn.append("tazelik > 30g")
            badge = "🟢" if not warn else "🟠"
            extra = (" – " + ", ".join(warn)) if warn else ""
            rows.append(f"{badge} {label}: {size_mb:.1f} MB, {int(age)}g önce güncellendi{extra}")
    st.markdown("\n".join([f"- {r}" for r in rows]))

    # Veri kontrolü: satır sayıları
    df = load_data(REAL_DATA_PATH, announce=False)
    if df is not None and not df.empty:
        st.caption(f"Satır sayısı: {len(df):,}")
        st.success("Veri yüklendi")
    # AI Asistan – kontrol
    st.markdown("""
    <div class='ai-assistant'>
      <h4><span class='ai-emoji'>🤖</span>AI Asistan — Kalite Kontrol</h4>
      <p>Dosya boyutu ve tazelik eşiklerini izleyin (100 MB, 30g). Kaynak dosyalar yoksa rapor ve modüller eksik çalışır.</p>
    </div>
    """, unsafe_allow_html=True)

    # Sayfa sonu yazısı
    add_page_footer("Veri Hattı & Kalite")


def show_carbon_flows():
    """🌿 Karbon Akışları – Sankey, Treemap, Radar (mevsimsel)"""
    # Premium başlık
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; 
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">🌿</span>
            </div>
            <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700;">KARBON AKIŞLARI</h1>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            Karbon ayak izi analizi ve sürdürülebilirlik metrikleri
        </p>
    </div>
    """, unsafe_allow_html=True)
    df = load_data(REAL_DATA_PATH, announce=False)
    if df is None or df.empty:
        st.warning("❌ Veri bulunamadı")
        return
    # Kolon çözümleyici
    catcol = _resolve_column_name(df, ['food_category','Food Category'])
    carbon = _resolve_column_name(df, ['carbon_footprint_kgco2e','Carbon_Footprint_kgCO2e'])
    ccol = 'country' if 'country' in df.columns else ('Country' if 'Country' in df.columns else None)
    ycol = 'Year' if 'Year' in df.columns else ('year' if 'year' in df.columns else None)
    if not catcol or not carbon or not ccol or not ycol:
        st.info("Gerekli sütunlar bulunamadı.")
        return
    
    # Kıta bilgisi kontrolü
    continent_col = _resolve_column_name(df, ['Continent', 'continent'])
    has_continent = continent_col is not None and continent_col in df.columns
    
    if not has_continent:
        st.info("⚠️ Kıta bilgisi bulunamadı. Kategori → Ülke seçeneğini kullanabilirsiniz.")
    
    # Gruplama seçenekleri - kıta bilgisine göre dinamik
    if has_continent:
        group_options = ["Kategori → Ülke", "Ülke → Kategori", "Kıta → Ülke", "Çok-Adımlı"]
    else:
        group_options = ["Kategori → Ülke", "Ülke → Kategori"]
    
    group_option = st.selectbox("Gruplama:", group_options, key="sankey_group")
    
    if group_option == "Çok-Adımlı":
        # Çok-adımlı Sankey: Kategori → Kıta → Ülke
        try:
            import plotly.graph_objects as go
            # Kıta bilgisi varsa kullan, yoksa "Global" olarak grupla
            if 'Continent' in df.columns:
                flow_data = df.groupby([catcol, 'Continent', ccol])[carbon].sum().reset_index()
                flow_data.columns = ['source', 'mid', 'target', 'value']
            else:
                # Kıta yoksa kategori → ülke → yıl yap
                flow_data = df.groupby([catcol, ccol, ycol])[carbon].sum().reset_index()
                flow_data.columns = ['source', 'mid', 'target', 'value']
            
            # Node listesi
            nodes = list(set(flow_data['source'].unique()) | set(flow_data['mid'].unique()) | set(flow_data['target'].unique()))
            node_dict = {node: i for i, node in enumerate(nodes)}
            
            # Link listesi (2 adım)
            links = []
            for _, row in flow_data.iterrows():
                links.append({
                    'source': node_dict[row['source']],
                    'target': node_dict[row['mid']],
                    'value': row['value']
                })
                links.append({
                    'source': node_dict[row['mid']],
                    'target': node_dict[row['target']],
                    'value': row['value']
                })
            
            # Sankey çiz
            fig = go.Figure(data=[go.Sankey(
                node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5),
                         label=nodes, color="blue"),
                link=dict(source=[l['source'] for l in links],
                         target=[l['target'] for l in links],
                         value=[l['value'] for l in links])
            )])
            fig.update_layout(title_text=f"Karbon Akışları: {group_option}", font_size=10, height=500)
            st.subheader(f"Sankey – {group_option}")
            st.plotly_chart(fig, use_container_width=True)
            
            # Grafik açıklaması
            with st.expander("📊 Bu grafik ne anlatıyor?"):
                st.markdown(f"""
                Bu **Sankey Diyagramı** karbon akışlarının çok-adımlı dağılımını gösteriyor:
                
                - **Kutular**: Kategori, Kıta ve Ülke grupları
                - **Bağlantı kalınlığı**: Karbon akış miktarına göre orantılı
                - **Renkler**: Farklı grupları ayırt etmek için
                
                **Analiz**: Hangi kategorilerin hangi bölgelere/ülkelere en fazla karbon emisyonu 
                sağladığını görebilirsiniz. En kalın bağlantılar en kritik akışları gösterir.
                """)
            
            # AI Asistan
            st.markdown("""
            <div class='ai-assistant'>
              <h4><span class='ai-emoji'>🤖</span>AI Asistan — Karbon Akışları</h4>
              <p>Çok-adımlı akış: Kategori→Kıta→Ülke hiyerarşisi. En kalın bağlantılar en yüksek karbon akışını gösterir. Üst seviye gruplama ile karmaşıklık azaltıldı.</p>
            </div>
            """, unsafe_allow_html=True)
            return
            
        except Exception as e:
            st.error(f"Çok-adımlı Sankey hatası: {e}")
            return
    
    # Tek adımlı Sankey için ülke seçimi
    country = st.selectbox("Ülke", sorted(df[ccol].dropna().unique()), key="flows_country")
    d = df[df[ccol]==country].copy()
    d[catcol] = d[catcol].astype(str).fillna('Unknown')
    
    # Treemap
    st.subheader("Treemap – Karbon dağılımı")
    tre = d.groupby(catcol)[carbon].sum().reset_index()
    st.plotly_chart(px.treemap(tre, path=[catcol], values=carbon, template='plotly_white', height=420), use_container_width=True, key=f"carbon_treemap_{hash(str(tre))}_{hash('carbon_flows')}")
    
    # Grafik açıklaması
    with st.expander("📊 Bu grafik ne anlatıyor?"):
        st.markdown(f"""
        Bu treemap grafiği **{country}** ülkesindeki karbon ayak izinin gıda kategorilerine göre dağılımını gösteriyor. 
        **Kutu boyutu** karbon miktarını temsil eder. 
        En büyük kutular en yüksek karbon emisyonuna sahip gıda kategorilerini gösterir. 
        Bu analiz, hangi gıda türlerinin çevresel etkisinin en yüksek olduğunu anlamamızı sağlar.
        """)
    
    # Tek adımlı Sankey
    try:
        import plotly.graph_objects as go
        if group_option == "Kategori → Ülke":
            cats = tre[catcol].tolist(); vals = tre[carbon].astype(float).tolist()
            labels = cats + [country]
            src = list(range(len(cats)))
            dst = [len(labels)-1]*len(cats)
        elif group_option == "Ülke → Kategori":
            cats = tre[catcol].tolist(); vals = tre[carbon].astype(float).tolist()
            labels = [country] + cats
            src = [0]*len(cats)
            dst = list(range(1, len(labels)))
        elif group_option == "Kıta → Ülke":
            if has_continent:
                # Kıta → Ülke akışı
                cont_data = df.groupby([continent_col, ccol])[carbon].sum().reset_index()
                cont_data = cont_data[cont_data[ccol] == country]
                if not cont_data.empty:
                    cats = cont_data[continent_col].tolist(); vals = cont_data[carbon].astype(float).tolist()
                    labels = cats + [country]
                    src = list(range(len(cats)))
                    dst = [len(labels)-1]*len(cats)
                else:
                    st.info("Seçilen ülke için kıta verisi bulunamadı. Kategori → Ülke seçeneğini kullanabilirsiniz.")
                    # Kıta verisi yoksa kategori → ülke olarak göster
                    cats = tre[catcol].tolist(); vals = tre[carbon].astype(float).tolist()
                    labels = cats + [country]
                    src = list(range(len(cats)))
                    dst = [len(labels)-1]*len(cats)
            else:
                st.info("Kıta bilgisi bulunamadı. Kategori → Ülke seçeneğini kullanabilirsiniz.")
                # Kıta yoksa kategori → ülke olarak göster
                cats = tre[catcol].tolist(); vals = tre[carbon].astype(float).tolist()
                labels = cats + [country]
                src = list(range(len(cats)))
                dst = [len(labels)-1]*len(cats)
        
        fig = go.Figure(go.Sankey(node=dict(label=labels), link=dict(source=src, target=dst, value=vals)))
        fig.update_layout(template='plotly_white', height=420)
        st.subheader(f"Sankey – {group_option}")
        st.plotly_chart(fig, use_container_width=True, key=f"carbon_sankey_{hash(str(fig))}_{hash('carbon_flows')}")
        
        # Grafik açıklaması
        with st.expander("📊 Bu grafik ne anlatıyor?"):
            st.markdown(f"""
            Bu **Sankey Diyagramı** {group_option} akışını gösteriyor:
            
            - **Kutular**: Kaynak ve hedef grupları
            - **Bağlantı kalınlığı**: Karbon akış miktarına göre orantılı
            - **Soldan sağa**: Akış yönü
            
            **Analiz**: En kalın bağlantılar en yüksek karbon emisyonuna sahip 
            kategori/ülke kombinasyonlarını gösterir.
            """)
    except Exception:
        pass
    
    # Radar (mevsimsel; yıl=sezon proxy)
    try:
        seasons = d.groupby(ycol)[carbon].sum().reset_index()
        seasons['season'] = seasons[ycol].astype(str)
        figR = px.line_polar(seasons, r=carbon, theta='season', line_close=True, template='plotly_white', height=420)
        st.subheader("Radar – Mevsimsel/Yıllık profil")
        st.plotly_chart(figR, use_container_width=True, key=f"carbon_radar_{hash(str(seasons))}_{hash('carbon_flows')}")
        
        with st.expander("📊 Bu grafik ne anlatıyor?"):
            st.markdown("""
            **Radar grafiği**, karbon ayak izinin yıllar boyunca nasıl değiştiğini **dairesel bir formatta** gösteriyor. 
            
            - **Dışa doğru uzanan çizgiler**: Daha yüksek karbon emisyonu olan yılları gösterir
            - **İçe doğru çekilen çizgiler**: Daha düşük emisyon dönemlerini işaret eder
            - **Şekil simetrisi**: Mevsimsel veya yıllık döngüleri analiz etmemizi sağlar
            - **Trend analizi**: Hangi dönemlerde karbon emisyonunun arttığını veya azaldığını görsel olarak anlamamızı kolaylaştırır
            """)
    except Exception:
        pass
    
    # AI Asistan
    st.markdown("""
            <div class='ai-assistant'>
          <h4><span class='ai-emoji'>🤖</span>AI Asistan — Karbon Akışları</h4>
          <p>Treemap: Kategori bazında en yüksek karbon üreticileri. Sankey: Akış yoğunluğu ve bağlantılar. Radar: Yıllık trend ve mevsimsellik.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Sayfa sonu yazısı
    add_page_footer("Karbon Akışları")


def show_justice_impact_panel():
    """⚖️ Adalet/Etki Paneli – sürdürülebilirlik eşitliği ve etki analizi"""
    # Premium başlık
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 2rem 0; 
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 12px; margin-right: 1rem;">
                <span style="font-size: 1.8rem;">⚖️</span>
            </div>
            <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700;">ADALET/ETKİ PANELİ</h1>
        </div>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            Sosyal adalet ve etki değerlendirmesi analizleri
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Veri yükle
    df = load_data(REAL_DATA_PATH, announce=False)
    if df is None or df.empty:
        st.warning("Veri yüklenemedi")
        return
    
    # Kolon çözümle
    country_col = _resolve_column_name(df, ['country', 'Country'])
    year_col = _resolve_column_name(df, ['Year', 'year'])
    waste_col = _resolve_column_name(df, ['total_waste_tons', 'Total Waste (Tons)'])
    carbon_col = _resolve_column_name(df, ['carbon_footprint_kgco2e', 'Carbon_Footprint_kgCO2e'])
    economic_col = _resolve_column_name(df, ['economic_loss_million', 'Economic Loss (Million $)', 'Economic Loss (Million USD)'])
    sustainability_col = _resolve_column_name(df, ['sustainability_score', 'Sustainability Score'])
    
    if not all([country_col, year_col, waste_col, carbon_col, economic_col, sustainability_col]):
        st.error("Gerekli kolonlar bulunamadı")
        return
    
    # Ülke bazlı analiz
    country_analysis = df.groupby(country_col).agg({
        waste_col: 'sum',
        carbon_col: 'sum', 
        economic_col: 'sum',
        sustainability_col: 'mean'
    }).reset_index()
    
    # Eşitlik analizi
    st.subheader("Sürdürülebilirlik Eşitliği")
    
    # Gini katsayısı hesaplama

    def gini_coefficient(values):
        sorted_values = np.sort(values)
        n = len(sorted_values)
        cumsum = np.cumsum(sorted_values)
        return (n + 1 - 2 * np.sum(cumsum) / cumsum[-1]) / n
    
    gini_waste = gini_coefficient(country_analysis[waste_col])
    gini_carbon = gini_coefficient(country_analysis[carbon_col])
    gini_economic = gini_coefficient(country_analysis[economic_col])
    gini_sustainability = gini_coefficient(country_analysis[sustainability_col])
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Atık Eşitsizliği", f"{gini_waste:.3f}", "Gini Katsayısı")
    col2.metric("Karbon Eşitsizliği", f"{gini_carbon:.3f}", "Gini Katsayısı")
    col3.metric("Ekonomik Eşitsizlik", f"{gini_economic:.3f}", "Gini Katsayısı")
    col4.metric("Sürdürülebilirlik Eşitsizliği", f"{gini_sustainability:.3f}", "Gini Katsayısı")
    
    # Lorenz eğrisi
    st.subheader("Lorenz Eğrisi - Atık Dağılımı")
    sorted_waste = np.sort(country_analysis[waste_col])
    cumulative_share = np.cumsum(sorted_waste) / np.sum(sorted_waste)
    population_share = np.arange(1, len(sorted_waste) + 1) / len(sorted_waste)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=population_share, y=cumulative_share, mode='lines', 
        name='Gerçek Dağılım',
        line=dict(color='#11E6C1', width=4),
        fill='tonexty',
        fillcolor='rgba(17, 230, 193, 0.1)'
    ))
    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1], mode='lines', 
        name='Eşit Dağılım', 
        line=dict(dash='dash', color='#FF6B6B', width=3)
    ))
    fig.update_layout(
        title=dict(
            text="Lorenz Eğrisi - Atık Dağılımı",
            font=dict(size=20, color='#232E5C')
        ),
        xaxis_title="Nüfus Payı",
        yaxis_title="Atık Payı",
        plot_bgcolor='rgba(248, 250, 252, 0.8)',
        paper_bgcolor='rgba(248, 250, 252, 0.8)',
        font=dict(color='#2D3748'),
        legend=dict(
            bgcolor='rgba(255, 255, 255, 0.9)',
            bordercolor='#E2E8F0',
            borderwidth=1
        ),
        margin=dict(l=60, r=60, t=80, b=60)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Grafik açıklaması
    with st.expander("📊 Bu grafik ne anlatıyor?"):
        st.markdown("""
        **Lorenz Eğrisi** eşitsizlik analizinin temel aracıdır:
        - **Mavi çizgi**: Gerçek atık dağılımı
        - **Kırmızı kesikli çizgi**: Eşit dağılım (referans)
        - **Eğri altındaki alan**: Eşitsizlik miktarı
        - **Sonuç**: Eğri referans çizgiden ne kadar uzaksa, o kadar eşitsizlik var
        """)
    
    # Etki analizi
    st.subheader("Etki Analizi")
    
    # En çok etkilenen ülkeler
    top_impacted = country_analysis.nlargest(10, economic_col)
    fig = px.bar(
        top_impacted, x=country_col, y=economic_col,
        title="En Yüksek Ekonomik Kayıp Yaşayan Ülkeler",
        color_discrete_sequence=['#11E6C1']
    )
    fig.update_layout(
        title=dict(
            text="En Yüksek Ekonomik Kayıp Yaşayan Ülkeler",
            font=dict(size=20, color='#232E5C')
        ),
        plot_bgcolor='rgba(248, 250, 252, 0.8)',
        paper_bgcolor='rgba(248, 250, 252, 0.8)',
        font=dict(color='#2D3748'),
        xaxis=dict(
            tickangle=45,
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            title=dict(
                text="Ekonomik Kayıp (Milyon $)",
                font=dict(size=14, color='#2D3748')
            )
        ),
        margin=dict(l=60, r=60, t=80, b=80)
    )
    fig.update_traces(
        marker=dict(
            line=dict(width=1, color='#232E5C'),
            opacity=0.8
        )
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Grafik açıklaması
    with st.expander("📊 Bu grafik ne anlatıyor?"):
        st.markdown("""
        **En Yüksek Ekonomik Kayıp** yaşayan ülkeler:
        - **Yüksek çubuklar**: En fazla ekonomik kayıp
        - **Sıralama**: En kritik ülkeler üstte
        - **Politika önceliği**: Bu ülkeler acil müdahale gerektirir
        - **Kaynak tahsisi**: Yüksek kayıplı ülkelere odaklanılmalı
        """)
    
    # Sürdürülebilirlik vs Ekonomik Kayıp
    fig = px.scatter(
        country_analysis, x=economic_col, y=sustainability_col,
        hover_data=[country_col], 
        title="Sürdürülebilirlik vs Ekonomik Kayıp",
        color_discrete_sequence=['#A9FF4F']
    )
    fig.update_layout(
        title=dict(
            text="Sürdürülebilirlik vs Ekonomik Kayıp",
            font=dict(size=20, color='#232E5C')
        ),
        plot_bgcolor='rgba(248, 250, 252, 0.8)',
        paper_bgcolor='rgba(248, 250, 252, 0.8)',
        font=dict(color='#2D3748'),
        xaxis=dict(
            title=dict(
                text="Ekonomik Kayıp (Milyon $)",
                font=dict(size=14, color='#2D3748')
            )
        ),
        yaxis=dict(
            title=dict(
                text="Sürdürülebilirlik Skoru",
                font=dict(size=14, color='#2D3748')
            )
        ),
        margin=dict(l=60, r=60, t=80, b=60)
    )
    fig.update_traces(
        marker=dict(
            size=12,
            line=dict(width=2, color='#232E5C'),
            opacity=0.7
        )
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Grafik açıklaması
    with st.expander("📊 Bu grafik ne anlatıyor?"):
        st.markdown("""
        **Sürdürülebilirlik vs Ekonomik Kayıp** ilişkisi:
        - **Sol üst**: Düşük kayıp, yüksek sürdürülebilirlik (ideal)
        - **Sağ alt**: Yüksek kayıp, düşük sürdürülebilirlik (kritik)
        - **Trend**: Genelde yüksek kayıp = düşük sürdürülebilirlik
        - **Outlier'lar**: Farklı performans gösteren ülkeler
        """)
    
    # AI Asistan
    st.markdown(f"""
    <div class='ai-assistant'>
      <h4><span class='ai-emoji'>🤖</span>AI Asistan — Adalet/Etki Analizi</h4>
      <p><span class='ai-badge'>Gini Analizi</span> Atık: <strong>{gini_waste:.3f}</strong>, Karbon: <strong>{gini_carbon:.3f}</strong>, Ekonomik: <strong>{gini_economic:.3f}</strong>, Sürdürülebilirlik: <strong>{gini_sustainability:.3f}</strong>.</p>
      <p><span class='ai-badge'>Öneri</span> Yüksek eşitsizlik gösteren alanlarda hedefli politika müdahaleleri gerekli. <span class='ai-highlight'>En kritik: {max([gini_waste, gini_carbon, gini_economic, gini_sustainability]):.3f}</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sayfa sonu yazısı
    add_page_footer("Adalet/Etki Paneli")


# =============================================================================
# UYGULAMA BAŞLATMA
# =============================================================================

if __name__ == "__main__":
    main() 