import pandas as pd

from src.attribution.linear_attribution import compute_linear_attribution


def test_compute_linear_attribution_groups_revenue_per_channel():
    df = pd.DataFrame(
        {
            "Journey": ["Email > Social", "Social"],
            "Revenue": [200, 100],
        }
    )

    result = compute_linear_attribution(df)

    assert set(result["Channel"]) == {"Email", "Social"}
    assert result.loc[result["Channel"] == "Email", "Attributed_Revenue"].iloc[0] == 100.0
