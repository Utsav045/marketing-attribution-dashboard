import pandas as pd
import matplotlib.pyplot as plt


def plot_roi():

    # Load ROI results
    roi_df = pd.read_csv(
        "data/processed/roi_results.csv"
    )

    # Calculate average ROI by channel
    roi_by_channel = (
        roi_df.groupby("Channel")["ROI"]
        .mean()
    )

    # Sort in descending order
    roi_by_channel = roi_by_channel.sort_values(
        ascending=False
    )

    print("\nAverage ROI by Channel:")
    print(roi_by_channel)

    # Convert to Python lists
    channels = list(roi_by_channel.index)
    roi_values = [float(value) for value in roi_by_channel.values]

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.bar(
        channels,
        roi_values
    )

    ax.set_title(
        "Average ROI by Marketing Channel"
    )

    ax.set_xlabel(
        "Marketing Channel"
    )

    ax.set_ylabel(
        "Average ROI (%)"
    )

    plt.xticks(rotation=45)

    plt.grid(
        axis="y",
        linestyle="--",
        alpha=0.7
    )

    # Display ROI values on bars
    for bar in bars:

        height = bar.get_height()

        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{height:.2f}%",
            ha="center",
            va="bottom"
        )

    plt.tight_layout()

    # Save plot
    plt.savefig(
        "reports/roi_analysis.png",
        dpi=300
    )

    plt.show()

    print("\nPlot saved successfully!")
    print("Location: reports/roi_analysis.png")


if __name__ == "__main__":
    plot_roi()