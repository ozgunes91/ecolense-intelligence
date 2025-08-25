# 🌱 **ECOLENSE INTELLIGENCE**
### *Premium Global Food Waste Analysis and Sustainable Solutions Platform*

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3+-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](https://ecolense-intelligence.streamlit.app/)

---

## 📊 **PROJECT SUMMARY**

<div align="center">

| 🎯 **Objective** | 📈 **Scope** | 🤖 **Technology** | 📊 **Performance** |
|:-------------:|:-------------:|:----------------:|:-----------------:|
| Global food waste analysis | 20 countries, 8 categories | Gradient Boosting | 95.7% Test R² |
| Sustainability scoring | 5000+ observations | SHAP Analysis | 0.8% Overfitting |
| Policy recommendations | 37 variables | Model Comparison | 22 Modules |

</div>

---

## 🌍 **PROBLEM DEFINITION**

### 📈 **Global Food Waste Crisis**

> **FAO Report (2021):** **33%** of food produced worldwide is wasted
> 
> **UNEP Study:** Food waste accounts for **8-10%** of global greenhouse gas emissions
> 
> **World Bank Analysis:** Household waste in developing countries, supply chain waste in developed countries
> 
> **OECD Research:** Per capita waste rates inversely proportional to country development level

### 🎯 **Our Solution Approach**
- **Machine Learning** for proactive analysis
- **AI-Powered** policy recommendations
- **Real-Time** dashboard platform
- **Sustainability** focused solutions

---

## 📚 **LITERATURE REVIEW AND RESEARCH**

### 🔬 **Existing Solutions and Gaps**

| **Research Area** | **Current State** | **Gaps** | **Our Contribution** |
|:-------------------|:-----------------|:----------------|:-------------------|
| **Data Analysis** | Static reports | No real-time analysis | Dynamic dashboard |
| **Modeling** | Simple regression | No multi-target | Gradient Boosting |
| **Visualization** | Basic charts | No interactivity | Plotly + Streamlit |
| **Recommendations** | General advice | No personalization | AI Assistant |

### 📖 **Reference Sources**
- **FAO (Food and Agriculture Organization)** - Food security reports
- **OECD (Organisation for Economic Co-operation and Development)** - Economic analyses
- **World Bank** - Development indicators
- **UN Environment Programme** - Environmental impact assessments
- **European Environment Agency** - Sustainability metrics

---

## 📊 **DATASET AND METHODOLOGY**

### 🗂️ **Data Sources**

<div align="center">

| **Dataset** | **Variables** | **Observations** | **Period** | **Source** |
|:-------------:|:-------------------:|:-----------------:|:---------:|:----------:|
| **Global Food Wastage** | 8 | 5000 | 2018-2024 | Kaggle |
| **Material Footprint** | 32 | 197 | 1990-2021 | Kaggle |
| **Merged Data** | 37 | 5000 | 2018-2024 | Inner Join |

</div>

**📝 Dataset Note:** This dataset is a small-scale sample of real-world data. The total waste amount (125 million tons) represents a very small fraction of real-world values (1.3 billion tons/year). Therefore, per-capita values and sustainability scores are calculated specifically for this dataset.

### 🔧 **Data Enrichment Process**

#### **1. Data Merging (Inner Join)**
```python
# Country matching with ISO codes
merged_df = food_waste.merge(material_footprint, 
                            left_on='Country', 
                            right_on='Country', 
                            how='inner')
```

#### **2. Feature Engineering (29 New Variables)**

| **Category** | **Features** | **Count** | **Example** |
|:-------------|:---------------|:---------|:----------|
| **📊 Per-Capita Metrics** | Per capita calculations | 6 | `Waste_Per_Capita_kg` |
| **⏰ Temporal Features** | Time-based variables | 8 | `Pandemic_Indicator` |
| **🌍 Geographic Features** | Continent, hemisphere | 4 | `Continent`, `Hemisphere` |
| **📈 Derived Features** | Efficiency, intensity | 6 | `Waste_Efficiency` |
| **🔄 Interaction Features** | Cross calculations | 3 | `Population_Material_Interaction` |
| **📊 Time-Based Trends** | Rolling average | 2 | `Waste_Trend_3Y` |

#### **3. Sustainability Score Calculation**
```python
def calculate_sustainability_score(row):
    # Real-world thresholds (adjusted for dataset)
    waste_threshold = 150  # kg/person/year (dataset average: 109.5)
    economic_threshold = 40  # USD/person/year (dataset average: 35.4)
    carbon_threshold = 0.5  # kg CO2e/person/year (based on dataset average)
    
    waste_score = max(0, 1 - (row['Waste_Per_Capita_kg'] / waste_threshold))
    economic_score = max(0, 1 - (row['Economic_Loss_Per_Capita_USD'] / economic_threshold))
    carbon_score = max(0, 1 - (row['Carbon_Per_Capita_kgCO2e'] / carbon_threshold))
    
    sustainability = (waste_score * 0.4 + economic_score * 0.3 + carbon_score * 0.3) * 100
    return max(0, min(100, sustainability))
```

### 🛠️ **Data Quality Improvements**

#### **📊 Missing Data Analysis and Imputation**
| **Data Type** | **Missing Count** | **Imputation Method** | **Reason** |
|:--------------|:---------------|:-------------------|:----------|
| **Material Footprint** | 2514 observations | Median value | Missing after merge |
| **Continent/Hemisphere** | 20 countries | Manual assignment | Geographic info missing |
| **Numeric Values** | Minimal | Median imputation | Data consistency |

#### **🔧 Missing Data Imputation Strategy**
```python
# Material Footprint missing values
footprint_median = merged_df['Material_Footprint_Per_Capita'].median()
merged_df['Material_Footprint_Per_Capita'].fillna(footprint_median, inplace=True)

# Manual continent assignment
country_continent_map = {
    'Turkey': 'Europe', 'USA': 'America', 'Germany': 'Europe',
    'France': 'Europe', 'UK': 'Europe', 'Italy': 'Europe',
    'Spain': 'Europe', 'Australia': 'Oceania', 'Indonesia': 'Asia',
    'India': 'Asia', 'China': 'Asia', 'South Africa': 'Africa',
    'Japan': 'Asia', 'Brazil': 'America', 'Canada': 'America',
    'Mexico': 'America', 'Russia': 'Europe', 'South Korea': 'Asia',
    'Saudi Arabia': 'Asia', 'Argentina': 'America'
}

# Median for numeric values
for col in numeric_cols:
    if merged_df[col].isnull().sum() > 0:
        median_val = merged_df[col].median()
        merged_df[col].fillna(median_val, inplace=True)
```

#### **📈 Other Data Quality Improvements**
| **Process** | **Method** | **Impact** |
|:----------|:----------|:---------|
| **Outliers** | Winsorization (1%-99%) | 15% improvement |
| **Categorical Encoding** | Label Encoding | Standardization |
| **Scaling** | StandardScaler | Model performance |

---

## 🤖 **MACHINE LEARNING MODELS**

### 🎯 **Model Selection and Performance (from 02_model_egitimi.py)**

#### **🏆 Main Model: Gradient Boosting Regressor**
- **Algorithm:** Gradient Boosting
- **Hyperparameters:** n_estimators=100, max_depth=4, learning_rate=0.05
- **Selection Criteria:** Model Comparison Winner + CV R² + Overfitting Control

#### **🔄 Alternative Models**
- **Random Forest:** Conservative approach
- **Linear Regression:** Baseline model
- **Ridge Regression:** Regularization
- **Lasso Regression:** Feature selection

#### **🎯 Multi-Target Approach**
- **Total Waste (Tons)**
- **Economic Loss (Million $)**
- **Carbon_Footprint_kgCO2e**

### 📊 **Model Performance Metrics**

<div align="center">

| **Metric** | **Value** | **Status** |
|:-----------|:----------|:----------|
| **Test R² Score** | **95.7%** | 🟢 Excellent |
| **Cross-Validation R²** | **95.8%** | 🟢 Excellent |
| **Overfitting Gap** | **0.8%** | 🟢 Very Good |
| **MAPE** | **10.2%** | 🟡 Good |

</div>

### ✅ **Model Validation**

| **Method** | **Details** | **Result** |
|:-----------|:----------|:----------|
| **Train-Test Split** | 80%/20% | ✅ Valid |
| **Cross-Validation** | 3-fold CV | ✅ Stable |
| **Model Comparison** | 27 combinations | ✅ Optimized |
| **SHAP Analysis** | Model explainability | ✅ Transparent |

---

## 🧪 **MODEL COMPARISON RESULTS (from 03_model_karsilastirma_analizi.py)**

### 📈 **Test Scope**

| **Test Group** | **Combination** | **Result** |
|:---------------|:----------------|:----------|
| **Model Types** | 3 different models | Gradient Boosting won |
| **Feature Groups** | 3 different groups | Core + Efficiency best |
| **Total Tests** | 27 combinations | 96.0% success |

### 🏆 **Best Performing Combinations**

| **Target** | **Model** | **Feature Group** | **Test R²** | **Overfitting** |
|:----------|:----------|:------------------|:------------|:----------------|
| **Total Waste** | Gradient Boosting | Core + Efficiency | 0.959 | 0.008 |
| **Economic Loss** | Gradient Boosting | Core + Trends | 0.955 | 0.012 |
| **Carbon Footprint** | Gradient Boosting | Core + Efficiency | 0.959 | 0.008 |

---

## 🔍 **CRITICAL FINDINGS AND INSIGHTS**

### 🏆 **Sustainability Leaders**

<div align="center">

| **Rank** | **Country** | **Sustainability Score** | **Key Feature** |
|:--------:|:---------|:---------------------------|:----------------------|
| **🥇** | **UK** | **45.59** | Balanced waste management |
| **🥈** | **Spain** | **44.30** | Efficient food management |
| **🥉** | **Russia** | **43.70** | Medium sustainability level |

</div>

### 🗑️ **Countries with Lowest Sustainability Scores**

| **Rank** | **Country** | **Sustainability Score** | **Main Issue** |
|:--------:|:---------|:---------------------------|:-------------|
| **1** | **Saudi Arabia** | **40.9** | High per capita waste |
| **2** | **France** | **41.0** | Inefficient food management |
| **3** | **Italy** | **41.5** | Medium sustainability level |

### 🍎 **Food Waste by Category (Dataset)**

| **Category** | **Total Waste (Million Tons)** | **Share (%)** | **Main Issue** |
|:-------------|:-----------------------------|:------------|:-------------|
| **Prepared Food** | **17.9M** | **14.3%** | Expiry date |
| **Beverages** | **16.4M** | **13.1%** | Packaging issues |
| **Bakery Items** | **15.6M** | **12.4%** | Fresh product waste |
| **Fruits & Vegetables** | **15.5M** | **12.4%** | Storage issues |
| **Meat & Seafood** | **15.4M** | **12.3%** | Hygiene standards |
| **Dairy Products** | **15.3M** | **12.2%** | Cold chain |
| **Frozen Food** | **15.0M** | **12.0%** | Freeze/thaw cycle |
| **Grains & Cereals** | **14.2M** | **11.3%** | Lowest waste |

### 🦠 **Pandemic Impact Analysis**

#### **General Impact**
- **General Waste:** Pandemic years (2020-2022) available in dataset
- **Economic Loss:** Pandemic effects can be analyzed
- **Carbon Footprint:** Changes during pandemic period observable

#### **Dataset Coverage**
| **Period** | **Year Range** | **Data Availability** |
|:----------|:----------------|:---------------------|
| **Pre-Pandemic** | 2018-2019 | ✅ Available |
| **Pandemic Period** | 2020-2022 | ✅ Available |
| **Post-Pandemic** | 2023-2024 | ✅ Available |

#### **Analysis Note**
- Pandemic impact analysis can be performed using "Data Analysis" page in dashboard
- Time series analysis can observe trend changes

---

## 🧠 **SHAP ANALYSIS RESULTS**

### 📊 **Most Important Features (Top 5)**

#### **Total Waste (Tons) Target (SHAP Analysis)**
| **Feature** | **SHAP Importance Score** | **Impact** |
|:------------|:-------------------|:---------|
| **Category_Waste_Share** | **62.6%** | 🟢 Very High |
| **Population (Million)** | **10.4%** | 🟢 High |
| **Waste_Efficiency** | **8.8%** | 🟡 Medium |
| **Carbon_Per_Capita_kgCO2e** | **7.2%** | 🟡 Medium |
| **Waste_Trend** | **2.3%** | 🟡 Low |

#### **Economic Loss (Million $) Target (SHAP Analysis)**
| **Feature** | **SHAP Importance Score** | **Impact** |
|:------------|:-------------------|:---------|
| **Category_Economic_Share** | **62.4%** | 🟢 Very High |
| **Population (Million)** | **10.2%** | 🟢 High |
| **Economic_Loss_Per_Capita_USD** | **7.7%** | 🟡 Medium |
| **GDP_Per_Capita_Proxy** | **7.4%** | 🟡 Medium |
| **Economic_Intensity** | **2.6%** | 🟡 Low |

#### **Carbon_Footprint_kgCO2e Target (SHAP Analysis)**
| **Feature** | **SHAP Importance Score** | **Impact** |
|:------------|:-------------------|:---------|
| **Category_Waste_Share** | **62.6%** | 🟢 Very High |
| **Population (Million)** | **10.4%** | 🟢 High |
| **Waste_Efficiency** | **8.7%** | 🟡 Medium |
| **Carbon_Per_Capita_kgCO2e** | **7.3%** | 🟡 Medium |
| **Waste_Trend** | **2.3%** | 🟡 Low |

### 🔍 **Pandemic Impact Analysis**
- **Is_Pandemic_Year:** 0.2% impact (detected in SHAP analysis)
- **Year_Trend:** Time-based increase trend
- **Is_Post_Pandemic:** 0.02% impact (detected in SHAP analysis)
- **Pandemic impact is similar across all targets (0.1-0.3% range)**

---

## 🖥️ **DASHBOARD MODULES**

### 📊 **22 Premium Modules**

<div align="center">

| **Module Category** | **Module Count** | **Key Features** |
|:---------------------|:-----------------|:-------------------|
| **🏠 Core Modules** | 5 | Data analysis, model performance |
| **🤖 AI-Powered** | 4 | Predictions, recommendations, simulation |
| **📈 Analytics** | 6 | SHAP, Model comparison, ROI |
| **📄 Reporting** | 4 | Report generator, model card |
| **⚙️ Utility** | 3 | Settings, help, about |

</div>

### 🎯 **Module Details and Benefits**

#### **🏠 Core Modules**
| **Module** | **Purpose** | **Benefits** | **User Capabilities** |
|:----------|:---------|:-------------|:-------------------------|
| **Home** | General overview | Quick KPI access | Dashboard navigation |
| **Data Analysis** | Data exploration | Detailed analysis | Filtering and visualization |
| **Model Performance** | Model evaluation | Performance tracking | Metric comparison |
| **Future Predictions** | Prediction modeling | Future planning | Scenario analysis |
| **AI Insights** | Smart recommendations | Automatic insights | Receive recommendations |

#### **🤖 AI-Powered Modules**
| **Module** | **Purpose** | **Benefits** | **User Capabilities** |
|:----------|:---------|:-------------|:-------------------------|
| **Policy Simulator** | Policy testing | Risk assessment | What-if analysis |
| **Goal Planner** | Goal setting | Strategic planning | Goal optimization |
| **ROI Calculator** | Investment analysis | Financial evaluation | ROI calculation |
| **Model Comparison** | Model comparison | Performance optimization | Test results |

#### **📈 Analytics Modules**
| **Module** | **Purpose** | **Benefits** | **User Capabilities** |
|:----------|:---------|:-------------|:-------------------------|
| **SHAP Analysis** | Model explainability | Transparency | Feature importance analysis |
| **Category Analysis** | Category-based analysis | Detailed examination | Category comparison |
| **Country Comparison** | Country analysis | Benchmarking | Country performance |
| **Trend Analysis** | Time series | Trend tracking | Time-based analysis |
| **Correlation Matrix** | Relationship analysis | Dependency discovery | Correlation examination |
| **Data Quality** | Data evaluation | Quality control | Data validation |

#### **📄 Reporting Modules**
| **Module** | **Purpose** | **Benefits** | **User Capabilities** |
|:----------|:---------|:-------------|:-------------------------|
| **Report Generator** | Automatic reporting | Time saving | Report download |
| **Model Card** | Model documentation | Transparency | Model details |
| **Performance Report** | Detailed analysis | Comprehensive evaluation | Performance tracking |
| **Data Report** | Data summary | Quick overview | Data understanding |

### 🤖 **AI Assistant System**
- **Automatic Smart Recommendations:** Recommendations based on model performance
- **Real-Time Insights:** Instant analysis and advice
- **Personalized Recommendations:** Customization based on user needs

---

## 🎯 **RESULTS AND RECOMMENDATIONS**

### 🏆 **Critical Insights**

#### **1. Model Performance**
- **95.7% Test R²:** Excellent prediction power
- **0.8% Overfitting Gap:** Very good generalization
- **95.8% CV R²:** Stable performance

#### **2. Data Quality**
- **5000+ observations:** Comprehensive dataset
- **37 variables:** Rich feature set
- **20 countries:** Global scope

#### **3. Business Value**
- **22 modules:** Comprehensive platform
- **AI-powered:** Smart recommendations
- **Real-time:** Instant analysis

### 💡 **Global Sustainability Insights and Action Recommendations**

#### **🌍 Global Insights**

##### **📊 Social Sustainability**
One-third of the food produced worldwide is wasted, amounting to 1.3 billion tons of food loss. While household waste is more common in developing countries, supply chain waste occurs throughout developed countries. This situation increases social inequalities and threatens food security. Education and awareness programs are critically important to solve this problem. Additionally, food waste has indirect effects on health systems.

##### **💰 Economic Sustainability**
Food waste causes an annual economic loss of 1.2 trillion USD. This is a significant burden on the world economy. Through supply chain optimization, 15-20% savings can be achieved. Investments in sustainable food systems provide 25-30% return on investment. Rising food prices and supply-demand imbalance also threaten economic stability.

##### **🌱 Environmental Sustainability**
Food waste accounts for 8-10% of global greenhouse gas emissions. This is one of the main causes of climate change. 250 km³ of water is used annually for wasted food. 1.4 billion hectares of agricultural land is used solely for food production that will be wasted. This situation reduces biodiversity and creates great pressure on ecosystems.

#### **🎯 Global Goals (2030)**

##### **📈 Social Goals**
We aim to reduce food waste by 50% by 2030. This aligns with the United Nations Sustainable Development Goal 12.3. We plan to ensure food security for 2 billion people and provide sustainable food education to 1 billion people. We aim to strengthen social justice by reducing inequalities in food access.

##### **💼 Economic Goals**
We aim to save 600 billion USD by reducing economic losses. We plan to create 10 million new jobs in the sustainable food sector and increase supply chain efficiency by 30%. We aim to attract 500 billion USD in sustainable food investment.

##### **🌿 Environmental Goals**
We aim to reduce 2.5 gigatons of CO2 emissions from the food sector. We plan to save 125 km³ of water to protect water resources. We aim to save 700 million hectares of land to protect natural areas and transition to a circular economy with an 80% recycling rate.

#### **🏛️ For Policy Makers**
- **Targeted Policies:** Category-based strategies
- **Country-Specific:** Regional solutions
- **Technology Investment:** IoT and blockchain
- **Regulation:** Food waste laws and standards
- **Incentive Programs:** Sustainable food production support

#### **🏢 For Business**
- **Supply Chain:** Optimization
- **Customer Education:** Awareness raising
- **Technology Adoption:** Smart systems
- **Sustainable Business Model:** Circular economy approach
- **Social Responsibility:** Food banks and donation programs

#### **🏫 For Educational Institutions**
- **Curriculum Update:** Sustainability-focused
- **Research Support:** Data-driven studies
- **Awareness Programs:** Student education
- **Applied Projects:** Food waste prevention campaigns
- **International Collaborations:** Global research networks

#### **🌍 For Civil Society**
- **Awareness Campaigns:** Social consciousness
- **Volunteer Programs:** Active participation
- **Monitoring Systems:** Transparency
- **Community Initiatives:** Local food rescue programs
- **Social Media:** Digital awareness campaigns

---

## 🚀 **FUTURE DEVELOPMENT RECOMMENDATIONS**

### 📱 **Phase 2: Model Improvements**
- **Deep Learning Models:** LSTM, Transformer
- **Real-time APIs:** Automatic updates
- **AutoML:** Automatic model selection
- **Ensemble Methods:** Multiple model combination

### 📱 **Phase 3: Dashboard Improvements**
- **Mobile App:** React Native
- **Multi-language:** 5 language support
- **Push Notifications:** Instant notifications
- **Offline Mode:** Offline operation

### 🌐 **Phase 4: Data Expansion**
- **IoT Sensors:** Real-time data
- **Blockchain:** Transparent supply chain
- **50+ Countries:** Extended scope
- **Satellite Data:** Remote sensing

### 💼 **Phase 5: Business Model Development**
- **SaaS Platform:** Subscription model
- **Enterprise Integrations:** API services
- **Policy Consulting:** Expert services
- **Training Programs:** Certification courses

---

## 🔗 **LIVE DASHBOARD ACCESS**

<div align="center">

### 🌐 **[Ecolense Intelligence Dashboard](https://ecolense-intelligence.streamlit.app/)**

[![Streamlit](https://img.shields.io/badge/Streamlit-Cloud-blue?style=for-the-badge&logo=streamlit)](https://ecolense-intelligence.streamlit.app/)
[![Status](https://img.shields.io/badge/Status-Live-brightgreen?style=for-the-badge)](https://ecolense-intelligence.streamlit.app/)

</div>

---

## 🎯 **DASHBOARD FEATURES**

### ✨ **Core Features**
- **🔄 Real-Time Updates:** Instant data refresh
- **📱 Responsive Design:** Compatible with all devices
- **🎨 Modern UI/UX:** User-friendly interface
- **⚡ Fast Performance:** Optimized code

### 🤖 **AI-Powered Features**
- **🧠 Smart Recommendations:** Model-based advice
- **🔮 Future Predictions:** Machine learning predictions
- **📊 Automatic Analysis:** Instant insight generation
- **🎯 Personalization:** Based on user preferences

### 📈 **Analytics Features**
- **📊 Interactive Charts:** Plotly-based visualization
- **🔍 Detailed Filtering:** Multi-criteria selection
- **📋 Comprehensive Reports:** PDF/Excel export
- **🔄 Comparative Analysis:** Multiple data comparison

---

## 👥 **PROJECT TEAM**

<div align="center">

| **Member** | **Role** | **Contribution** |
|:--------|:--------|:----------|
| **Özge Güneş** | Data Scientist | Model development, analysis |
| **Kübra Saruhan** | Data Scientist | Data analysis, documentation |

</div>

### 🎓 **Project Information**
- **Institution:** Miuul Data Scientist Bootcamp
- **Project Type:** Final Project
- **Period:** 2025
- **Technology:** Python, Streamlit, Scikit-learn

---

## 📚 **REFERENCES**

### 📖 **Academic Sources**
- **FAO (2021):** "The State of Food and Agriculture"
- **UNEP (2021):** "Food Waste Index Report"
- **World Bank (2022):** "Food Loss and Waste Database"
- **OECD (2023):** "Material Resources, Productivity and the Environment"

### 🌐 **Technical Sources**
- **Scikit-learn Documentation:** Model selection and optimization
- **Streamlit Documentation:** Dashboard development
- **SHAP Documentation:** Model explainability
- **Plotly Documentation:** Interactive visualization

---

<div align="center">

### 🌱 **Data-driven solutions for a sustainable future**

[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/ozgunes91/ecolense-intelligence)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

</div> 
