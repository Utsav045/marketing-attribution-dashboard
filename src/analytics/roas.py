import pandas as pd
import numpy as np


def calculate_roas():
    

    # Load datasets
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
    roas_df = pd.merge(
        interaction_df,
        revenue_df,
        on="User_id",
        how="inner"
    )

    roas_df = pd.merge(
        roas_df,
        adspend_df,
        on="Campaign_id",
        how="inner"
    )

    # Calculate ROAS
    roas_df["ROAS"] = np.where(
        roas_df["Spend"] > 0,
        roas_df["Revenue"] / roas_df["Spend"],
        0
    )

    return roas_df


def save_roas_results(df):
    """
    Save ROAS results.
    """

    output_file = "data/processed/roas_results.csv"

    df.to_csv(
        output_file,
        index=False
    )

    print("\nROAS Results Saved Successfully")
    print(f"Output File: {output_file}")


def main():
    """
    Main execution function.
    """

    roas_df = calculate_roas()

    save_roas_results(roas_df)

    print("\nSample Results:")
    print(
        roas_df[
            [
                "User_id",
                "Campaign_id",
                "Channel",
                "Spend",
                "Revenue",
                "ROAS"
            ]
        ].head()
    )


if __name__ == "__main__":
    main()