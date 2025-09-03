from fastapi import FastAPI, UploadFile, File
import pandas as pd
import io
from .detector import AnomalyDetector
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI(title="Anomaly Detection API")

# Example: pre-trained baseline stats
NORMAL_MEAN = 50.0
NORMAL_STD = 5.0
THRESHOLD_MULTIPLIER = 3.0

detector = AnomalyDetector(NORMAL_MEAN, NORMAL_STD, THRESHOLD_MULTIPLIER)

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
    os.makedirs(os.path.dirname(ANOMALY_OUTPUT_PATH), exist_ok=True)

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
                ANOMALY_OUTPUT_PATH, mode="a", header=not os.path.exists(ANOMALY_OUTPUT_PATH), index=False
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