import pandas as pd


def first_touch_attribution():

    df = pd.read_csv(
        "data/processed/customer_journeys.csv"
    )

    df["First_Touch"] = (
        df["Journey"]
        .str.split(" > ")
        .str[0]
    )

    result = (
        df.groupby("First_Touch")["Revenue"]
        .sum()
        .reset_index()
    )

    result.rename(
        columns={"Revenue": "Attributed_Revenue"},
        inplace=True
    )

    result.to_csv(
        "data/processed/first_touch_results.csv",
        index=False
    )

    print(result)


if __name__ == "__main__":
    first_touch_attribution()