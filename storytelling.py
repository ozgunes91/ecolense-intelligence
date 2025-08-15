import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from typing import Optional
import warnings
warnings.filterwarnings('ignore')

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
            'forecasts': '📈 Tahminler',
            'smart_insights': '🧠 Akıllı Çıkarımlar',
            'future_goals': '🚀 Gelecek Hedefleri'
        },
        'EN': {
            'title': '📖 PREMIUM STORY MODE',
            'desc': 'AI-Powered Data Storytelling & Strategic Insights Platform',
            'active_story': 'Active Story',
            'home': '🏠 Home',
            'analysis': '📊 Analysis',
            'targets': '🎯 Targets',
            'ai_insights': '🤖 AI Insights',
            'forecasts': '📈 Forecasts',
            'smart_insights': '🧠 Smart Insights',
            'future_goals': '🚀 Future Goals'
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
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    
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
    
    with col6:
        if st.button(texts['smart_insights'], key="nav_smart", use_container_width=True):
            st.session_state['page'] = 'PAGE_SMART_INSIGHTS'
            st.rerun()
    
    with col7:
        if st.button(texts['future_goals'], key="nav_goals", use_container_width=True):
            st.session_state['page'] = 'PAGE_FUTURE_GOALS'
            st.rerun()
    
    # Tek kapsamlı hikaye bölümü
    show_comprehensive_story(df)

def show_comprehensive_story(df: pd.DataFrame):
    """🌍 KAPSAMLI GIDA İSRAFI ANALİZİ - Gerçek Verilerle Ekonomik, Çevresel ve Sürdürülebilirlik"""
    
    # Hero bölümü
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 3rem; border-radius: 25px; color: white; margin: 2rem 0; 
                box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);">
        <h1 style="margin: 0; font-size: 2.8rem; font-weight: 800;">🌍 KAPSAMLI GIDA İSRAFI ANALİZİ</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            Gerçek Verilerle Ekonomik, Çevresel ve Sürdürülebilirlik Etkilerinin Bütünsel Değerlendirmesi
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Veri kaynağı bilgisi - ISO'lu veri seti
    st.info("📊 **Veri Kaynağı:** Ecolense Final Enriched with ISO Dataset (2018-2024) - 5000+ veri noktası, 20 ülke, 8 gıda kategorisi")
    
    # Gerçek verilerden hesaplamalar - ISO'lu veri seti sütunları (küçük harfli sütun adları)
    total_waste = df['total_waste_(tons)'].sum() if 'total_waste_(tons)' in df.columns else 0
    total_economic_loss = df['economic_loss_(million_$)'].sum() if 'economic_loss_(million_$)' in df.columns else 0
    total_carbon = df['carbon_footprint_kgco2e'].sum() if 'carbon_footprint_kgco2e' in df.columns else 0
    countries_count = df['country'].nunique() if 'country' in df.columns else 0
    categories_count = df['food_category'].nunique() if 'food_category' in df.columns else 0
    
    # Kapsamlı Metrikler
    st.markdown("### 📊 KAPSAMLI METRİKLER PANELİ")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; text-align: center; 
                    box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3);">
            <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">🥗 Gıda İsrafı</h3>
            <p style="margin: 0; font-size: 1.8rem; font-weight: 700;">{total_waste/1_000_000:.1f}M</p>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.8;">ton (2018-2024)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #fdcb6e 0%, #e17055 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; text-align: center; 
                    box-shadow: 0 8px 25px rgba(253, 203, 110, 0.3);">
            <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">💰 Ekonomik Kayıp</h3>
            <p style="margin: 0; font-size: 1.8rem; font-weight: 700;">${total_economic_loss/1_000:.1f}B</p>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.8;">milyon $</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #00b894 0%, #00a085 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; text-align: center; 
                    box-shadow: 0 8px 25px rgba(0, 184, 148, 0.3);">
            <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">🌍 Karbon Ayak İzi</h3>
            <p style="margin: 0; font-size: 1.8rem; font-weight: 700;">{total_carbon/1_000_000_000:.1f}B</p>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.8;">kg CO2e</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; text-align: center; 
                    box-shadow: 0 8px 25px rgba(108, 92, 231, 0.3);">
            <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">🌐 Kapsam</h3>
            <p style="margin: 0; font-size: 1.8rem; font-weight: 700;">{countries_count} ülke</p>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.8;">{categories_count} kategori</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Kapsamlı Analiz
    st.markdown("### 🔍 KAPSAMLI ETKİ ANALİZİ")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ff7675 0%, #fd79a8 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; margin-bottom: 1rem;">
            <h4 style="margin: 0 0 1rem 0; font-size: 1.3rem;">💰 EKONOMİK ETKİ</h4>
            <ul style="margin: 0; padding-left: 1.2rem; font-size: 0.95rem;">
                <li>Yıllık ekonomik kayıp milyarlarca dolar</li>
                <li>GDP üzerinde önemli etki</li>
                <li>İş gücü verimliliği kaybı</li>
                <li>Yatırım fırsatları ve maliyet-fayda analizi</li>
                <li>Döngüsel ekonomi potansiyeli</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; margin-bottom: 1rem;">
            <h4 style="margin: 0 0 1rem 0; font-size: 1.3rem;">🌍 ÇEVRESEL ETKİ</h4>
            <ul style="margin: 0; padding-left: 1.2rem; font-size: 0.95rem;">
                <li>Karbon ayak izi ve sera gazı emisyonları</li>
                <li>Su ve toprak kaynaklarının israfı</li>
                <li>Biyoçeşitlilik üzerindeki etki</li>
                <li>İklim değişikliği katkısı</li>
                <li>Sürdürülebilirlik skorları</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #55a3ff 0%, #0066ff 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; margin-bottom: 1rem;">
            <h4 style="margin: 0 0 1rem 0; font-size: 1.3rem;">🌱 SÜRDÜRÜLEBİLİRLİK</h4>
            <ul style="margin: 0; padding-left: 1.2rem; font-size: 0.95rem;">
                <li>2030 sürdürülebilirlik hedefleri</li>
                <li>Döngüsel ekonomi modelleri</li>
                <li>Teknoloji adaptasyonu ve inovasyon</li>
                <li>Politika önerileri ve düzenlemeler</li>
                <li>Paydaş işbirliği ve eğitim</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #a29bfe 0%, #6c5ce7 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; margin-bottom: 1rem;">
            <h4 style="margin: 0 0 1rem 0; font-size: 1.3rem;">🎯 ÇÖZÜM STRATEJİLERİ</h4>
            <ul style="margin: 0; padding-left: 1.2rem; font-size: 0.95rem;">
                <li>Akıllı tedarik zinciri optimizasyonu</li>
                <li>Teknoloji tabanlı izleme sistemleri</li>
                <li>Farkındalık ve eğitim programları</li>
                <li>Politika ve düzenleme iyileştirmeleri</li>
                <li>Uluslararası işbirliği ve standartlar</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Hikaye akışı
    st.markdown("### 📖 HİKAYE AKIŞI: PROBLEM → ANALİZ → ÇÖZÜM")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin: 1rem 0;">
        <h4 style="margin: 0 0 1rem 0; font-size: 1.4rem;">🚨 PROBLEM: Küresel Gıda İsrafı Krizi</h4>
        <p style="margin: 0; font-size: 1rem; line-height: 1.6;">
            Dünya genelinde üretilen gıdaların yaklaşık üçte biri israf ediliyor. Bu durum sadece ekonomik kayıplara değil, 
            aynı zamanda çevresel felaketlere ve sosyal adaletsizliğe yol açıyor. Gıda israfı, karbon emisyonlarının %8'ini 
            oluşturuyor ve su kaynaklarının büyük bir kısmını boşa harcıyor. Bu kriz, acil ve kapsamlı çözümler gerektiriyor.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Gelecek önerileri ve aksiyonlar
    st.markdown("### 🎯 ÇÖZÜM: GELECEK ÖNERİLERİ VE AKSİYONLAR")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #00b894 0%, #00a085 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; margin-bottom: 1rem;">
            <h4 style="margin: 0 0 1rem 0; font-size: 1.3rem;">⚡ Kısa Vadeli Aksiyonlar (2025-2026)</h4>
            <ul style="margin: 0; padding-left: 1.2rem; font-size: 0.9rem;">
                <li>Akıllı izleme sistemlerinin kurulması</li>
                <li>Farkındalık kampanyalarının başlatılması</li>
                <li>Tedarik zinciri optimizasyonu</li>
                <li>Politika düzenlemelerinin hızlandırılması</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fdcb6e 0%, #e17055 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; margin-bottom: 1rem;">
            <h4 style="margin: 0 0 1rem 0; font-size: 1.3rem;">🎯 Orta Vadeli Hedefler (2026-2028)</h4>
            <ul style="margin: 0; padding-left: 1.2rem; font-size: 0.9rem;">
                <li>Döngüsel ekonomi modellerinin uygulanması</li>
                <li>Teknoloji adaptasyonunun tamamlanması</li>
                <li>Uluslararası standartların belirlenmesi</li>
                <li>Eğitim programlarının yaygınlaştırılması</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; margin-bottom: 1rem;">
            <h4 style="margin: 0 0 1rem 0; font-size: 1.3rem;">🚀 Uzun Vadeli Vizyon (2028-2030)</h4>
            <ul style="margin: 0; padding-left: 1.2rem; font-size: 0.9rem;">
                <li>Sürdürülebilir gıda sistemlerinin kurulması</li>
                <li>%50 gıda israfı azaltımı hedefine ulaşma</li>
                <li>Karbon nötr gıda üretimi</li>
                <li>Küresel gıda güvenliği sağlanması</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fd79a8 0%, #fdcb6e 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; margin-bottom: 1rem;">
            <h4 style="margin: 0 0 1rem 0; font-size: 1.3rem;">🔑 Kritik Başarı Faktörleri</h4>
            <ul style="margin: 0; padding-left: 1.2rem; font-size: 0.9rem;">
                <li>Paydaş işbirliği ve koordinasyon</li>
                <li>Teknoloji ve inovasyon yatırımları</li>
                <li>Politika ve düzenleme desteği</li>
                <li>Toplumsal farkındalık ve eğitim</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # İnteraktif öneriler
    st.markdown("### 🎮 İNTERAKTİF ÖNERİLER")
    
    col1, col2 = st.columns(2)
    
    with col1:
        priority = st.selectbox(
            "🎯 Hangi aksiyon önceliğiniz?",
            ["Teknoloji Yatırımı", "Politika Düzenlemesi", "Eğitim Programı", "Tedarik Zinciri Optimizasyonu"],
            key="priority_selector"
        )
    
    with col2:
        budget = st.slider(
            "💰 Tahmini Bütçe (Milyon $)",
            min_value=1,
            max_value=1000,
            value=100,
            step=10,
            key="budget_slider"
        )
    
    # Dinamik öneriler
    if priority == "Teknoloji Yatırımı":
        if budget >= 500:
            st.success(f"🚀 **Mükemmel!** ${budget}M bütçe ile AI tabanlı izleme sistemleri, IoT sensörleri ve blockchain teknolojileri kurabilirsiniz. Bu yatırım 3-5 yıl içinde %40 verimlilik artışı sağlayacaktır.")
        elif budget >= 200:
            st.warning(f"📊 **İyi Başlangıç!** ${budget}M ile temel izleme sistemleri ve veri analitik platformları kurabilirsiniz. Daha fazla bütçe ile daha kapsamlı çözümler mümkün.")
        else:
            st.info(f"💡 **Başlangıç Seviyesi:** ${budget}M ile pilot projeler ve temel teknoloji altyapısı kurabilirsiniz. Kademeli olarak genişletmeyi düşünün.")
    
    elif priority == "Politika Düzenlemesi":
        if budget >= 300:
            st.success(f"📋 **Kapsamlı Politika!** ${budget}M ile ulusal gıda israfı stratejisi, düzenlemeler ve denetim sistemleri kurabilirsiniz.")
        elif budget >= 100:
            st.warning(f"📝 **Temel Düzenlemeler:** ${budget}M ile temel politika çerçevesi ve pilot uygulamalar başlatabilirsiniz.")
        else:
            st.info(f"📄 **Başlangıç:** ${budget}M ile politika araştırması ve öneri geliştirme süreçleri başlatabilirsiniz.")
    
    elif priority == "Eğitim Programı":
        if budget >= 200:
            st.success(f"🎓 **Kapsamlı Eğitim!** ${budget}M ile ulusal eğitim kampanyası, okul programları ve toplumsal farkındalık projeleri yürütebilirsiniz.")
        elif budget >= 50:
            st.warning(f"📚 **Temel Eğitim:** ${budget}M ile pilot eğitim programları ve farkındalık kampanyaları başlatabilirsiniz.")
        else:
            st.info(f"📖 **Başlangıç:** ${budget}M ile eğitim materyali geliştirme ve pilot uygulamalar yapabilirsiniz.")
    
    else:  # Tedarik Zinciri Optimizasyonu
        if budget >= 400:
            st.success(f"🔗 **Tam Optimizasyon!** ${budget}M ile end-to-end tedarik zinciri optimizasyonu, akıllı lojistik sistemleri ve verimlilik artırıcı teknolojiler kurabilirsiniz.")
        elif budget >= 150:
            st.warning(f"⚙️ **Kısmi Optimizasyon:** ${budget}M ile kritik noktalarda optimizasyon ve temel iyileştirmeler yapabilirsiniz.")
        else:
            st.info(f"🔧 **Temel İyileştirmeler:** ${budget}M ile pilot optimizasyon projeleri ve verimlilik analizleri yapabilirsiniz.")
