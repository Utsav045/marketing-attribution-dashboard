import pandas as pd
import matplotlib.pyplot as plt


def plot_spend_by_channel(adspend_df):
   

    spend_data = (
        adspend_df.groupby("Channel")["Spend"]
        .sum()
    )

    plt.figure(figsize=(8, 5))
    spend_data.plot(kind="bar")

    plt.title("Total Spend by Channel")
    plt.xlabel("Channel")
    plt.ylabel("Spend")

    plt.ticklabel_format(
        style="plain",
        axis="y"
    )

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_clicks_by_channel(adspend_df):
   

    click_data = (
        adspend_df.groupby("Channel")["Clicks"]
        .sum()
    )

    plt.figure(figsize=(8, 5))
    click_data.plot(kind="bar")

    plt.title("Total Clicks by Channel")
    plt.xlabel("Channel")
    plt.ylabel("Clicks")

    plt.ticklabel_format(
        style="plain",
        axis="y"
    )

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_revenue_distribution(revenue_df):
   

    plt.figure(figsize=(8, 5))

    plt.hist(
        revenue_df["Revenue"],
        bins=20
    )

    plt.title("Revenue Distribution")
    plt.xlabel("Revenue")
    plt.ylabel("Frequency")

    plt.ticklabel_format(
        style="plain",
        axis="x"
    )

    plt.tight_layout()
    plt.show()


def plot_revenue_category(revenue_df):

    category_data = (
        revenue_df["Revenue_Category"]
        .value_counts()
    )

    plt.figure(figsize=(8, 5))
    category_data.plot(kind="bar")

    plt.title("Revenue Category Distribution")
    plt.xlabel("Category")
    plt.ylabel("Count")

    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()


def main():
    """
    Main execution function.
    """

    adspend_df = pd.read_csv(
        "data/processed/adspend_featured_eng.csv"
    )

    revenue_df = pd.read_csv(
        "data/processed/revenue_featured_eng.csv"
    )

    print("Generating Charts...")

    plot_spend_by_channel(adspend_df)
    plot_clicks_by_channel(adspend_df)
    plot_revenue_distribution(revenue_df)
    plot_revenue_category(revenue_df)

    print("Charts Generated Successfully")


if __name__ == "__main__":
    main()