from pathlib import Path
import pandas as pd


def load_data(root_dir: Path | None = None):
    """Load raw datasets and return them as a dictionary of DataFrames."""
    root = Path(root_dir) if root_dir else Path(__file__).resolve().parents[2]
    raw_dir = root / "data" / "raw"

    datasets = {
        "add_spend": "add_spend_dataset.csv",
        "customer_interaction": "customer_interaction_dataset.csv",
        "revenue": "revenue_dataset.csv",
    }

    return {
        name: pd.read_csv(raw_dir / filename) for name, filename in datasets.items()
    }
