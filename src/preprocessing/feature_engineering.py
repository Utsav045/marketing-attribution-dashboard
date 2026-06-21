import pandas as pd
import numpy as np


def create_ctr(df):
    """
    Click Through Rate (CTR)
    CTR = (Clicks / Impressions) * 100
    """
    df["CTR"] = np.where(
        df["Impressions"] > 0,
        (df["Clicks"] / df["Impressions"]) * 100,
        0
    )
    return df


def create_cpc(df):
    """
    Cost Per Click (CPC)
    CPC = Spend / Clicks
    """
    df["CPC"] = np.where(
        df["Clicks"] > 0,
        df["Spend"] / df["Clicks"],
        0
    )
    return df


def create_cpm(df):
    """
    Cost Per Mille (CPM)
    CPM = (Spend / Impressions) * 1000
    """
    df["CPM"] = np.where(
        df["Impressions"] > 0,
        (df["Spend"] / df["Impressions"]) * 1000,
        0
    )
    return df


def create_campaign_efficiency(df):
    """
    Campaign Efficiency Score
    Efficiency = Clicks / Spend
    """
    df["Campaign_Efficiency"] = np.where(
        df["Spend"] > 0,
        df["Clicks"] / df["Spend"],
        0
    )
    return df


def create_engagement_score(df):
    """
    Engagement Score
    Engagement = CTR * Campaign Efficiency
    """
    df["Engagement_Score"] = (
        df["CTR"] * df["Campaign_Efficiency"]
    )
    return df


def create_spend_category(df):
    """
    Categorize Campaign Spend
    """
    df["Spend_Category"] = pd.cut(
        df["Spend"],
        bins=[0, 1000, 5000, 10000, float("inf")],
        labels=["Low", "Medium", "High", "Very High"],
        include_lowest=True
    )
    return df


def create_click_category(df):
    """
    Categorize Click Performance
    """
    df["Click_Category"] = pd.cut(
        df["Clicks"],
        bins=[0, 100, 500, 1000, float("inf")],
        labels=["Low", "Medium", "High", "Very High"],
        include_lowest=True
    )
    return df


def feature_engineering(df):
    """
    Main Feature Engineering Pipeline
    """

    print("Starting Feature Engineering...")

    df = create_ctr(df)
    df = create_cpc(df)
    df = create_cpm(df)
    df = create_campaign_efficiency(df)
    df = create_engagement_score(df)
    df = create_spend_category(df)
    df = create_click_category(df)

    print("Feature Engineering Completed")

    return df


if __name__ == "__main__":

    INPUT_FILE = "data/raw/Add Spend Dataset.csv"
    OUTPUT_FILE = "data/processed/featured_engineering_dataset.csv"

    df = pd.read_csv(INPUT_FILE)

    df = feature_engineering(df)

    df.to_csv(OUTPUT_FILE, index=False)

    print("\nFeature Engineered Dataset Saved Successfully")
    print(f"Output File: {OUTPUT_FILE}")

    print("\nNew Columns Added:")
    print([
        "CTR",
        "CPC",
        "CPM",
        "Campaign_Efficiency",
        "Engagement_Score",
        "Spend_Category",
        "Click_Category"
    ])

    print("\nDataset Preview:")
    print(df.head())