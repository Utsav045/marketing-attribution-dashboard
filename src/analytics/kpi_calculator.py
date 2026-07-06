import pandas as pd


def calculate_kpis():

    # Load Featured Datasets
    adspend_df = pd.read_csv("data/processed/adspend_featured.csv")

    revenue_df = pd.read_csv("data/processed/revenue_featured.csv")

    # ==========================
    # DEBUG (Verify Data)
    # ==========================
    print("\n========== DATA CHECK ==========")
    print("Ad Spend Rows :", adspend_df.shape[0])
    print("Revenue Rows  :", revenue_df.shape[0])

    print(f"Total Spend   : {adspend_df['Spend'].sum():,.2f}")
    print(f"Total Revenue : {revenue_df['Revenue'].sum():,.2f}")

    # ==========================
    # KPI VALUES
    # ==========================

    total_spend = adspend_df["Spend"].sum()
    total_clicks = adspend_df["Clicks"].sum()
    total_impressions = adspend_df["Impressions"].sum()

    total_revenue = revenue_df["Revenue"].sum()
    total_conversions = revenue_df.shape[0]

    # ==========================
    # KPI CALCULATIONS
    # ==========================

    ctr = total_clicks / total_impressions * 100 if total_impressions > 0 else 0

    cpc = total_spend / total_clicks if total_clicks > 0 else 0

    cpm = total_spend / total_impressions * 1000 if total_impressions > 0 else 0

    roi = (total_revenue - total_spend) / total_spend * 100 if total_spend > 0 else 0

    roas = total_revenue / total_spend if total_spend > 0 else 0

    conversion_rate = total_conversions / total_clicks * 100 if total_clicks > 0 else 0

    avg_revenue_per_conversion = (
        total_revenue / total_conversions if total_conversions > 0 else 0
    )

    kpis = {
        "Total Spend": round(total_spend, 2),
        "Total Revenue": round(total_revenue, 2),
        "Total Clicks": int(total_clicks),
        "Total Impressions": int(total_impressions),
        "Total Conversions": int(total_conversions),
        "CTR (%)": round(ctr, 2),
        "CPC": round(cpc, 2),
        "CPM": round(cpm, 2),
        "ROI (%)": round(roi, 2),
        "ROAS": round(roas, 2),
        "Conversion Rate (%)": round(conversion_rate, 2),
        "Avg Revenue Per Conversion": round(avg_revenue_per_conversion, 2),
    }

    return kpis


def save_kpis():

    kpis = calculate_kpis()

    kpi_df = pd.DataFrame(list(kpis.items()), columns=["KPI", "Value"])

    kpi_df.to_csv("data/processed/kpi_summary.csv", index=False)

    print("\n========== MARKETING KPI SUMMARY ==========\n")

    for key, value in kpis.items():
        print(f"{key:<30}: {value}")

    print("\nKPI file saved successfully!")
    print("Location: data/processed/kpi_summary.csv")


if __name__ == "__main__":
    save_kpis()
