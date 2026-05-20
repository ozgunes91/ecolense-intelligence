#!/usr/bin/env python3
"""
03_generate_forecasts.py
========================
Eğitilmiş modelleri kullanarak 2024-2030 tahminleri üretir.

Çıktı: forecasts.csv
"""

import pandas as pd
import numpy as np
import json, os, joblib, warnings
warnings.filterwarnings("ignore")

DATA_PATH     = "data/processed.csv"
MODEL_DIR     = "models"
FORECAST_PATH = "forecasts.csv"

TARGETS = [
    "Total Waste (Tons)",
    "Economic Loss (Million $)",
    "Carbon_Footprint_kgCO2e",
]

FORECAST_YEARS = list(range(2024, 2031))

# FAO Gıda Fiyat Endeksi – 2024-2030 IMF/FAO projeksiyon (2014-16=100)
FAO_FFPI_PROJ = {2024:121, 2025:118, 2026:115, 2027:113, 2028:111, 2029:109, 2030:107}

# IMF WEO 2024 büyüme tahminleri
IMF_GROWTH_PROJ = {2024:3.2, 2025:3.2, 2026:3.1, 2027:3.1, 2028:3.0, 2029:3.0, 2030:2.9}


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
            if g >= 13000:   return 1 + growth * 0.9
            elif g >= 4000:  return 1 + growth * 1.1
            else:            return 1 + growth * 1.3
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
        proj["Year_Sin"]        = np.sin(2 * np.pi * (year - 2010) / 5)
        proj["Year_Cos"]        = np.cos(2 * np.pi * (year - 2010) / 5)

        # Log özellikler güncelle
        proj["Log_Population"]  = np.log1p(proj["Population (Million)"].clip(lower=0.001))
        proj["Log_GDP_PC"]      = np.log1p(proj["GDP_Per_Capita_USD"].clip(lower=1))

        # Kayan ortalamalar – son 3 yıl ortalaması
        proj["Total Waste (Tons)_MA3"]          = last["Total Waste (Tons)"]
        proj["Economic Loss (Million $)_MA3"]   = last["Economic Loss (Million $)"]
        proj["Carbon_Footprint_kgCO2e_MA3"]     = last["Carbon_Footprint_kgCO2e"]

        proj["Forecast_Year"] = True
        rows.append(proj)

    return pd.concat(rows, ignore_index=True)


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

    # Negatif tahminleri sıfırla
    for t in TARGETS:
        out[t] = out[t].clip(lower=0)

    out.to_csv(FORECAST_PATH, index=False)
    print(f"\n  ✅ {FORECAST_PATH}  ({len(out):,} satır)")
    print(f"  Ülke: {out['Country'].nunique()} | Yıl: {sorted(out['Year'].unique().tolist())}")


if __name__ == "__main__":
    main()
