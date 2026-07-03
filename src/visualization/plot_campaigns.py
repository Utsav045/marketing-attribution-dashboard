import pandas as pd
import matplotlib.pyplot as plt


def plot_campaigns():

    # Load dataset
    df = pd.read_csv(
        "data/processed/adspend_featured.csv"
    )

    # Total spend by channel
    spend_by_channel = (
        df.groupby("Channel")["Spend"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\nTotal Spend by Channel:")
    print(spend_by_channel)

    # Create plot
    plt.figure(figsize=(10, 6))

    spend_by_channel.plot(
        kind="bar"
    )

    plt.title(
        "Campaign Spend by Channel"
    )

    plt.xlabel(
        "Marketing Channel"
    )

    plt.ylabel(
        "Total Spend ($)"
    )

    plt.xticks(
        rotation=45
    )

    plt.grid(
        axis="y",
        linestyle="--",
        alpha=0.7
    )

    plt.tight_layout()

    # Save plot to reports folder
    plt.savefig(
        "reports/campaign_spend.png"
    )

    # Show plot
    plt.show()

    print(
        "\nPlot saved successfully to reports/campaign_spend.png"
    )


if __name__ == "__main__":
    plot_campaigns()