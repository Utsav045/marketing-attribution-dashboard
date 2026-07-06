"""
Test-to-Source Mapper
Maps each test file/folder to its corresponding source module.
"""

from pathlib import Path


# Mapping: test sub-folder name → source module path
MODULE_MAP: dict[str, str] = {
    "analytics":    "src.analytics",
    "attribution":  "src.attribution",
    "preprocessing":"src.preprocessing",
    "ingestion":    "src.ingestion",
    "pipeline":     "src.pipeline",
    "database":     "src.database",
    "utils":        "src.utils",
    "visualization":"src.visualization",
    "runner":       "tests.runner",
    "sql_validation":"sql",
}

TESTS_ROOT = Path(__file__).resolve().parents[1]


def get_module_for_test_file(filepath: Path | str) -> str:
    """
    Given a test file path, return the corresponding source module string.

    Args:
        filepath: Path to a test file.

    Returns:
        Dotted module string (e.g. 'src.analytics') or 'unknown'.
    """
    filepath = Path(filepath)
    # Check if the parent folder name matches any key in MODULE_MAP
    parent_name = filepath.parent.name
    return MODULE_MAP.get(parent_name, "unknown")


def build_test_module_map(test_files: list[Path]) -> list[dict[str, str]]:
    """
    Build a list of mappings: {test_file, source_module}.

    Args:
        test_files: List of test file paths.

    Returns:
        List of dicts with 'test_file' and 'source_module' keys.
    """
    return [
        {
            "test_file": str(fp.relative_to(TESTS_ROOT)),
            "source_module": get_module_for_test_file(fp),
        }
        for fp in test_files
    ]


def print_module_map(mappings: list[dict[str, str]]) -> None:
    """Pretty-print the test → source module mapping table."""
    print(f"\n{'Test File':<55} {'Source Module'}")
    print("-" * 80)
    for m in mappings:
        print(f"  {m['test_file']:<53} {m['source_module']}")


if __name__ == "__main__":
    from discovery import discover_test_files

    files = discover_test_files()
    mappings = build_test_module_map(files)
    print_module_map(mappings)
    print(f"\nTotal: {len(mappings)} test files mapped.")
