# 🚀 Ecolense Intelligence - Canlıya Alma Rehberi

## 📋 Proje Dosyalama

### 📁 Ana Dizin Yapısı
```
EcolenseIntelligence/
├── 📄 app.py                          # Ana Streamlit uygulaması
├── 📄 storytelling.py                 # Premium storytelling modülü
├── 📄 ecolense_presentation.html      # Sunum dosyası
├── 📄 sustainability_ranking_analysis.md
├── 📄 deployment_guide.md             # Bu dosya
├── 📄 requirements.txt                # Python bağımlılıkları
├── 📄 README.md                       # Proje açıklaması
├── 📁 data/                           # Veri dosyaları
│   ├── ecolense_final_enriched.csv
│   ├── global_food_wastage_dataset.csv
│   └── material_footprint.csv
├── 📁 models/                         # Model dosyaları
│   ├── model_performance_dashboard.json
│   └── shap_importance_*.csv
├── 📁 static/                         # Statik dosyalar
│   ├── css/
│   ├── js/
│   └── images/
└── 📁 docs/                           # Dokümantasyon
    ├── api_docs.md
    └── user_guide.md
```

## 🌐 Canlıya Alma Seçenekleri

### 1. 🆓 Ücretsiz Seçenekler

#### A) Streamlit Cloud (Önerilen)
```bash
# 1. GitHub'a yükle
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/kullaniciadi/ecolense-intelligence.git
git push -u origin main

# 2. Streamlit Cloud'da deploy et
# https://share.streamlit.io/
```

#### B) Heroku (Ücretsiz Tier Kaldırıldı)
```bash
# Procfile oluştur
echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# Heroku CLI ile deploy
heroku create ecolense-intelligence
git push heroku main
```

### 2. 💰 Ücretli Seçenekler

#### A) AWS EC2
```bash
# EC2 instance kurulumu
sudo apt update
sudo apt install python3-pip
pip3 install streamlit pandas plotly

# Uygulamayı başlat
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```

#### B) Google Cloud Platform
```bash
# App Engine deployment
gcloud app deploy app.yaml
```

#### C) DigitalOcean Droplet
```bash
# Droplet kurulumu
sudo apt update
sudo apt install python3-pip nginx
pip3 install streamlit pandas plotly

# Nginx reverse proxy
sudo nano /etc/nginx/sites-available/ecolense
```

## 📦 Gerekli Dosyalar

### requirements.txt
```
streamlit==1.28.0
pandas==2.1.0
plotly==5.17.0
numpy==1.24.3
scikit-learn==1.3.0
shap==0.43.0
```

### .gitignore
```
__pycache__/
*.pyc
.env
.DS_Store
*.log
data/*.csv
models/*.json
```

### README.md
```markdown
# 🌍 Ecolense Intelligence

Sürdürülebilir gıda sistemi analizi ve AI destekli tahmin platformu.

## 🚀 Kurulum

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📊 Özellikler

- 17 ülke sürdürülebilirlik analizi
- AI destekli tahmin modelleri
- Interactive dashboard
- Real-time raporlama

## 🌐 Canlı Demo

[Streamlit Cloud Link]
```

## 🔧 Konfigürasyon

### config.py
```python
import os

# Veri yolları
DATA_PATH = "data/"
MODELS_PATH = "models/"
STATIC_PATH = "static/"

# API anahtarları (gerekirse)
API_KEYS = {
    "openai": os.getenv("OPENAI_API_KEY"),
    "google": os.getenv("GOOGLE_API_KEY")
}

# Uygulama ayarları
APP_CONFIG = {
    "title": "Ecolense Intelligence",
    "theme": "dark",
    "page_icon": "🌍"
}
```

## 📊 Veri Yönetimi

### Veri Güncelleme Scripti
```python
# update_data.py
import pandas as pd
import requests

def update_datasets():
    """Veri setlerini güncelle"""
    # API'den yeni veri çek
    # CSV dosyalarını güncelle
    # Model performansını yeniden hesapla
    pass

if __name__ == "__main__":
    update_datasets()
```

## 🔒 Güvenlik

### Güvenlik Kontrol Listesi
- [ ] API anahtarları environment variables'da
- [ ] HTTPS kullanımı
- [ ] Input validation
- [ ] Rate limiting
- [ ] Error handling

## 📈 Monitoring

### Logging Konfigürasyonu
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ecolense.log'),
        logging.StreamHandler()
    ]
)
```

## 🚀 Deployment Checklist

### Pre-Deployment
- [ ] Tüm bağımlılıklar requirements.txt'de
- [ ] .gitignore dosyası hazır
- [ ] README.md güncel
- [ ] Test edildi
- [ ] Güvenlik kontrolleri yapıldı

### Deployment
- [ ] Repository oluşturuldu
- [ ] Kod yüklendi
- [ ] CI/CD pipeline kuruldu
- [ ] Domain ayarlandı
- [ ] SSL sertifikası eklendi

### Post-Deployment
- [ ] Monitoring aktif
- [ ] Backup sistemi kuruldu
- [ ] Performance testleri yapıldı
- [ ] User feedback toplandı

## 💡 Öneriler

### Performance Optimizasyonu
1. **Caching**: Streamlit cache kullan
2. **Lazy Loading**: Büyük veri setlerini lazy load et
3. **CDN**: Statik dosyalar için CDN kullan
4. **Database**: Büyük veri için PostgreSQL

### SEO ve Marketing
1. **Meta tags** ekle
2. **Social media** preview'ları
3. **Analytics** entegrasyonu
4. **Sitemap** oluştur

## 📞 Destek

- **Email**: support@ecolense.com
- **GitHub**: github.com/ecolense-intelligence
- **Documentation**: docs.ecolense.com

---

*Bu rehber Ecolense Intelligence projesi için hazırlanmıştır.* 