from fastapi import FastAPI, UploadFile, File
import pandas as pd
import io
import asyncio
import logging
import os

from .detector import AnomalyDetector
from .utils import load_config


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI(title="Anomaly Detection API")

default_config_path = "config/config.yaml"

def get_anomaly_values(config_path=default_config_path):
    config = load_config(config_path)
    return (config["model"]["normal_mean"], 
            config["model"]["normal_std"], 
            config["model"].get("threshold_multiplier", 3.0), 
            config["data"].get("anomaly_output_path", "data/output/anomalies_streaming.csv"))

normal_mean, normal_std, threshold_multiplier, anomaly_output_path = get_anomaly_values()

detector = AnomalyDetector(normal_mean, normal_std, threshold_multiplier)

@app.get("/")
def root():
    return {"message": "Anomaly Detection API is running"}

@app.post("/detect/")
async def detect_anomalies(file: UploadFile = File(...)):
    """
    Upload a CSV file with 'timestamp' and 'value' columns to detect anomalies.
    """
    # Read uploaded file into DataFrame
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Detect anomalies
    anomalies = detector.detect(df)

    # Return anomalies as JSON
    return {
        "total_anomalies": len(anomalies),
        "anomalies": anomalies.to_dict(orient="records")
    }

@app.post("/simulate/")
async def simulate_stream(file: UploadFile = File(...)):
    """
    Simulate receiving one record per second.
    If a record is anomalous, log it and save it into anomalies_streaming.csv
    """
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    results = []

    # Ensure output directory exists
    os.makedirs(os.path.dirname(anomaly_output_path), exist_ok=True)

    for _, row in df.iterrows():
        value = row["value"]
        timestamp = row["timestamp"]

        anomalies = detector.detect(pd.DataFrame([row]))

        if not anomalies.empty:
            anomaly_record = {
                "timestamp": str(timestamp),
                "value": value,
                "reason": f"Value {value:.2f} outside normal range"
            }
            logger.warning(f"⚠️ Anomaly detected -> {anomaly_record}")

            # Save anomaly to CSV (append mode)
            pd.DataFrame([anomaly_record]).to_csv(
                anomaly_output_path, mode="a", header=not os.path.exists(anomaly_output_path), index=False
            )

            results.append({"timestamp": str(timestamp), "value": value, "status": "ANOMALY"})
        else:
            logger.info(f"✅ Normal record -> {row.to_dict()}")
            results.append({"timestamp": str(timestamp), "value": value, "status": "OK"})

        # Simulate real-time arrival
        await asyncio.sleep(1)

    return {
        "message": "Streaming simulation completed",
        "results": results
    }