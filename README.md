# 📊 Anomaly Detection API

This project is a **Python-based anomaly detection system** that works both in **batch mode** (uploading a CSV file) and **streaming simulation mode** (processing one record per second).  

It’s built with **FastAPI** and designed with a production-style structure (config files, reusable modules, and logging).

---

## 🚀 Features
- Upload a CSV with `timestamp` and `value` columns to detect anomalies.  
- Simulate a streaming process: one record arrives every second.  
- Anomalies are logged ⚠️ and **saved to `data/output/anomalies_streaming.csv`**.  
- Configurable detection thresholds (`mean`, `std`, and multiplier).  
- Clean modular structure (`src/`, `scripts/`, `config/`).

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/anomaly-detector.git
cd anomaly-detector

---

## Configurations

Edit config/config.yaml to set paths and thresholds. Example:
data:
  test_data_path: "data/test/test.csv"
  output_path: "data/output/anomalies_batch.csv"

model:
  normal_mean: 50.0
  normal_std: 5.0
  threshold_multiplier: 3.0

---

## Usage

Start the server 

```bash
uvicorn src.anomaly_detector.api:app --reload