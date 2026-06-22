import pandas as pd
import numpy as np


def feature_engineering(adspend_df, interaction_df, revenue_df):
    """
    Apply feature engineering to all datasets.
    """

    print("Starting Feature Engineering...")

    # =====================================================
    # AD SPEND DATASET FEATURES
    # =====================================================

    adspend_df["CTR"] = np.where(
        adspend_df["Impressions"] > 0,
        (adspend_df["Clicks"] / adspend_df["Impressions"]) * 100,
        0
    )

    adspend_df["CPC"] = np.where(
        adspend_df["Clicks"] > 0,
        adspend_df["Spend"] / adspend_df["Clicks"],
        0
    )

    adspend_df["CPM"] = np.where(
        adspend_df["Impressions"] > 0,
        (adspend_df["Spend"] / adspend_df["Impressions"]) * 1000,
        0
    )

    adspend_df["Campaign_Efficiency"] = np.where(
        adspend_df["Spend"] > 0,
        adspend_df["Clicks"] / adspend_df["Spend"],
        0
    )

    adspend_df["Engagement_Score"] = (
        adspend_df["CTR"] *
        adspend_df["Campaign_Efficiency"]
    )

    # =====================================================
    # CUSTOMER INTERACTION DATASET FEATURES
    # =====================================================

    if {
        "Impressions",
        "Clicks",
        "Spend"
    }.issubset(interaction_df.columns):
        interaction_df["Interaction_Rate"] = np.where(
            interaction_df["Impressions"] > 0,
            interaction_df["Clicks"] / interaction_df["Impressions"],
            0
        )

        interaction_df["Engagement_Index"] = np.where(
            interaction_df["Impressions"] > 0,
            (interaction_df["Clicks"] * 100) /
            interaction_df["Impressions"],
            0
        )

        interaction_df["Channel_Performance"] = np.where(
            interaction_df["Spend"] > 0,
            interaction_df["Clicks"] / interaction_df["Spend"],
            0
        )
    else:
        if "Interaction_date" in interaction_df.columns:
            interaction_df["Interaction_Day"] = pd.to_datetime(
                interaction_df["Interaction_date"],
                errors="coerce"
            ).dt.day_name()
            interaction_df["Interaction_Month"] = pd.to_datetime(
                interaction_df["Interaction_date"],
                errors="coerce"
            ).dt.month

    # =====================================================
    # REVENUE DATASET FEATURES
    # =====================================================

    if "Revenue" in revenue_df.columns:
        revenue_df["Revenue"] = (
            revenue_df["Revenue"]
            .astype(str)
            .replace(r"[\$,]", "", regex=True)
            .replace("nan", "")
            .astype(float)
        )

        revenue_df["Revenue_Log"] = np.log1p(
            revenue_df["Revenue"]
        )

        revenue_df["Revenue_Rank"] = (
            revenue_df["Revenue"]
            .rank(method="dense", ascending=False)
        )

        revenue_df["High_Value_Conversion"] = np.where(
            revenue_df["Revenue"] >
            revenue_df["Revenue"].median(),
            1,
            0
        )

        revenue_df["Revenue_Category"] = pd.cut(
            revenue_df["Revenue"],
            bins=[0, 100, 500, 1000, float("inf")],
            labels=["Low", "Medium", "High", "Very High"],
            include_lowest=True
        )

    print("Feature Engineering Completed")

    return adspend_df, interaction_df, revenue_df


def save_featured_datasets(
    adspend_df,
    interaction_df,
    revenue_df
):
    """
    Save processed datasets.
    """

    adspend_df.to_csv(
        "data/processed/adspend_featured.csv",
        index=False
    )

    interaction_df.to_csv(
        "data/processed/interaction_featured.csv",
        index=False
    )

    revenue_df.to_csv(
        "data/processed/revenue_featured.csv",
        index=False
    )

    print("\nFiles Generated:")
    print("data/processed/adspend_featured.csv")
    print("data/processed/interaction_featured.csv")
    print("data/processed/revenue_featured.csv")


def main():
    """
    Main execution function.
    """

    adspend_df = pd.read_csv(
        "data/raw/add_spend_dataset.csv"
    )

    interaction_df = pd.read_csv(
        "data/raw/customer_interaction_dataset.csv"
    )

    revenue_df = pd.read_csv(
        "data/raw/revenue_dataset.csv"
    )

    (
        adspend_df,
        interaction_df,
        revenue_df
    ) = feature_engineering(
        adspend_df,
        interaction_df,
        revenue_df
    )

    save_featured_datasets(
        adspend_df,
        interaction_df,
        revenue_df
    )

    print("\nFeature Engineering Completed Successfully")


if __name__ == "__main__":
    main()