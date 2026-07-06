"""
Test Discovery Module
Scans the tests/ directory and collects all test files and test functions.
"""

import ast
from pathlib import Path


TESTS_ROOT = Path(__file__).resolve().parents[1]


def discover_test_files(root: Path | None = None) -> list[Path]:
    """
    Recursively find all test_*.py files under the tests/ directory.

    Args:
        root: Override root directory (defaults to tests/).

    Returns:
        Sorted list of Path objects for each discovered test file.
    """
    base = root or TESTS_ROOT
    return sorted(base.rglob("test_*.py"))


def discover_test_functions(filepath: Path) -> list[str]:
    """
    Parse a Python test file and return all function names starting with 'test_'.

    Args:
        filepath: Path to the test file.

    Returns:
        List of test function names found in the file.
    """
    try:
        source = filepath.read_text(encoding="utf-8")
        tree = ast.parse(source)
    except (SyntaxError, UnicodeDecodeError):
        return []

    return [
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")
    ]


def build_discovery_report(root: Path | None = None) -> dict[str, list[str]]:
    """
    Build a full map of {filepath → [test_function_names]}.

    Args:
        root: Override root directory.

    Returns:
        Dict mapping file path string → list of test function names.
    """
    report: dict[str, list[str]] = {}
    for filepath in discover_test_files(root):
        functions = discover_test_functions(filepath)
        report[str(filepath)] = functions
    return report


if __name__ == "__main__":
    report = build_discovery_report()
    total_tests = sum(len(v) for v in report.values())
    print(f"Discovered {len(report)} test files — {total_tests} test functions\n")
    for filepath, funcs in report.items():
        rel = Path(filepath).relative_to(TESTS_ROOT)
        print(f"  {rel}  ({len(funcs)} tests)")
