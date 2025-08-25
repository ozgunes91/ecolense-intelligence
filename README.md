# 🌱 ECOLENSE Intelligence - AI-Powered Sustainability Platform

## 📋 Project Overview

**Ecolense Intelligence** is a comprehensive AI-powered platform that analyzes global food waste data and provides sustainable solutions. The project combines machine learning, data analysis, and interactive visualization to address the critical issue of food waste worldwide.

## 🎯 Key Features

- **Global Analysis:** 20 countries, 8 food categories, 5,000+ data points
- **AI-Powered Predictions:** 95.7% accuracy with Gradient Boosting
- **Interactive Dashboard:** Real-time analysis and visualization
- **SHAP Analysis:** Model explainability and feature importance
- **Interactive AI Assistant:** Personalized recommendations

## 🚀 Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
```

### Run Locally
```bash
streamlit run app.py
```

### Access Dashboard
- **Local:** http://localhost:8501
- **Live Demo:** https://ecolense-intelligence.streamlit.app/

## 📊 Dataset

### Data Sources
- **Global Food Wastage Dataset:** 8 variables, 5,000 observations (2018-2024)
- **Material Footprint Dataset:** 32 variables, 197 observations (1990-2021)
- **Enriched Dataset:** 37 features after feature engineering

### Data Processing
- Country matching with ISO codes
- 29 new engineered features
- Sustainability score calculation
- Missing value imputation and outlier detection

## 🤖 Machine Learning Models

### Model Performance
- **Gradient Boosting:** 95.7% R² score (Primary model)
- **Random Forest:** 93.8% R² score (Secondary model)
- **Linear Regression:** 87.9% R² score (Baseline model)

### Target Variables
- **Total Waste (Tons)**
- **Economic Loss (Million $)**
- **Carbon Footprint (kgCO2e)**

### Model Validation
- 3-fold Cross-Validation
- Overfitting control (< 1% gap)
- SHAP analysis for explainability

## 📈 Key Findings

### Global Impact (2018-2024)
- **Total Waste:** 125.3 million tons
- **Economic Loss:** 125.2 billion USD
- **Carbon Footprint:** 313.3 million tons CO2e
- **Sustainability Score:** Global average 42.5/100

### Most Critical Issues
- **Prepared Food:** Highest waste rate (17.9M tons)
- **Beverages:** Second highest waste rate (16.4M tons)
- **Developed Countries:** High per capita waste
- **Supply Chain:** Optimization needed

## 🛠️ Technical Stack

### Backend
- **Python 3.9+**
- **Pandas:** Data manipulation
- **NumPy:** Numerical computing
- **Scikit-learn:** Machine learning

### Frontend
- **Streamlit:** Interactive web app
- **Plotly:** Interactive visualizations
- **Matplotlib:** Static plots

### Machine Learning
- **Gradient Boosting:** Primary model
- **Random Forest:** Ensemble method
- **SHAP:** Model explainability
- **Cross-validation:** Model validation

## 📁 Project Structure

```
EcolenseIntelligence/
├── app.py                          # Main Streamlit application
├── storytelling.py                 # Interactive AI features
├── 01_veri_hazirlama.py           # Data preparation
├── 02_model_egitimi.py            # Model training
├── 03_model_karsilastirma_analizi.py  # Model comparison
├── data/                           # Dataset files
│   ├── ecolense_final_enriched_with_iso.csv
│   ├── global_food_wastage_dataset.csv
│   └── material_footprint.csv
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```

## 🌐 Access Information

- **Local URL:** http://localhost:8501
- **Network URL:** http://192.168.1.103:8501
- **Live Demo:** https://ecolense-intelligence.streamlit.app/
- **GitHub Repository:** https://github.com/ozgunes91/ecolense-intelligence

## 📊 Model Performance Metrics

| Metric | Total Waste | Economic Loss | Carbon Footprint |
|--------|-------------|---------------|------------------|
| R² Score | 0.957 | 0.957 | 0.957 |
| RMSE | 8,240 | 6,180 | 12,450 |
| MAE | 5,890 | 4,320 | 8,760 |
| MAPE | 10.2% | 10.2% | 10.2% |

## 🔮 Future Enhancements

- **Real-time Data Integration:** IoT sensors and live data feeds
- **Expanded Coverage:** 50+ countries and more food categories
- **Blockchain Integration:** Transparent supply chain tracking
- **Mobile Application:** Cross-platform mobile app
- **Advanced AI Features:** Enhanced chatbot and recommendations

## 📞 Contact

**Project Developer:** Özge Güneş  
**Email:** ozgekayagunes@gmail.com  
**Date:** August 2025  
**Institution:** Miuul Data Scientist Bootcamp  

---

*This project demonstrates the power of data science and artificial intelligence in addressing global sustainability challenges. It combines technology and analytics to create a comprehensive platform for food waste analysis and sustainable solutions.* 
