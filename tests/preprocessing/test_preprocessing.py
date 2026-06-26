import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

import pandas as pd

sample_df = pd.DataFrame({
    "Campaign_id": ["C1", "C2"],
    "Spend": [1000, 2000],
    "Clicks": [100, 200],
    "Impressions": [10000, 20000],
    "Date": ["2025-01-01", "2025-01-02"]
})

print("\n========== PREPROCESSING TESTS ==========")

# data_cleaner

try:

    from src.preprocessing.data_cleaner import *

    print("[PASS] data_cleaner.py")

except Exception as e:

    print(f"[FAIL] data_cleaner.py -> {e}")

# handle_missing

try:

    from src.preprocessing.handle_missing import *

    print("[PASS] handle_missing.py")

except Exception as e:

    print(f"[FAIL] handle_missing.py -> {e}")

# transform_dates

try:

    from src.preprocessing.transform_dates import *

    print("[PASS] transform_dates.py")

except Exception as e:

    print(f"[FAIL] transform_dates.py -> {e}")

# feature_engineering

try:

    from src.preprocessing.feature_engineering import feature_engineering

    result = feature_engineering(sample_df)

    print("[PASS] feature_engineering.py")

except Exception as e:

    print(f"[FAIL] feature_engineering.py -> {e}")