#!/usr/bin/env python3
"""
02_train_models.py
==================
processed.csv → GradientBoosting modelleri eğitir →
model pkl + model_performance.json + shap_*.csv üretir.

Not: Hız ve okunabilirlik için özellik önemleri doğrudan modelden alınır.
"""

import pandas as pd
import numpy as np
import json, os, joblib, warnings
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
warnings.filterwarnings("ignore")

DATA_PATH = "data/processed.csv"
META_PATH = "data/meta.json"
MODEL_DIR = "models"
PERF_PATH = "model_performance.json"

TARGETS = [
    "Total Waste (Tons)",
    "Economic Loss (Million $)",
    "Carbon_Footprint_kgCO2e",
]
BASE_EXCLUDE = TARGETS + [
    "Country","Food Category","Continent","Subregion",
    "Hemisphere","Income_Group","ISO3","Sustainability_Score",
    "Log_Total_Waste","Log_Econ_Loss",
]

LEAKAGE_EXCLUDE = {
    "Total Waste (Tons)_MA3",
    "Economic Loss (Million $)_MA3",
    "Carbon_Footprint_kgCO2e_MA3",
    "Waste_Trend_3Y",
    "Economic_Trend_3Y",
    "Economic_Loss_Per_Capita_USD",
    "Carbon_Per_Capita_kgCO2e",
    "Waste_Per_Capita_kg",
    "Category_Waste_Share",
    "Category_Economic_Share",
    "Cat_Waste_Share",
    "Cat_Econ_Share",
    "Waste_Efficiency",
    "Economic_Intensity",
    "Carbon_Intensity",
    "Econ_GDP_Ratio",
    "GDP_Waste_PC",
}


def load():
    df   = pd.read_csv(DATA_PATH)
    meta = json.load(open(META_PATH, encoding="utf-8"))
    numeric_candidates = [c for c in df.columns if c not in BASE_EXCLUDE and df[c].dtype != object]
    print(f"  Veri: {len(df):,} satır | Aday feature: {len(numeric_candidates)}")
    return df, numeric_candidates, meta


def features_for_target(numeric_candidates, target):
    """Hedef değişkenden doğrudan türetilmiş kolonları çıkar."""
    return [c for c in numeric_candidates if c not in LEAKAGE_EXCLUDE]


def train_one(df, numeric_candidates, target):
    print(f"\n  🎯 {target}")
    feats = features_for_target(numeric_candidates, target)
    print(f"    Kullanılan feature: {len(feats)}")
    sub = df[feats + [target]].dropna()
    X, y = sub[feats].values, sub[target].values
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)

    model = GradientBoostingRegressor(
        n_estimators=100, max_depth=4, learning_rate=0.05,
        subsample=0.8, min_samples_leaf=5, random_state=42,
    )
    model.fit(Xtr, ytr)

    tr_r2 = r2_score(ytr, model.predict(Xtr))
    te_r2 = r2_score(yte, model.predict(Xte))
    cv    = cross_val_score(model, Xtr, ytr, cv=3, scoring="r2")
    overfit = abs(tr_r2 - te_r2) / (abs(tr_r2) + 1e-8)
    rmse  = float(np.sqrt(mean_squared_error(yte, model.predict(Xte))))
    mae   = float(mean_absolute_error(yte, model.predict(Xte)))
    mape  = float(np.mean(np.abs((yte - model.predict(Xte)) / (np.abs(yte)+1e-8))) * 100)

    print(f"    Train R²={tr_r2:.4f}  Test R²={te_r2:.4f}  "
          f"CV={cv.mean():.4f}±{cv.std():.4f}  Overfit={overfit:.4f}")

    # Feature importance (tree-based, hızlı)
    imp = pd.DataFrame({
        "feature":    feats,
        "importance": model.feature_importances_,
    }).sort_values("importance", ascending=False)
    safe = target.replace(" ","_").replace("(","").replace(")","").replace("$","USD")
    imp.to_csv(f"shap_{safe}.csv", index=False)
    joblib.dump({"model": model, "features": feats},
                os.path.join(MODEL_DIR, f"model_{safe}.pkl"))

    return {
        "target": target,
        "train":  {"r2": round(tr_r2,4)},
        "test":   {"r2": round(te_r2,4), "rmse": round(rmse,2),
                   "mae": round(mae,2),   "mape": round(mape,2)},
        "cv_mean": round(float(cv.mean()),4),
        "cv_std":  round(float(cv.std()),4),
        "overfit": round(float(overfit),4),
        "n_train": int(len(Xtr)),
        "n_test":  int(len(Xte)),
        "n_features": int(len(feats)),
        "top5_importance": imp.head(5)["feature"].tolist(),
    }


def main():
    print("=" * 55)
    print("  MODEL EĞİTİMİ")
    print("=" * 55)

    df, feats, meta = load()
    os.makedirs(MODEL_DIR, exist_ok=True)
    results = {}

    for target in TARGETS:
        results[target] = train_one(df, feats, target)

    avg_r2 = np.mean([r["test"]["r2"] for r in results.values()])
    avg_of = np.mean([r["overfit"]    for r in results.values()])
    quality = "Mükemmel" if avg_r2>0.90 else ("İyi" if avg_r2>0.75 else "Geliştirilmeli")

    perf = {
        "generated_at":    pd.Timestamp.now().isoformat(),
        "data_source":     meta.get("sources", []),
        "n_countries":     meta.get("countries"),
        "year_range":      meta.get("years"),
        "n_rows":          meta.get("n_rows"),
        "model_type":      "GradientBoostingRegressor",
        "hyperparameters": {"n_estimators":100,"max_depth":4,
                            "learning_rate":0.05,"subsample":0.8},
        "train_test_split":"80/20",
        "cv_folds":        3,
        "average_test_r2": round(avg_r2,4),
        "average_overfit": round(avg_of,4),
        "quality_label":   quality,
        "targets":         results,
    }
    with open(PERF_PATH, "w", encoding="utf-8") as f:
        json.dump(perf, f, indent=2, ensure_ascii=False)

    print(f"\n  ✅ {PERF_PATH}")
    print(f"  Ortalama Test R²: {avg_r2:.4f}  |  Kalite: {quality}\n")


if __name__ == "__main__":
    main()
