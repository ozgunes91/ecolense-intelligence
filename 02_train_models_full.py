#!/usr/bin/env python3
"""
02_train_models.py
==================
processed.csv'yi okur → 3 hedef için GradientBoosting eğitir →
model pkl + performans JSON + SHAP CSV üretir.

Çıktılar:
  models/model_<target>.pkl
  model_performance.json
  shap_<target>.csv
"""

import pandas as pd
import numpy as np
import json, os, joblib, warnings
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import shap
warnings.filterwarnings("ignore")

DATA_PATH  = "data/processed.csv"
META_PATH  = "data/meta.json"
MODEL_DIR  = "models"
PERF_PATH  = "model_performance.json"

TARGETS = [
    "Total Waste (Tons)",
    "Economic Loss (Million $)",
    "Carbon_Footprint_kgCO2e",
]
EXCLUDE = TARGETS + [
    "Country","Food Category","Continent","Subregion",
    "Hemisphere","Income_Group","ISO3","Sustainability_Score",
    # log türevleri target ile korelasyon yüksek → sızdırma riski
    "Log_Total_Waste","Log_Econ_Loss",
]


def load():
    df  = pd.read_csv(DATA_PATH)
    meta = json.load(open(META_PATH, encoding="utf-8"))
    feats = [c for c in df.columns if c not in EXCLUDE and df[c].dtype != object]
    print(f"  Veri: {len(df):,} satır | Feature: {len(feats)}")
    return df, feats, meta


def metrics(y_true, y_pred):
    r2   = r2_score(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae  = mean_absolute_error(y_true, y_pred)
    mape = float(np.mean(np.abs((y_true - y_pred) / (np.abs(y_true) + 1e-8))) * 100)
    return {"r2": round(r2,4), "rmse": round(rmse,2), "mae": round(mae,2), "mape": round(mape,2)}


def shap_importance(model, X_train, X_test, feature_names, target_label):
    """SHAP değerlerini hesapla ve CSV kaydet."""
    try:
        explainer = shap.TreeExplainer(model)
        sv = explainer.shap_values(X_test)
        imp = pd.DataFrame({
            "feature":    feature_names,
            "importance": np.abs(sv).mean(axis=0),
        }).sort_values("importance", ascending=False)
        safe = target_label.replace(" ","_").replace("(","").replace(")","").replace("$","USD").replace("/","_")
        path = f"shap_{safe}.csv"
        imp.to_csv(path, index=False)
        print(f"    SHAP → {path}")
        return imp
    except Exception as e:
        print(f"    SHAP hata: {e}")
        return None


def train_one(df, feats, target):
    print(f"\n  🎯 Hedef: {target}")
    sub = df[feats + [target]].dropna()
    X   = sub[feats].values
    y   = sub[target].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = GradientBoostingRegressor(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        min_samples_leaf=5,
        random_state=42,
    )
    model.fit(X_train, y_train)

    tr   = metrics(y_train, model.predict(X_train))
    te   = metrics(y_test,  model.predict(X_test))
    cv   = cross_val_score(model, X_train, y_train, cv=5, scoring="r2")

    overfit = abs(tr["r2"] - te["r2"]) / (abs(tr["r2"]) + 1e-8)
    print(f"    Train R²={tr['r2']:.4f}  Test R²={te['r2']:.4f}  CV={cv.mean():.4f}±{cv.std():.4f}  Overfit={overfit:.4f}")

    shap_df = shap_importance(model, X_train, X_test, feats, target)

    result = {
        "target":     target,
        "train":      tr,
        "test":       te,
        "cv_mean":    round(float(cv.mean()),4),
        "cv_std":     round(float(cv.std()),4),
        "overfit":    round(float(overfit),4),
        "n_train":    int(len(X_train)),
        "n_test":     int(len(X_test)),
        "n_features": int(len(feats)),
        "top5_shap":  shap_df.head(5)["feature"].tolist() if shap_df is not None else [],
    }
    return model, result


def main():
    print("=" * 55)
    print("  MODEL EĞİTİMİ")
    print("=" * 55)

    df, feats, meta = load()
    os.makedirs(MODEL_DIR, exist_ok=True)

    all_results = {}
    for target in TARGETS:
        model, res = train_one(df, feats, target)
        safe  = target.replace(" ","_").replace("(","").replace(")","").replace("$","USD").replace("/","_")
        mpath = os.path.join(MODEL_DIR, f"model_{safe}.pkl")
        joblib.dump({"model": model, "features": feats}, mpath)
        print(f"    Model → {mpath}")
        all_results[target] = res

    # Özet
    avg_test_r2  = np.mean([r["test"]["r2"]  for r in all_results.values()])
    avg_overfit  = np.mean([r["overfit"]     for r in all_results.values()])
    quality      = "Mükemmel" if avg_test_r2 > 0.90 else ("İyi" if avg_test_r2 > 0.75 else "Geliştirilmeli")

    perf = {
        "generated_at":    pd.Timestamp.now().isoformat(),
        "data_source":     meta.get("sources", []),
        "n_countries":     meta.get("countries"),
        "year_range":      meta.get("years"),
        "n_rows":          meta.get("n_rows"),
        "model_type":      "GradientBoostingRegressor",
        "hyperparameters": {"n_estimators":200,"max_depth":4,"learning_rate":0.05,"subsample":0.8},
        "train_test_split":"80/20",
        "cv_folds":        5,
        "average_test_r2": round(avg_test_r2,4),
        "average_overfit": round(avg_overfit,4),
        "quality_label":   quality,
        "targets":         all_results,
    }
    with open(PERF_PATH, "w", encoding="utf-8") as f:
        json.dump(perf, f, indent=2, ensure_ascii=False)

    print(f"\n  ✅ {PERF_PATH}")
    print(f"  Ortalama Test R² : {avg_test_r2:.4f}")
    print(f"  Kalite etiketi   : {quality}\n")


if __name__ == "__main__":
    main()
