import logging
import pandas as pd
from datetime import datetime
from pathlib import Path
from .detector import AnomalyDetector

logger = logging.getLogger(__name__)

def load_data(path: str) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Test data file not found at {path}")
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

def run_pipeline(test_data_path: str, normal_mean: float, normal_std: float,
                 threshold_multiplier: float = 3.0, output_path: str = "data/output/anomalies.csv"):
    logger.info(f"Loading test data from {test_data_path}")
    df = load_data(test_data_path)

    detector = AnomalyDetector(normal_mean, normal_std, threshold_multiplier)
    anomalies = detector.detect(df)

    if anomalies.empty:
        logger.info("No anomalies detected ✅")
    else:
        logger.warning(f"{len(anomalies)} anomalies found ⚠️")
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        anomalies.to_csv(f'{output_path.split(".")[0]}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv', index=False)
        logger.info(f"Anomaly report saved at {output_path}")

    return anomalies