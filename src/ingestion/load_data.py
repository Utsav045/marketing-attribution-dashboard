from pathlib import Path
import pandas as pd


def load_data():
    """Load raw datasets and return them as a dictionary of DataFrames."""
    root = Path(__file__).resolve().parents[2]
    raw_dir = root / "data" / "raw"

    datasets = {
        "add_spend": "Add Spend Dataset.csv",
        "customer_interaction": "Customer Interaction Dataset.csv",
        "revenue": "Revenue Dataset.csv",
    }

    return {name: pd.read_csv(raw_dir / filename) for name, filename in datasets.items()}
