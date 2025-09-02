import logging
import argparse
from src.anomaly_detector.pipeline import run_pipeline
from src.anomaly_detector.utils import load_config

logging.basicConfig(level=logging.INFO)

def main():
    parser = argparse.ArgumentParser(description="Run anomaly detection on test data.")
    parser.add_argument("--config", type=str, required=True, help="Path to YAML config file.")
    args = parser.parse_args()

    config = load_config(args.config)

    test_data_path = config["data"]["test_data_path"]
    output_path = config["data"].get("output_path", "data/output/anomalies.csv")

    normal_mean = config["model"]["normal_mean"]
    normal_std = config["model"]["normal_std"]
    threshold_multiplier = config["model"].get("threshold_multiplier", 3.0)

    run_pipeline(test_data_path, normal_mean, normal_std, threshold_multiplier, output_path)

if __name__ == "__main__":
    main()