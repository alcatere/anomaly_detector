import logging
import argparse
import pandas as pd
from pathlib import Path
from src.utils import load_config
import yaml

logging.basicConfig(level=logging.INFO)

def main():
    parser = argparse.ArgumentParser(description="Train baseline stats for anomaly detection.")
    parser.add_argument("--config", type=str, required=True, help="Path to YAML config file.")
    args = parser.parse_args()

    config = load_config(args.config)

    train_path = Path(config["data"]["train_data_path"])
    window_size = config["data"]["rolling_window_size"]

    try:
        train_df = pd.read_csv(train_path)
        train_df['timestamp'] = pd.to_datetime(train_df['timestamp'])
        train_df.set_index('timestamp', inplace=True)

        # Calculate rolling statistics on the training data
        rolling_mean = train_df['value'].rolling(window=window_size).mean()
        rolling_std = train_df['value'].rolling(window=window_size).std()

        # Use the last calculated values as our "model" for normal behavior
        # This is a naive approach but serves for the POC.
        NORMAL_MEAN = rolling_mean.iloc[-1]
        NORMAL_STD = rolling_std.iloc[-1]

        print(f"Training complete. Normal baseline: Mean={NORMAL_MEAN:.2f}, StdDev={NORMAL_STD:.2f}")

    except FileNotFoundError:
        print(f"Error: Training data file not found at '{train_path}'")
        exit()

    logging.info(f"Computed mean={NORMAL_MEAN:.2f}, std={NORMAL_STD:.2f}")

    # Save back into config
    config["model"]["normal_mean"] = float(NORMAL_MEAN)
    config["model"]["normal_std"] = float(NORMAL_STD)

    with open(args.config, "w") as f:
        yaml.safe_dump(config, f)

    logging.info(f"Updated config file at {args.config}")

if __name__ == "__main__":
    main()