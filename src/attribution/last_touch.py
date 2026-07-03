import pandas as pd


def last_touch_attribution():

    df = pd.read_csv("data/processed/customer_journeys.csv")

    df["Last_Touch"] = df["Journey"].str.split(" > ").str[-1]

    result = df.groupby("Last_Touch")["Revenue"].sum().reset_index()

    result.rename(columns={"Revenue": "Attributed_Revenue"}, inplace=True)

    result.to_csv("data/processed/last_touch_results.csv", index=False)

    print(result)


if __name__ == "__main__":
    last_touch_attribution()
