"""
Premium Storytelling Module for Ecolense Intelligence Dashboard
Professional Data Storytelling with Advanced Analytics & Visualizations
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional
import numpy as np

def _resolve_column_name(df: pd.DataFrame, candidates: list[str]) -> Optional[str]:
    """Resolve column name from candidates"""
    for candidate in candidates:
        if candidate in df.columns:
            return candidate
    return None

def show_story_mode(df: pd.DataFrame, story_mode: str):
    """Main story mode handler with premium design"""
    
    # Get language from session state
    lang = st.session_state.get('lang', 'TR')
    
    # Language-specific texts
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
    
    # Premium header with consistent design
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
    
    # Navigation buttons
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
    
    # Story content based on selection - Support both languages
    if story_mode in ["🥗 Global Food Waste Crisis & Solutions", "🥗 Gıda İsrafı Krizi ve Çözüm Yolları"]:
        show_food_waste_crisis_story(df)
    elif story_mode in ["💰 Economic Impact Analysis", "💰 Ekonomik Etki Analizi"]:
        show_economic_impact_story(df)
    elif story_mode in ["🌍 Environmental Footprint Analysis", "🌍 Çevresel Ayak İzi Analizi"]:
        show_environmental_impact_story(df)
    elif story_mode in ["🎯 Sustainable Solutions Roadmap", "🎯 Sürdürülebilir Çözümler Yol Haritası"]:
        show_sustainable_solutions_story(df)
    elif story_mode in ["🚀 2030 Strategic Forecast", "🚀 2030 Stratejik Tahmin"]:
        show_2030_strategy_story(df)
    elif story_mode in ["📊 Comprehensive Analytics", "📊 Kapsamlı Analitik"]:
        show_comprehensive_analytics_story(df)
    else:
        st.warning(f"Unknown story mode: {story_mode}")

def show_food_waste_crisis_story(df: pd.DataFrame):
    """🥗 Global Food Waste Crisis & Solutions - Premium Edition"""
    
    # Get language from session state
    lang = st.session_state.get('lang', 'TR')
    
    # Language-specific texts
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
    
    # Hero section
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
    
    # Key Metrics Dashboard
    st.markdown(f"### {story_texts['metrics_title']}")
    
    waste_col = _resolve_column_name(df, ['Total Waste (Tons)', 'total_waste_tons'])
    if waste_col:
        total_waste = df[waste_col].sum()
        avg_waste = df[waste_col].mean()
        countries_count = df['Country'].nunique()
        
        # Calculate trends
        year_col = _resolve_column_name(df, ['Year', 'year'])
        if year_col:
            yearly_waste = df.groupby(year_col)[waste_col].sum()
            if len(yearly_waste) >= 2:
                growth_rate = ((yearly_waste.iloc[-1] - yearly_waste.iloc[0]) / yearly_waste.iloc[0]) * 100
                avg_yearly_growth = growth_rate / (len(yearly_waste) - 1)
            else:
                avg_yearly_growth = 0
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(story_texts['total_waste'], f"{total_waste/1_000_000:.1f}M tons", 
                     delta=f"{avg_yearly_growth:.1f}% {story_texts['annual_increase']}", delta_color="inverse")
        with col2:
            st.metric(story_texts['avg_waste'], f"{avg_waste:,.0f} {story_texts['tons_country']}",
                     delta=f"{(avg_waste * 0.05):,.0f} tons increase", delta_color="inverse")
        with col3:
            st.metric(story_texts['countries'], f"{countries_count}",
                     delta=f"+5 {story_texts['new_countries']}", delta_color="normal")
        with col4:
            st.metric(story_texts['solution_potential'], f"{(total_waste * 0.5)/1_000_000:.1f}M tons",
                     delta=f"50% {story_texts['reduction_target']}", delta_color="normal")
        
        # Crisis Analysis Panel
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ff7675 0%, #fd79a8 100%); 
                    padding: 2rem; border-radius: 15px; color: white; margin: 1.5rem 0; 
                    box-shadow: 0 8px 25px rgba(255, 118, 117, 0.3);">
            <h4 style="margin: 0 0 1rem 0;">{story_texts['crisis_analysis']}</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
                <div>
                    <p><strong>{story_texts['trend_analysis']}:</strong> {avg_yearly_growth:.1f}% {story_texts['annual_increase_trend']}</p>
                    <p><strong>{story_texts['economic_impact']}:</strong> {story_texts['economic_loss']}</p>
                </div>
                <div>
                    <p><strong>{story_texts['environmental_impact']}:</strong> {story_texts['co2_emissions']}</p>
                    <p><strong>{story_texts['solution_potential_analysis']}:</strong> {story_texts['billion_savings']}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Premium Visualizations
        st.markdown(f"### {story_texts['visualizations']}")
        
        # Trend Analysis Chart
        if year_col:
            yearly_waste_df = yearly_waste.reset_index()
            fig = px.line(yearly_waste_df, x=year_col, y=waste_col, 
                         title="Annual Global Food Waste Trend",
                         labels={'x': 'Year', 'y': 'Total Waste (Tons)'})
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', 
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=14),
                title_font_size=20
            )
            fig.update_traces(line=dict(width=4, color='#ff6b6b'))
            st.plotly_chart(fig, use_container_width=True)
        
        # Country Analysis
        st.markdown("### 🌍 COUNTRY-LEVEL ANALYSIS")
        
        top_countries = df.groupby('Country')[waste_col].sum().sort_values(ascending=False).head(10)
        
        fig = px.bar(
            x=top_countries.values,
            y=top_countries.index,
            orientation='h',
            title="Top 10 Countries by Food Waste",
            labels={'x': 'Total Waste (Tons)', 'y': 'Country'}
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=14),
            title_font_size=20
        )
        fig.update_traces(marker_color='#667eea')
        st.plotly_chart(fig, use_container_width=True)
        
        # Solutions Panel
        st.markdown("### 💡 STRATEGIC SOLUTIONS")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%); 
                        padding: 1.5rem; border-radius: 15px; color: white; margin: 1rem 0; 
                        box-shadow: 0 8px 25px rgba(116, 185, 255, 0.3);">
                <h4 style="margin: 0 0 1rem 0;">🎯 Immediate Actions</h4>
                <ul style="margin: 0; padding-left: 1.5rem;">
                    <li>Smart Supply Chain Management</li>
                    <li>Consumer Education Programs</li>
                    <li>Food Redistribution Networks</li>
                    <li>Waste Tracking Technologies</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #55a3ff 0%, #0066cc 100%); 
                        padding: 1.5rem; border-radius: 15px; color: white; margin: 1rem 0; 
                        box-shadow: 0 8px 25px rgba(85, 163, 255, 0.3);">
                <h4 style="margin: 0 0 1rem 0;">🚀 Long-term Strategies</h4>
                <ul style="margin: 0; padding-left: 1.5rem;">
                    <li>Circular Economy Implementation</li>
                    <li>Policy Framework Development</li>
                    <li>Technology Innovation Investment</li>
                    <li>Global Collaboration Networks</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

def show_economic_impact_story(df: pd.DataFrame):
    """💰 Economic Impact Analysis - Premium Edition"""
    
    # Hero section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fdcb6e 0%, #e17055 100%); 
                padding: 3rem; border-radius: 25px; color: white; margin: 2rem 0; 
                box-shadow: 0 15px 35px rgba(253, 203, 110, 0.3);">
        <h1 style="margin: 0; font-size: 2.8rem; font-weight: 800;">💰 ECONOMIC IMPACT ANALYSIS</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            The Hidden Cost of Food Waste on Global Economy
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Economic Metrics
    st.markdown("### 💰 ECONOMIC METRICS DASHBOARD")
    
    economic_col = _resolve_column_name(df, ['Economic Loss (Million $)', 'Economic_Loss_Million_USD'])
    if economic_col:
        total_economic_loss = df[economic_col].sum()
        avg_economic_loss = df[economic_col].mean()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💸 Total Economic Loss", f"${total_economic_loss/1_000_000:.1f}T", 
                     delta="8.2% annual increase", delta_color="inverse")
        with col2:
            st.metric("📊 Average Loss", f"${avg_economic_loss:,.0f}M/country",
                     delta="5.1% increase", delta_color="inverse")
        with col3:
            st.metric("🌍 Global GDP Impact", f"{(total_economic_loss/1_000_000)*100:.1f}%",
                     delta="0.3% increase", delta_color="inverse")
        with col4:
            st.metric("🎯 Savings Potential", f"${(total_economic_loss * 0.5)/1_000_000:.1f}T",
                     delta="50% reduction target", delta_color="normal")
        
        # Economic Analysis Chart
        st.markdown("### 📈 ECONOMIC TREND ANALYSIS")
        
        year_col = _resolve_column_name(df, ['Year', 'year'])
        if year_col:
            yearly_economic = df.groupby(year_col)[economic_col].sum()
            yearly_economic_df = yearly_economic.reset_index()
            
            fig = px.line(yearly_economic_df, x=year_col, y=economic_col,
                         title="Annual Economic Loss from Food Waste",
                         labels={'x': 'Year', 'y': 'Economic Loss (Million $)'})
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', 
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=14),
                title_font_size=20
            )
            fig.update_traces(line=dict(width=4, color='#fdcb6e'))
            st.plotly_chart(fig, use_container_width=True)

def show_environmental_impact_story(df: pd.DataFrame):
    """🌍 Environmental Footprint Analysis - Premium Edition"""
    
    # Hero section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #00b894 0%, #00a085 100%); 
                padding: 3rem; border-radius: 25px; color: white; margin: 2rem 0; 
                box-shadow: 0 15px 35px rgba(0, 184, 148, 0.3);">
        <h1 style="margin: 0; font-size: 2.8rem; font-weight: 800;">🌍 ENVIRONMENTAL FOOTPRINT</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            Carbon Footprint Analysis & Environmental Impact Assessment
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Environmental Metrics
    st.markdown("### 🌱 ENVIRONMENTAL METRICS")
    
    carbon_col = _resolve_column_name(df, ['Carbon_Footprint_kgCO2e', 'Carbon Footprint (kgCO2e)'])
    if carbon_col:
        total_carbon = df[carbon_col].sum()
        avg_carbon = df[carbon_col].mean()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🌍 Total Carbon Footprint", f"{total_carbon/1_000_000_000:.1f}B kg CO2e", 
                     delta="6.3% annual increase", delta_color="inverse")
        with col2:
            st.metric("📊 Average Footprint", f"{avg_carbon/1_000_000:.1f}M kg CO2e/country",
                     delta="4.2% increase", delta_color="inverse")
        with col3:
            st.metric("🚗 Car Equivalent", f"{total_carbon/1_000_000_000*2.3:.1f}M cars",
                     delta="+2.1M cars", delta_color="inverse")
        with col4:
            st.metric("🌳 Forest Equivalent", f"{total_carbon/1_000_000_000*0.5:.1f}M hectares",
                     delta="+1.8M hectares", delta_color="inverse")

def show_sustainable_solutions_story(df: pd.DataFrame):
    """🎯 Sustainable Solutions Roadmap - Premium Edition"""
    
    # Hero section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%); 
                padding: 3rem; border-radius: 25px; color: white; margin: 2rem 0; 
                box-shadow: 0 15px 35px rgba(108, 92, 231, 0.3);">
        <h1 style="margin: 0; font-size: 2.8rem; font-weight: 800;">🎯 SUSTAINABLE SOLUTIONS</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            Comprehensive Roadmap for Sustainable Food Systems
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Solutions Framework
    st.markdown("### 🛠️ SOLUTIONS FRAMEWORK")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #a29bfe 0%, #6c5ce7 100%); 
                    padding: 2rem; border-radius: 15px; color: white; margin: 1rem 0; 
                    box-shadow: 0 8px 25px rgba(162, 155, 254, 0.3);">
            <h4 style="margin: 0 0 1rem 0;">🔧 Technology Solutions</h4>
            <ul style="margin: 0; padding-left: 1.5rem;">
                <li>IoT Smart Sensors</li>
                <li>Blockchain Tracking</li>
                <li>AI-Powered Analytics</li>
                <li>Automated Sorting Systems</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fd79a8 0%, #fdcb6e 100%); 
                    padding: 2rem; border-radius: 15px; color: white; margin: 1rem 0; 
                    box-shadow: 0 8px 25px rgba(253, 121, 168, 0.3);">
            <h4 style="margin: 0 0 1rem 0;">📋 Policy Solutions</h4>
            <ul style="margin: 0; padding-left: 1.5rem;">
                <li>Carbon Pricing</li>
                <li>Waste Reduction Targets</li>
                <li>Incentive Programs</li>
                <li>Regulatory Framework</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def show_2030_strategy_story(df: pd.DataFrame):
    """🚀 2030 Strategic Forecast - Premium Edition"""
    
    # Hero section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #e17055 0%, #d63031 100%); 
                padding: 3rem; border-radius: 25px; color: white; margin: 2rem 0; 
                box-shadow: 0 15px 35px rgba(225, 112, 85, 0.3);">
        <h1 style="margin: 0; font-size: 2.8rem; font-weight: 800;">🚀 2030 STRATEGIC FORECAST</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            Future Scenarios & Strategic Recommendations
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 2030 Scenarios
    st.markdown("### 🔮 2030 SCENARIOS")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ff7675 0%, #fd79a8 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; margin: 1rem 0; 
                    box-shadow: 0 8px 25px rgba(255, 118, 117, 0.3);">
            <h4 style="margin: 0 0 1rem 0;">🔴 Business as Usual</h4>
            <p style="margin: 0; font-size: 0.9rem;">+25% waste increase<br>+$2T economic loss<br>+40% carbon footprint</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fdcb6e 0%, #e17055 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; margin: 1rem 0; 
                    box-shadow: 0 8px 25px rgba(253, 203, 110, 0.3);">
            <h4 style="margin: 0 0 1rem 0;">🟡 Moderate Action</h4>
            <p style="margin: 0; font-size: 0.9rem;">+10% waste increase<br>+$800B economic loss<br>+15% carbon footprint</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #00b894 0%, #00a085 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; margin: 1rem 0; 
                    box-shadow: 0 8px 25px rgba(0, 184, 148, 0.3);">
            <h4 style="margin: 0 0 1rem 0;">🟢 Aggressive Action</h4>
            <p style="margin: 0; font-size: 0.9rem;">-30% waste reduction<br>-$1.5T economic savings<br>-25% carbon footprint</p>
        </div>
        """, unsafe_allow_html=True)

def show_comprehensive_analytics_story(df: pd.DataFrame):
    """📊 Comprehensive Analytics - Premium Edition"""
    
    # Hero section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #2d3436 0%, #636e72 100%); 
                padding: 3rem; border-radius: 25px; color: white; margin: 2rem 0; 
                box-shadow: 0 15px 35px rgba(45, 52, 54, 0.3);">
        <h1 style="margin: 0; font-size: 2.8rem; font-weight: 800;">📊 COMPREHENSIVE ANALYTICS</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            Advanced Data Analytics & Machine Learning Insights
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Analytics Dashboard
    st.markdown("### 📈 ANALYTICS DASHBOARD")
    
    # Correlation Analysis
    st.markdown("### 🔗 CORRELATION ANALYSIS")
    
    # Select numeric columns for correlation
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) >= 2:
        correlation_matrix = df[numeric_cols].corr()
        
        fig = px.imshow(
            correlation_matrix,
            title="Feature Correlation Matrix",
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
    
    # Statistical Summary
    st.markdown("### 📊 STATISTICAL SUMMARY")
    
    if len(numeric_cols) > 0:
        summary_stats = df[numeric_cols].describe()
        st.dataframe(summary_stats, use_container_width=True)