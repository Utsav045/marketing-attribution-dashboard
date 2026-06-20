import pandas as pd

from src.attribution.linear_attribution import compute_linear_attribution


def test_compute_linear_attribution_handles_currency_strings():
    df = pd.DataFrame([
        {
            "Journey": "Email Marketing > Facebook Ads",
            "Revenue": "$1,200.00"
        },
        {
            "Journey": "Instagram Ads",
            "Revenue": "$3,000.50"
        },
        {
            "Journey": "Email Marketing > Instagram Ads > Facebook Ads",
            "Revenue": "$2,700"
        }
    ])

    result = compute_linear_attribution(df)

    assert "Channel" in result.columns
    assert "Attributed_Revenue" in result.columns

    email_row = result[result["Channel"] == "Email Marketing"].iloc[0]
    facebook_row = result[result["Channel"] == "Facebook Ads"].iloc[0]
    instagram_row = result[result["Channel"] == "Instagram Ads"].iloc[0]

    assert email_row["Attributed_Revenue"] == 1_200.00 / 2 + 2_700.00 / 3
    assert facebook_row["Attributed_Revenue"] == 1_200.00 / 2 + 2_700.00 / 3
    assert instagram_row["Attributed_Revenue"] == 3_000.50 + 2_700.00 / 3
