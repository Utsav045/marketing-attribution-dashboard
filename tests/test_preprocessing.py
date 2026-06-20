import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

from src.preprocessing.data_cleaner import clean_data
from src.preprocessing.handle_missing import handle_missing
from src.preprocessing.transform_dates import transform_dates


def test_preprocessing():

    dataset_path = ROOT / "data" / "raw" / "Add_Spend_Dataset.csv"

    df = pd.read_csv(dataset_path)

    print("\n===== ORIGINAL DATA =====")
    print(df.shape)

    df = clean_data(df)

    print("\n✓ clean_data executed")
    print(df.shape)

    df = handle_missing(df)

    print("\n✓ handle_missing executed")
    print(df.shape)

    df = transform_dates(df)

    print("\n✓ transform_dates executed")
    print(df.shape)

    print("\n===== FINAL DATA =====")
    print(df.head())

    print("\n✓ Preprocessing Test Passed")


if __name__ == "__main__":
    test_preprocessing()