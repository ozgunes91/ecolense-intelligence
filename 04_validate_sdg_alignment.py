#!/usr/bin/env python3
"""
Validate the Ecolense food-system sustainability score against the official
Sustainable Development Report / SDG Index database.

The Ecolense score is not an official SDG Index score. This script checks
external alignment at country level and writes reproducible validation outputs.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.request import urlretrieve

import matplotlib.pyplot as plt
import pandas as pd


DEFAULT_SDG_URL = "https://dashboards.sdgindex.org/static/downloads/files/SDR2025-data.xlsx"
LOCAL_DATA_PATH = Path("data/processed.csv")
OUTPUT_DIR = Path("outputs/validation")
ASSET_DIR = Path("docs/assets")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare Ecolense score with 2025 SDG Index data.")
    parser.add_argument(
        "--sdg-xlsx",
        type=Path,
        default=Path("data/external/SDR2025-data.xlsx"),
        help="Path to SDR2025-data.xlsx. If missing and --download is set, it will be downloaded.",
    )
    parser.add_argument(
        "--download",
        action="store_true",
        help="Download SDR2025-data.xlsx from the SDG Index dashboard before validation.",
    )
    return parser.parse_args()


def ensure_sdg_file(path: Path, download: bool) -> Path:
    if path.exists():
        return path
    if not download:
        raise FileNotFoundError(
            f"{path} bulunamadı. Dosyayı ekleyin veya script'i --download ile çalıştırın."
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    urlretrieve(DEFAULT_SDG_URL, path)
    return path


def build_comparison(local_path: Path, sdg_path: Path) -> tuple[pd.DataFrame, dict]:
    local_df = pd.read_csv(local_path)
    latest_year = int(pd.to_numeric(local_df["Year"], errors="coerce").max())

    local_country = (
        local_df[local_df["Year"] == latest_year]
        .groupby(["ISO3", "Country"], as_index=False)
        .agg(
            ecolense_score=("Sustainability_Score", "mean"),
            total_waste_tons=("Total Waste (Tons)", "sum"),
            economic_loss_musd=("Economic Loss (Million $)", "sum"),
            carbon_kgco2e=("Carbon_Footprint_kgCO2e", "sum"),
            category_count=("Food Category", "nunique"),
        )
    )

    sdg = pd.read_excel(sdg_path, sheet_name="SDR2025 Data")
    sdg_country = sdg[
        [
            "Country Code ISO3",
            "Country",
            "2025 SDG Index Score",
            "2025 SDG Index Rank",
            "Goal 2 Score",
            "Goal 12 Score",
            "Goal 13 Score",
        ]
    ].rename(
        columns={
            "Country Code ISO3": "ISO3",
            "Country": "sdg_country",
            "2025 SDG Index Score": "sdg_2025_score",
            "2025 SDG Index Rank": "sdg_2025_rank",
            "Goal 2 Score": "sdg_goal2_score",
            "Goal 12 Score": "sdg_goal12_score",
            "Goal 13 Score": "sdg_goal13_score",
        }
    )

    comparison = local_country.merge(sdg_country, on="ISO3", how="inner")
    comparison["ecolense_rank"] = comparison["ecolense_score"].rank(ascending=False, method="min").astype(int)
    comparison["score_gap"] = comparison["ecolense_score"] - comparison["sdg_2025_score"]
    comparison["rank_gap"] = comparison["ecolense_rank"] - comparison["sdg_2025_rank"]
    comparison = comparison.sort_values("ecolense_rank")

    summary = {
        "source": "Sustainable Development Report 2025 / SDG Index dashboard database",
        "source_url": DEFAULT_SDG_URL,
        "accessed": "2026-06-02",
        "local_year": latest_year,
        "local_countries": int(local_country["ISO3"].nunique()),
        "sdg_countries": int(sdg_country["ISO3"].nunique()),
        "matched_countries": int(comparison["ISO3"].nunique()),
        "ecolense_zero_country_scores": int((local_country["ecolense_score"] == 0).sum()),
        "ecolense_min_score": float(local_country["ecolense_score"].min()),
        "ecolense_max_score": float(local_country["ecolense_score"].max()),
        "pearson_sdg_index": float(comparison["ecolense_score"].corr(comparison["sdg_2025_score"], method="pearson")),
        "spearman_sdg_index": float(comparison["ecolense_score"].corr(comparison["sdg_2025_score"], method="spearman")),
        "pearson_sdg_goal2": float(comparison["ecolense_score"].corr(comparison["sdg_goal2_score"], method="pearson")),
        "pearson_sdg_goal12": float(comparison["ecolense_score"].corr(comparison["sdg_goal12_score"], method="pearson")),
        "pearson_sdg_goal13": float(comparison["ecolense_score"].corr(comparison["sdg_goal13_score"], method="pearson")),
    }
    return comparison, summary


def write_chart(comparison: pd.DataFrame, summary: dict, output_path: Path, lang: str = "EN") -> None:
    is_tr = lang.upper() == "TR"
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.6), dpi=160)

    axes[0].scatter(
        comparison["sdg_2025_score"],
        comparison["ecolense_score"],
        s=36,
        color="#232E5C",
        alpha=0.76,
        edgecolor="white",
        linewidth=0.4,
    )
    for iso in ["TUR", "IND", "ROU", "FIN", "SWE", "AFG"]:
        row = comparison[comparison["ISO3"] == iso]
        if not row.empty:
            r = row.iloc[0]
            axes[0].annotate(
                iso,
                (r["sdg_2025_score"], r["ecolense_score"]),
                textcoords="offset points",
                xytext=(5, 5),
                fontsize=8,
                color="#0F172A",
            )
    axes[0].set_title(
        "Ecolense skoru ve 2025 SDG Index" if is_tr else "Ecolense Score vs. 2025 SDG Index",
        fontsize=13,
        fontweight="bold",
        color="#0F172A",
    )
    axes[0].set_xlabel("2025 SDG Index skoru" if is_tr else "2025 SDG Index Score")
    axes[0].set_ylabel("Ecolense gıda sistemi skoru" if is_tr else "Ecolense food-system score")
    axes[0].text(
        0.02,
        0.03,
        f"Pearson r = {summary['pearson_sdg_index']:.2f}",
        transform=axes[0].transAxes,
        fontsize=10,
        color="#334155",
    )

    correlations = pd.Series(
        {
            "SDG Index": summary["pearson_sdg_index"],
            "SDG 2": summary["pearson_sdg_goal2"],
            "SDG 12": summary["pearson_sdg_goal12"],
            "SDG 13": summary["pearson_sdg_goal13"],
        }
    )
    axes[1].bar(correlations.index, correlations.values, color=["#232E5C", "#4B5563", "#0F766E", "#15803D"], alpha=0.88)
    axes[1].axhline(0, color="#94A3B8", linewidth=1)
    axes[1].set_ylim(-0.2, 0.5)
    axes[1].set_title("Dış uyum kontrolü" if is_tr else "External Alignment Check", fontsize=13, fontweight="bold", color="#0F172A")
    axes[1].set_ylabel("Pearson korelasyonu" if is_tr else "Pearson correlation")
    for i, value in enumerate(correlations.values):
        axes[1].text(i, value + (0.02 if value >= 0 else -0.05), f"{value:.2f}", ha="center", fontsize=10, color="#0F172A")

    fig.suptitle(
        "SDG Index çapraz kontrolü: kapsam göstergesi, doğrudan ikame değil"
        if is_tr
        else "SDG Index Cross-check: scope, not direct replacement",
        fontsize=15,
        fontweight="bold",
        color="#0F172A",
    )
    fig.text(
        0.5,
        0.01,
        "Kaynak: Sustainable Development Report 2025 veritabanı, erişim 2026-06-02. Yerel skor 2023 Ecolense ülke ortalamalarını kullanır."
        if is_tr
        else "Source: Sustainable Development Report 2025 database, accessed 2026-06-02. Local score uses 2023 Ecolense country averages.",
        ha="center",
        fontsize=9,
        color="#475569",
    )
    fig.tight_layout(rect=[0, 0.04, 1, 0.94])
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    args = parse_args()
    sdg_path = ensure_sdg_file(args.sdg_xlsx, args.download)
    comparison, summary = build_comparison(LOCAL_DATA_PATH, sdg_path)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    comparison.to_csv(OUTPUT_DIR / "sdg_index_comparison.csv", index=False)
    (OUTPUT_DIR / "sdg_index_comparison_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    write_chart(comparison, summary, ASSET_DIR / "sdg_index_alignment.png", lang="EN")
    write_chart(comparison, summary, ASSET_DIR / "sdg_index_alignment_tr.png", lang="TR")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
