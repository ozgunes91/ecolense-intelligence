#!/usr/bin/env python3
"""
02_train_models.py
==================
processed.csv → GradientBoosting modelleri eğitir →
model pkl + outputs/metrics/model_performance.json + outputs/explainability/shap_*.csv üretir.

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
OUTPUT_DIR = "outputs"
METRICS_DIR = os.path.join(OUTPUT_DIR, "metrics")
SHAP_DIR = os.path.join(OUTPUT_DIR, "explainability")
PERF_PATH = os.path.join(METRICS_DIR, "model_performance.json")
ASSET_DIR = "docs/assets"

TARGETS = [
    "Total Waste (Tons)",
    "Economic Loss (Million $)",
    "Carbon_Footprint_kgCO2e",
]
SHAP_VISUALS = {
    "Total Waste (Tons)": {
        "csv": os.path.join(SHAP_DIR, "shap_Total_Waste_Tons.csv"),
        "png": "shap_total_waste.png",
        "title": "Toplam Gıda İsrafı",
        "color": "#10b981",
    },
    "Economic Loss (Million $)": {
        "csv": os.path.join(SHAP_DIR, "shap_Economic_Loss_Million_USD.csv"),
        "png": "shap_economic_loss.png",
        "title": "Ekonomik Kayıp",
        "color": "#6366f1",
    },
    "Carbon_Footprint_kgCO2e": {
        "csv": os.path.join(SHAP_DIR, "shap_Carbon_Footprint_kgCO2e.csv"),
        "png": "shap_carbon_footprint.png",
        "title": "Karbon Ayak İzi",
        "color": "#ef4444",
    },
}
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
    imp.to_csv(os.path.join(SHAP_DIR, f"shap_{safe}.csv"), index=False)
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


def create_shap_visuals():
    """Model özellik etkilerini dashboard ve rapor için PNG olarak üret."""
    os.environ.setdefault("MPLCONFIGDIR", os.path.join("/tmp", "ecolense_mpl"))
    os.environ.setdefault("XDG_CACHE_HOME", os.path.join("/tmp", "ecolense_cache"))
    os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
    os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)
    try:
        import matplotlib.pyplot as plt
    except Exception:
        print("  Matplotlib yüklenemedi; görsel çıktılar atlandı.")
        return

    os.makedirs(ASSET_DIR, exist_ok=True)
    overview_frames = []

    for spec in SHAP_VISUALS.values():
        if not os.path.exists(spec["csv"]):
            continue
        df = pd.read_csv(spec["csv"])
        if df.empty or "feature" not in df.columns:
            continue

        value_col = "importance" if "importance" in df.columns else df.columns[-1]
        top = df.sort_values(value_col, ascending=False).head(10).copy()
        total = top[value_col].sum()
        if total > 0:
            top[value_col] = top[value_col] / total

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(top["feature"], top[value_col], color=spec["color"], alpha=0.9)
        ax.invert_yaxis()
        ax.set_title(f"{spec['title']} - SHAP / Özellik Etkisi", fontsize=13, weight="bold")
        ax.set_xlabel("Normalize Etki Skoru")
        ax.grid(axis="x", alpha=0.18)
        ax.spines[["top", "right", "left"]].set_visible(False)
        fig.tight_layout()
        fig.savefig(os.path.join(ASSET_DIR, spec["png"]), dpi=180, bbox_inches="tight")
        plt.close(fig)

        overview = top.head(6)[["feature", value_col]].copy()
        overview["target"] = spec["title"]
        overview["color"] = spec["color"]
        overview_frames.append(overview)

    if not overview_frames:
        return

    fig, axes = plt.subplots(1, len(overview_frames), figsize=(15, 5), sharex=False)
    if len(overview_frames) == 1:
        axes = [axes]

    for ax, frame in zip(axes, overview_frames):
        color = frame["color"].iloc[0]
        title = frame["target"].iloc[0]
        value_col = [c for c in frame.columns if c not in {"feature", "target", "color"}][0]
        ax.barh(frame["feature"], frame[value_col], color=color, alpha=0.9)
        ax.invert_yaxis()
        ax.set_title(title, fontsize=12, weight="bold")
        ax.set_xlabel("Etki")
        ax.grid(axis="x", alpha=0.16)
        ax.spines[["top", "right", "left"]].set_visible(False)

    fig.suptitle("SHAP / Özellik Etkisi Özeti", fontsize=16, weight="bold", y=1.04)
    fig.tight_layout()
    fig.savefig(os.path.join(ASSET_DIR, "shap_feature_impact_overview.png"), dpi=180, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✅ SHAP görselleri: {ASSET_DIR}")


def main():
    print("=" * 55)
    print("  MODEL EĞİTİMİ")
    print("=" * 55)

    df, feats, meta = load()
    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs(METRICS_DIR, exist_ok=True)
    os.makedirs(SHAP_DIR, exist_ok=True)
    results = {}

    for target in TARGETS:
        results[target] = train_one(df, feats, target)

    create_shap_visuals()

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
