"""
Helper Functions
"""

import pandas as pd
from pathlib import Path


def load_csv(file_path):
    """
    Load CSV file and return DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        print(f"Successfully loaded: {file_path}")
        return df
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None


def save_csv(df, file_path):
    """
    Save DataFrame to CSV.
    """
    try:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(file_path, index=False)
        print(f"Successfully saved: {file_path}")
    except Exception as e:
        print(f"Error saving file: {e}")


def get_dataset_info(df):
    """
    Print dataset information.
    """
    print("\nDataset Shape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)


def check_missing_values(df):
    """
    Return missing value summary.
    """
    return df.isnull().sum()


def check_duplicates(df):
    """
    Return duplicate row count.
    """
    return df.duplicated().sum()


def generate_summary(df):
    """
    Return statistical summary.
    """
    return df.describe(include="all")
