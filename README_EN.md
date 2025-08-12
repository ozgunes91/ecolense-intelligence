# 🌱 Ecolense Intelligence - Food Waste Analysis Platform

## 📋 Project Summary

**Ecolense Intelligence** is a comprehensive data analysis and machine learning platform that analyzes global food waste problems and provides sustainable solutions. Developed with 20 countries, 8 food categories, and 5000+ observations, this platform provides in-depth analysis of the economic, environmental, and social impacts of food waste.

### 🎯 Main Objectives
- Analyze global food waste trends
- Calculate carbon footprint and economic losses
- Create sustainability scores
- Develop policy recommendations
- Provide interactive dashboard for data visualization

## 📊 Dataset and Methodology

### Data Sources
- **Global Food Wastage Dataset**: 8 basic variables (country, year, food category, total waste, economic loss, etc.)
- **Material Footprint Dataset**: 32 variables (ISO codes, continent, development level, etc.)

### Data Enrichment Process
- **Inner Join** of two datasets
- **ISO Code Mapping** for country code standardization
- **29 new features** engineering for total of 37 variables
- **5000 observations** enriched final dataset

### Feature Engineering (from 01_veri_hazirlama.py)
- **Per capita metrics**: Waste, economic loss, carbon footprint
- **Temporal features**: Pandemic period, year trends, cyclical features
- **Geographic features**: Continent, hemisphere, development level
- **Derived features**: Efficiency, intensity, share ratios
- **Interaction features**: Population-material interaction, year-population interaction
- **Time-based trends**: 3-year rolling average trends
- **Category-based features**: Category share ratios

### Sustainability Score Calculation
```python
# Formula from 01_veri_hazirlama.py
waste_score = max(0, 1 - (Waste_Per_Capita_kg / 0.5))
economic_score = max(0, 1 - (Economic_Loss_Per_Capita_USD / 300))
carbon_score = max(0, 1 - (Carbon_Per_Capita_kgCO2e / 0.5))
sustainability = (waste_score * 0.4 + economic_score * 0.3 + carbon_score * 0.3) * 100
```

### Data Quality Improvements
- **Outlier handling**: Winsorization (clipping to 1%-99% range)
- **Missing value imputation**: KNN Imputer and median imputation
- **Encoding**: Label Encoding for categorical variables

## 🤖 Machine Learning Models

### Model Selection and Performance (from 02_model_egitimi.py)
- **Primary Model**: Gradient Boosting Regressor
- **Alternative Models**: Random Forest, Linear Regression, Ridge, Lasso
- **Multi-target**: Total Waste, Economic Loss, Carbon Footprint

### Model Performance Metrics
| Metric | Value |
|--------|-------|
| Test R² Score | 96.0% |
| Cross-Validation R² | 95.8% |
| Overfitting Gap | 0.8% |
| MAPE | 10.2% |

### Model Validation
- **Train-Test Split**: 80%/20%
- **Cross-Validation**: 3-fold CV
- **A/B Testing**: 27 different model-feature combinations
- **SHAP Analysis**: Model interpretability

### A/B Testing Results (from 03_ab_testing_analizi.py)
- **Total Tests**: 27 combinations
- **Best Model**: Gradient Boosting
- **Best Feature Group**: Core + Trends
- **Target Variables**: 3 (Waste, Economic Loss, Carbon)

## 📈 Critical Findings and Insights

### Food Waste by Category (from Dataset)
1. **Prepared Food**: 17.9M tons (highest)
2. **Beverages**: 16.4M tons
3. **Bakery Items**: 15.6M tons
4. **Fruits & Vegetables**: 15.5M tons
5. **Meat & Seafood**: 15.4M tons
6. **Dairy Products**: 15.3M tons
7. **Frozen Food**: 15.0M tons
8. **Grains & Cereals**: 14.2M tons (lowest)

### Country Performance (from Dashboard Analysis)
- **Highest Waste**: Turkey (6.9M tons), Canada (6.8M tons), Spain (6.8M tons)
- **Lowest Waste**: Indonesia, Brazil, China
- **Highest CO2**: Turkey (6.9B kg), Canada (6.8B kg), Spain (6.8B kg)
- **Sustainability Leaders**: China (86.7), Russia (86.2), USA (85.2)

### Pandemic Impact (from Dashboard Analysis)
- **General Effect**: Slight decrease during pandemic (%1.0 waste, %1.6 economic loss)
- **Sustainability**: %0.4 increase during pandemic (83.6 → 83.9)
- **Food Categories**: 
  - **Beverages**: %6.5 increase (most affected)
  - **Dairy Products**: %10.3 decrease (most decreased)
  - **Prepared Food**: %4.8 decrease (ready-to-eat consumption decline)
- **Country-based Impact**:
  - **Most increased**: Indonesia (%24.3), Argentina (%23.3), UK (%14.5)
  - **Most decreased**: Saudi Arabia (%13.1), China (%10.4), USA (%9.7)
- **Post-pandemic Trend**: Slight recovery in 2022-2024 (%1.1 increase)

### Model Success and Insights
- **96.0% Test R²**: Model makes predictions with very high accuracy

### SHAP Analysis Results (Model Interpretability)

#### Most Important Features (For All Targets):
1. **Category_Waste_Share**: Food category waste share (most effective)
2. **Waste_Efficiency**: Waste efficiency (second most effective)
3. **Population (Million)**: Population size
4. **GDP_Per_Capita_Proxy**: GDP per capita
5. **Country_Trend**: Country trend
6. **Waste_Trend**: Waste trend
7. **Population_Material_Interaction**: Population-material interaction

#### Target-based Importance Ranking:
- **Total Waste**: Category_Waste_Share > Waste_Efficiency > Population
- **Economic Loss**: Category_Economic_Share > GDP_Per_Capita_Proxy > Population
- **Carbon Footprint**: Category_Waste_Share > Waste_Efficiency > Population

#### Pandemic Impact:
- **Is_Pandemic_Year**: Low impact on all targets (33-47 importance score)
- **Is_Post_Pandemic**: Lowest impact (2-3 importance score)

### Dashboard Features and Modules (22 Modules)

#### 📊 Analysis Modules
1. **Home**: Project summary and basic metrics
2. **Data Analysis**: Interactive data exploration
3. **Trend Analysis**: Time series visualizations
4. **Geographic Analysis**: Country-based comparisons
5. **Category Analysis**: Food type-based examinations
6. **Sustainability Scores**: Country performance
7. **Carbon Footprint**: Environmental impact analysis
8. **Economic Impact**: Financial loss calculations

#### 🤖 AI and Model Modules
9. **Model Performance**: ML model results
10. **SHAP Analysis**: Feature importance levels
11. **A/B Testing**: Model comparisons
12. **Prediction Engine**: Future projections
13. **AI Assistant**: Smart recommendations system

#### 🎯 Policy and Strategy Modules
14. **Policy Simulator**: What-if analyses
15. **ROI Calculator**: Investment return
16. **Driver Analysis**: Factor impact analysis
17. **Anomaly Monitoring**: Abnormal situation detection
18. **Carbon Flows**: Environmental impact maps

#### 📋 Reporting Modules
19. **Report Builder**: Automatic report generation
20. **Model Card**: Model documentation
21. **Data Quality**: Data accuracy report
22. **About**: Project information

### Dashboard Output Analysis and Reasons

#### Sustainability Scores (0-100 Range)
- **China (86.7)**: Low per capita waste (0.22 kg) and carbon (0.22 kg CO2e) values
- **Russia (86.2)**: Population advantage and natural resource wealth
- **USA (85.2)**: Technology and efficiency-focused approach

#### Highest Waste Producing Countries
- **Turkey (6.9M tons)**: Population density and developing economy
- **Canada (6.8M tons)**: Large geography and cold climate effect
- **Spain (6.8M tons)**: Tourism sector and food culture

#### Food Category Distribution
- **Prepared Food (17.9M tons)**: Ready-to-eat food consumption habits
- **Beverages (16.4M tons)**: Large volume of beverage sector
- **Bakery Items (15.6M tons)**: High fresh product waste

#### CO2 Footprint Impact
- **Turkey (6.9B kg)**: Industrial production and energy consumption
- **Canada (6.8B kg)**: Natural resource extraction and processing
- **Spain (6.8B kg)**: Agriculture and tourism sector impact
- **0.8% Overfitting Gap**: Model has excellent generalization ability
- **10.2% MAPE**: Low mean absolute percentage error
- **Gradient Boosting**: Best performing model

## 🎛️ Dashboard Modules (22 Modules)

### 📊 Analysis Modules
1. **Overview**: Project summary and basic metrics
2. **Data Exploration**: Interactive data analysis
3. **Trend Analysis**: Time series visualizations
4. **Geographic Analysis**: Country-based comparisons
5. **Category Analysis**: Food type-based examinations
6. **Sustainability Scores**: Country performance
7. **Carbon Footprint**: Environmental impact analysis
8. **Economic Impact**: Financial loss calculations

### 🤖 AI and Model Modules
9. **Model Performance**: ML model results
10. **SHAP Analysis**: Feature importance levels
11. **A/B Testing**: Model comparisons
12. **Prediction Engine**: Future projections
13. **AI Assistant**: Smart recommendations system

### 🎯 Policy and Strategy Modules
14. **Policy Simulator**: What-if analyses
15. **ROI Calculator**: Investment return
16. **Driver Analysis**: Factor impact analysis
17. **Anomaly Monitoring**: Abnormal situation detection
18. **Carbon Flows**: Environmental impact maps

### 📋 Reporting Modules
19. **Report Builder**: Automatic report generation
20. **Model Card**: Model documentation
21. **Data Quality**: Data accuracy report
22. **About**: Project information

## 🚀 Technical Features

### Technology Stack
- **Frontend**: Streamlit
- **Backend**: Python
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **ML**: Scikit-learn, SHAP
- **Deployment**: Streamlit Cloud

### Performance Features
- **Real-time Analysis**: Instant data processing
- **Interactive Charts**: Dynamic visualizations
- **Responsive Design**: Mobile-compatible interface
- **Fast Loading**: Optimized performance

## 📊 Results and Recommendations

### Key Findings
- 40% of global food waste is household type
- Annual economic loss: 1.3 trillion USD
- Carbon footprint: 3.3 gigatons CO2e
- Average sustainability score: 84/100
- Highest sustainability: China (86.5/100)

### Critical Insights

#### 1. **Model Success**
- **96.0% accuracy** with very high prediction success
- **Low overfitting** (0.8%) with reliable generalization
- **Gradient Boosting** most effective model

#### 2. **Data Quality**
- **29 new features** enriched dataset
- **Winsorization** for outlier control
- **KNN Imputation** for missing data filling

#### 3. **Sustainability Analysis**
- **Multi-factor scoring** system
- **Weighted calculation** (waste 40%, economic 30%, carbon 30%)
- **Normalized scores** in 0-100 range

#### 4. **Country Performance**
- **Turkey, Canada, Spain** highest waste
- **China, Russia, Spain** highest sustainability
- **Geographic differences** significant

### Action Recommendations

#### 1. **Policy Level**
- **Food waste laws** and incentives
- **International cooperation** programs
- **Sustainability goal** setting

#### 2. **Corporate Level**
- **Supply chain optimization**
- **Waste management systems**
- **Green technology investments**

#### 3. **Individual Level**
- **Awareness campaigns**
- **Education programs**
- **Behavior change** incentives

#### 4. **Technological**
- **IoT and AI-supported** solutions
- **Blockchain** supply chain tracking
- **Smart waste management** systems

### Future Development Recommendations

#### 1. **Model Improvements**
- **Deep Learning** model integration
- **Real-time** prediction systems
- **Ensemble** model combinations

#### 2. **Dashboard Improvements**
- **Mobile app** development
- **API** integration
- **Multi-language** support

#### 3. **Data Expansion**
- **More countries** addition
- **New data sources** integration
- **Real-time** data flow

## 🔗 Live Dashboard

**🌐 Access Link**: [Ecolense Intelligence Dashboard](https://ecolense-intelligence.streamlit.app/)

### Dashboard Features:
- **22 Interactive Modules**: Comprehensive analysis tools
- **Real-time Data**: Current analyses with 5000+ observations
- **AI-powered Recommendations**: Smart insights and suggestions
- **Advanced Visualization**: Interactive charts with Plotly
- **Mobile Compatible**: Usable on all devices
- **Automatic Reporting**: Report generation in PDF and HTML formats

## 📁 Project Structure

```
EcolenseIntelligence/
├── app.py                          # Main Streamlit application
├── 01_veri_hazirlama.py            # Data preparation and feature engineering
├── 02_model_egitimi.py             # Model training and evaluation
├── 03_ab_testing_analizi.py        # A/B testing and model comparison
├── data/                           # Datasets
├── models/                         # ML models
├── static/                         # Visual files
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```

## 👥 Project Team

**Miuul Data Scientist Bootcamp Final Project**

- **Özge Güneş**: Data Scientist

**Project Period**: 2025

## 📚 References

- FAO (Food and Agriculture Organization)
- OECD (Organisation for Economic Co-operation and Development)
- World Bank Development Indicators
- UN Environment Programme
- European Environment Agency

## 🛠️ Installation and Running

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

---

**🌱 Data-driven solutions for a sustainable future** 