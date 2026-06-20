import pandas as pd


def linear_attribution():

    # Load customer journeys
    df = pd.read_csv(
        "data/processed/customer_journeys.csv"
    )

    attribution_rows = []

    # Split revenue equally across all channels
    for _, row in df.iterrows():

        channels = str(row["Journey"]).split(" > ")

        revenue = row["Revenue"]

        credit_per_channel = revenue / len(channels)

        for channel in channels:

            attribution_rows.append(
                {
                    "Channel": channel,
                    "Attributed_Revenue": credit_per_channel
                }
            )

    # Create dataframe
    result_df = pd.DataFrame(attribution_rows)

    # Sum revenue by channel
    result_df = (
        result_df
        .groupby("Channel")["Attributed_Revenue"]
        .sum()
        .reset_index()
    )

    # Sort descending
    result_df = result_df.sort_values(
        by="Attributed_Revenue",
        ascending=False
    )

    # Save results
    result_df.to_csv(
        "data/processed/linear attribution results.csv",
        index=False
    )

    print("\nLinear Attribution Results")
    print(result_df.head())

    print(
        "\nSaved to: data/processed/linear attribution results.csv"
    )


if __name__ == "__main__":
    linear_attribution()