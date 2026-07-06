import pandas as pd


def build_customer_journeys():
    # Load dataset
    interaction_df = pd.read_csv(
        "data/processed/cleaned_customer_interaction_dataset.csv"
    )

    revenue_df = pd.read_csv("data/processed/cleaned_revenue_dataset.csv")

    # Clean column names
    interaction_df.columns = interaction_df.columns.str.strip()
    revenue_df.columns = revenue_df.columns.str.strip()

    # Convert dates
    interaction_df["Interaction_date"] = pd.to_datetime(
        interaction_df["Interaction_date"], dayfirst=True, errors="coerce"
    )

    revenue_df["Conversion_date"] = pd.to_datetime(
        revenue_df["Conversion_date"], dayfirst=True, errors="coerce"
    )

    # Sort interactions
    interaction_df = interaction_df.sort_values(by=["User_id", "Interaction_date"])

    # Build Journey (Channel path)
    journey_df = (
        interaction_df.groupby("User_id")["Channel"]
        .apply(lambda x: " > ".join(x))
        .reset_index()
    )

    journey_df.rename(columns={"Channel": "Journey"}, inplace=True)

    # Add campaign journey
    campaign_journey = (
        interaction_df.groupby("User_id")["Campaign_id"]
        .apply(lambda x: " > ".join(x.astype(str)))
        .reset_index()
    )

    journey_df = journey_df.merge(campaign_journey, on="User_id", how="left")

    # Merge revenue
    journey_df = journey_df.merge(
        revenue_df[["User_id", "Conversion_id", "Revenue", "Conversion_date"]],
        on="User_id",
        how="left",
    )

    # Journey length
    journey_df["Journey_Length"] = journey_df["Journey"].str.split(" > ").str.len()

    # Save output
    output_path = "data/processed/customer_journeys.csv"
    journey_df.to_csv(output_path, index=False)

    print("Customer Journey created successfully")
    print(journey_df.head())

    return journey_df


if __name__ == "__main__":
    build_customer_journeys()
