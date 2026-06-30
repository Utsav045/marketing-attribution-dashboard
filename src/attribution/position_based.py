import pandas as pd


def position_based_attribution():

    journey_df = pd.read_csv(

        "data/processed/customer_journeys.csv"

    )

    attribution_records = []

    for _, row in journey_df.iterrows():

        revenue = row["Revenue"]

        channels = row["Journey"].split(" > ")

        n = len(channels)

        if n == 1:

            weights = [1.0]

        elif n == 2:

            weights = [0.5, 0.5]

        else:

            middle = n - 2

            middle_weight = 0.2 / middle

            weights = [0.4]

            weights.extend(
                [middle_weight] * middle
            )

            weights.append(0.4)

        for channel, weight in zip(
            channels,
            weights
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

        "data/processed/position_based_attribution.csv",

        index=False

    )

    print(
        "Position Based Attribution Completed Successfully"
    )


if __name__ == "__main__":

    position_based_attribution()