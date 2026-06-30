import traceback
import os
import sys

from src.attribution.attribution_engine import build_customer_journeys
from src.attribution.first_touch import first_touch_attribution
from src.attribution.last_touch import last_touch_attribution
from src.attribution.linear_attribution import linear_attribution
from src.attribution.time_decay import time_decay_attribution
from src.attribution.position_based import position_based_attribution

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

sys.path.insert(0, PROJECT_ROOT)

from src.attribution.attribution_engine import (
    build_customer_journeys,
)

from src.attribution.first_touch import (
    first_touch_attribution,
)

from src.attribution.last_touch import (
    last_touch_attribution,
)

from src.attribution.linear_attribution import (
    linear_attribution,
)

from src.attribution.time_decay import (
    time_decay_attribution,
)

from src.attribution.position_based import (
    position_based_attribution,
)


def run_test(module_name, function):
    """
    Runs a single attribution module and reports status.
    """

    print("\n" + "=" * 60)
    print(f"Testing : {module_name}")
    print("=" * 60)

    try:
        function()
        print(f"[PASS] {module_name}")

    except Exception:
        print(f"[FAIL] {module_name}")
        traceback.print_exc()


def test_attribution():

    print("\n" + "#" * 70)
    print("RUNNING ATTRIBUTION MODULE TESTS")
    print("#" * 70)

    run_test(
        "Customer Journey Builder",
        build_customer_journeys
    )

    run_test(
        "First Touch Attribution",
        first_touch_attribution
    )

    run_test(
        "Last Touch Attribution",
        last_touch_attribution
    )

    run_test(
        "Linear Attribution",
        linear_attribution
    )

    run_test(
        "Time Decay Attribution",
        time_decay_attribution
    )

    run_test(
        "Position Based Attribution",
        position_based_attribution
    )

    print("\n" + "#" * 70)
    print("ALL ATTRIBUTION TESTS COMPLETED")
    print("#" * 70)


if __name__ == "__main__":
    test_attribution()