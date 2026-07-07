"""
Test Discovery Module

Purpose:
    Discover Python test files inside the tests folder.
"""

from __future__ import annotations

from pathlib import Path
from typing import List


def discover_test_files(
    tests_root: str | Path = "tests",
    pattern: str = "test_*.py",
) -> List[Path]:
    """
    Discover test files recursively.

    Args:
        tests_root: Root test directory.
        pattern: Test file pattern.

    Returns:
        List of discovered test file paths.
    """

    root = Path(tests_root)

    if not root.exists():
        raise FileNotFoundError(f"Test directory not found: {root}")

    return sorted(root.rglob(pattern))


def filter_test_files_by_keyword(
    test_files: List[Path],
    keyword: str,
) -> List[Path]:
    """
    Filter discovered test files by keyword.

    Example:
        keyword='attribution' returns files with attribution in the path.
    """

    keyword_lower = keyword.lower()

    return [
        file_path
        for file_path in test_files
        if keyword_lower in str(file_path).lower()
    ]


def summarize_discovery(test_files: List[Path]) -> dict:
    """
    Return summary of discovered test files.
    """

    folders = {}

    for file_path in test_files:
        folder_name = str(file_path.parent)
        folders[folder_name] = folders.get(folder_name, 0) + 1

    return {
        "total_test_files": len(test_files),
        "folders": folders,
        "files": [str(file_path) for file_path in test_files],
    }


if __name__ == "__main__":
    files = discover_test_files()
    print(summarize_discovery(files))