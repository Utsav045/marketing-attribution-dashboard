from pathlib import Path
import pandas as pd


def load_raw_data(root_dir: Path | str | None = None) -> dict[str, pd.DataFrame]:
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


def print_raw_previews(root_dir: Path | str | None = None) -> None:
    data = load_raw_data(root_dir)
    for name, df in data.items():
        print(f"{name} preview:")
        print(df.head())


if __name__ == "__main__":
    print_raw_previews()
