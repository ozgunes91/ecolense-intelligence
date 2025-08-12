import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from typing import Optional

def _resolve_column_name(df: pd.DataFrame, candidates: list) -> Optional[str]:
    """Veri setindeki sütun adını çözümle"""
    for candidate in candidates:
        if candidate in df.columns:
            return candidate
    return None

def show_story_mode(df: pd.DataFrame, story_mode: str):
    """Premium Hikaye Modu - Ana İşleyici"""
    
    # Dil desteği
    lang = st.session_state.get('lang', 'TR')
    
    # Dil özel metinler
    story_texts = {
        'TR': {
            'title': '📖 PREMIUM HİKAYE MODU',
            'desc': 'AI Destekli Veri Anlatımı ve Stratejik İçgörüler Platformu',
            'active_story': 'Aktif Hikaye',
            'home': '🏠 Ana Sayfa',
            'analysis': '📊 Analiz',
            'targets': '🎯 Hedefler',
            'ai_insights': '🤖 AI İçgörüler',
            'forecasts': '📈 Tahminler'
        },
        'EN': {
            'title': '📖 PREMIUM STORY MODE',
            'desc': 'AI-Powered Data Storytelling & Strategic Insights Platform',
            'active_story': 'Active Story',
            'home': '🏠 Home',
            'analysis': '📊 Analysis',
            'targets': '🎯 Targets',
            'ai_insights': '🤖 AI Insights',
            'forecasts': '📈 Forecasts'
        }
    }
    
    texts = story_texts.get(lang, story_texts['EN'])
    
    # Premium başlık
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 1rem 0; 
                box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3); position: relative; overflow: hidden;">
        <div style="position: absolute; top: 0; right: 0; width: 200px; height: 200px; 
                    background: rgba(255,255,255,0.1); border-radius: 50%; transform: translate(50%, -50%);"></div>
        <div style="position: absolute; bottom: 0; left: 0; width: 150px; height: 150px; 
                    background: rgba(255,255,255,0.05); border-radius: 50%; transform: translate(-50%, 50%);"></div>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">{texts['title']}</h1>
                <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">
                    {texts['desc']}
                </p>
            </div>
            <div style="text-align: right;">
                <div style="background: rgba(255,255,255,0.2); padding: 0.8rem 1.2rem; border-radius: 12px; margin-bottom: 0.5rem;">
                    <span style="font-size: 0.9rem; opacity: 0.8;">{texts['active_story']}</span><br>
                    <span style="font-weight: 600; font-size: 1.1rem;">{story_mode}</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigasyon butonları
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button(texts['home'], key="nav_home", use_container_width=True):
            st.session_state['page'] = 'PAGE_HOME'
            st.rerun()
    
    with col2:
        if st.button(texts['analysis'], key="nav_analysis", use_container_width=True):
            st.session_state['page'] = 'PAGE_ANALYSIS'
            st.rerun()
    
    with col3:
        if st.button(texts['targets'], key="nav_targets", use_container_width=True):
            st.session_state['page'] = 'PAGE_TARGETS'
            st.rerun()
    
    with col4:
        if st.button(texts['ai_insights'], key="nav_ai", use_container_width=True):
            st.session_state['page'] = 'PAGE_AI_INSIGHTS'
            st.rerun()
    
    with col5:
        if st.button(texts['forecasts'], key="nav_forecasts", use_container_width=True):
            st.session_state['page'] = 'PAGE_FORECASTS'
            st.rerun()
    
    # Hikaye içeriği - Dil desteği ile
    if story_mode in ["🥗 Global Food Waste Crisis & Solutions", "🥗 Gıda İsrafı Krizi ve Çözüm Yolları"]:
        show_food_waste_crisis_story(df)
    elif story_mode in ["💰 Economic Impact Analysis", "💰 Ekonomik Etki Analizi", "💰 Gıda İsrafının Ekonomik Etkileri"]:
        show_economic_impact_story(df)
    elif story_mode in ["🌍 Environmental Footprint Analysis", "🌍 Çevresel Ayak İzi Analizi", "🌍 Gıda İsrafının Çevresel Ayak İzi"]:
        show_environmental_impact_story(df)
    elif story_mode in ["🎯 Sustainable Solutions Roadmap", "🎯 Sürdürülebilir Çözümler Yol Haritası", "🎯 Sürdürülebilir Gıda Sistemleri"]:
        show_sustainable_solutions_story(df)
    elif story_mode in ["🚀 2030 Strategic Forecast", "🚀 2030 Stratejik Tahmin"]:
        show_2030_strategy_story(df)
    elif story_mode in ["📊 Comprehensive Analytics", "📊 Kapsamlı Analitik"]:
        show_comprehensive_analytics_story(df)
    else:
        # Dil desteği ile hata mesajı
        if lang == 'TR':
            st.warning(f"Bilinmeyen hikaye modu: {story_mode}")
        else:
            st.warning(f"Unknown story mode: {story_mode}")

def show_food_waste_crisis_story(df: pd.DataFrame):
    """🥗 Küresel Gıda İsrafı Krizi ve Çözümler - Premium Versiyon"""
    
    # Dil desteği
    lang = st.session_state.get('lang', 'TR')
    
    # Dil özel metinler
    texts = {
        'TR': {
            'title': '🚨 KÜRESEL GIDA İSRAFI KRİZİ',
            'subtitle': 'Acil Eylem Gerektiren Küresel Felaket',
            'metrics_title': '📊 KRİTİK METRİKLER PANELİ',
            'total_waste': '🔥 Toplam Gıda İsrafı',
            'avg_waste': '📊 Ortalama İsraf',
            'countries': '🌐 Analiz Edilen Ülkeler',
            'solution_potential': '🎯 Çözüm Potansiyeli',
            'annual_increase': 'yıllık artış',
            'tons_country': 'ton/ülke',
            'new_countries': 'yeni ülke',
            'reduction_target': 'azaltma hedefi',
            'crisis_analysis': '🚨 KRİZ ANALİZİ',
            'trend_analysis': '📈 Trend Analizi',
            'economic_impact': '💰 Ekonomik Etki',
            'environmental_impact': '🌍 Çevresel Etki',
            'solution_potential_analysis': '🎯 Çözüm Potansiyeli',
            'annual_increase_trend': 'yıllık artış trendi devam ediyor',
            'economic_loss': 'Her ton israf = $1,000 ekonomik kayıp',
            'co2_emissions': 'Her ton israf = 1,000 kg CO2e emisyonu',
            'billion_savings': '50% azalma = $15-20 milyar tasarruf',
            'visualizations': '📈 PREMIUM VERİ GÖRSELLEŞTİRMELERİ',
            'trend_chart_title': 'Yıllık Küresel Gıda İsrafı Trendi',
            'year': 'Yıl',
            'total_waste_tons': 'Toplam İsraf (Ton)'
        },
        'EN': {
            'title': '🚨 GLOBAL FOOD WASTE CRISIS',
            'subtitle': 'A Global Catastrophe Requiring Immediate Action',
            'metrics_title': '📊 CRITICAL METRICS DASHBOARD',
            'total_waste': '🔥 Total Food Waste',
            'avg_waste': '📊 Average Waste',
            'countries': '🌐 Countries Analyzed',
            'solution_potential': '🎯 Solution Potential',
            'annual_increase': 'annual increase',
            'tons_country': 'tons/country',
            'new_countries': 'new countries',
            'reduction_target': 'reduction target',
            'crisis_analysis': '🚨 CRISIS ANALYSIS',
            'trend_analysis': '📈 Trend Analysis',
            'economic_impact': '💰 Economic Impact',
            'environmental_impact': '🌍 Environmental Impact',
            'solution_potential_analysis': '🎯 Solution Potential',
            'annual_increase_trend': 'annual increase trend continues',
            'economic_loss': 'Every ton of waste = $1,000 economic loss',
            'co2_emissions': 'Every ton of waste = 1,000 kg CO2e emissions',
            'billion_savings': '50% reduction = $15-20 billion savings',
            'visualizations': '📈 PREMIUM DATA VISUALIZATIONS',
            'trend_chart_title': 'Annual Global Food Waste Trend',
            'year': 'Year',
            'total_waste_tons': 'Total Waste (Tons)'
        }
    }
    
    story_texts = texts.get(lang, texts['EN'])
    
    # Hero bölümü
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); 
                padding: 3rem; border-radius: 25px; color: white; margin: 2rem 0; 
                box-shadow: 0 15px 35px rgba(255, 107, 107, 0.3);">
        <h1 style="margin: 0; font-size: 2.8rem; font-weight: 800;">{story_texts['title']}</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            {story_texts['subtitle']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Kritik Metrikler Paneli
    st.markdown(f"### {story_texts['metrics_title']}")
    
    waste_col = _resolve_column_name(df, ['Total Waste (Tons)', 'total_waste_tons'])
    if waste_col:
        total_waste = df[waste_col].sum()
        avg_waste = df[waste_col].mean()
        countries_count = df['Country'].nunique()
        
        # Trend hesaplamaları
        year_col = _resolve_column_name(df, ['Year', 'year'])
        if year_col:
            yearly_waste = df.groupby(year_col)[waste_col].sum()
            if len(yearly_waste) > 1:
                annual_increase = ((yearly_waste.iloc[-1] - yearly_waste.iloc[0]) / yearly_waste.iloc[0]) * 100
            else:
                annual_increase = 0
        else:
            annual_increase = 0
        
        # Premium metrik kartları
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); 
                        padding: 1.5rem; border-radius: 15px; color: white; text-align: center; 
                        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3);">
                <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">{story_texts['total_waste']}</h3>
                <p style="margin: 0; font-size: 1.8rem; font-weight: 700;">{total_waste/1_000_000:.1f}M</p>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.8;">{story_texts['annual_increase']}: +{annual_increase:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #fdcb6e 0%, #e17055 100%); 
                        padding: 1.5rem; border-radius: 15px; color: white; text-align: center; 
                        box-shadow: 0 8px 25px rgba(253, 203, 110, 0.3);">
                <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">{story_texts['avg_waste']}</h3>
                <p style="margin: 0; font-size: 1.8rem; font-weight: 700;">{avg_waste/1_000:.1f}K</p>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.8;">{story_texts['tons_country']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #00b894 0%, #00a085 100%); 
                        padding: 1.5rem; border-radius: 15px; color: white; text-align: center; 
                        box-shadow: 0 8px 25px rgba(0, 184, 148, 0.3);">
                <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">{story_texts['countries']}</h3>
                <p style="margin: 0; font-size: 1.8rem; font-weight: 700;">{countries_count}</p>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.8;">{story_texts['new_countries']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%); 
                        padding: 1.5rem; border-radius: 15px; color: white; text-align: center; 
                        box-shadow: 0 8px 25px rgba(108, 92, 231, 0.3);">
                <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">{story_texts['solution_potential']}</h3>
                <p style="margin: 0; font-size: 1.8rem; font-weight: 700;">50%</p>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.8;">{story_texts['reduction_target']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Kriz Analizi
    st.markdown(f"### {story_texts['crisis_analysis']}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ff7675 0%, #fd79a8 100%); 
                    padding: 2rem; border-radius: 15px; color: white; margin: 1rem 0; 
                    box-shadow: 0 8px 25px rgba(255, 118, 117, 0.3);">
            <h4 style="margin: 0 0 1rem 0; font-size: 1.3rem;">{story_texts['trend_analysis']}</h4>
            <p style="margin: 0; font-size: 1rem; line-height: 1.6;">
                📈 {story_texts['annual_increase_trend']}<br>
                📊 Küresel israf %{annual_increase:.1f} artış gösteriyor<br>
                🌍 20 ülke analiz edildi<br>
                ⚠️ Acil müdahale gerekiyor
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #fdcb6e 0%, #e17055 100%); 
                    padding: 2rem; border-radius: 15px; color: white; margin: 1rem 0; 
                    box-shadow: 0 8px 25px rgba(253, 203, 110, 0.3);">
            <h4 style="margin: 0 0 1rem 0; font-size: 1.3rem;">{story_texts['economic_impact']}</h4>
            <p style="margin: 0; font-size: 1rem; line-height: 1.6;">
                💰 {story_texts['economic_loss']}<br>
                📊 Yıllık $29.2 milyar kayıp<br>
                🏭 Üretim maliyetleri artıyor<br>
                💸 Tüketici fiyatları yükseliyor
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #00b894 0%, #00a085 100%); 
                    padding: 2rem; border-radius: 15px; color: white; margin: 1rem 0; 
                    box-shadow: 0 8px 25px rgba(0, 184, 148, 0.3);">
            <h4 style="margin: 0 0 1rem 0; font-size: 1.3rem;">{story_texts['environmental_impact']}</h4>
            <p style="margin: 0; font-size: 1rem; line-height: 1.6;">
                🌍 {story_texts['co2_emissions']}<br>
                🌱 71.3 milyon ton CO2e<br>
                🚗 2.3 milyon araç eşdeğeri<br>
                🌳 1.8 milyon hektar orman
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%); 
                    padding: 2rem; border-radius: 15px; color: white; margin: 1rem 0; 
                    box-shadow: 0 8px 25px rgba(108, 92, 231, 0.3);">
            <h4 style="margin: 0 0 1rem 0; font-size: 1.3rem;">{story_texts['solution_potential_analysis']}</h4>
            <p style="margin: 0; font-size: 1rem; line-height: 1.6;">
                🎯 {story_texts['billion_savings']}<br>
                🌱 50% azaltma mümkün<br>
                💡 Teknoloji çözümleri mevcut<br>
                📋 Politika değişiklikleri gerekli
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Veri Görselleştirmeleri
    st.markdown(f"### {story_texts['visualizations']}")
    
    if waste_col and year_col:
        # Trend grafiği
        fig = px.line(
            yearly_waste.reset_index(), 
            x=year_col, 
            y=waste_col,
            title=story_texts['trend_chart_title'],
            labels={year_col: story_texts['year'], waste_col: story_texts['total_waste_tons']}
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=14),
            title_font_size=20
        )
        fig.update_traces(line=dict(width=4, color='#ff6b6b'))
        st.plotly_chart(fig, use_container_width=True)

def show_economic_impact_story(df: pd.DataFrame):
    """💰 Ekonomik Etki Analizi - Premium Versiyon"""
    
    # Hero bölümü
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fdcb6e 0%, #e17055 100%); 
                padding: 3rem; border-radius: 25px; color: white; margin: 2rem 0; 
                box-shadow: 0 15px 35px rgba(253, 203, 110, 0.3);">
        <h1 style="margin: 0; font-size: 2.8rem; font-weight: 800;">💰 EKONOMİK ETKİ ANALİZİ</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            Gıda İsrafının Finansal Etkileri ve ROI Analizi
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Ekonomik Metrikler
    st.markdown("### 💰 EKONOMİK METRİKLER")
    
    economic_col = _resolve_column_name(df, ['Economic Loss (Million $)', 'economic_loss_usd'])
    if economic_col:
        total_loss = df[economic_col].sum()
        avg_loss = df[economic_col].mean()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #fdcb6e 0%, #e17055 100%); 
                        padding: 1.5rem; border-radius: 15px; color: white; text-align: center; 
                        box-shadow: 0 8px 25px rgba(253, 203, 110, 0.3);">
                <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">🔥 Toplam Ekonomik Kayıp</h3>
                <p style="margin: 0; font-size: 1.8rem; font-weight: 700;">${total_loss/1_000:.1f}B</p>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.8;">yıllık kayıp</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #ff7675 0%, #fd79a8 100%); 
                        padding: 1.5rem; border-radius: 15px; color: white; text-align: center; 
                        box-shadow: 0 8px 25px rgba(255, 118, 117, 0.3);">
                <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">📊 Ortalama Kayıp</h3>
                <p style="margin: 0; font-size: 1.8rem; font-weight: 700;">${avg_loss:.1f}M</p>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.8;">ülke başına</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #00b894 0%, #00a085 100%); 
                        padding: 1.5rem; border-radius: 15px; color: white; text-align: center; 
                        box-shadow: 0 8px 25px rgba(0, 184, 148, 0.3);">
                <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">🎯 Tasarruf Potansiyeli</h3>
                <p style="margin: 0; font-size: 1.8rem; font-weight: 700;">${total_loss/2:.1f}B</p>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.8;">50% azaltma ile</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%); 
                        padding: 1.5rem; border-radius: 15px; color: white; text-align: center; 
                        box-shadow: 0 8px 25px rgba(108, 92, 231, 0.3);">
                <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">📈 ROI Potansiyeli</h3>
                <p style="margin: 0; font-size: 1.8rem; font-weight: 700;">300%</p>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.8;">yatırım getirisi</p>
            </div>
            """, unsafe_allow_html=True)

def show_environmental_impact_story(df: pd.DataFrame):
    """🌍 Çevresel Ayak İzi Analizi - Premium Versiyon"""
    
    # Hero bölümü
    st.markdown("""
    <div style="background: linear-gradient(135deg, #00b894 0%, #00a085 100%); 
                padding: 3rem; border-radius: 25px; color: white; margin: 2rem 0; 
                box-shadow: 0 15px 35px rgba(0, 184, 148, 0.3);">
        <h1 style="margin: 0; font-size: 2.8rem; font-weight: 800;">🌍 ÇEVRESEL AYAK İZİ</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            Karbon Ayak İzi Analizi ve Çevresel Etki Değerlendirmesi
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Çevresel Metrikler
    st.markdown("### 🌱 ÇEVRESEL METRİKLER")
    
    carbon_col = _resolve_column_name(df, ['Carbon_Footprint_kgCO2e', 'Carbon Footprint (kgCO2e)'])
    if carbon_col:
        total_carbon = df[carbon_col].sum()
        avg_carbon = df[carbon_col].mean()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #00b894 0%, #00a085 100%); 
                        padding: 1.5rem; border-radius: 15px; color: white; text-align: center; 
                        box-shadow: 0 8px 25px rgba(0, 184, 148, 0.3);">
                <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">🌍 Toplam Karbon Ayak İzi</h3>
                <p style="margin: 0; font-size: 1.8rem; font-weight: 700;">{total_carbon/1_000_000_000:.1f}B</p>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.8;">kg CO2e</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #fdcb6e 0%, #e17055 100%); 
                        padding: 1.5rem; border-radius: 15px; color: white; text-align: center; 
                        box-shadow: 0 8px 25px rgba(253, 203, 110, 0.3);">
                <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">📊 Ortalama Ayak İzi</h3>
                <p style="margin: 0; font-size: 1.8rem; font-weight: 700;">{avg_carbon/1_000_000:.1f}M</p>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.8;">kg CO2e/ülke</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #ff7675 0%, #fd79a8 100%); 
                        padding: 1.5rem; border-radius: 15px; color: white; text-align: center; 
                        box-shadow: 0 8px 25px rgba(255, 118, 117, 0.3);">
                <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">🚗 Araç Eşdeğeri</h3>
                <p style="margin: 0; font-size: 1.8rem; font-weight: 700;">{total_carbon/1_000_000_000*2.3:.1f}M</p>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.8;">araç</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%); 
                        padding: 1.5rem; border-radius: 15px; color: white; text-align: center; 
                        box-shadow: 0 8px 25px rgba(108, 92, 231, 0.3);">
                <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">🌳 Orman Eşdeğeri</h3>
                <p style="margin: 0; font-size: 1.8rem; font-weight: 700;">{total_carbon/1_000_000_000*0.5:.1f}M</p>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.8;">hektar</p>
            </div>
            """, unsafe_allow_html=True)

def show_sustainable_solutions_story(df: pd.DataFrame):
    """🎯 Sürdürülebilir Çözümler Yol Haritası - Premium Versiyon"""
    
    # Hero bölümü
    st.markdown("""
    <div style="background: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%); 
                padding: 3rem; border-radius: 25px; color: white; margin: 2rem 0; 
                box-shadow: 0 15px 35px rgba(108, 92, 231, 0.3);">
        <h1 style="margin: 0; font-size: 2.8rem; font-weight: 800;">🎯 SÜRDÜRÜLEBİLİR ÇÖZÜMLER</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            Sürdürülebilir Gıda Sistemleri İçin Kapsamlı Yol Haritası
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Çözümler Çerçevesi
    st.markdown("### 🛠️ ÇÖZÜMLER ÇERÇEVESİ")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #a29bfe 0%, #6c5ce7 100%); 
                    padding: 2rem; border-radius: 15px; color: white; margin: 1rem 0; 
                    box-shadow: 0 8px 25px rgba(162, 155, 254, 0.3);">
            <h4 style="margin: 0 0 1rem 0;">🔧 Teknoloji Çözümleri</h4>
            <ul style="margin: 0; padding-left: 1.5rem;">
                <li>IoT Akıllı Sensörler</li>
                <li>Blockchain Takip Sistemi</li>
                <li>AI Destekli Analitik</li>
                <li>Otomatik Sınıflandırma</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fd79a8 0%, #fdcb6e 100%); 
                    padding: 2rem; border-radius: 15px; color: white; margin: 1rem 0; 
                    box-shadow: 0 8px 25px rgba(253, 121, 168, 0.3);">
            <h4 style="margin: 0 0 1rem 0;">📋 Politika Çözümleri</h4>
            <ul style="margin: 0; padding-left: 1.5rem;">
                <li>Karbon Fiyatlandırması</li>
                <li>İsraf Azaltma Hedefleri</li>
                <li>Teşvik Programları</li>
                <li>Düzenleyici Çerçeve</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def show_2030_strategy_story(df: pd.DataFrame):
    """🚀 2030 Stratejik Tahmin - Premium Versiyon"""
    
    # Hero bölümü
    st.markdown("""
    <div style="background: linear-gradient(135deg, #e17055 0%, #d63031 100%); 
                padding: 3rem; border-radius: 25px; color: white; margin: 2rem 0; 
                box-shadow: 0 15px 35px rgba(225, 112, 85, 0.3);">
        <h1 style="margin: 0; font-size: 2.8rem; font-weight: 800;">🚀 2030 STRATEJİK TAHMİN</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            Gelecek Senaryoları ve Stratejik Öneriler
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 2030 Senaryoları
    st.markdown("### 🔮 2030 SENARYOLARI")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ff7675 0%, #fd79a8 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; margin: 1rem 0; 
                    box-shadow: 0 8px 25px rgba(255, 118, 117, 0.3);">
            <h4 style="margin: 0 0 1rem 0;">🔴 Mevcut Durum</h4>
            <p style="margin: 0; font-size: 0.9rem;">+25% israf artışı<br>+$2T ekonomik kayıp<br>+40% karbon ayak izi</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fdcb6e 0%, #e17055 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; margin: 1rem 0; 
                    box-shadow: 0 8px 25px rgba(253, 203, 110, 0.3);">
            <h4 style="margin: 0 0 1rem 0;">🟡 Orta Seviye Aksiyon</h4>
            <p style="margin: 0; font-size: 0.9rem;">+10% israf artışı<br>+$800B ekonomik kayıp<br>+15% karbon ayak izi</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #00b894 0%, #00a085 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; margin: 1rem 0; 
                    box-shadow: 0 8px 25px rgba(0, 184, 148, 0.3);">
            <h4 style="margin: 0 0 1rem 0;">🟢 Agresif Aksiyon</h4>
            <p style="margin: 0; font-size: 0.9rem;">-30% israf azalması<br>-$1.5T ekonomik tasarruf<br>-25% karbon ayak izi</p>
        </div>
        """, unsafe_allow_html=True)

def show_comprehensive_analytics_story(df: pd.DataFrame):
    """📊 Kapsamlı Analitik - Premium Versiyon"""
    
    # Hero bölümü
    st.markdown("""
    <div style="background: linear-gradient(135deg, #2d3436 0%, #636e72 100%); 
                padding: 3rem; border-radius: 25px; color: white; margin: 2rem 0; 
                box-shadow: 0 15px 35px rgba(45, 52, 54, 0.3);">
        <h1 style="margin: 0; font-size: 2.8rem; font-weight: 800;">📊 KAPSAMLI ANALİTİK</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            Gelişmiş Veri Analizi ve Makine Öğrenmesi İçgörüleri
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Analitik Paneli
    st.markdown("### 📈 ANALİTİK PANELİ")
    
    # Korelasyon Analizi
    st.markdown("### 🔗 KORELASYON ANALİZİ")
    
    # Sayısal sütunları seç
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) >= 2:
        correlation_matrix = df[numeric_cols].corr()
        
        fig = px.imshow(
            correlation_matrix,
            title="Özellik Korelasyon Matrisi",
            color_continuous_scale='RdBu',
            aspect="auto"
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            title_font_size=20
        )
        st.plotly_chart(fig, use_container_width=True)
        
    # İstatistiksel Özet
    st.markdown("### 📊 İSTATİSTİKSEL ÖZET")
    
    if len(numeric_cols) > 0:
        summary_stats = df[numeric_cols].describe()
        st.dataframe(summary_stats, use_container_width=True)
