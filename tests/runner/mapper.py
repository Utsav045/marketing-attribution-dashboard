"""
Test Mapper Module

Purpose:
    Map project source modules to their related test files.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List


SOURCE_TO_TEST_MAP = {
    "src/attribution/first_touch.py": "tests/attribution/test_first_touch.py",
    "src/attribution/last_touch.py": "tests/attribution/test_last_touch.py",
    "src/attribution/linear_attribution.py": "tests/attribution/test_linear.py",
    "src/attribution/position_based.py": "tests/attribution/test_position_based.py",
    "src/attribution/attribution_engine.py": "tests/attribution/test_attribution_engine.py",
    "src/analytics/kpi_calculator.py": "tests/analytics/test_kpi_calculator.py",
    "src/analytics/eda.py": "tests/analytics/test_eda.py",
    "src/preprocessing/data_cleaner.py": "tests/preprocessing/test_data_cleaner.py",
    "src/preprocessing/transform_dates.py": "tests/preprocessing/test_transform_dates.py",
    "src/preprocessing/handle_missing.py": "tests/preprocessing/test_handle_missing.py",
    "src/preprocessing/feature_engineering.py": "tests/preprocessing/test_feature_engineering.py",
    "src/ingestion/data_loader.py": "tests/ingestion/test_ingestion.py",
    "src/pipeline/run_pipeline.py": "tests/pipeline/test_run_pipeline.py",
    "src/pipeline/orchestrator.py": "tests/pipeline/test_orchestrator.py",
}


def normalize_path(path: str | Path) -> str:
    """
    Normalize path to forward slash format.
    """

    return str(path).replace("\\", "/")


def get_test_for_source(source_path: str | Path) -> str | None:
    """
    Return mapped test file for a source file.
    """

    normalized = normalize_path(source_path)

    return SOURCE_TO_TEST_MAP.get(normalized)


def get_sources_for_test(test_path: str | Path) -> List[str]:
    """
    Return source files mapped to a test file.
    """

    normalized = normalize_path(test_path)

    return [
        source
        for source, test in SOURCE_TO_TEST_MAP.items()
        if test == normalized
    ]


def build_test_map() -> Dict[str, str]:
    """
    Return the full source to test map.
    """

    return dict(SOURCE_TO_TEST_MAP)


def check_missing_mapped_tests() -> List[str]:
    """
    Return mapped test files that do not exist.
    """

    missing = []

    for test_path in SOURCE_TO_TEST_MAP.values():
        if not Path(test_path).exists():
            missing.append(test_path)

    return missing


if __name__ == "__main__":
    print("Source to test map:")
    for source, test in build_test_map().items():
        print(f"{source} -> {test}")

    missing_tests = check_missing_mapped_tests()

    if missing_tests:
        print("\nMissing mapped tests:")
        for item in missing_tests:
            print(item)
    else:
        print("\nAll mapped tests exist.")