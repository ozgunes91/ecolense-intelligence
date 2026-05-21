#!/usr/bin/env python3
"""
run_pipeline.py
===============
Tüm pipeline'ı sırasıyla çalıştırır:
  1. Veri hazırlama
  2. Model eğitimi
  3. Tahmin üretimi

Kullanım: python run_pipeline.py
"""
import subprocess, sys, time

STEPS = [
    ("01_prepare_data.py",      "📦 Veri Hazırlama"),
    ("02_train_models.py",      "📈 Model Eğitimi"),
    ("03_generate_forecasts.py","🔮 Tahmin Üretimi"),
]

def run(script, label):
    print(f"\n{'='*55}")
    print(f"  {label}")
    print(f"{'='*55}")
    t0 = time.time()
    result = subprocess.run([sys.executable, script], capture_output=False)
    elapsed = time.time() - t0
    if result.returncode != 0:
        print(f"  ❌ HATA: {script} başarısız oldu (exit {result.returncode})")
        sys.exit(1)
    print(f"  ⏱  {elapsed:.1f}s")

if __name__ == "__main__":
    t_start = time.time()
    for script, label in STEPS:
        run(script, label)
    print(f"\n{'='*55}")
    print(f"  ✅ TÜM PIPELINE TAMAMLANDI  ({time.time()-t_start:.0f}s)")
    print(f"{'='*55}\n")
    print("  Dashboard başlatmak için:")
    print("    streamlit run app.py\n")
