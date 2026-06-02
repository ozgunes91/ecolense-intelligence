#!/usr/bin/env python3
"""
01_prepare_data.py
==================
Ham CSV'yi alır → özellik mühendisliği → model için hazır CSV üretir.

Giriş : data/global_food_waste_real_world.csv  (ISO3 tekilleştirme öncesi ham gerçek veri)
Çıkış : data/processed.csv                     (tüm özellikler, encode edilmiş, temiz)
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import warnings, os, json
warnings.filterwarnings("ignore")

RAW_PATH  = "data/global_food_waste_real_world.csv"
OUT_PATH  = "data/processed.csv"
META_PATH = "data/meta.json"

COUNTRY_ALIASES = {
    "UK": "United Kingdom",
    "UAE": "United Arab Emirates",
}


def load(path):
    df = pd.read_csv(path)
    if "Country" in df.columns:
        df["Country"] = df["Country"].replace(COUNTRY_ALIASES)
    stale_encoded = [
        "Country_Encoded",
        "Food Category_Encoded",
        "Continent_Encoded",
        "Hemisphere_Encoded",
        "Income_Group_Encoded",
    ]
    df = df.drop(columns=[c for c in stale_encoded if c in df.columns])
    keys = [c for c in ["Country", "ISO3", "Year", "Food Category"] if c in df.columns]
    if keys:
        numeric_cols = [c for c in df.select_dtypes(include=[np.number]).columns if c not in keys]
        other_cols = [c for c in df.columns if c not in keys and c not in numeric_cols]
        agg = {c: "mean" for c in numeric_cols}
        agg.update({c: "first" for c in other_cols})
        before = len(df)
        df = df.groupby(keys, as_index=False, dropna=False).agg(agg)
        collapsed = before - len(df)
        if collapsed:
            print(f"  Kanonik ülke adlarıyla {collapsed:,} yinelenen alias satırı tekilleştirildi")
    print(f"  Yüklendi: {len(df):,} satır × {len(df.columns)} sütun")
    return df

def add_features(df):
    """Türetilmiş özellikler – hepsi veriden hesaplanır, sabit değer yok."""
    df = df.copy()

    # ── Zaman ──────────────────────────────────────────────────────────
    df["Year_Norm"]       = (df["Year"] - df["Year"].min()) / (df["Year"].max() - df["Year"].min())
    df["Pandemic_Flag"]   = df["Year"].isin([2020, 2021]).astype(int)
    df["Year_Sin"]        = np.sin(2 * np.pi * df["Years_from_2010"] / 5)
    df["Year_Cos"]        = np.cos(2 * np.pi * df["Years_from_2010"] / 5)

    # ── Kişi başı oranlar (zaten mevcut, normalize edilmiş versiyonlar) ─
    pop = df["Population (Million)"].clip(lower=0.001)
    df["Log_Population"]   = np.log1p(pop)
    df["Log_GDP_PC"]       = np.log1p(df["GDP_Per_Capita_USD"].clip(lower=1))
    df["Log_Total_Waste"]  = np.log1p(df["Total Waste (Tons)"].clip(lower=0))
    df["Log_Econ_Loss"]    = np.log1p(df["Economic Loss (Million $)"].clip(lower=0))

    # ── Kategori payları (yeniden hesapla) ─────────────────────────────
    total_w = df.groupby(["Country","Year"])["Total Waste (Tons)"].transform("sum")
    total_e = df.groupby(["Country","Year"])["Economic Loss (Million $)"].transform("sum")
    df["Cat_Waste_Share"]  = df["Total Waste (Tons)"]        / total_w.clip(lower=1)
    df["Cat_Econ_Share"]   = df["Economic Loss (Million $)"] / total_e.clip(lower=1)

    # ── Verimlilik endeksleri ──────────────────────────────────────────
    df["Waste_Efficiency"]    = df["Economic Loss (Million $)"] / df["Total Waste (Tons)"].clip(lower=1) * 1000
    df["Carbon_Intensity"]    = df["Carbon_Footprint_kgCO2e"]  / df["Total Waste (Tons)"].clip(lower=1)
    df["Econ_GDP_Ratio"]      = df["Economic Loss (Million $)"] / (df["GDP_Per_Capita_USD"] * pop / 1000).clip(lower=0.001)

    # ── 3 yıllık kayan ortalamalar ─────────────────────────────────────
    df = df.sort_values(["Country","Food Category","Year"]).reset_index(drop=True)
    for col in ["Total Waste (Tons)","Economic Loss (Million $)","Carbon_Footprint_kgCO2e"]:
        df[f"{col}_MA3"] = (
            df.groupby(["Country","Food Category"])[col]
              .transform(lambda x: x.rolling(3, min_periods=1).mean())
        )

    # ── Etkileşim terimleri ───────────────────────────────────────────
    df["Pop_MatFP"]     = df["Population (Million)"] * df["Material_Footprint_Per_Capita"]
    df["GDP_Waste_PC"]  = df["Log_GDP_PC"] * df["Waste_Per_Capita_kg"]

    return df

def encode(df):
    """Kategorik sütunları encode et; orijinalleri koru."""
    cat_cols = ["Country","Food Category","Continent","Subregion","Hemisphere","Income_Group"]
    encoders = {}
    for col in cat_cols:
        if col in df.columns:
            le = LabelEncoder()
            df[f"{col}_Enc"] = le.fit_transform(df[col].astype(str))
            encoders[col] = list(le.classes_)
    return df, encoders

def validate(df):
    null_count = df.isnull().sum().sum()
    inf_count  = np.isinf(df.select_dtypes("number")).sum().sum()
    print(f"  Eksik değer : {null_count}")
    print(f"  Sonsuz değer: {inf_count}")
    if inf_count > 0:
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.fillna(df.median(numeric_only=True))
    return df

def main():
    print("=" * 55)
    print("  VERİ HAZIRLAMA")
    print("=" * 55)

    df = load(RAW_PATH)
    print("  Özellik mühendisliği...")
    df = add_features(df)
    print(f"  Özellik sayısı: {len(df.columns)}")

    df, encoders = encode(df)
    df = validate(df)

    os.makedirs("data", exist_ok=True)
    df.to_csv(OUT_PATH, index=False)

    # Meta kaydet
    meta = {
        "n_rows": len(df),
        "n_cols": len(df.columns),
        "countries": int(df["Country"].nunique()),
        "years": [int(df["Year"].min()), int(df["Year"].max())],
        "categories": sorted(df["Food Category"].unique().tolist()),
        "continents": sorted(df["Continent"].unique().tolist()),
        "encoders": encoders,
        "targets": ["Total Waste (Tons)", "Economic Loss (Million $)", "Carbon_Footprint_kgCO2e"],
        "sources": [
            "2010-2023 veri serisi – Gapminder Foundation – GDP per capita",
            "2010-2023 veri serisi – FAO Food Price Index",
            "2018 – Poore & Nemecek, Science – gıda kategorisi CO2e katsayıları",
            "2021 – UNEP Food Waste Index Report – Tablo A4.1 ve ülke göstergeleri",
            "2024 güncel veri tabanı – UNEP IRP Global Material Flows Database – material footprint",
            "Ekim 2024 – IMF World Economic Outlook Database – 2024-2030 büyüme varsayımları",
            "Erişim: 2 Haziran 2026 – ülke meta verileri – bölge, gelir grubu ve ISO kodları",
        ],
    }
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    print(f"\n  ✅ {OUT_PATH}  ({len(df):,} satır × {len(df.columns)} sütun)")
    print(f"  ✅ {META_PATH}")
    print()

if __name__ == "__main__":
    main()
