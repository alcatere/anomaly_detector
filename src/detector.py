import pandas as pd

class AnomalyDetector:
    """
    Rule-based anomaly detector using mean ± threshold * std bounds.
    """

    def __init__(self, normal_mean: float, normal_std: float, threshold_multiplier: float = 3.0):
        self.normal_mean = normal_mean
        self.normal_std = normal_std
        self.threshold_multiplier = threshold_multiplier

    def detect(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Detect anomalies in a DataFrame with 'timestamp' and 'value' columns.
        Returns a DataFrame with anomalies and reasons.
        """
        upper_bound = self.normal_mean + self.threshold_multiplier * self.normal_std
        lower_bound = self.normal_mean - self.threshold_multiplier * self.normal_std

        mask = ~df["value"].between(lower_bound, upper_bound)
        anomalies = df.loc[mask].copy()

        anomalies["reason"] = anomalies["value"].apply(
            lambda v: f"Value {v:.2f} is outside range [{lower_bound:.2f}, {upper_bound:.2f}]"
        )

        return anomalies