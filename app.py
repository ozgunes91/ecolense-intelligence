#!/usr/bin/env python3
"""
app.py — EcoLense Intelligence Dashboard
=========================================
Tüm içerik data/processed.csv + model_performance.json + forecasts.csv'den gelir.
Hiçbir sabit/ezber sayı yoktur.
"""

import streamlit as st
import pandas as pd
import numpy as np
import json, os, warnings
import plotly.express as px
import plotly.graph_objects as go
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
# SAYFA AYARLARI
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EcoLense Intelligence",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS — premium, minimal, temiz
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
:root{--green:#2e7d32;--teal:#00796b;--amber:#f57c00;--red:#c62828;--blue:#1565c0;
      --card-bg:#f8fffe;--border:#e0f2f1;}
body{background:#f5f9f8;}
.kpi-card{background:white;border-radius:14px;padding:1.2rem 1.4rem;
  box-shadow:0 2px 12px rgba(0,100,80,.08);border-left:4px solid var(--teal);
  margin:.3rem 0;}
.kpi-label{font-size:.78rem;color:#607d8b;font-weight:600;text-transform:uppercase;letter-spacing:.06em;}
.kpi-value{font-size:1.9rem;font-weight:700;color:#1a3c34;line-height:1.1;}
.kpi-delta{font-size:.82rem;margin-top:.25rem;}
.section-header{background:linear-gradient(135deg,#1b5e20,#004d40);
  color:white;border-radius:14px;padding:1.3rem 1.8rem;margin:1rem 0 .8rem;}
.section-header h2{margin:0;font-size:1.6rem;}
.section-header p{margin:.3rem 0 0;opacity:.85;font-size:.95rem;}
.source-badge{background:#e8f5e9;color:#1b5e20;border-radius:20px;
  padding:.2rem .7rem;font-size:.73rem;font-weight:600;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# VERİ YÜKLEME (önbellekli)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_processed():
    return pd.read_csv("data/processed.csv")

@st.cache_data(show_spinner=False)
def load_meta():
    with open("data/meta.json", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data(show_spinner=False)
def load_perf():
    with open("model_performance.json", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data(show_spinner=False)
def load_forecasts():
    return pd.read_csv("forecasts.csv")

@st.cache_data(show_spinner=False)
def load_shap(target):
    safe = target.replace(" ","_").replace("(","").replace(")","").replace("$","USD")
    path = f"shap_{safe}.csv"
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

TARGETS = ["Total Waste (Tons)","Economic Loss (Million $)","Carbon_Footprint_kgCO2e"]

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
def sidebar():
    with st.sidebar:
        st.markdown("""
        <div style='text-align:center;padding:1rem 0;'>
          <span style='font-size:2.2rem;'>🌱</span>
          <h3 style='margin:.3rem 0 0;color:#1b5e20;'>EcoLense</h3>
          <p style='font-size:.8rem;color:#607d8b;margin:0;'>Intelligence Dashboard</p>
        </div>
        <hr style='border-color:#e0f2f1;margin:.5rem 0;'>
        """, unsafe_allow_html=True)

        pages = [
            "🏠 Ana Sayfa",
            "📊 Veri Analizi",
            "🌍 Ülke Karşılaştırma",
            "🤖 Model Performansı",
            "🔮 Gelecek Tahminleri",
            "🎯 Hedef Simülatörü",
            "📈 SHAP & Önem",
            "⚠️ Risk & Fırsat",
            "📄 Rapor",
        ]
        page = st.radio("Sayfa", pages, label_visibility="collapsed")
        st.markdown("<hr style='border-color:#e0f2f1;'>", unsafe_allow_html=True)

        meta = load_meta()
        st.markdown(f"""
        <div style='font-size:.75rem;color:#607d8b;'>
          <b>Veri Kaynakları</b><br>
          {'<br>'.join([f'• {s.split("–")[0].strip()}' for s in meta.get("sources",[])])}
          <br><br>
          <b>Kapsam</b><br>
          • {meta.get("countries")} ülke<br>
          • {meta.get("years",[2010,2023])[0]}–{meta.get("years",[2010,2023])[1]} yıl aralığı<br>
          • {meta.get("n_rows",0):,} gözlem
        </div>
        """, unsafe_allow_html=True)
    return page

# ─────────────────────────────────────────────────────────────────────────────
# YARDIMCI: KPI KARTI
# ─────────────────────────────────────────────────────────────────────────────
def kpi(label, value, delta=None, color="#00796b"):
    delta_html = ""
    if delta is not None:
        sign = "▲" if delta >= 0 else "▼"
        col  = "#c62828" if delta >= 0 else "#2e7d32"
        delta_html = f'<div class="kpi-delta" style="color:{col};">{sign} {abs(delta):.1f}%</div>'
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color:{color};">
      <div class="kpi-label">{label}</div>
      <div class="kpi-value">{value}</div>
      {delta_html}
    </div>""", unsafe_allow_html=True)

def section(title, desc="", icon=""):
    st.markdown(f"""
    <div class="section-header">
      <h2>{icon} {title}</h2>
      {'<p>' + desc + '</p>' if desc else ''}
    </div>""", unsafe_allow_html=True)

def fmt(n, unit="", decimals=1):
    if n >= 1e12: return f"{n/1e12:.{decimals}f} T {unit}"
    if n >= 1e9:  return f"{n/1e9:.{decimals}f} Mrd {unit}"
    if n >= 1e6:  return f"{n/1e6:.{decimals}f} M {unit}"
    if n >= 1e3:  return f"{n/1e3:.{decimals}f} K {unit}"
    return f"{n:.{decimals}f} {unit}"

# ─────────────────────────────────────────────────────────────────────────────
# SAYFA 1: ANA SAYFA
# ─────────────────────────────────────────────────────────────────────────────
def page_home(df, meta, perf):
    section("Ana Sayfa", "Gerçek veriye dayalı küresel gıda israfı analiz platformu", "🏠")

    # ── KPI'lar – son yıldan ────────────────────────────────────────────
    last_yr   = df["Year"].max()
    prev_yr   = last_yr - 1
    df_last   = df[df["Year"] == last_yr]
    df_prev   = df[df["Year"] == prev_yr]

    total_waste_last = df_last["Total Waste (Tons)"].sum()
    total_waste_prev = df_prev["Total Waste (Tons)"].sum()
    econ_last        = df_last["Economic Loss (Million $)"].sum()
    carbon_last      = df_last["Carbon_Footprint_kgCO2e"].sum()
    countries_n      = df_last["Country"].nunique()

    waste_chg = (total_waste_last - total_waste_prev) / (total_waste_prev + 1) * 100

    cols = st.columns(4)
    with cols[0]: kpi(f"Toplam Atık ({last_yr})", fmt(total_waste_last,"ton"), waste_chg, "#c62828")
    with cols[1]: kpi(f"Ekonomik Kayıp ({last_yr})", fmt(econ_last,"M$"), color="#f57c00")
    with cols[2]: kpi(f"Karbon ({last_yr})", fmt(carbon_last,"kgCO2e"), color="#6a1b9a")
    with cols[3]: kpi("Kapsanan Ülke", str(countries_n), color="#1565c0")

    st.markdown("")

    # ── Küresel atık trendi ─────────────────────────────────────────────
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📈 Küresel Atık Trendi")
        trend = df.groupby("Year")["Total Waste (Tons)"].sum().reset_index()
        fig = px.area(trend, x="Year", y="Total Waste (Tons)",
                      color_discrete_sequence=["#00796b"],
                      template="plotly_white", height=300)
        fig.update_traces(fillcolor="rgba(0,121,107,.15)")
        fig.update_layout(margin=dict(t=10,b=20,l=10,r=10))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("🌍 Kıta Bazlı Atık Payı")
        by_cont = df_last.groupby("Continent")["Total Waste (Tons)"].sum().reset_index()
        fig2 = px.pie(by_cont, values="Total Waste (Tons)", names="Continent",
                      color_discrete_sequence=px.colors.qualitative.Set2,
                      template="plotly_white", height=300)
        fig2.update_layout(margin=dict(t=10,b=20,l=10,r=10))
        st.plotly_chart(fig2, use_container_width=True)

    # ── Harita ─────────────────────────────────────────────────────────
    st.subheader("🗺️ Ülke Bazlı Atık Haritası")
    map_df = df_last.groupby(["Country","ISO3"])["Total Waste (Tons)"].sum().reset_index()
    fig_map = px.choropleth(map_df, locations="ISO3",
                            color="Total Waste (Tons)",
                            hover_name="Country",
                            color_continuous_scale="YlOrRd",
                            template="plotly_white", height=420)
    fig_map.update_layout(margin=dict(t=0,b=0,l=0,r=0))
    st.plotly_chart(fig_map, use_container_width=True)

    # ── Veri kaynakları ──────────────────────────────────────────────────
    st.markdown("**📚 Veri Kaynakları**")
    for s in meta.get("sources",[]):
        st.markdown(f'<span class="source-badge">✓ {s}</span>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SAYFA 2: VERİ ANALİZİ
# ─────────────────────────────────────────────────────────────────────────────
def page_analysis(df):
    section("Veri Analizi", "Gerçek ölçüm verilerine dayalı keşifsel analiz", "📊")

    # Filtreler
    fc1, fc2, fc3 = st.columns(3)
    continents = ["Tümü"] + sorted(df["Continent"].dropna().unique().tolist())
    sel_cont   = fc1.selectbox("Kıta", continents)
    years      = sorted(df["Year"].unique().tolist())
    sel_yr     = fc2.slider("Yıl", int(min(years)), int(max(years)), (int(min(years)), int(max(years))))
    categories = ["Tümü"] + sorted(df["Food Category"].dropna().unique().tolist())
    sel_cat    = fc3.selectbox("Kategori", categories)

    dff = df[df["Year"].between(sel_yr[0], sel_yr[1])]
    if sel_cont != "Tümü": dff = dff[dff["Continent"] == sel_cont]
    if sel_cat  != "Tümü": dff = dff[dff["Food Category"] == sel_cat]

    st.caption(f"Filtreli kayıt: {len(dff):,}")

    t1, t2, t3, t4 = st.tabs(["Genel Bakış","Kategori","Ülke Sıralaması","Dağılım"])

    with t1:
        c1,c2 = st.columns(2)
        with c1:
            by_yr = dff.groupby("Year")["Total Waste (Tons)"].sum().reset_index()
            fig = px.bar(by_yr, x="Year", y="Total Waste (Tons)",
                         color_discrete_sequence=["#2e7d32"], template="plotly_white",
                         title="Yıllık Toplam Atık")
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            by_yr2 = dff.groupby("Year")["Economic Loss (Million $)"].sum().reset_index()
            fig2 = px.line(by_yr2, x="Year", y="Economic Loss (Million $)",
                           markers=True, color_discrete_sequence=["#f57c00"],
                           template="plotly_white", title="Yıllık Ekonomik Kayıp")
            st.plotly_chart(fig2, use_container_width=True)

    with t2:
        cat_agg = dff.groupby("Food Category").agg(
            Atık=("Total Waste (Tons)","sum"),
            Ekonomi=("Economic Loss (Million $)","sum"),
            Karbon=("Carbon_Footprint_kgCO2e","sum"),
        ).reset_index().sort_values("Atık", ascending=False)
        fig = px.bar(cat_agg, x="Food Category", y="Atık",
                     color="Karbon", color_continuous_scale="Reds",
                     template="plotly_white", height=380,
                     title="Kategori Bazlı Atık & Karbon")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(cat_agg.style.format({"Atık":"{:,.0f}","Ekonomi":"{:,.1f}","Karbon":"{:,.0f}"}),
                     use_container_width=True)

    with t3:
        top_n  = st.slider("Kaç ülke?", 10, 50, 20)
        target = st.selectbox("Metrik", TARGETS)
        top_df = dff.groupby("Country")[target].sum().nlargest(top_n).reset_index()
        fig = px.bar(top_df, x=target, y="Country", orientation="h",
                     color=target, color_continuous_scale="YlOrRd",
                     template="plotly_white", height=500,
                     title=f"Top {top_n} Ülke – {target}")
        fig.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True)

    with t4:
        col_x = st.selectbox("X ekseni", TARGETS, index=0)
        col_y = st.selectbox("Y ekseni", TARGETS, index=1)
        samp  = dff.groupby(["Country","Continent"])[list(set([col_x,col_y]))].sum().reset_index()
        fig = px.scatter(samp, x=col_x, y=col_y, color="Continent",
                         hover_name="Country", size_max=18,
                         template="plotly_white", height=420,
                         title="Dağılım Grafiği")
        st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# SAYFA 3: ÜLKE KARŞILAŞTIRMA
# ─────────────────────────────────────────────────────────────────────────────
def page_country(df):
    section("Ülke Karşılaştırma", "Seçilen ülkeler arasında derinlemesine karşılaştırma", "🌍")

    all_countries = sorted(df["Country"].unique().tolist())
    defaults = ["Turkey","Germany","India","USA","China","Brazil"] if "Turkey" in all_countries else all_countries[:6]
    sel = st.multiselect("Ülke seçin (en fazla 10)", all_countries, default=defaults[:6])
    if not sel:
        st.info("En az bir ülke seçin.")
        return

    dff = df[df["Country"].isin(sel)]
    target = st.selectbox("Metrik", TARGETS)

    c1,c2 = st.columns(2)
    with c1:
        tr = dff.groupby(["Country","Year"])[target].sum().reset_index()
        fig = px.line(tr, x="Year", y=target, color="Country",
                      markers=True, template="plotly_white", height=360,
                      title="Yıllık Trend")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        last_yr = df["Year"].max()
        bar_df  = dff[dff["Year"]==last_yr].groupby("Country")[target].sum().reset_index()
        fig2 = px.bar(bar_df.sort_values(target), x=target, y="Country",
                      orientation="h", color=target, color_continuous_scale="Blues",
                      template="plotly_white", height=360, title=f"Son Yıl ({last_yr})")
        st.plotly_chart(fig2, use_container_width=True)

    # Kategori heat-map
    st.subheader("🔥 Kategori × Ülke Isı Haritası")
    hm = dff.groupby(["Country","Food Category"])[target].sum().reset_index()
    hm_pivot = hm.pivot(index="Food Category", columns="Country", values=target).fillna(0)
    fig3 = px.imshow(hm_pivot, color_continuous_scale="YlOrRd",
                     template="plotly_white", height=380, aspect="auto",
                     title=f"{target} – Kategori × Ülke")
    st.plotly_chart(fig3, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# SAYFA 4: MODEL PERFORMANSI
# ─────────────────────────────────────────────────────────────────────────────
def page_model(perf, meta):
    section("Model Performansı", "Gerçek veri üzerinde eğitilmiş modellerin metrikleri", "🤖")

    # Üst KPI'lar – JSON'dan
    c1,c2,c3,c4 = st.columns(4)
    avg_r2 = perf.get("average_test_r2",0)
    avg_of = perf.get("average_overfit",0)
    with c1: kpi("Ort. Test R²",     f"{avg_r2:.4f}", color="#2e7d32")
    with c2: kpi("Model Tipi",       perf.get("model_type","—"), color="#1565c0")
    with c3: kpi("Kalite Etiketi",   perf.get("quality_label","—"), color="#00796b")
    with c4: kpi("Ort. Overfit",     f"{avg_of:.4f}", color="#f57c00")

    st.markdown("")

    # Hedef bazlı detay
    tgt_data = perf.get("targets",{})
    rows = []
    for tgt, info in tgt_data.items():
        rows.append({
            "Hedef":       tgt,
            "Train R²":    info["train"]["r2"],
            "Test R²":     info["test"]["r2"],
            "CV Ort.":     info.get("cv_mean","—"),
            "Overfit":     info.get("overfit","—"),
            "Test RMSE":   info["test"].get("rmse","—"),
            "Test MAPE":   info["test"].get("mape","—"),
        })
    df_tbl = pd.DataFrame(rows)
    st.dataframe(df_tbl.style
        .format({"Train R²":"{:.4f}","Test R²":"{:.4f}","CV Ort.":"{:.4f}","Overfit":"{:.4f}"})
        .background_gradient(subset=["Test R²"], cmap="Greens"),
        use_container_width=True)

    # Radar grafiği
    st.subheader("🎯 Hedef Karşılaştırma")
    cats = ["Train R²","Test R²","CV Ort."]
    fig = go.Figure()
    for tgt, info in tgt_data.items():
        vals = [info["train"]["r2"], info["test"]["r2"], info.get("cv_mean",0)]
        fig.add_trace(go.Scatterpolar(r=vals, theta=cats, fill="toself", name=tgt))
    fig.update_layout(polar=dict(radialaxis=dict(range=[0.95,1])),
                      template="plotly_white", height=380)
    st.plotly_chart(fig, use_container_width=True)

    # Veri meta bilgisi
    with st.expander("📋 Veri & Model Detayları"):
        st.write(f"**Ülke sayısı:** {perf.get('n_countries')}")
        st.write(f"**Yıl aralığı:** {perf.get('year_range')}")
        st.write(f"**Toplam gözlem:** {perf.get('n_rows',0):,}")
        st.write(f"**Eğitim tarihi:** {perf.get('generated_at','—')[:10]}")
        st.write("**Hiperparametreler:**")
        st.json(perf.get("hyperparameters",{}))
        st.write("**Veri kaynakları:**")
        for s in perf.get("data_source",[]):
            st.markdown(f"- {s}")

# ─────────────────────────────────────────────────────────────────────────────
# SAYFA 5: GELECEK TAHMİNLERİ
# ─────────────────────────────────────────────────────────────────────────────
def page_forecasts(fc_df, df):
    section("Gelecek Tahminleri", "Makine öğrenmesi modeli ile 2024-2030 projeksiyonu", "🔮")

    all_countries = sorted(fc_df["Country"].unique().tolist())
    sel_country   = st.selectbox("Ülke seçin", all_countries,
                                  index=all_countries.index("Turkey") if "Turkey" in all_countries else 0)
    sel_target    = st.selectbox("Metrik", TARGETS)

    # Geçmiş + tahmin birleştir
    hist = df[df["Country"] == sel_country].groupby("Year")[sel_target].sum().reset_index()
    hist["Tür"] = "Gerçek"
    fut  = fc_df[fc_df["Country"] == sel_country].groupby("Year")[sel_target].sum().reset_index()
    fut["Tür"] = "Tahmin"
    combined = pd.concat([hist, fut], ignore_index=True)

    fig = go.Figure()
    h = combined[combined["Tür"]=="Gerçek"]
    f = combined[combined["Tür"]=="Tahmin"]
    fig.add_trace(go.Scatter(x=h["Year"], y=h[sel_target], mode="lines+markers",
                             name="Gerçek", line=dict(color="#2e7d32", width=2.5)))
    fig.add_trace(go.Scatter(x=f["Year"], y=f[sel_target], mode="lines+markers",
                             name="Tahmin", line=dict(color="#f57c00", width=2.5, dash="dash")))
    fig.add_vrect(x0=2023.5, x1=2030.5, fillcolor="#fff3e0", opacity=0.4, line_width=0)
    fig.update_layout(template="plotly_white", height=400,
                      title=f"{sel_country} — {sel_target}",
                      xaxis_title="Yıl", yaxis_title=sel_target)
    st.plotly_chart(fig, use_container_width=True)

    # Tablo
    st.subheader("📋 Tahmin Değerleri")
    st.dataframe(fut[["Year",sel_target]].style.format({sel_target:"{:,.0f}"}),
                 use_container_width=True)

    # Büyüme hesapla
    if len(fut) >= 2:
        pct_chg = (fut[sel_target].iloc[-1] - fut[sel_target].iloc[0]) / (fut[sel_target].iloc[0]+1) * 100
        col_pct = "🔴" if pct_chg > 0 else "🟢"
        st.metric(f"{col_pct} 2024→2030 Değişim", f"{pct_chg:+.1f}%")

    # Tüm ülkeler 2030 karşılaştırması
    st.subheader("🌐 2030 Ülke Sıralaması")
    top_n = st.slider("Kaç ülke?", 10, 50, 20)
    fc_2030 = fc_df[fc_df["Year"]==2030].groupby(["Country","ISO3"])[sel_target].sum().nlargest(top_n).reset_index()
    fig2 = px.choropleth(fc_2030, locations="ISO3", color=sel_target,
                         hover_name="Country", color_continuous_scale="YlOrRd",
                         template="plotly_white", height=380,
                         title=f"2030 Tahmin — {sel_target}")
    st.plotly_chart(fig2, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# SAYFA 6: HEDEF SİMÜLATÖRÜ
# ─────────────────────────────────────────────────────────────────────────────
def page_simulator(df, fc_df):
    section("Hedef Simülatörü", "Politika senaryolarını simüle edin", "🎯")

    all_countries = sorted(df["Country"].unique().tolist())
    sel_country   = st.selectbox("Ülke", all_countries,
                                  index=all_countries.index("Turkey") if "Turkey" in all_countries else 0)
    sel_target    = st.selectbox("Hedef metrik", TARGETS)

    c1, c2 = st.columns(2)
    waste_red = c1.slider("Atık Azaltım Politikası (%)", 0, 50, 20)
    tech_ada  = c2.slider("Teknoloji Adaptasyon Hızı (%)", 0, 50, 15)

    # Tahmin verisini al
    fc = fc_df[fc_df["Country"]==sel_country].groupby("Year")[sel_target].sum().reset_index()
    if fc.empty:
        st.warning("Bu ülke için tahmin verisi yok.")
        return

    reduction = 1 - (waste_red + tech_ada * 0.5) / 100
    fc["Simülasyon"] = (fc[sel_target] * reduction).clip(lower=0)
    fc["Baz Senaryo"]= fc[sel_target]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=fc["Year"], y=fc["Baz Senaryo"], name="Baz Senaryo",
                             line=dict(color="#f57c00", dash="dash")))
    fig.add_trace(go.Scatter(x=fc["Year"], y=fc["Simülasyon"], name="Politika Senaryosu",
                             line=dict(color="#2e7d32"), fill="tozeroy",
                             fillcolor="rgba(46,125,50,.08)"))
    fig.update_layout(template="plotly_white", height=380,
                      title=f"{sel_country} — {sel_target} Senaryosu")
    st.plotly_chart(fig, use_container_width=True)

    savings = (fc["Baz Senaryo"].sum() - fc["Simülasyon"].sum())
    st.success(f"✅ Toplam tasarruf (2024-2030): **{savings:,.0f}** {sel_target.split('(')[-1].replace(')','').strip()}")

# ─────────────────────────────────────────────────────────────────────────────
# SAYFA 7: SHAP & ÖNEMLİLİK
# ─────────────────────────────────────────────────────────────────────────────
def page_shap():
    section("SHAP & Özellik Önemi", "Model kararlarını açıklayan özellik analizi", "📈")

    sel_target = st.selectbox("Hedef", TARGETS)
    shap_df    = load_shap(sel_target)

    if shap_df is None or shap_df.empty:
        st.warning("SHAP verisi bulunamadı. Pipeline'ı yeniden çalıştırın.")
        return

    top_n = st.slider("Kaç özellik gösterilsin?", 5, 30, 15)
    plot_df = shap_df.head(top_n).sort_values("importance")

    fig = px.bar(plot_df, x="importance", y="feature", orientation="h",
                 color="importance", color_continuous_scale="Greens",
                 template="plotly_white", height=max(350, top_n*26),
                 title=f"Özellik Önemi — {sel_target}")
    fig.update_layout(showlegend=False, margin=dict(l=10,r=10,t=40,b=20))
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 Tüm özellikler"):
        st.dataframe(shap_df.style.format({"importance":"{:.6f}"}), use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# SAYFA 8: RİSK & FIRSAT
# ─────────────────────────────────────────────────────────────────────────────
def page_risk(df):
    section("Risk & Fırsat", "Ülkeleri atık ve ekonomik etki boyutlarında konumlandır", "⚠️")

    last_yr = df["Year"].max()
    agg = df[df["Year"]==last_yr].groupby(["Country","Continent"]).agg(
        Waste  =("Total Waste (Tons)","sum"),
        Econ   =("Economic Loss (Million $)","sum"),
        Carbon =("Carbon_Footprint_kgCO2e","sum"),
        Score  =("Sustainability_Score","mean"),
    ).reset_index()

    # Normalize
    for col in ["Waste","Econ","Carbon","Score"]:
        rng = agg[col].max() - agg[col].min()
        agg[f"{col}_N"] = (agg[col] - agg[col].min()) / (rng + 1e-9)

    agg["Risk"]    = (agg["Waste_N"] + agg["Econ_N"]) / 2
    agg["Firsat"]  = 1 - agg["Score_N"]

    fig = px.scatter(agg, x="Risk", y="Firsat",
                     size="Econ", color="Continent",
                     hover_name="Country", size_max=30,
                     template="plotly_white", height=480,
                     title=f"Risk × Fırsat Matrisi ({last_yr})",
                     labels={"Risk":"Risk Skoru","Firsat":"İyileştirme Potansiyeli"})
    fig.add_hline(y=0.5, line_dash="dot", line_color="gray", opacity=0.5)
    fig.add_vline(x=0.5, line_dash="dot", line_color="gray", opacity=0.5)
    st.plotly_chart(fig, use_container_width=True)

    high_risk = agg[agg["Risk"]>0.6].nlargest(10,"Risk")[["Country","Risk","Firsat","Econ"]]
    st.subheader("🔴 Yüksek Riskli Ülkeler (Top 10)")
    st.dataframe(high_risk.style.format({"Risk":"{:.2f}","Firsat":"{:.2f}","Econ":"{:,.1f}"}),
                 use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# SAYFA 9: RAPOR
# ─────────────────────────────────────────────────────────────────────────────
def page_report(df, perf, meta):
    section("Rapor", "Otomatik oluşturulan veri odaklı rapor", "📄")

    last_yr  = df["Year"].max()
    avg_r2   = perf.get("average_test_r2",0)
    n        = meta.get("n_rows",0)
    ctrs     = meta.get("countries",0)
    years    = meta.get("years",[2010,2023])
    tw       = df[df["Year"]==last_yr]["Total Waste (Tons)"].sum()
    el       = df[df["Year"]==last_yr]["Economic Loss (Million $)"].sum()
    cf       = df[df["Year"]==last_yr]["Carbon_Footprint_kgCO2e"].sum()

    report_md = f"""
# EcoLense Intelligence — Analiz Raporu
**Oluşturulma:** {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")}

---

## 1. Veri Seti Özeti
| Metrik | Değer |
|--------|-------|
| Kayıt sayısı | {n:,} |
| Ülke | {ctrs} |
| Yıl aralığı | {years[0]}–{years[1]} |
| Gıda kategorisi | {df["Food Category"].nunique()} |
| Kıta | {df["Continent"].nunique()} |

## 2. {last_yr} Temel Göstergeler
- **Toplam atık:** {tw:,.0f} ton
- **Ekonomik kayıp:** {el:,.1f} Milyon USD
- **Karbon ayak izi:** {cf:,.0f} kgCO2e

## 3. Model Performansı
- **Model:** {perf.get("model_type")}
- **Ortalama Test R²:** {avg_r2:.4f}
- **Kalite:** {perf.get("quality_label")}
- **CV folds:** {perf.get("cv_folds")}

### Hedef Bazlı Sonuçlar
{"".join([f"- **{t}** → Test R²: {info['test']['r2']:.4f} | Overfit: {info.get('overfit',0):.4f}\\n" for t,info in perf.get("targets",{}).items()])}

## 4. Veri Kaynakları
{"".join([f"- {s}\\n" for s in meta.get("sources",[])])}
"""

    st.markdown(report_md)
    st.download_button("⬇️ Raporu İndir (.md)", report_md.encode("utf-8"),
                       file_name="ecolense_report.md", mime="text/markdown")

# ─────────────────────────────────────────────────────────────────────────────
# ANA UYGULAMA
# ─────────────────────────────────────────────────────────────────────────────
def main():
    # Veriyi yükle
    try:
        df   = load_processed()
        meta = load_meta()
        perf = load_perf()
        fc   = load_forecasts()
    except FileNotFoundError as e:
        st.error(f"⛔ Dosya bulunamadı: {e}")
        st.info("Lütfen önce `python run_pipeline.py` komutunu çalıştırın.")
        st.stop()

    page = sidebar()

    if   page == "🏠 Ana Sayfa":              page_home(df, meta, perf)
    elif page == "📊 Veri Analizi":           page_analysis(df)
    elif page == "🌍 Ülke Karşılaştırma":    page_country(df)
    elif page == "🤖 Model Performansı":     page_model(perf, meta)
    elif page == "🔮 Gelecek Tahminleri":    page_forecasts(fc, df)
    elif page == "🎯 Hedef Simülatörü":      page_simulator(df, fc)
    elif page == "📈 SHAP & Önem":           page_shap()
    elif page == "⚠️ Risk & Fırsat":         page_risk(df)
    elif page == "📄 Rapor":                 page_report(df, perf, meta)

if __name__ == "__main__":
    main()
