"""
Test Executer (Main Entry Point)
Orchestrates discovery → mapping → execution → reporting
for the full test suite.

Usage:
    python -m tests.runner.executer
    python -m tests.runner.executer --module analytics
    python -m tests.runner.executer --file tests/attribution/test_first_touch.py
"""

import argparse
import sys
from pathlib import Path

from .discovery import discover_test_files, build_discovery_report
from .mapper import build_test_module_map, print_module_map
from .execution_handler import run_pytest_for_modules
from .reporter import write_report, print_summary


TESTS_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Marketing Attribution Dashboard — Custom Test Runner"
    )
    parser.add_argument(
        "--module",
        type=str,
        default=None,
        help="Run tests only for a specific module folder (e.g. analytics, attribution).",
    )
    parser.add_argument(
        "--file",
        type=str,
        default=None,
        help="Run a single test file.",
    )
    parser.add_argument(
        "--discover",
        action="store_true",
        help="Only discover and print test files — do not run.",
    )
    parser.add_argument(
        "--report",
        type=str,
        default="test_all.txt",
        help="Output report filename (default: test_all.txt).",
    )
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Skip writing the report file.",
    )
    return parser.parse_args()


def main() -> int:
    """
    Main execution flow:
    1. Parse CLI arguments
    2. Discover test files
    3. Map files to source modules
    4. Execute tests
    5. Report results

    Returns:
        Exit code: 0 = all pass, 1 = failures exist.
    """
    args = parse_args()

    print("=" * 70)
    print("  MARKETING ATTRIBUTION DASHBOARD — TEST RUNNER")
    print("=" * 70)

    # ------------------------------------------------------------------ #
    # DISCOVER
    # ------------------------------------------------------------------ #
    if args.file:
        test_files = [Path(args.file)]
    elif args.module:
        module_dir = TESTS_ROOT / args.module
        if not module_dir.exists():
            print(f"[ERROR] Module folder not found: {module_dir}")
            return 1
        test_files = list(module_dir.rglob("test_*.py"))
    else:
        test_files = discover_test_files()

    print(f"\n[DISCOVERY] Found {len(test_files)} test file(s)")

    if args.discover:
        report = build_discovery_report()
        total = sum(len(v) for v in report.values())
        print(f"  Total test functions: {total}\n")
        for fp, funcs in report.items():
            rel = Path(fp).relative_to(TESTS_ROOT)
            print(f"  {rel}  ({len(funcs)} tests)")
        return 0

    # ------------------------------------------------------------------ #
    # MAP
    # ------------------------------------------------------------------ #
    mappings = build_test_module_map(test_files)
    print_module_map(mappings)

    # ------------------------------------------------------------------ #
    # EXECUTE
    # ------------------------------------------------------------------ #
    print("\n[EXECUTION] Running tests...\n")
    results = run_pytest_for_modules(test_files)

    # ------------------------------------------------------------------ #
    # REPORT
    # ------------------------------------------------------------------ #
    print_summary(results)

    if not args.no_report:
        write_report(results, filename=args.report)

    total_failed = sum(r.failed + r.errors for r in results)
    return 1 if total_failed > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
