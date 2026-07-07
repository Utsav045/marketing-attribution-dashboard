"""
Schema Validation Module
Multi-Touch Marketing Attribution & ROI Dashboard
"""

import pandas as pd


# Expected columns for each dataset
EXPECTED_SCHEMAS: dict[str, list[str]] = {
    "add_spend": [
        "Campaign_id",
        "Channel",
        "Spend",
        "Clicks",
        "Impressions",
    ],
    "customer_interaction": [
        "User_id",
        "Campaign_id",
        "Channel",
        "Timestamp",
        "Conversion",
    ],
    "revenue": [
        "User_id",
        "Revenue",
        "Conversion_Date",
    ],
}


class SchemaValidationError(Exception):
    """Raised when a DataFrame does not match the expected schema."""


def validate_schema(
    df: pd.DataFrame,
    dataset_name: str,
    strict: bool = False,
) -> bool:
    """
    Validate that a DataFrame contains the expected columns.

    Args:
        df: The DataFrame to validate.
        dataset_name: Key into EXPECTED_SCHEMAS ('add_spend', 'customer_interaction', 'revenue').
        strict: If True, raises SchemaValidationError on failure instead of returning False.

    Returns:
        bool: True if all expected columns are present.

    Raises:
        KeyError: If dataset_name is not recognised.
        SchemaValidationError: If strict=True and validation fails.
    """
    if dataset_name not in EXPECTED_SCHEMAS:
        raise KeyError(
            f"[ERROR] Unknown dataset '{dataset_name}'. "
            f"Valid options: {list(EXPECTED_SCHEMAS.keys())}"
        )

    expected = set(EXPECTED_SCHEMAS[dataset_name])
    actual = set(df.columns.str.strip())
    missing = expected - actual

    if missing:
        msg = (
            f"[SCHEMA ERROR] Dataset '{dataset_name}' is missing columns: {missing}. "
            f"Found columns: {list(df.columns)}"
        )
        if strict:
            raise SchemaValidationError(msg)
        print(msg)
        return False

    print(f"[INFO] Schema validation passed for '{dataset_name}'.")
    return True


def validate_all_schemas(
    datasets: dict[str, pd.DataFrame],
    strict: bool = False,
) -> dict[str, bool]:
    """
    Validate schemas for all provided datasets.

    Args:
        datasets: Dict mapping dataset name → DataFrame.
        strict: If True, raises on first validation failure.

    Returns:
        dict[str, bool]: Validation result for each dataset.
    """
    results = {}
    for name, df in datasets.items():
        results[name] = validate_schema(df, name, strict=strict)
    return results


def check_no_empty_dataframe(df: pd.DataFrame, dataset_name: str) -> bool:
    """
    Check that a DataFrame is not empty.

    Args:
        df: The DataFrame to check.
        dataset_name: Name used in error messaging.

    Returns:
        bool: True if the DataFrame has at least one row.
    """
    if df.empty:
        print(f"[WARN] Dataset '{dataset_name}' is empty (0 rows).")
        return False
    return True


if __name__ == "__main__":
    # Quick smoke test with dummy data
    dummy_spend = pd.DataFrame(
        columns=["Campaign_id", "Channel", "Spend", "Clicks", "Impressions"]
    )
    validate_schema(dummy_spend, "add_spend")

    dummy_revenue = pd.DataFrame(columns=["User_id", "Revenue"])  # missing Conversion_Date
    validate_schema(dummy_revenue, "revenue")
