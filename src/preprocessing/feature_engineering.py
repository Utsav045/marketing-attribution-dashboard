import pandas as pd
import numpy as np

# =====================================================
# AD SPEND FEATURES
# =====================================================


def create_ctr(df):

    df["CTR"] = np.where(
        df["Impressions"] > 0, (df["Clicks"] / df["Impressions"]) * 100, 0
    )

    return df


def create_cpc(df):

    df["CPC"] = np.where(df["Clicks"] > 0, df["Spend"] / df["Clicks"], 0)

    return df


def create_cpm(df):

    df["CPM"] = np.where(
        df["Impressions"] > 0, (df["Spend"] / df["Impressions"]) * 1000, 0
    )

    return df


def create_campaign_efficiency(df):

    df["Campaign_Efficiency"] = np.where(df["Spend"] > 0, df["Clicks"] / df["Spend"], 0)

    return df


def create_engagement_score(df):

    df["Engagement_Score"] = df["CTR"] * df["Campaign_Efficiency"]

    return df


def create_spend_category(df):

    df["Spend_Category"] = pd.cut(
        df["Spend"],
        bins=[0, 1000, 5000, 10000, float("inf")],
        labels=["Low", "Medium", "High", "Very High"],
        include_lowest=True,
    )

    return df


def create_click_category(df):

    df["Click_Category"] = pd.cut(
        df["Clicks"],
        bins=[0, 100, 500, 1000, float("inf")],
        labels=["Low", "Medium", "High", "Very High"],
        include_lowest=True,
    )

    return df


# =====================================================
# CUSTOMER INTERACTION FEATURES
# =====================================================


def create_interaction_features(df):

    df["Interaction_date"] = pd.to_datetime(df["Interaction_date"], errors="coerce")

    df["Interaction_Day"] = df["Interaction_date"].dt.day_name()

    df["Interaction_Month"] = df["Interaction_date"].dt.month_name()

    df["Interaction_Quarter"] = df["Interaction_date"].dt.quarter

    df["Is_Weekend"] = np.where(df["Interaction_date"].dt.dayofweek >= 5, 1, 0)

    return df


# =====================================================
# REVENUE FEATURES
# =====================================================


def create_revenue_log(df):

    df["Revenue_Log"] = np.log1p(df["Revenue"])

    return df


def create_revenue_rank(df):

    df["Revenue_Rank"] = df["Revenue"].rank(method="dense", ascending=False)

    return df


def create_high_value_conversion(df):

    df["High_Value_Conversion"] = np.where(df["Revenue"] > df["Revenue"].median(), 1, 0)

    return df


def create_revenue_category(df):

    df["Revenue_Category"] = pd.cut(
        df["Revenue"],
        bins=[0, 100, 500, 1000, float("inf")],
        labels=["Low", "Medium", "High", "Very High"],
        include_lowest=True,
    )

    return df


# =====================================================
# MAIN FEATURE ENGINEERING FUNCTION
# =====================================================


def feature_engineering(adspend_df, interaction_df, revenue_df):

    print("Starting Feature Engineering...")

    # Ad Spend Features
    adspend_df = create_ctr(adspend_df)
    adspend_df = create_cpc(adspend_df)
    adspend_df = create_cpm(adspend_df)
    adspend_df = create_campaign_efficiency(adspend_df)
    adspend_df = create_engagement_score(adspend_df)
    adspend_df = create_spend_category(adspend_df)
    adspend_df = create_click_category(adspend_df)

    # Customer Interaction Features
    interaction_df = create_interaction_features(interaction_df)

    # Revenue Features
    revenue_df = create_revenue_log(revenue_df)
    revenue_df = create_revenue_rank(revenue_df)
    revenue_df = create_high_value_conversion(revenue_df)
    revenue_df = create_revenue_category(revenue_df)

    print("Feature Engineering Completed")

    return (adspend_df, interaction_df, revenue_df)


# =====================================================
# SAVE FILES
# =====================================================


def save_featured_datasets(adspend_df, interaction_df, revenue_df):

    adspend_df.to_csv("data/processed/adspend_featured_eng.csv", index=False)

    interaction_df.to_csv("data/processed/interaction_featured_eng.csv", index=False)

    revenue_df.to_csv("data/processed/revenue_featured_eng.csv", index=False)

    print("\nFiles Generated:")
    print("data/processed/adspend_featured.csv")
    print("data/processed/interaction_featured.csv")
    print("data/processed/revenue_featured.csv")


# =====================================================
# MAIN FUNCTION
# =====================================================


def main():

    adspend_df = pd.read_csv("data/processed/cleaned_add_spend_dataset.csv")

    interaction_df = pd.read_csv(
        "data/processed/cleaned_customer_interaction_dataset.csv"
    )

    revenue_df = pd.read_csv("data/processed/cleaned_revenue_dataset.csv")

    adspend_df, interaction_df, revenue_df = feature_engineering(
        adspend_df, interaction_df, revenue_df
    )

    save_featured_datasets(adspend_df, interaction_df, revenue_df)

    print("\nFeature Engineering Completed Successfully")


if __name__ == "__main__":
    main()
