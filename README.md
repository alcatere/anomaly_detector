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

## 📂 Project Structure
anomaly-detector/
│── config/
│   └── config.yaml               # Configuration file
│── data/
│   ├── test/                     # Example test datasets
│   └── output/                   # Generated anomaly reports
│── scripts/
│   ├── train_model.py            # Training script (set normal mean/std)
│   └── run_api.py                # Entry point for the FastAPI server
│── src/
│   └── anomaly_detector/
│       ├── init.py
│       ├── utils.py              # Config loader
│       ├── detector.py           # Core anomaly detector class
│       └── api.py                # FastAPI app (batch + streaming)
│── README.md
│── requirements.txt