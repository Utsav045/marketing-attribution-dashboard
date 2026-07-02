import pandas as pd


def calculate_cac():

    adspend_df = pd.read_csv("data/processed/adspend_featured.csv")

    interaction_df = pd.read_csv("data/processed/interaction_featured.csv")

    total_spend = adspend_df["Spend"].sum()

    total_customers = interaction_df["User_id"].nunique()

    cac = total_spend / total_customers

    print("Total Spend:", total_spend)
    print("Total Customers:", total_customers)
    print("CAC:", round(cac, 2))


if __name__ == "__main__":
    calculate_cac()
