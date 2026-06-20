import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

AD_SPEND_FILE = ROOT / "data" / "raw" / "Add_Spend_Dataset.csv"
INTERACTION_FILE = ROOT / "data" / "raw" / "Customer_Interaction_dataset.csv"
REVENUE_FILE = ROOT / "data" / "raw" / "Revenue_dataset.csv"


def test_datasets():

    print("\n===== LOADING DATASETS =====")

    addspend_df = pd.read_csv(AD_SPEND_FILE)
    interaction_df = pd.read_csv(INTERACTION_FILE)
    revenue_df = pd.read_csv(REVENUE_FILE)

    print("\n===== DATASET SHAPES =====")
    print("Ad Spend:", addspend_df.shape)
    print("Interaction:", interaction_df.shape)
    print("Revenue:", revenue_df.shape)

    print("\n===== AD SPEND COLUMNS =====")
    print(addspend_df.columns.tolist())

    print("\n===== INTERACTION COLUMNS =====")
    print(interaction_df.columns.tolist())

    print("\n===== REVENUE COLUMNS =====")
    print(revenue_df.columns.tolist())

    print("\n===== NULL VALUES =====")
    print("\nAd Spend")
    print(addspend_df.isnull().sum())

    print("\nInteraction")
    print(interaction_df.isnull().sum())

    print("\nRevenue")
    print(revenue_df.isnull().sum())

    print("\n===== SAMPLE DATA =====")
    print(addspend_df.head())
    print(interaction_df.head())
    print(revenue_df.head())

    print("\n✓ Dataset Test Passed")


if __name__ == "__main__":
    test_datasets()