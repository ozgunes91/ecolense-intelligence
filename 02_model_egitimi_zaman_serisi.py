#!/usr/bin/env python3
import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import json
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import shap

class ZamanSerisiModelEgitimi:
    def __init__(self):
        self.df = None
        self.models = {}
        self.model_metrics = {}
        self.target_columns = ['Total Waste (Tons)', 'Economic Loss (Million $)', 'Carbon_Footprint_kgCO2e', 'Sustainability_Score']
        
    def veri_yukle(self):
        """Veriyi yükle ve zaman serisi için hazırla"""
        print("🚀 ZAMAN SERİSİ MODEL EĞİTİMİ BAŞLIYOR...")
        print("=" * 60)
        
        print("📊 Veri yükleniyor...")
        self.df = pd.read_csv('data/ecolense_final_enriched_with_iso.csv')
        
        # Zaman serisi için veriyi sırala
        self.df = self.df.sort_values(['Country', 'Year']).reset_index(drop=True)
        print(f"✅ Veri yüklendi ve sıralandı: {self.df.shape}")
        
        # Zaman serisi özellikleri ekle
        self.zaman_serisi_ozellikleri_ekle()
        
    def zaman_serisi_ozellikleri_ekle(self):
        """Zaman serisi için özel özellikler ekle"""
        print("\n⏰ Zaman serisi özellikleri ekleniyor...")
        
        # Ülke bazında lag özellikleri
        for target in self.target_columns:
            if target in self.df.columns:
                # 1 yıl önceki değer
                self.df[f'{target}_lag1'] = self.df.groupby('Country')[target].shift(1)
                # 2 yıl önceki değer
                self.df[f'{target}_lag2'] = self.df.groupby('Country')[target].shift(2)
                # 3 yıl önceki değer
                self.df[f'{target}_lag3'] = self.df.groupby('Country')[target].shift(3)
                
                # Rolling mean (3 yıl)
                self.df[f'{target}_rolling_mean3'] = self.df.groupby('Country')[target].rolling(window=3, min_periods=1).mean().reset_index(0, drop=True)
                
                # Rolling std (3 yıl)
                self.df[f'{target}_rolling_std3'] = self.df.groupby('Country')[target].rolling(window=3, min_periods=1).std().reset_index(0, drop=True)
                
                # Trend (son 3 yılın eğimi)
                self.df[f'{target}_trend'] = self.df.groupby('Country')[target].rolling(window=3, min_periods=1).apply(
                    lambda x: np.polyfit(range(len(x)), x, 1)[0] if len(x) > 1 else 0
                ).reset_index(0, drop=True)
        
        # Zaman bazlı özellikler
        self.df['Year_Sin'] = np.sin(2 * np.pi * self.df['Year'] / 10)  # 10 yıllık döngü
        self.df['Year_Cos'] = np.cos(2 * np.pi * self.df['Year'] / 10)
        
        # Ülke bazında büyüme oranları
        for target in self.target_columns:
            if target in self.df.columns:
                self.df[f'{target}_growth_rate'] = self.df.groupby('Country')[target].pct_change()
                self.df[f'{target}_growth_rate_lag1'] = self.df.groupby('Country')[f'{target}_growth_rate'].shift(1)
        
        print("✅ Zaman serisi özellikleri eklendi")
        
    def zaman_serisi_model_egitimi(self):
        """Zaman serisi model eğitimi"""
        print("\n🤖 Zaman serisi model eğitimi başlıyor...")
        
        for target in self.target_columns:
            print(f"\n🎯 {target} için zaman serisi model eğitimi...")
            
            # Zaman serisi özellikleri
            time_series_features = [
                'Population (Million)', 'Years_From_2018', 'Material_Footprint_Per_Capita',
                'Year_Trend', 'Country_Trend', 'Year_Cycle', 'Year_Cycle_Cos',
                'Is_Pandemic_Year', 'Is_Post_Pandemic', 'Food Category_Encoded',
                'Population_Material_Interaction', 'Year_Population_Interaction',
                'GDP_Per_Capita_Proxy', 'Waste_Efficiency', 'Economic_Intensity',
                'Waste_Trend', 'Economic_Trend', 'Category_Waste_Share', 'Category_Economic_Share',
                'Year_Sin', 'Year_Cos'
            ]
            
            # Lag özellikleri ekle
            for lag_target in self.target_columns:
                if lag_target in self.df.columns:
                    time_series_features.extend([
                        f'{lag_target}_lag1', f'{lag_target}_lag2', f'{lag_target}_lag3',
                        f'{lag_target}_rolling_mean3', f'{lag_target}_rolling_std3',
                        f'{lag_target}_trend', f'{lag_target}_growth_rate',
                        f'{lag_target}_growth_rate_lag1'
                    ])
            
            # Mevcut özellikleri kontrol et
            available_features = [f for f in time_series_features if f in self.df.columns]
            if len(available_features) != len(time_series_features):
                print(f"⚠️ Bazı özellikler eksik: {set(time_series_features) - set(self.df.columns)}")
            
            X = self.df[available_features].copy()
            y = self.df[target].copy()
            
            # NaN değerleri temizle
            mask = ~(X.isnull().any(axis=1) | y.isnull())
            X_clean = X[mask]
            y_clean = y[mask]
            
            print(f"📊 Temizlenmiş veri: {X_clean.shape}")
            
            # ZAMAN SERİSİ SPLIT (Önemli!)
            # Son 2 yılı test için ayır
            unique_years = sorted(X_clean.index.to_series().map(self.df.loc[X_clean.index, 'Year']).unique())
            train_years = unique_years[:-2]  # Son 2 yıl hariç
            test_years = unique_years[-2:]   # Son 2 yıl
            
            train_mask = self.df.loc[X_clean.index, 'Year'].isin(train_years)
            test_mask = self.df.loc[X_clean.index, 'Year'].isin(test_years)
            
            X_train = X_clean[train_mask]
            y_train = y_clean[train_mask]
            X_test = X_clean[test_mask]
            y_test = y_clean[test_mask]
            
            print(f"📈 Train seti: {X_train.shape[0]} örnek ({train_years[0]}-{train_years[-1]})")
            print(f"📊 Test seti: {X_test.shape[0]} örnek ({test_years[0]}-{test_years[-1]})")
            
            # Zaman serisi cross-validation
            tscv = TimeSeriesSplit(n_splits=3)
            
            # Modeller
            models = {
                'RandomForest': RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42),
                'GradientBoosting': GradientBoostingRegressor(n_estimators=100, max_depth=8, random_state=42)
            }
            
            best_model = None
            best_cv_r2 = -np.inf
            
            for model_name, model in models.items():
                print(f"   🔄 {model_name} test ediliyor...")
                
                # Zaman serisi cross-validation
                cv_scores = []
                for train_idx, val_idx in tscv.split(X_train):
                    X_cv_train, X_cv_val = X_train.iloc[train_idx], X_train.iloc[val_idx]
                    y_cv_train, y_cv_val = y_train.iloc[train_idx], y_train.iloc[val_idx]
                    
                    model.fit(X_cv_train, y_cv_train)
                    y_cv_pred = model.predict(X_cv_val)
                    cv_r2 = r2_score(y_cv_val, y_cv_pred)
                    cv_scores.append(cv_r2)
                
                cv_r2_mean = np.mean(cv_scores)
                cv_r2_std = np.std(cv_scores)
                
                print(f"      TS-CV R²: {cv_r2_mean:.4f} ± {cv_r2_std:.4f}")
                
                if cv_r2_mean > best_cv_r2:
                    best_cv_r2 = cv_r2_mean
                    best_model = model_name
            
            # En iyi modeli eğit
            print(f"🏆 En iyi model: {best_model}")
            
            if best_model == 'RandomForest':
                final_model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
            else:
                final_model = GradientBoostingRegressor(n_estimators=100, max_depth=8, random_state=42)
            
            # Model eğitimi
            final_model.fit(X_train, y_train)
            
            # Tahminler
            train_pred = final_model.predict(X_train)
            test_pred = final_model.predict(X_test)
            
            # Metrikler
            train_r2 = r2_score(y_train, train_pred)
            test_r2 = r2_score(y_test, test_pred)
            train_rmse = np.sqrt(mean_squared_error(y_train, train_pred))
            test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
            train_mae = mean_absolute_error(y_train, train_pred)
            test_mae = mean_absolute_error(y_test, test_pred)
            
            # MAPE hesaplama
            non_zero_mask = y_test != 0
            if non_zero_mask.sum() > 0:
                mape = np.mean(np.abs((y_test[non_zero_mask] - test_pred[non_zero_mask]) / y_test[non_zero_mask])) * 100
            else:
                mape = 0
            
            # Overfitting kontrolü
            overfitting_score = train_r2 - test_r2
            
            print(f"📊 Train R²: {train_r2:.4f}")
            print(f"📊 Test R²: {test_r2:.4f}")
            print(f"📊 TS-CV R²: {best_cv_r2:.4f}")
            print(f"📊 Train RMSE: {train_rmse:.4f}")
            print(f"📊 Test RMSE: {test_rmse:.4f}")
            print(f"📊 Train MAE: {train_mae:.4f}")
            print(f"📊 Test MAE: {test_mae:.4f}")
            print(f"📊 MAPE: {mape:.2f}%")
            print(f"📊 Overfitting: {overfitting_score:.4f}")
            
            # Overfitting değerlendirmesi
            if overfitting_score < 0.05:
                print("✅ Overfitting yok - Güçlü zaman serisi modeli!")
            elif overfitting_score < 0.1:
                print("⚠️ Hafif overfitting - Dikkat!")
            else:
                print("❌ Overfitting var - Model iyileştirilmeli!")
            
            # Model ve metrikleri kaydet
            self.models[target] = final_model
            self.model_metrics[target] = {
                'model_type': f"{best_model} (TimeSeries)",
                'train_r2': train_r2,
                'test_r2': test_r2,
                'cv_r2': best_cv_r2,
                'train_rmse': train_rmse,
                'test_rmse': test_rmse,
                'train_mae': train_mae,
                'test_mae': test_mae,
                'mape': mape,
                'overfitting_score': overfitting_score,
                'feature_count': len(available_features),
                'train_years': f"{train_years[0]}-{train_years[-1]}",
                'test_years': f"{test_years[0]}-{test_years[-1]}"
            }
            
            # SHAP analizi
            self.shap_analizi(final_model, X_test, target)
        
        print(f"\n✅ Zaman serisi model eğitimi tamamlandı! {len(self.models)} model eğitildi")
    
    def shap_analizi(self, model, X_test, target):
        """SHAP analizi yap"""
        print(f"   🔍 {target} için SHAP analizi...")
        
        try:
            # SHAP değerlerini hesapla
            if hasattr(model, 'feature_importances_'):
                explainer = shap.TreeExplainer(model)
                shap_values = explainer.shap_values(X_test)
            else:
                explainer = shap.LinearExplainer(model, X_test)
                shap_values = explainer.shap_values(X_test)
            
            # Özellik önemini hesapla
            feature_importance = np.abs(shap_values).mean(0)
            feature_names = X_test.columns
            
            # Önem sıralaması
            importance_df = pd.DataFrame({
                'feature': feature_names,
                'importance': feature_importance
            }).sort_values('importance', ascending=False)
            
            # CSV olarak kaydet
            importance_df.to_csv(f'zaman_serisi_shap_importance_{target}.csv', index=False)
            print(f"      ✅ SHAP önem CSV kaydedildi: zaman_serisi_shap_importance_{target}.csv")
            
            # Görsel oluştur
            plt.figure(figsize=(10, 8))
            plt.barh(range(len(importance_df)), importance_df['importance'])
            plt.yticks(range(len(importance_df)), importance_df['feature'])
            plt.xlabel('SHAP Önem')
            plt.title(f'{target} - Zaman Serisi Özellik Önem Sıralaması')
            plt.gca().invert_yaxis()
            plt.tight_layout()
            plt.savefig(f'zaman_serisi_shap_summary_{target}.png', dpi=300, bbox_inches='tight')
            plt.close()
            print(f"      ✅ SHAP görsel kaydedildi: zaman_serisi_shap_summary_{target}.png")
            
        except Exception as e:
            print(f"      ❌ SHAP analizi hatası: {e}")
    
    def gelecek_tahminleri(self):
        """Gelecek tahminleri oluştur (zaman serisi yaklaşımı)"""
        print("\n🔮 Zaman serisi gelecek tahminleri oluşturuluyor...")
        
        predictions = []
        
        # 2025-2030 yılları için tahmin
        for year in range(2025, 2031):
            print(f"   📅 {year} yılı tahminleri...")
            
            # Ülke bazında 2024 verilerini al
            df_2024 = self.df[self.df['Year'] == 2024].copy()
            if len(df_2024) == 0:
                last_year = self.df['Year'].max()
                df_2024 = self.df[self.df['Year'] == last_year].copy()
            
            country_2024 = df_2024.groupby('Country').agg({
                'Total Waste (Tons)': 'sum',
                'Economic Loss (Million $)': 'sum',
                'Carbon_Footprint_kgCO2e': 'sum',
                'Population (Million)': 'first',
                'Material_Footprint_Per_Capita': 'first',
                'Country_Trend': 'first'
            }).reset_index()
            
            for _, row in country_2024.iterrows():
                country = row['Country']
                print(f"      🌍 {country} için tahminler...")
                
                # Nüfus büyüme tahmini
                population_growth = row['Population (Million)'] * (1.012) ** (year - 2024)
                
                # Temel değerler
                base_waste = row['Total Waste (Tons)']
                base_economic = row['Economic Loss (Million $)']
                base_carbon = row['Carbon_Footprint_kgCO2e']
                base_material_footprint = row['Material_Footprint_Per_Capita']
                
                # Her hedef için tahmin
                for target in self.target_columns:
                    if target in self.models:
                        model = self.models[target]
                        
                        # Zaman serisi özellikleri oluştur
                        feature_values = self.zaman_serisi_ozellikleri_olustur(
                            country, year, base_waste, base_economic, base_carbon, 
                            base_material_footprint, population_growth
                        )
                        
                        # Özellik vektörü oluştur
                        X_pred = pd.DataFrame([feature_values])
                        
                        # Tahmin
                        prediction = model.predict(X_pred)[0]
                        
                        # Kişi başına değerler
                        waste_per_capita = (prediction * 1000) / (population_growth * 1000000) if population_growth > 0 else 0
                        economic_per_capita = (prediction * 1000000) / (population_growth * 1000000) if population_growth > 0 else 0
                        carbon_per_capita = prediction / (population_growth * 1000000) if population_growth > 0 else 0
                        
                        # Sürdürülebilirlik skoru
                        sustainability_score = self.sustainability_score_hesapla(waste_per_capita, economic_per_capita, carbon_per_capita)
                        
                        predictions.append({
                            'Country': country,
                            'Year': year,
                            'Target': target,
                            'Prediction': prediction,
                            'Population_Million': population_growth,
                            'Waste_Per_Capita_kg': waste_per_capita,
                            'Economic_Loss_Per_Capita_USD': economic_per_capita,
                            'Carbon_Per_Capita_kgCO2e': carbon_per_capita,
                            'Sustainability_Score': sustainability_score
                        })
        
        # DataFrame'e çevir ve kaydet
        predictions_df = pd.DataFrame(predictions)
        predictions_df.to_csv('zaman_serisi_2025_2030_predictions.csv', index=False)
        print(f"✅ Zaman serisi gelecek tahminleri kaydedildi: {predictions_df.shape}")
        
        # Örnek tahminler
        print("\n📊 Örnek 2025 tahminleri:")
        sample_2025 = predictions_df[predictions_df['Year'] == 2025].head(3)
        for _, row in sample_2025.iterrows():
            print(f"   {row['Country']} - {row['Target']}: {row['Prediction']:.2f}")
    
    def zaman_serisi_ozellikleri_olustur(self, country, year, base_waste, base_economic, base_carbon, base_material_footprint, population_growth):
        """Zaman serisi özellikleri oluştur"""
        # Temel özellikler
        features = {
            'Population (Million)': population_growth,
            'Years_From_2018': year - 2018,
            'Material_Footprint_Per_Capita': base_material_footprint,
            'Year_Trend': (year - 2018) ** 2,
            'Country_Trend': 0,  # Varsayılan
            'Year_Cycle': np.sin(2 * np.pi * (year - 2018) / 7),
            'Year_Cycle_Cos': np.cos(2 * np.pi * (year - 2018) / 7),
            'Is_Pandemic_Year': 0,
            'Is_Post_Pandemic': 1,
            'Food Category_Encoded': 0,
            'Population_Material_Interaction': population_growth * base_material_footprint,
            'Year_Population_Interaction': (year - 2018) * population_growth,
            'GDP_Per_Capita_Proxy': 0,  # Varsayılan
            'Waste_Efficiency': base_waste / population_growth if population_growth > 0 else 0,
            'Economic_Intensity': base_economic / base_waste if base_waste > 0 else 0,
            'Waste_Trend': base_waste * (1.025) ** (year - 2024),
            'Economic_Trend': base_economic * (1.025) ** (year - 2024),
            'Category_Waste_Share': 1.0,
            'Category_Economic_Share': 1.0,
            'Year_Sin': np.sin(2 * np.pi * year / 10),
            'Year_Cos': np.cos(2 * np.pi * year / 10)
        }
        
        # Lag özellikleri (tahmin için varsayılan değerler)
        for target in self.target_columns:
            if target == 'Total Waste (Tons)':
                base_value = base_waste
            elif target == 'Economic Loss (Million $)':
                base_value = base_economic
            elif target == 'Carbon_Footprint_kgCO2e':
                base_value = base_carbon
            else:
                base_value = 50  # Sustainability_Score için varsayılan
            
            features[f'{target}_lag1'] = base_value * 0.95  # 1 yıl önce
            features[f'{target}_lag2'] = base_value * 0.90  # 2 yıl önce
            features[f'{target}_lag3'] = base_value * 0.85  # 3 yıl önce
            features[f'{target}_rolling_mean3'] = base_value * 0.93
            features[f'{target}_rolling_std3'] = base_value * 0.05
            features[f'{target}_trend'] = base_value * 0.02
            features[f'{target}_growth_rate'] = 0.025
            features[f'{target}_growth_rate_lag1'] = 0.020
        
        return features
    
    def sustainability_score_hesapla(self, waste_pc, economic_pc, carbon_pc):
        """Sürdürülebilirlik skoru hesapla"""
        waste_threshold = 0.5
        economic_threshold = 100
        carbon_threshold = 0.005
        
        waste_score = max(0, 1 - (waste_pc / waste_threshold))
        economic_score = max(0, 1 - (economic_pc / economic_threshold))
        carbon_score = max(0, 1 - (carbon_pc / carbon_threshold))
        
        sustainability = (waste_score * 0.4 + economic_score * 0.3 + carbon_score * 0.3) * 100
        return max(0, min(100, sustainability))
    
    def model_performans_raporu(self):
        """Model performans raporu oluştur"""
        print("\n📊 Zaman serisi model performans raporu oluşturuluyor...")
        
        # En iyi modeli belirle
        avg_test_r2 = np.mean([metrics['test_r2'] for metrics in self.model_metrics.values()])
        main_model_metrics = self.model_metrics['Total Waste (Tons)']
        
        report = {
            'model_type': f"{main_model_metrics['model_type']} (TimeSeries)",
            'selection_criteria': 'TimeSeries Cross-Validation R²',
            'train_test_split': 'Temporal Split (Last 2 years for test)',
            'cv_method': 'TimeSeriesSplit (3-fold)',
            'targets': {
                'Total Waste (Tons)': {
                    'train_r2': self.model_metrics['Total Waste (Tons)']['train_r2'],
                    'test_r2': self.model_metrics['Total Waste (Tons)']['test_r2'],
                    'cv_r2': self.model_metrics['Total Waste (Tons)']['cv_r2'],
                    'train_rmse': self.model_metrics['Total Waste (Tons)']['train_rmse'],
                    'test_rmse': self.model_metrics['Total Waste (Tons)']['test_rmse'],
                    'train_mae': self.model_metrics['Total Waste (Tons)']['train_mae'],
                    'test_mae': self.model_metrics['Total Waste (Tons)']['test_mae'],
                    'mape': self.model_metrics['Total Waste (Tons)']['mape'],
                    'overfitting_score': self.model_metrics['Total Waste (Tons)']['overfitting_score'],
                    'train_years': self.model_metrics['Total Waste (Tons)']['train_years'],
                    'test_years': self.model_metrics['Total Waste (Tons)']['test_years']
                },
                'Economic Loss (Million $)': {
                    'train_r2': self.model_metrics['Economic Loss (Million $)']['train_r2'],
                    'test_r2': self.model_metrics['Economic Loss (Million $)']['test_r2'],
                    'cv_r2': self.model_metrics['Economic Loss (Million $)']['cv_r2'],
                    'train_rmse': self.model_metrics['Economic Loss (Million $)']['train_rmse'],
                    'test_rmse': self.model_metrics['Economic Loss (Million $)']['test_rmse'],
                    'train_mae': self.model_metrics['Economic Loss (Million $)']['train_mae'],
                    'test_mae': self.model_metrics['Economic Loss (Million $)']['test_mae'],
                    'mape': self.model_metrics['Economic Loss (Million $)']['mape'],
                    'overfitting_score': self.model_metrics['Economic Loss (Million $)']['overfitting_score'],
                    'train_years': self.model_metrics['Economic Loss (Million $)']['train_years'],
                    'test_years': self.model_metrics['Economic Loss (Million $)']['test_years']
                },
                'Carbon_Footprint_kgCO2e': {
                    'train_r2': self.model_metrics['Carbon_Footprint_kgCO2e']['train_r2'],
                    'test_r2': self.model_metrics['Carbon_Footprint_kgCO2e']['test_r2'],
                    'cv_r2': self.model_metrics['Carbon_Footprint_kgCO2e']['cv_r2'],
                    'train_rmse': self.model_metrics['Carbon_Footprint_kgCO2e']['train_rmse'],
                    'test_rmse': self.model_metrics['Carbon_Footprint_kgCO2e']['test_rmse'],
                    'train_mae': self.model_metrics['Carbon_Footprint_kgCO2e']['train_mae'],
                    'test_mae': self.model_metrics['Carbon_Footprint_kgCO2e']['test_mae'],
                    'mape': self.model_metrics['Carbon_Footprint_kgCO2e']['mape'],
                    'overfitting_score': self.model_metrics['Carbon_Footprint_kgCO2e']['overfitting_score'],
                    'train_years': self.model_metrics['Carbon_Footprint_kgCO2e']['train_years'],
                    'test_years': self.model_metrics['Carbon_Footprint_kgCO2e']['test_years']
                },
                'Sustainability_Score': {
                    'train_r2': self.model_metrics['Sustainability_Score']['train_r2'],
                    'test_r2': self.model_metrics['Sustainability_Score']['test_r2'],
                    'cv_r2': self.model_metrics['Sustainability_Score']['cv_r2'],
                    'train_rmse': self.model_metrics['Sustainability_Score']['train_rmse'],
                    'test_rmse': self.model_metrics['Sustainability_Score']['test_rmse'],
                    'train_mae': self.model_metrics['Sustainability_Score']['train_mae'],
                    'test_mae': self.model_metrics['Sustainability_Score']['test_mae'],
                    'mape': self.model_metrics['Sustainability_Score']['mape'],
                    'overfitting_score': self.model_metrics['Sustainability_Score']['overfitting_score'],
                    'train_years': self.model_metrics['Sustainability_Score']['train_years'],
                    'test_years': self.model_metrics['Sustainability_Score']['test_years']
                }
            },
            'average_test_r2': avg_test_r2,
            'feature_selection': 'Time Series Features (Lags, Rolling Stats, Trends)',
            'data_preprocessing': 'Temporal Sorting, Lag Features, Rolling Statistics',
            'validation_strategy': 'TimeSeriesSplit + Temporal Train-Test Split',
            'time_series_features': [
                'Lag Features (1,2,3 years)', 'Rolling Mean/Std (3 years)', 
                'Trend Features', 'Growth Rate Features', 'Seasonal Features'
            ],
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # JSON olarak kaydet
        with open('zaman_serisi_model_performance.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print("✅ Zaman serisi model performans raporu kaydedildi: zaman_serisi_model_performance.json")
        
        # Özet
        print(f"\n📊 Zaman Serisi Model Performans Özeti:")
        print(f"   🏆 En İyi Model: {main_model_metrics['model_type']}")
        print(f"   📈 Ortalama Test R²: {avg_test_r2:.4f}")
        print(f"   🔍 Özellik Sayısı: {main_model_metrics['feature_count']}")
        print(f"   ✅ Train Yılları: {main_model_metrics['train_years']}")
        print(f"   ✅ Test Yılları: {main_model_metrics['test_years']}")
        print(f"   ✅ Cross-Validation: TimeSeriesSplit (3-fold)")
    
    def calistir(self):
        """Ana çalıştırma fonksiyonu"""
        self.veri_yukle()
        self.zaman_serisi_model_egitimi()
        self.gelecek_tahminleri()
        self.model_performans_raporu()
        
        print("\n🎉 ZAMAN SERİSİ MODEL EĞİTİMİ TAMAMLANDI!")
        print("=" * 60)

if __name__ == "__main__":
    zaman_serisi_model = ZamanSerisiModelEgitimi()
    zaman_serisi_model.calistir() 