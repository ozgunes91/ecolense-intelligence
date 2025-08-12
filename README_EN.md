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

### Feature Engineering
- **Per capita metrics**: Waste, economic loss, carbon footprint
- **Temporal features**: Pandemic period, year trends, cyclical features
- **Geographic features**: Continent, hemisphere, development level
- **Derived features**: Efficiency, intensity, share ratios

## 🤖 Machine Learning Models

### Model Selection and Performance
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

## 📈 Critical Findings

### Food Waste by Category
1. **Prepared Foods**: Highest waste rate
2. **Fruits & Vegetables**: Second highest
3. **Dairy Products**: Third highest
4. **Grains & Cereals**: Fourth highest

### Country Performance
- **Highest Waste**: China, USA, India
- **Lowest Waste**: Australia, Canada, Germany
- **Sustainability Leaders**: China (86.5), Russia (86.2), Spain (84.7)

### Pandemic Impact
- 15-20% increase in 2020-2021 period
- 30% increase in household waste
- 40% decrease in restaurant waste

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

### Action Recommendations
1. **Policy Level**: Food waste laws and incentives
2. **Corporate Level**: Supply chain optimization
3. **Individual Level**: Awareness campaigns
4. **Technological**: IoT and AI-supported solutions

## 🔗 Live Dashboard

**🌐 Access Link**: [Ecolense Intelligence Dashboard](https://ecolense-intelligence.streamlit.app/)

## 📁 Project Structure

```
EcolenseIntelligence/
├── app.py                          # Main Streamlit application
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