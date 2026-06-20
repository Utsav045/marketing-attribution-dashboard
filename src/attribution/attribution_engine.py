import pandas as pd


def build_customer_journeys():

    interaction_df = pd.read_csv(
        "data/processed/cleaned_Customer_Interaction_Dataset.csv"
    )

    revenue_df = pd.read_csv(
        "data/processed/cleaned_Revenue_Dataset.csv"
    )

    interaction_df["Interaction_date"] = pd.to_datetime(
        interaction_df["Interaction_date"],
        dayfirst=True,
        errors="coerce"
    )

    interaction_df = interaction_df.sort_values(
        by=["User_id", "Interaction_date"]
    )

    journey_df = (
        interaction_df.groupby("User_id")
        .agg({
            "Channel": lambda x: " > ".join(x),
            "Campaign_id": lambda x: " > ".join(x)
        })
        .reset_index()
    )

    journey_df.rename(
        columns={"Channel": "Journey"},
        inplace=True
    )

    journey_df = journey_df.merge(
        revenue_df,
        on="User_id",
        how="left"
    )

    journey_df["Journey_Length"] = (
        journey_df["Journey"]
        .str.split(" > ")
        .str.len()
    )

    journey_df.to_csv(
        "data/processed/customer_journeys.csv",
        index=False
    )

    print("Customer journeys created successfully")


if __name__ == "__main__":
    build_customer_journeys()