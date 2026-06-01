# Ecolense Intelligence Technical Report

**Date:** June 1, 2026<br>
**Live Dashboard:** [ecolense-intelligence.streamlit.app](https://ecolense-intelligence.streamlit.app)<br>
**Turkish Report:** [ecolense_intelligence_raporu_2026.md](ecolense_intelligence_raporu_2026.md)<br>
**Authors:** Özge Güneş · Kübra Saruhan<br>
**Program:** Miuul Data Scientist Bootcamp

---

## Executive Summary

Ecolense Intelligence is a sustainability decision support platform that analyzes global food waste together with environmental and economic impact. The project combines country, year, and food category slices for the 2010-2023 historical period and produces 2024-2030 projections.

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

## Dataset

The dataset is prepared at country-year-food category level. It includes food waste, economic loss, carbon footprint, population, GDP per capita, material footprint, food price index, income group, and regional metadata.

| Source | Content |
|---|---|
| UNEP Food Waste Index Report | Country-level food waste indicators |
| FAO Food Price Index | Food price index and time effects |
| Gapminder GDP per capita | Income series |
| IMF WEO assumptions | 2024-2030 macro projection inputs |
| Poore & Nemecek carbon factors | Category-level CO2e impact |
| Country metadata | Region, income group, ISO code, and population |

![2023 category distribution](docs/assets/category_waste_2023.png)

---

## Modeling Approach

Gradient Boosting Regressor is used as the production model because it provides a strong balance between test performance and interpretability.

| Target | Test R² | CV R² | Overfit |
|---|---:|---:|---:|
| Total food waste | 0.9674 | 0.9684 | 0.0195 |
| Economic loss | 0.9464 | 0.9458 | 0.0302 |
| Carbon footprint | 0.9464 | 0.9609 | 0.0398 |
| Average | 0.9534 | 0.9584 | 0.0300 |

![Model performance](docs/assets/model_performance_summary.png)

---

## Explainability

Model explainability is tracked through target-level feature impact outputs. These outputs show which variables are most influential in model decisions.

![SHAP feature impact overview](docs/assets/shap_feature_impact_overview.png)

![Total waste feature impact](docs/assets/shap_total_waste.png)

![Economic loss feature impact](docs/assets/shap_economic_loss.png)

![Carbon footprint feature impact](docs/assets/shap_carbon_footprint.png)

The results show that category and population-related variables play a strong role across targets. Policy interpretation should therefore consider both country scale and category composition.

---

## 2024-2030 Projection

The forecast visual uses separate panels for the four metrics. This prevents economic loss and carbon lines from appearing incorrectly close to zero because of mixed units.

![Forecast trends](docs/assets/forecast_trends.png)

| Year | Food waste | Economic loss | Carbon footprint | Average score |
|---:|---:|---:|---:|---:|
| 2024 | 545.7 million tons | 2.29 trillion USD | 3.46 trillion kg CO2e | 77.6 |
| 2025 | 554.7 million tons | 2.38 trillion USD | 3.54 trillion kg CO2e | 77.6 |
| 2026 | 566.0 million tons | 2.45 trillion USD | 3.56 trillion kg CO2e | 77.8 |
| 2027 | 571.3 million tons | 2.50 trillion USD | 3.59 trillion kg CO2e | 77.9 |
| 2028 | 578.2 million tons | 2.56 trillion USD | 3.63 trillion kg CO2e | 77.9 |
| 2029 | 583.2 million tons | 2.62 trillion USD | 3.67 trillion kg CO2e | 77.9 |
| 2030 | 590.5 million tons | 2.68 trillion USD | 3.73 trillion kg CO2e | 77.9 |

---

## Sustainability Score

The sustainability score is a 0-100 composite indicator that reads food waste per capita, economic loss per capita, and carbon pressure per capita together. As the score rises, the country is managing these three pressures more consistently.

In the 2023 data, the average score is 82.7/100 and the country median is 82.9/100. The highest scores are observed in India, Russia, Romania, South Africa, and Lithuania. The lowest scores are concentrated in Kuwait, Nigeria, Saudi Arabia, Qatar, and Australia. The 2024-2030 projection uses each country's 2023 score as the baseline and updates it according to projected changes in per-capita waste, economic loss, and carbon pressure.

---

## Dashboard Modules

| Module | Purpose |
|---|---|
| Home | Main KPI cards, quick navigation, data chatbot, and story entry points. |
| Data Analysis | Data coverage, quality, distributions, correlations, and category analysis. |
| Model Performance | Test/CV metrics, errors, and target-level model quality. |
| Forecasts | 2024-2030 country and metric forecasts. |
| Target-based Forecasts | Custom country/metric target tracking across the forecast horizon. |
| What-if | Effects of changed assumptions on outputs. |
| Country Deep Dive | Detailed historical and forecast analysis for one country. |
| Driver Sensitivity | Comparison of driver effects on metrics. |
| ROI / NPV | Financial return calculation for reduction scenarios. |
| Benchmark & League | Comparative country performance ranking. |
| Anomaly & Monitoring | Outlier and monitoring signal checks. |
| Data Lineage & Quality | Source, file, row/column, and production flow checks. |
| Carbon Flows | Category, country, or continent distribution of carbon load. |
| Model Comparison | Model results, target performance, and feature impact. |
| Policy Simulator | Waste reduction, carbon price, and technology adoption scenarios. |
| Insight Panel | Data chatbot, CAGR analysis, SHAP effects, and contextual answers. |
| Risk & Opportunity | Country positioning on risk and opportunity axes. |
| Target Planner | Annual change required to reach a 2030 target. |
| Report Builder | Different HTML/Markdown outputs by report type. |
| Model Card | Methodology, performance, limitations, and ethics summary. |
| Justice / Impact Panel | Impact analysis by country, region, and income group. |
| Story Mode | Stories with findings, interpretation, and recommended actions generated from title-specific data slices. |

---

## Data Chatbot

The data chatbot is not a fixed-response text box. It extracts country, category, metric, year, and intent from the question; when the input contains multiple questions, it separates them into distinct data-reading steps. It then retrieves the relevant historical, forecast, and explainability slices. Each answer includes an evidence note.

---

## Conclusion

Ecolense Intelligence combines food waste, economic loss, and carbon impact into one decision layer. The project does not only produce forecasts; it also shows which countries, categories, and drivers deserve attention through explainability, scenario, and reporting modules.

---

## References

- FAO. *The State of Food and Agriculture.*
- UNEP. *Food Waste Index Report.*
- Poore, J. & Nemecek, T. Reducing food's environmental impacts through producers and consumers. *Science.*
- IMF. *World Economic Outlook.*
- Lundberg, S. M. & Lee, S.-I. A Unified Approach to Interpreting Model Predictions. *NeurIPS.*

---

*Ecolense Intelligence provides data-driven decision support for sustainable food systems.*
