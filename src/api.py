from fastapi import FastAPI, UploadFile, File
import pandas as pd
import io
from .detector import AnomalyDetector

app = FastAPI(title="Anomaly Detection API")

# Example: pre-trained baseline stats
NORMAL_MEAN = 50.0
NORMAL_STD = 5.0
THRESHOLD_MULTIPLIER = 3.0

detector = AnomalyDetector(NORMAL_MEAN, NORMAL_STD, THRESHOLD_MULTIPLIER)

@app.get("/")
def root():
    return {"message": "Anomaly Detection API is running 🚀"}

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