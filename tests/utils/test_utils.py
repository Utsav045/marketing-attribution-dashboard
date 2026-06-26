import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

import pandas as pd

print("\n========== UTILS TESTS ==========")

try:
    from src.utils.config import *
    print("[PASS] config.py")
except Exception as e:
    print(f"[FAIL] config.py -> {e}")

try:
    from src.utils.constants import *
    print("[PASS] constants.py")
except Exception as e:
    print(f"[FAIL] constants.py -> {e}")

try:
    from src.utils.helpers import *
    
    sample_df = pd.DataFrame({
        "A": [1, 2, None],
        "B": [4, 5, 6]
    })

    get_dataset_info(sample_df)
    check_missing_values(sample_df)

    print("[PASS] helpers.py")

except Exception as e:
    print(f"[FAIL] helpers.py -> {e}")

try:
    from src.utils.file_manager import *

    test_dir = ROOT / "temp_test"

    create_directory(test_dir)

    print("[PASS] file_manager.py")

except Exception as e:
    print(f"[FAIL] file_manager.py -> {e}")