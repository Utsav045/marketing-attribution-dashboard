"""
ROI Visualization Module
Multi-Touch Marketing Attribution & ROI Dashboard
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot_roi_by_channel(roi_df: pd.DataFrame) -> None:
    """
    Bar chart of ROI (%) per marketing channel.

    Args:
        roi_df: DataFrame with columns ['Channel', 'ROI'].
    """
    grouped = roi_df.groupby("Channel")["ROI"].mean().sort_values(ascending=False)

    values = grouped.to_numpy()
    labels: list[str] = list(grouped.index)
    colors: list[str] = ["#2ecc71" if v >= 0 else "#e74c3c" for v in values]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(labels, values, color=colors, edgecolor="white", linewidth=0.8)

    for bar, val in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.5,
            f"{val:.1f}%",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
    ax.set_title("Average ROI (%) by Marketing Channel", fontsize=14, fontweight="bold")
    ax.set_xlabel("Channel")
    ax.set_ylabel("ROI (%)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig("reports/roi_by_channel.png", dpi=150)
    plt.show()
    print("[INFO] Saved: reports/roi_by_channel.png")


def plot_roi_vs_spend(roi_df: pd.DataFrame) -> None:
    """
    Scatter plot of ROI (%) vs Spend per campaign/row.

    Args:
        roi_df: DataFrame with columns ['Spend', 'ROI'] and optionally ['Channel'].
    """
    fig, ax = plt.subplots(figsize=(9, 6))

    if "Channel" in roi_df.columns:
        channels = roi_df["Channel"].unique()
        colormap = plt.matplotlib.colormaps["tab10"]
        for i, channel in enumerate(channels):
            subset = roi_df[roi_df["Channel"] == channel]
            color = colormap(i / max(len(channels) - 1, 1))
            ax.scatter(
                subset["Spend"].to_numpy(),
                subset["ROI"].to_numpy(),
                label=str(channel),
                alpha=0.7,
                color=color,
                s=40,
            )
        ax.legend(title="Channel", fontsize=8)
    else:
        ax.scatter(
            roi_df["Spend"].to_numpy(),
            roi_df["ROI"].to_numpy(),
            alpha=0.6,
            color="#3498db",
            s=40,
        )

    ax.axhline(0, color="red", linewidth=0.8, linestyle="--", label="Break-even")
    ax.set_title("ROI (%) vs Ad Spend", fontsize=14, fontweight="bold")
    ax.set_xlabel("Spend ($)")
    ax.set_ylabel("ROI (%)")
    ax.ticklabel_format(style="plain", axis="x")
    plt.tight_layout()
    plt.savefig("reports/roi_vs_spend.png", dpi=150)
    plt.show()
    print("[INFO] Saved: reports/roi_vs_spend.png")


def plot_revenue_vs_spend(roi_df: pd.DataFrame) -> None:
    """
    Side-by-side bar chart comparing Revenue and Spend per channel.

    Args:
        roi_df: DataFrame with columns ['Channel', 'Spend', 'Revenue'].
    """
    grouped = roi_df.groupby("Channel")[["Spend", "Revenue"]].sum()

    x = np.arange(len(grouped))
    bar_width: float = 0.35
    labels: list[str] = list(grouped.index)

    spend_vals = grouped["Spend"].to_numpy()
    revenue_vals = grouped["Revenue"].to_numpy()

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.bar(x - bar_width / 2, spend_vals, width=bar_width, label="Spend", color="#e67e22", alpha=0.85)
    ax.bar(x + bar_width / 2, revenue_vals, width=bar_width, label="Revenue", color="#27ae60", alpha=0.85)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=30, ha="right")
    ax.set_title("Revenue vs Spend by Channel", fontsize=14, fontweight="bold")
    ax.set_xlabel("Channel")
    ax.set_ylabel("Amount ($)")
    ax.legend()
    ax.ticklabel_format(style="plain", axis="y")
    plt.tight_layout()
    plt.savefig("reports/revenue_vs_spend.png", dpi=150)
    plt.show()
    print("[INFO] Saved: reports/revenue_vs_spend.png")


def main() -> None:
    """Generate all ROI visualisations from processed data."""
    roi_df = pd.read_csv("data/processed/roi_results.csv")

    print("Generating ROI charts...")
    plot_roi_by_channel(roi_df)
    plot_roi_vs_spend(roi_df)

    if "Revenue" in roi_df.columns:
        plot_revenue_vs_spend(roi_df)

    print("ROI charts generated successfully.")


def plot_roi() -> None:
    """Backward-compatible wrapper for the ROI plotting entry point."""
    main()


if __name__ == "__main__":
    main()
