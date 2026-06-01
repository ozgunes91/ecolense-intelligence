<div align="center">

# Ecolense Intelligence

### Global Food Waste Analytics and Sustainability Decision Support Platform

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3+-orange.svg)](https://scikit-learn.org/)
[![Dashboard](https://img.shields.io/badge/Dashboard-Live-brightgreen.svg)](https://ecolense-intelligence.streamlit.app/)

[Live Dashboard](https://ecolense-intelligence.streamlit.app/) · [Technical Report](ecolense_intelligence_report_2026_en.md) · [Türkçe README](README.md)

</div>

---

## Overview

Ecolense Intelligence is a data-driven decision support platform for global food waste analysis. It combines food waste, economic loss, carbon footprint, and sustainability scoring at country-year-category granularity.

| Metric | Value |
|---|---:|
| Countries | 148 |
| Historical period | 2010-2023 |
| Forecast horizon | 2024-2030 |
| Observations | 16,576 |
| Average test R² | 0.9534 |
| 2023 average sustainability score | 82.7/100 |
| 2030 average sustainability projection | 77.9/100 |
| Dashboard modules | 22 |

---

## Dashboard Preview

![Dashboard home](docs/assets/dashboard_home.jpg)

![Model performance page](docs/assets/dashboard_model_performance.jpg)

![SHAP section](docs/assets/dashboard_shap_section.jpg)

---

## Analytical Visuals

The forecast visual does not compress unrelated scales onto one axis. Waste, economic loss, carbon, and score are shown as separate panels.

![Forecast trends](docs/assets/forecast_trends.png)

![2023 category distribution](docs/assets/category_waste_2023.png)

![Model performance](docs/assets/model_performance_summary.png)

![SHAP feature impact overview](docs/assets/shap_feature_impact_overview.png)

---

## Sustainability Score

The sustainability score is a 0-100 composite indicator that reads country-level food waste per capita, economic loss per capita, and carbon pressure per capita together. A higher score means these three pressures are more controlled at the same time.

In 2023, the average score is 82.7/100 and the country median is 82.9/100. The strongest scores are concentrated in India, Russia, Romania, South Africa, and Lithuania. The 2024-2030 projection keeps the score connected to the 2023 country scale and updates it according to projected changes in per-capita waste, economic loss, and carbon pressure.

---

## Dataset And Methodology

The dataset is prepared at country-year-food category level. It uses food waste, economic loss, carbon footprint, population, GDP per capita, material footprint, food price index, income group, and regional metadata.

| Source | Usage |
|---|---|
| UNEP Food Waste Index Report | Country-level food waste indicators |
| FAO Food Price Index | Food price index and time effects |
| Gapminder GDP per capita | Country income series |
| IMF WEO assumptions | 2024-2030 macro projection inputs |
| Poore & Nemecek factors | Category-level carbon impact |
| Country metadata | Region, income group, ISO code, and population |

The pipeline has three main steps:

1. Prepare source data at a shared country-year-category level
2. Build ratios, intensity metrics, interaction variables, and time features
3. Export forecast, explainability, dashboard, and report artifacts

---

## Modeling

Separate models are trained for three targets:

| Target | Description | Test R² | CV R² |
|---|---|---:|---:|
| `Total Waste (Tons)` | Total food waste | 0.9674 | 0.9684 |
| `Economic Loss (Million $)` | Economic loss | 0.9464 | 0.9458 |
| `Carbon_Footprint_kgCO2e` | Carbon footprint | 0.9464 | 0.9609 |

Gradient Boosting Regressor is used as the production model. Explainability outputs are stored as CSV files under `outputs/explainability/`, and report-ready PNG visuals are stored under `docs/assets/`.

![Total waste feature impact](docs/assets/shap_total_waste.png)

![Economic loss feature impact](docs/assets/shap_economic_loss.png)

![Carbon footprint feature impact](docs/assets/shap_carbon_footprint.png)

---

## Dashboard Modules

| Module | Purpose |
|---|---|
| Home | Shows core KPI cards, quick navigation, the data chatbot, and story entry points. |
| Data Analysis | Reviews data coverage, missing values, distributions, correlations, and category breakdowns. |
| Model Performance | Displays test R², CV R², error metrics, and target-level model quality. |
| Forecasts | Visualizes 2024-2030 forecasts by country and metric. |
| Target-based Forecasts | Tracks custom country/metric goals across the forecast horizon. |
| What-if | Calculates scenario effects for population, category reduction, and policy assumptions. |
| Country Deep Dive | Explains a single country through historical data, category impact, and forecast path. |
| Driver Sensitivity | Compares how driver variables affect the selected target metric. |
| ROI / NPV | Calculates financial return and net present value for reduction scenarios. |
| Benchmark & League | Ranks countries and compares their performance positions. |
| Anomaly & Monitoring | Checks outliers and monitoring signals. |
| Data Lineage & Quality | Summarizes file sources, data coverage, row/column quality, and production flow. |
| Carbon Flows | Shows how carbon load is distributed by category, country, or continent. |
| Model Comparison | Reviews model results, target-level performance, and feature impact together. |
| Policy Simulator | Tests inputs such as waste reduction, carbon price, and technology adoption. |
| Insight Panel | Combines the data chatbot, CAGR analysis, SHAP effects, and selected context. |
| Risk & Opportunity | Places countries on risk and opportunity axes. |
| Target Planner | Calculates the annual change required to reach a 2030 target. |
| Report Builder | Generates data-driven HTML/Markdown reports with different sections by report type. |
| Model Card | Documents methodology, performance, limitations, and ethics in one view. |
| Justice / Impact Panel | Reviews impact distribution by country, region, and income group. |
| Story Mode | Presents data stories with findings, interpretation, and recommended actions generated from slices that match each title. |

---

## Data Chatbot

The dashboard chatbot does not return a fixed script. It detects country, metric, category, year, and intent from the question; when the input contains multiple questions, it answers each part separately. Answers are generated from the relevant historical, forecast, and explainability slices and include an evidence note.

---

## Setup

```bash
git clone https://github.com/ozgunes91/ecolense-intelligence.git
cd ecolense-intelligence

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the full pipeline:

```bash
python run_pipeline.py
```

Start the dashboard:

```bash
streamlit run app.py
```

---

## Repository Structure

```text
ecolense-intelligence/
├── data/
├── docs/assets/
├── outputs/
│   ├── forecasts/forecasts.csv
│   ├── metrics/model_performance.json
│   └── explainability/shap_*.csv
├── models/
├── 01_prepare_data.py
├── 02_train_models.py
├── 03_generate_forecasts.py
├── run_pipeline.py
└── app.py
```

---

## References

- FAO. *The State of Food and Agriculture.*
- UNEP. *Food Waste Index Report.*
- Poore, J. & Nemecek, T. Reducing food's environmental impacts through producers and consumers. *Science.*
- IMF. *World Economic Outlook.*
- Lundberg, S. M. & Lee, S.-I. A Unified Approach to Interpreting Model Predictions. *NeurIPS.*

---

Ecolense Intelligence provides data-driven decision support for sustainable food systems.
