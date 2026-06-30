import pandas as pd


def time_decay_attribution():

    journey_df = pd.read_csv(
        "data/processed/customer_journeys.csv"
    )

    attribution_records = []

    for _, row in journey_df.iterrows():

        revenue = row["Revenue"]

        channels = row["Journey"].split(" > ")

        n = len(channels)

        if n == 0:
            continue

        weights = list(range(1, n + 1))

        total_weight = sum(weights)

        normalized_weights = [
            w / total_weight
            for w in weights
        ]

        for channel, weight in zip(
            channels,
            normalized_weights
        ):

            attribution_records.append({

                "User_id": row["User_id"],

                "Channel": channel,

                "Weight": round(weight, 4),

                "Attributed_Revenue": round(
                    revenue * weight,
                    2
                )

            })

    result_df = pd.DataFrame(
        attribution_records
    )

    result_df.to_csv(

        "data/processed/time_decay_attribution.csv",

        index=False

    )

    print(
        "Time Decay Attribution Completed Successfully"
    )


if __name__ == "__main__":

    time_decay_attribution()