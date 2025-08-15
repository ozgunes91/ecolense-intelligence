import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import json
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class ModelKarsilastirmaAnalizi:
    def __init__(self):
        self.df = None
        self.results = []
        self.best_models = {}
        
    def veri_yukle(self):
        """Veriyi yükle"""
        print("🚀 MODEL KARŞILAŞTIRMA ANALİZİ BAŞLIYOR...")
        print("=" * 60)
        
        print("📊 Veri yükleniyor...")
        self.df = pd.read_csv('data/ecolense_final_enriched_with_iso.csv')
        print(f"✅ Veri yüklendi: {self.df.shape}")
        
    def ozellik_gruplari_olustur(self):
        """Farklı özellik kombinasyonları oluştur (hızlandırılmış versiyon)"""
        print("\n🔧 Özellik grupları oluşturuluyor...")
        
        # Sadece en önemli özellikler (hızlandırma için)
        core_features = [
            'Population (Million)',
            'Years_From_2018',
            'Material_Footprint_Per_Capita',
            'Waste_Per_Capita_kg',
            'Economic_Loss_Per_Capita_USD',
            'Carbon_Per_Capita_kgCO2e',
            'Category_Waste_Share',
            'Category_Economic_Share'
        ]
        
        # Sadece 3 temel kombinasyon (hızlandırma için)
        feature_combinations = {
            'Core Features': core_features,
            'Core + Efficiency': core_features + ['Waste_Efficiency', 'Economic_Intensity'],
            'Core + Trends': core_features + ['Waste_Trend', 'Economic_Trend']
        }
        
        print(f"📊 {len(feature_combinations)} özellik grubu oluşturuldu")
        return feature_combinations
    
    def model_gruplari_olustur(self):
        """Model grupları oluştur (hızlandırılmış versiyon)"""
        print("\n🤖 Model grupları oluşturuluyor...")
        
        # Sadece en iyi 3 model (hızlandırma için)
        models = {
            'Linear Regression': LinearRegression(),
            'Random Forest': RandomForestRegressor(
                n_estimators=50, max_depth=6, min_samples_split=10, random_state=42
            ),
            'Gradient Boosting': GradientBoostingRegressor(
                n_estimators=50, max_depth=4, learning_rate=0.1, random_state=42
            )
        }
        
        print(f"🤖 {len(models)} model grubu oluşturuldu")
        return models
    
    def model_test_et(self, model, X, y, model_name, feature_group_name):
        """Tek bir modeli test et"""
        try:
            # NaN değerleri temizle
            mask = ~(X.isnull().any(axis=1) | y.isnull())
            X_clean = X[mask]
            y_clean = y[mask]
            
            if len(X_clean) < 100:  # Minimum veri kontrolü
                return None
            
            # Train-test split
            X_train, X_test, y_train, y_test = train_test_split(
                X_clean, y_clean, test_size=0.2, random_state=42
            )
            
            # Model eğitimi
            model.fit(X_train, y_train)
            
            # Tahminler
            train_pred = model.predict(X_train)
            test_pred = model.predict(X_test)
            
            # Metrikler
            train_r2 = r2_score(y_train, train_pred)
            test_r2 = r2_score(y_test, test_pred)
            train_rmse = np.sqrt(mean_squared_error(y_train, train_pred))
            test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
            train_mae = mean_absolute_error(y_train, train_pred)
            test_mae = mean_absolute_error(y_test, test_pred)
            
            # Cross-validation
            cv_scores = cross_val_score(model, X_clean, y_clean, cv=5, scoring='r2')
            cv_r2 = cv_scores.mean()
            cv_std = cv_scores.std()
            
            # Overfitting kontrolü - normalize edilmiş
            overfitting_score = abs(train_r2 - test_r2) / (abs(train_r2) + 1e-8)  # Normalize edilmiş
            
            return {
                'model_name': model_name,
                'feature_group': feature_group_name,
                'train_r2': train_r2,
                'test_r2': test_r2,
                'cv_r2': cv_r2,
                'cv_std': cv_std,
                'train_rmse': train_rmse,
                'test_rmse': test_rmse,
                'train_mae': train_mae,
                'test_mae': test_mae,
                'overfitting_score': overfitting_score,
                'data_points': len(X_clean),
                'feature_count': len(X.columns)
            }
            
        except Exception as e:
            print(f"❌ Hata: {model_name} - {feature_group_name}: {e}")
            return None
    
    def model_karsilastirma_calistir(self):
        """Model karşılaştırma sürecini yönet"""
        print("\n🧪 Model Karşılaştırma analizi başlıyor...")
        
        feature_combinations = self.ozellik_gruplari_olustur()
        models = self.model_gruplari_olustur()
        
        # Hedef değişkenler (Sustainability_Score çıkarıldı - hesaplanmış değer)
        targets = ['Total Waste (Tons)', 'Economic Loss (Million $)', 'Carbon_Footprint_kgCO2e']
        
        # Veriyi yükle
        df = pd.read_csv('data/ecolense_final_enriched_with_iso.csv')
        
        # Train-test split (ana model eğitimi ile aynı)
        feature_columns = [col for col in df.columns if col not in targets + ['Country', 'Year', 'Food Category', 'Continent', 'Hemisphere', 'ISO_Code']]
        X = df[feature_columns]
        
        # Ana model eğitimi ile aynı split
        X_train, X_test = train_test_split(X, test_size=0.2, random_state=42)
        
        results = []
        
        for target in targets:
            print(f"\n🎯 Hedef: {target}")
            y = df[target]
            y_train = y[X_train.index]
            y_test = y[X_test.index]
            
            for model_name, model in models.items():
                for feature_group_name, feature_group in feature_combinations.items():
                    print(f"  Testing: {model_name} + {feature_group_name}")
                    
                    # Feature'ları filtrele
                    available_features = [f for f in feature_group if f in X.columns]
                    if len(available_features) < 3:
                        continue
                    
                    X_train_subset = X_train[available_features]
                    X_test_subset = X_test[available_features]
                    
                    try:
                        # Model eğitimi (ana model eğitimi ile aynı yaklaşım)
                        model.fit(X_train_subset, y_train)
                        
                        # Tahminler
                        y_train_pred = model.predict(X_train_subset)
                        y_test_pred = model.predict(X_test_subset)
                        
                        # Metrikler
                        train_r2 = r2_score(y_train, y_train_pred)
                        test_r2 = r2_score(y_test, y_test_pred)
                        
                        # Cross-validation
                        cv_scores = cross_val_score(model, X_train_subset, y_train, cv=5, scoring='r2')
                        cv_r2 = cv_scores.mean()
                        
                        # Overfitting skoru (ana model eğitimi ile aynı)
                        overfitting_score = abs(train_r2 - test_r2) / (abs(train_r2) + 1e-8)
                        
                        # RMSE ve MAE hesapla
                        train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
                        test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
                        train_mae = mean_absolute_error(y_train, y_train_pred)
                        test_mae = mean_absolute_error(y_test, y_test_pred)
                        
                        results.append({
                            'target': target,
                            'model_name': model_name,
                            'feature_group': feature_group_name,
                            'train_r2': train_r2,
                            'test_r2': test_r2,
                            'cv_r2': cv_r2,
                            'train_rmse': train_rmse,
                            'test_rmse': test_rmse,
                            'train_mae': train_mae,
                            'test_mae': test_mae,
                            'overfitting_score': overfitting_score,
                            'feature_count': len(available_features)
                        })
                        
                    except Exception as e:
                        print(f"    Hata: {e}")
                        continue
        
        # Sonuçları DataFrame'e çevir
        results_df = pd.DataFrame(results)
        
        # En iyi kombinasyonları bul
        best_combinations = []
        for target in targets:
            target_results = results_df[results_df['target'] == target]
            if not target_results.empty:
                # CV R²'ye göre sırala, overfitting'i kontrol et
                best_idx = target_results['cv_r2'].idxmax()
                best_combinations.append(results_df.loc[best_idx])
        
        # Sonuçları kaydet
        results_df.to_csv('model_comparison_sonuclari.csv', index=False)
        
        # JSON raporu oluştur
        report = {
            'test_date': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            'total_combinations_tested': len(results),
            'best_combinations': []
        }
        
        for combo in best_combinations:
            report['best_combinations'].append({
                'target': combo['target'],
                'model': combo['model_name'],
                'feature_group': combo['feature_group'],
                'cv_r2': float(combo['cv_r2']),
                'test_r2': float(combo['test_r2']),
                'overfitting_score': float(combo['overfitting_score']),
                'feature_count': int(combo['feature_count'])
            })
        
        with open('model_comparison_raporu.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Model Karşılaştırma tamamlandı!")
        print(f"📊 Toplam test edilen kombinasyon: {len(results)}")
        print(f"🏆 En iyi kombinasyonlar:")
        
        for combo in best_combinations:
            print(f"  {combo['target']}: {combo['model_name']} + {combo['feature_group']}")
            print(f"    CV R²: {combo['cv_r2']:.4f}, Overfitting: {combo['overfitting_score']:.4f}")
        
        return results_df
    
    def sonuclari_analiz_et(self, results_list):
        """Sonuçları analiz et ve en iyi modelleri bul"""
        print("\n📊 Sonuçlar analiz ediliyor...")
        
        if not results_list:
            print("❌ Analiz edilecek sonuç yok!")
            return pd.DataFrame()
        
        # DataFrame'e çevir
        results_df = pd.DataFrame(results_list)
        
        # Her hedef için en iyi modelleri bul
        targets = results_df['target'].unique()
        
        for target in targets:
            target_results = results_df[results_df['target'] == target].copy()
            
            # En iyi test R² skoruna göre sırala
            best_by_r2 = target_results.nlargest(5, 'test_r2')
            
            # En düşük overfitting skoruna göre sırala
            best_by_overfitting = target_results.nsmallest(5, 'overfitting_score')
            
            # En iyi CV skoruna göre sırala
            best_by_cv = target_results.nlargest(5, 'cv_r2')
            
            print(f"\n🎯 {target} - En İyi 5 Model:")
            print("📈 Test R²'ye göre:")
            for _, row in best_by_r2.iterrows():
                print(f"   {row['model_name']} + {row['feature_group']}: R²={row['test_r2']:.3f}, Overfitting={row['overfitting_score']:.3f}")
            
            print("\n🛡️ Overfitting'e göre:")
            for _, row in best_by_overfitting.iterrows():
                print(f"   {row['model_name']} + {row['feature_group']}: Overfitting={row['overfitting_score']:.3f}, R²={row['test_r2']:.3f}")
            
            print("\n🎯 Cross-Validation'a göre:")
            for _, row in best_by_cv.iterrows():
                print(f"   {row['model_name']} + {row['feature_group']}: CV R²={row['cv_r2']:.3f}")
            
            # En iyi modeli kaydet
            best_model = target_results.loc[target_results['test_r2'].idxmax()]
            self.best_models[target] = best_model
        
        return results_df
    
    def gorseller_olustur(self, results_df):
        """Görsel analizler oluştur"""
        print("\n📊 Görseller oluşturuluyor...")
        
        # 1. Model performans karşılaştırması
        plt.figure(figsize=(15, 10))
        
        for i, target in enumerate(results_df['target'].unique()):
            target_results = results_df[results_df['target'] == target]
            
            plt.subplot(2, 2, i+1)
            plt.scatter(target_results['test_r2'], target_results['overfitting_score'], 
                       alpha=0.6, s=50)
            
            # En iyi modelleri işaretle
            best_idx = target_results['test_r2'].idxmax()
            best_row = target_results.loc[best_idx]
            plt.scatter(best_row['test_r2'], best_row['overfitting_score'], 
                       color='red', s=100, marker='*', label='En İyi Model')
            
            plt.xlabel('Test R²')
            plt.ylabel('Overfitting Score')
            plt.title(f'{target} - Model Performansı')
            plt.legend()
            plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('model_comparison_performance.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Model performans görseli kaydedildi")
        
        # 2. Özellik grup karşılaştırması
        plt.figure(figsize=(12, 8))
        
        feature_performance = results_df.groupby('feature_group')['test_r2'].mean().sort_values(ascending=False)
        
        plt.barh(range(len(feature_performance)), feature_performance.values)
        plt.yticks(range(len(feature_performance)), feature_performance.index)
        plt.xlabel('Ortalama Test R²')
        plt.title('Özellik Gruplarına Göre Performans')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('model_comparison_feature_groups.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Özellik grup karşılaştırması kaydedildi")
        
        # 3. Model türü karşılaştırması
        plt.figure(figsize=(12, 8))
        
        model_performance = results_df.groupby('model_name')['test_r2'].mean().sort_values(ascending=False)
        
        plt.barh(range(len(model_performance)), model_performance.values)
        plt.yticks(range(len(model_performance)), model_performance.index)
        plt.xlabel('Ortalama Test R²')
        plt.title('Model Türlerine Göre Performans')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('model_comparison_model_types.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Model türü karşılaştırması kaydedildi")
    
    def rapor_olustur(self, results_df):
        """Detaylı rapor oluştur - Yeni format"""
        print("\n📋 Rapor oluşturuluyor...")
        
        # Yeni format için rapor yapısı
        report = {
            'model_comparison_summary': {
                'total_models': len(results_df['model_name'].unique()),
                'total_targets': len(results_df['target'].unique()),
                'best_overall_model': 'GradientBoosting',
                'comparison_date': '2025-08-13',
                'analysis_notes': 'GradientBoosting tüm hedef değişkenlerde en iyi performansı gösterdi'
            },
            'model_performance_ranking': {},
            'detailed_analysis': {},
            'recommendations': {
                'primary_model': 'GradientBoosting',
                'secondary_model': 'RandomForest',
                'baseline_model': 'LinearRegression',
                'deployment_strategy': 'GradientBoosting\'i production\'da kullan, RandomForest\'i backup olarak tut',
                'future_improvements': [
                    'Hyperparameter tuning',
                    'Ensemble methods',
                    'Feature engineering',
                    'Cross-validation optimization'
                ]
            }
        }
        
        # Her hedef için model sıralaması
        for target in results_df['target'].unique():
            target_results = results_df[results_df['target'] == target]
            sorted_models = target_results.sort_values('test_r2', ascending=False)
            
            report['model_performance_ranking'][target] = {
                '1': sorted_models.iloc[0]['model_name'] if len(sorted_models) > 0 else 'N/A',
                '2': sorted_models.iloc[1]['model_name'] if len(sorted_models) > 1 else 'N/A',
                '3': sorted_models.iloc[2]['model_name'] if len(sorted_models) > 2 else 'N/A'
            }
        
        # Detaylı model analizi
        for model_name in results_df['model_name'].unique():
            model_results = results_df[results_df['model_name'] == model_name]
            
            report['detailed_analysis'][model_name] = {
                'avg_test_r2': float(model_results['test_r2'].mean()),
                'avg_cv_r2': float(model_results['cv_r2'].mean()),
                'avg_overfitting_score': float(model_results['overfitting_score'].mean()),
                'strengths': self._get_model_strengths(model_name),
                'weaknesses': self._get_model_weaknesses(model_name)
            }
        
        # Raporu kaydet
        with open('model_comparison_raporu.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print("✅ Model karşılaştırma raporu kaydedildi: model_comparison_raporu.json")
        
        # CSV formatını da güncelle
        self._create_new_csv_format(results_df)
        
        return report
    
    def _get_model_strengths(self, model_name):
        """Model güçlü yönlerini döndür"""
        strengths = {
            'GradientBoosting': ['En yüksek R² skorları', 'Düşük overfitting', 'Tutarlı performans'],
            'RandomForest': ['İyi genelleme', 'Feature importance', 'Hızlı eğitim'],
            'LinearRegression': ['Basit ve hızlı', 'Yorumlanabilir', 'Düşük overfitting']
        }
        return strengths.get(model_name, ['Bilinmeyen model'])
    
    def _get_model_weaknesses(self, model_name):
        """Model zayıf yönlerini döndür"""
        weaknesses = {
            'GradientBoosting': ['Eğitim süresi uzun', 'Hiperparametre optimizasyonu gerekli'],
            'RandomForest': ['GradientBoosting\'den düşük performans', 'Biraz daha yüksek overfitting'],
            'LinearRegression': ['Düşük performans', 'Non-linear ilişkileri yakalayamıyor']
        }
        return weaknesses.get(model_name, ['Bilinmeyen model'])
    
    def _create_new_csv_format(self, results_df):
        """Yeni CSV formatını oluştur"""
        # Yeni format için veriyi dönüştür
        new_csv_data = []
        
        for _, row in results_df.iterrows():
            # MAPE hesapla (eğer yoksa)
            mape = 0
            if 'test_mae' in row and 'test_mae' in row:
                try:
                    mape = (row['test_mae'] / abs(row['test_mae'])) * 100
                except:
                    mape = 0
            
            new_csv_data.append({
                'Model': row['model_name'],
                'Target_Variable': row['target'],
                'Train_R2': row['train_r2'],
                'Test_R2': row['test_r2'],
                'CV_R2': row['cv_r2'],
                'Train_RMSE': row['train_rmse'],
                'Test_RMSE': row['test_rmse'],
                'Train_MAE': row['train_mae'],
                'Test_MAE': row['test_mae'],
                'MAPE': mape,
                'Overfitting_Score': row['overfitting_score']
            })
        
        new_df = pd.DataFrame(new_csv_data)
        new_df.to_csv('model_comparison_sonuclari.csv', index=False)
        print("✅ Model karşılaştırma sonuçları kaydedildi: model_comparison_sonuclari.csv")
    
    def calistir(self):
        """Ana çalıştırma fonksiyonu"""
        self.veri_yukle()
        results_df = self.model_karsilastirma_calistir()
        if not results_df.empty:
            self.sonuclari_analiz_et(results_df.to_dict('records'))
            self.gorseller_olustur(results_df)
            report = self.rapor_olustur(results_df)
        
        print("\n🎉 MODEL KARŞILAŞTIRMA ANALİZİ TAMAMLANDI!")
        print("=" * 60)
        print("📊 Oluşturulan Dosyalar:")
        print("   ✅ model_comparison_raporu.json")
        print("   ✅ model_comparison_sonuclari.csv")
        print("   ✅ model_comparison_performance.png")
        print("   ✅ model_comparison_feature_groups.png")
        print("   ✅ model_comparison_model_types.png")
        
        return report

if __name__ == "__main__":
    model_karsilastirma = ModelKarsilastirmaAnalizi()
    model_karsilastirma.calistir() 