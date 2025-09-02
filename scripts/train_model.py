import logging
import argparse
import pandas as pd
from pathlib import Path
from src.anomaly_detector.utils import load_config
import yaml

logging.basicConfig(level=logging.INFO)

def main():
    parser = argparse.ArgumentParser(description="Train baseline stats for anomaly detection.")
    parser.add_argument("--config", type=str, required=True, help="Path to YAML config file.")
    args = parser.parse_args()

    config = load_config(args.config)
    train_path = Path(config["data"]["train_data_path"])

    if not train_path.exists():
        raise FileNotFoundError(f"Training data not found at {train_path}")

    train_df = pd.read_csv(train_path)
    normal_mean = train_df["value"].mean()
    normal_std = train_df["value"].std()

    logging.info(f"Computed mean={normal_mean:.2f}, std={normal_std:.2f}")

    # Save back into config
    config["model"]["normal_mean"] = float(normal_mean)
    config["model"]["normal_std"] = float(normal_std)

    with open(args.config, "w") as f:
        yaml.safe_dump(config, f)

    logging.info(f"Updated config file at {args.config}")

if __name__ == "__main__":
    main()