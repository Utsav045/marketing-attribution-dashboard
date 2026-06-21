import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

print("\n========== INGESTION TESTS ==========")

try:

    from src.ingestion.load_data import load_data

    datasets = load_data()

    print("[PASS] load_data.py")

except Exception as e:

    print(f"[FAIL] load_data.py -> {e}")