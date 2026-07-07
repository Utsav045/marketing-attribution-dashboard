"""
CSV Loading Module
Multi-Touch Marketing Attribution & ROI Dashboard
"""

from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

# Mapping of dataset keys to their CSV filenames
DATASET_FILES = {
    "add_spend": "add_spend_dataset.csv",
    "customer_interaction": "customer_interaction_dataset.csv",
    "revenue": "revenue_dataset.csv",
}


def load_csv(filepath: Path | str) -> pd.DataFrame:
    """
    Load a single CSV file into a pandas DataFrame.

    Args:
        filepath: Absolute or relative path to the CSV file.

    Returns:
        pd.DataFrame: Loaded dataframe.

    Raises:
        FileNotFoundError: If the specified file does not exist.
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"[ERROR] CSV file not found: {filepath}")

    df = pd.read_csv(filepath)
    print(f"[INFO] Loaded '{filepath.name}' → {df.shape[0]} rows, {df.shape[1]} columns")
    return df


def load_all_raw_csvs(raw_dir: Path | str | None = None) -> dict[str, pd.DataFrame]:
    """
    Load all three raw CSV datasets from the raw data directory.

    Args:
        raw_dir: Optional override for the raw data directory.

    Returns:
        dict[str, pd.DataFrame]: Dict with keys 'add_spend', 'customer_interaction', 'revenue'.
    """
    base = Path(raw_dir) if raw_dir else RAW_DIR
    datasets = {}

    for key, filename in DATASET_FILES.items():
        filepath = base / filename
        datasets[key] = load_csv(filepath)

    return datasets


def load_csv_from_name(dataset_name: str, raw_dir: Path | str | None = None) -> pd.DataFrame:
    """
    Load a single dataset by its logical name.

    Args:
        dataset_name: One of 'add_spend', 'customer_interaction', 'revenue'.
        raw_dir: Optional override for the raw data directory.

    Returns:
        pd.DataFrame: The loaded dataset.

    Raises:
        KeyError: If dataset_name is not recognized.
    """
    if dataset_name not in DATASET_FILES:
        raise KeyError(
            f"[ERROR] Unknown dataset '{dataset_name}'. "
            f"Valid options: {list(DATASET_FILES.keys())}"
        )

    base = Path(raw_dir) if raw_dir else RAW_DIR
    return load_csv(base / DATASET_FILES[dataset_name])


if __name__ == "__main__":
    data = load_all_raw_csvs()
    for name, df in data.items():
        print(f"\n--- {name} ---")
        print(df.head(3))
