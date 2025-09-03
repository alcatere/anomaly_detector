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
```
---

## Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

## Install dependencies:

```bash
pip install -r requirements.txt
```

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

Train the model (calculate baseline stats):

```bash
python -m scripts.train_model.py --config config/config.yaml
```


Start FastAPI the server 

```bash
uvicorn src.api:app --reload
```
The server will be available at http://127.0.0.1:8000

## Available Endpoints

You can interact with the API through the following endpoints:

### Batch Detection

Endpoint: POST /detect/

Upload a CSV file for processing. The system will return a JSON response with the anomalies found.

Example usage with curl:

```bash
curl -X POST "http://127.0.0.1:8000/detect/" \  
  -F "file=@data/test/sensor_data_test.csv"
```

### Streaming Simulation

Endpoint: POST /simulate/

Starts a simulation that processes one record per second from the test file (test_data_path in config.yaml). Anomalies will be displayed in the server log and saved to data/output/anomalies_streaming.csv.

Example usage with curl:

```bash
curl -X POST "http://127.0.0.1:8000/simulate/" \  
  -F "file=@data/test/sensor_data_test.csv"
```