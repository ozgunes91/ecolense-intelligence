#!/usr/bin/env python3
"""
03_generate_forecasts.py
========================
Eğitilmiş modelleri kullanarak 2024-2030 tahminleri üretir.

Çıktı: outputs/forecasts/forecasts.csv
"""

import pandas as pd
import numpy as np
import json, os, joblib, warnings
warnings.filterwarnings("ignore")

DATA_PATH     = "data/processed.csv"
MODEL_DIR     = "models"
OUTPUT_DIR    = "outputs"
FORECAST_DIR  = os.path.join(OUTPUT_DIR, "forecasts")
FORECAST_PATH = os.path.join(FORECAST_DIR, "forecasts.csv")

TARGETS = [
    "Total Waste (Tons)",
    "Economic Loss (Million $)",
    "Carbon_Footprint_kgCO2e",
]

FORECAST_YEARS = list(range(2024, 2031))

# FAO Gıda Fiyat Endeksi – veri setinde 2014-16=1.00 ölçeğine normalize edilir.
FAO_FFPI_PROJ = {2024:1.21, 2025:1.18, 2026:1.15, 2027:1.13, 2028:1.11, 2029:1.09, 2030:1.07}

# IMF WEO 2024 büyüme tahminleri
IMF_GROWTH_PROJ = {2024:3.2, 2025:3.2, 2026:3.1, 2027:3.1, 2028:3.0, 2029:3.0, 2030:2.9}

TREND_LIMITS = {
    "Total Waste (Tons)": (-0.025, 0.045),
    "Economic Loss (Million $)": (-0.035, 0.050),
    "Carbon_Footprint_kgCO2e": (-0.030, 0.045),
}

MACRO_WEIGHTS = {
    "Total Waste (Tons)": {"pop": 0.55, "gdp": 0.10, "price": -0.05},
    "Economic Loss (Million $)": {"pop": 0.30, "gdp": 0.55, "price": 0.45},
    "Carbon_Footprint_kgCO2e": {"pop": 0.50, "gdp": 0.12, "price": -0.03},
}


def load_model(target):
    safe  = target.replace(" ","_").replace("(","").replace(")","").replace("$","USD").replace("/","_")
    path  = os.path.join(MODEL_DIR, f"model_{safe}.pkl")
    obj   = joblib.load(path)
    return obj["model"], obj["features"]


def build_future_rows(df):
    """2023 son gözlemlerini temel alarak 2024-2030 satırları oluştur."""
    last = df[df["Year"] == df["Year"].max()].copy()
    rows = []
    for year in FORECAST_YEARS:
        proj = last.copy()
        proj["Year"] = year
        dt = year - 2023
        growth = IMF_GROWTH_PROJ.get(year, 3.0) / 100

        # GDP büyümesi (gelir grubuna göre farklı)
        def gdp_factor(row):
            g = row.get("GDP_Per_Capita_USD", 5000)
            if g >= 13000:
                annual = growth * 0.9
            elif g >= 4000:
                annual = growth * 1.1
            else:
                annual = growth * 1.3
            return (1 + annual) ** dt
        proj["GDP_Per_Capita_USD"] = proj["GDP_Per_Capita_USD"] * proj.apply(gdp_factor, axis=1)

        # Nüfus büyümesi
        def pop_factor(row):
            inc = row.get("Income_Group_Enc", 2)
            rates = {0:0.004, 1:0.010, 2:0.020, 3:0.028}
            return (1 + rates.get(int(inc), 0.012)) ** dt
        proj["Population (Million)"] = proj["Population (Million)"] * proj.apply(pop_factor, axis=1)

        # FAO FFPI
        proj["FAO_Food_Price_Index"] = FAO_FFPI_PROJ.get(year, 1.1)

        # Zaman özellikleri
        proj["Years_from_2010"] = year - 2010
        proj["Year_Trend"]      = year - 2010
        proj["Year_Norm"]       = (year - 2010) / 13
        proj["Pandemic_Flag"]   = 0
        proj["Pandemic_Indicator"] = 0
        proj["Year_Sin"]        = np.sin(2 * np.pi * (year - 2010) / 5)
        proj["Year_Cos"]        = np.cos(2 * np.pi * (year - 2010) / 5)
        proj["Year_Cycle"]      = np.sin(2 * np.pi * (year - 2010) / 5)
        proj["Year_Cycle_Cos"]  = np.cos(2 * np.pi * (year - 2010) / 5)

        # Log özellikler güncelle
        proj["Log_Population"]  = np.log1p(proj["Population (Million)"].clip(lower=0.001))
        proj["Log_GDP_PC"]      = np.log1p(proj["GDP_Per_Capita_USD"].clip(lower=1))

        # Modelde kullanılan dışsal etkileşimleri de yıl yıl güncelle
        proj["Population_Material_Interaction"] = (
            proj["Population (Million)"] * proj["Material_Footprint_Per_Capita"]
        )
        proj["Year_Population_Interaction"] = proj["Years_from_2010"] * proj["Population (Million)"]
        proj["GDP_Per_Capita_Proxy"] = proj["GDP_Per_Capita_USD"] / 1000
        proj["Pop_MatFP"] = proj["Population (Million)"] * proj["Material_Footprint_Per_Capita"]

        # Kayan ortalamalar – son 3 yıl ortalaması
        proj["Total Waste (Tons)_MA3"]          = last["Total Waste (Tons)"]
        proj["Economic Loss (Million $)_MA3"]   = last["Economic Loss (Million $)"]
        proj["Carbon_Footprint_kgCO2e_MA3"]     = last["Carbon_Footprint_kgCO2e"]

        proj["Forecast_Year"] = True
        rows.append(proj)

    return pd.concat(rows, ignore_index=True)


def _entity_trends(df, target):
    """Son altı tarihsel yılı kullanarak ülke-kategori bazlı kontrollü yıllık trend çıkar."""
    max_year = int(df["Year"].max())
    recent = df[df["Year"] >= max_year - 5].copy()
    low, high = TREND_LIMITS[target]

    def trend_from_group(group):
        group = group.sort_values("Year")
        first = float(group[target].iloc[0])
        last = float(group[target].iloc[-1])
        years = max(int(group["Year"].iloc[-1] - group["Year"].iloc[0]), 1)
        if first <= 0 or last <= 0:
            return 0.0
        trend = (last / first) ** (1 / years) - 1
        if not np.isfinite(trend):
            return 0.0
        return float(np.clip(trend, low, high))

    entity = (
        recent.groupby(["Country", "Food Category"], as_index=False)
              .apply(lambda g: trend_from_group(g), include_groups=False)
              .rename(columns={None: "entity_trend"})
    )
    if "entity_trend" not in entity.columns:
        entity.columns = ["Country", "Food Category", "entity_trend"]

    category_year = recent.groupby(["Food Category", "Year"], as_index=False)[target].sum()
    category = (
        category_year.groupby("Food Category", as_index=False)
                     .apply(lambda g: trend_from_group(g), include_groups=False)
                     .rename(columns={None: "category_trend"})
    )
    if "category_trend" not in category.columns:
        category.columns = ["Food Category", "category_trend"]

    global_year = recent.groupby("Year", as_index=False)[target].sum()
    global_trend = trend_from_group(global_year)

    return entity, category, global_trend


def apply_projection_dynamics(future, target):
    """Ağaç modelinin sabit yaprak çıktısını tarihsel trend ve makro varsayımla yumuşat."""
    pred_col = f"pred_{target}"
    key_cols = ["Country", "Food Category"]
    hist = pd.read_csv(DATA_PATH)
    entity, category, global_trend = _entity_trends(hist, target)
    last_year = int(hist["Year"].max())
    anchor = (
        hist[hist["Year"] == last_year]
        .groupby(key_cols, as_index=False)[target]
        .mean()
        .rename(columns={target: "hist_anchor"})
    )
    low, high = TREND_LIMITS[target]
    weights = MACRO_WEIGHTS[target]

    work = future.sort_values(key_cols + ["Year"]).copy()
    work["_row_id"] = work.index
    work = work.merge(entity, on=key_cols, how="left")
    work = work.merge(category, on="Food Category", how="left")
    work = work.merge(anchor, on=key_cols, how="left")
    work["entity_trend"] = work["entity_trend"].fillna(work["category_trend"]).fillna(global_trend)
    work["category_trend"] = work["category_trend"].fillna(global_trend)
    work["annual_trend"] = (
        0.65 * work["entity_trend"] +
        0.25 * work["category_trend"] +
        0.10 * global_trend
    ).clip(low, high)

    group = work.groupby(key_cols, sort=False)
    base_pred_raw = group[pred_col].transform("first")
    anchor_2024 = work["hist_anchor"].fillna(group[pred_col].transform("median")).clip(lower=0)
    anchor_2024 = anchor_2024 * (1 + work["annual_trend"]).clip(0.85, 1.15)
    base_pred = base_pred_raw.where(base_pred_raw > 0, anchor_2024).replace(0, np.nan)
    base_pop = group["Population (Million)"].transform("first").clip(lower=0.001)
    base_gdp = group["GDP_Per_Capita_USD"].transform("first").clip(lower=1)
    base_price = group["FAO_Food_Price_Index"].transform("first").clip(lower=0.001)

    dt = (work["Year"] - FORECAST_YEARS[0]).clip(lower=0)
    raw_ratio = (work[pred_col] / base_pred).replace([np.inf, -np.inf], np.nan).fillna(1.0)
    trend_ratio = (1 + work["annual_trend"]) ** dt
    macro_ratio = (
        (work["Population (Million)"].clip(lower=0.001) / base_pop) ** weights["pop"] *
        (work["GDP_Per_Capita_USD"].clip(lower=1) / base_gdp) ** weights["gdp"] *
        (work["FAO_Food_Price_Index"].clip(lower=0.001) / base_price) ** weights["price"]
    ).replace([np.inf, -np.inf], np.nan).fillna(1.0)

    blended_ratio = (
        0.50 * raw_ratio.clip(0.75, 1.35) +
        0.35 * trend_ratio.clip(0.75, 1.35) +
        0.15 * macro_ratio.clip(0.80, 1.25)
    )
    adjusted = (base_pred.fillna(work[pred_col]) * blended_ratio).clip(lower=0)

    future.loc[work["_row_id"].to_numpy(), pred_col] = adjusted.to_numpy()
    constant_share = (
        future.groupby(key_cols)[pred_col].nunique(dropna=False).le(1).mean()
    )
    print(f"    Dinamik projeksiyon: sabit seri oranı %{constant_share * 100:.1f}")
    return future


def main():
    print("=" * 55)
    print("  TAHMİN ÜRETİMİ  (2024-2030)")
    print("=" * 55)

    df = pd.read_csv(DATA_PATH)
    df["Forecast_Year"] = False

    future = build_future_rows(df)
    records = []

    for target in TARGETS:
        model, feats = load_model(target)
        available = [f for f in feats if f in future.columns]
        missing   = [f for f in feats if f not in future.columns]
        if missing:
            print(f"  ⚠️  {target}: {len(missing)} özellik eksik, sıfır ile dolduruldu")
            for col in missing:
                future[col] = 0.0

        X = future[feats].fillna(0).values
        future[f"pred_{target}"] = model.predict(X)
        future = apply_projection_dynamics(future, target)
        print(f"  ✅ {target}: {FORECAST_YEARS[0]}-{FORECAST_YEARS[-1]} tahminleri üretildi")

    # Uzun format (ülke × yıl × kategori × hedef)
    id_cols   = ["Country","ISO3","Year","Food Category","Continent",
                 "Hemisphere","Income_Group","Population (Million)","GDP_Per_Capita_USD"]
    pred_cols = [f"pred_{t}" for t in TARGETS]

    out = future[id_cols + pred_cols].rename(columns={
        f"pred_{TARGETS[0]}": TARGETS[0],
        f"pred_{TARGETS[1]}": TARGETS[1],
        f"pred_{TARGETS[2]}": TARGETS[2],
    })

    # Negatif tahminleri sıfırla ve kişi başı/kompozit skorları ekle
    for t in TARGETS:
        out[t] = out[t].clip(lower=0)

    pop_people = (out["Population (Million)"].clip(lower=0.001) * 1_000_000)
    out["Waste_Per_Capita_kg"] = out["Total Waste (Tons)"] * 1000 / pop_people
    out["Economic_Loss_Per_Capita_USD"] = out["Economic Loss (Million $)"] / out["Population (Million)"].clip(lower=0.001)
    out["Carbon_Per_Capita_kgCO2e"] = out["Carbon_Footprint_kgCO2e"] / pop_people

    hist = pd.read_csv(DATA_PATH)
    ref = hist.groupby(["Country", "Year"], as_index=False).agg({
        "Total Waste (Tons)": "sum",
        "Economic Loss (Million $)": "sum",
        "Carbon_Footprint_kgCO2e": "sum",
        "Population (Million)": "first",
    })
    ref_pop = ref["Population (Million)"].clip(lower=0.001) * 1_000_000
    ref_waste_pc = ref["Total Waste (Tons)"] * 1000 / ref_pop
    ref_loss_pc = ref["Economic Loss (Million $)"] / ref["Population (Million)"].clip(lower=0.001)
    ref_carbon_pc = ref["Carbon_Footprint_kgCO2e"] / ref_pop

    def inverse_score(values, reference):
        low = float(reference.quantile(0.05))
        high = float(reference.quantile(0.95))
        if high <= low:
            high = float(reference.max()) or 1.0
            low = float(reference.min())
        return (1 - (values - low) / (high - low + 1e-9)).clip(0.05, 0.98)

    country_year = out.groupby(["Country", "Year"], as_index=False).agg({
        "Total Waste (Tons)": "sum",
        "Economic Loss (Million $)": "sum",
        "Carbon_Footprint_kgCO2e": "sum",
        "Population (Million)": "first",
    })
    cy_pop_m = country_year["Population (Million)"].clip(lower=0.001)
    cy_pop_people = cy_pop_m * 1_000_000
    country_year["Waste_Per_Capita_kg"] = country_year["Total Waste (Tons)"] * 1000 / cy_pop_people
    country_year["Economic_Loss_Per_Capita_USD"] = country_year["Economic Loss (Million $)"] / cy_pop_m
    country_year["Carbon_Per_Capita_kgCO2e"] = country_year["Carbon_Footprint_kgCO2e"] / cy_pop_people
    country_year["Sustainability_Score"] = (
        0.40 * inverse_score(country_year["Waste_Per_Capita_kg"], ref_waste_pc)
        + 0.30 * inverse_score(country_year["Economic_Loss_Per_Capita_USD"], ref_loss_pc)
        + 0.30 * inverse_score(country_year["Carbon_Per_Capita_kgCO2e"], ref_carbon_pc)
    ) * 100
    out = out.merge(country_year[["Country", "Year", "Sustainability_Score"]], on=["Country", "Year"], how="left")

    os.makedirs(FORECAST_DIR, exist_ok=True)
    out.to_csv(FORECAST_PATH, index=False)
    print(f"\n  ✅ {FORECAST_PATH}  ({len(out):,} satır)")
    print(f"  Ülke: {out['Country'].nunique()} | Yıl: {sorted(out['Year'].unique().tolist())}")


if __name__ == "__main__":
    main()
