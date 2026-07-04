import os
import pandas as pd
import matplotlib.pyplot as plt


def plot_channels():

    os.makedirs("reports", exist_ok=True)

    df = pd.read_csv(
        "data/processed/adspend_featured.csv"
    )

    channel_counts = df["Channel"].value_counts()

    print("\nCampaign Count by Channel:")
    print(channel_counts)

    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.bar(
        channel_counts.index.tolist(),
        channel_counts.astype(int).tolist()
    )

    ax.set_title("Number of Campaigns by Channel")
    ax.set_xlabel("Marketing Channel")
    ax.set_ylabel("Number of Campaigns")

    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Display actual values on bars
    for bar in bars:
        height = bar.get_height()

        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            str(int(height)),
            ha="center",
            va="bottom"
        )

    plt.tight_layout()

    plt.savefig(
        "reports/channel_distribution.png"
    )

    plt.show()

    print("\nPlot saved to reports/channel_distribution.png")


if __name__ == "__main__":
    plot_channels()