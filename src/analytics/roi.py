import pandas as pd
import numpy as np


def calculate_roi():

    adspend_df = pd.read_csv(
        "data/processed/adspend_featured_eng.csv"
    )

    interaction_df = pd.read_csv(
        "data/processed/interaction_featured_eng.csv"
    )

    revenue_df = pd.read_csv(
        "data/processed/revenue_featured_eng.csv"
    )

    # Keep only required columns
    adspend_df = adspend_df[
        ["Campaign_id", "Channel", "Spend"]
    ]

    interaction_df = interaction_df[
        ["User_id", "Campaign_id"]
    ]

    revenue_df = revenue_df[
        ["User_id", "Revenue"]
    ]

    # Merge datasets
    roi_df = pd.merge(
        interaction_df,
        revenue_df,
        on="User_id",
        how="inner"
    )

    roi_df = pd.merge(
        roi_df,
        adspend_df,
        on="Campaign_id",
        how="inner"
    )

    # Calculate ROI
    roi_df["ROI"] = np.where(
        roi_df["Spend"] > 0,
        ((roi_df["Revenue"] - roi_df["Spend"])
         / roi_df["Spend"]) * 100,
        0
    )

    return roi_df


def main():

    roi_df = calculate_roi()

    output_file = (
        "data/processed/roi_results.csv"
    )

    roi_df.to_csv(
        output_file,
        index=False
    )

    print("ROI calculation completed successfully")
    print(f"Output File: {output_file}")

    print("\nColumns:")
    print(roi_df.columns.tolist())

    print("\nSample:")
    print(roi_df.head())


if __name__ == "__main__":
    main()