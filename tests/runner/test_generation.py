"""
Tests for the runner sub-system itself.
Verifies discovery, mapping, and reporting work correctly.
"""

import pytest
from pathlib import Path

from .discovery import (
    discover_test_files,
    discover_test_functions,
    build_discovery_report,
)
from .mapper import (
    get_module_for_test_file,
    build_test_module_map,
)
from .reporter import build_summary_report, format_result_block
from .execution_handler import ExecutionResult


TESTS_ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------------
# Discovery tests
# ---------------------------------------------------------------------------

def test_discover_test_files_returns_list():
    files = discover_test_files()
    assert isinstance(files, list)
    assert len(files) > 0


def test_all_discovered_files_are_python():
    files = discover_test_files()
    assert all(f.suffix == ".py" for f in files)


def test_all_discovered_filenames_start_with_test():
    files = discover_test_files()
    assert all(f.name.startswith("test_") for f in files)


def test_discover_test_functions_from_this_file():
    this_file = Path(__file__)
    funcs = discover_test_functions(this_file)
    assert "test_discover_test_files_returns_list" in funcs


def test_discover_test_functions_empty_on_nontest_file(tmp_path):
    f = tmp_path / "not_a_test.py"
    f.write_text("def helper(): pass\n")
    funcs = discover_test_functions(f)
    assert funcs == []


def test_build_discovery_report_returns_dict():
    report = build_discovery_report()
    assert isinstance(report, dict)
    assert len(report) > 0


# ---------------------------------------------------------------------------
# Mapper tests
# ---------------------------------------------------------------------------

def test_get_module_for_analytics_test():
    fp = TESTS_ROOT / "analytics" / "test_roas.py"
    assert get_module_for_test_file(fp) == "src.analytics"


def test_get_module_for_attribution_test():
    fp = TESTS_ROOT / "attribution" / "test_first_touch.py"
    assert get_module_for_test_file(fp) == "src.attribution"


def test_get_module_unknown_folder():
    fp = Path("some_unknown_folder") / "test_something.py"
    assert get_module_for_test_file(fp) == "unknown"


def test_build_test_module_map_structure():
    files = [
        TESTS_ROOT / "analytics" / "test_roas.py",
        TESTS_ROOT / "preprocessing" / "test_data_cleaner.py",
    ]
    mappings = build_test_module_map(files)
    assert len(mappings) == 2
    assert all("test_file" in m and "source_module" in m for m in mappings)


# ---------------------------------------------------------------------------
# Reporter tests
# ---------------------------------------------------------------------------

def _make_result(name, returncode=0, passed=3, failed=0):
    return ExecutionResult(
        target=f"tests/analytics/{name}",
        returncode=returncode,
        passed=passed,
        failed=failed,
    )


def test_format_result_block_pass():
    result = _make_result("test_roas.py", returncode=0, passed=4)
    block = format_result_block(result)
    assert "PASS" in block
    assert "4" in block


def test_format_result_block_fail():
    result = _make_result("test_roi.py", returncode=1, passed=2, failed=1)
    block = format_result_block(result)
    assert "FAIL" in block


def test_build_summary_report_contains_totals():
    results = [
        _make_result("test_roas.py", 0, passed=3),
        _make_result("test_roi.py", 1, passed=1, failed=2),
    ]
    report = build_summary_report(results)
    assert "4" in report   # total passed
    assert "2" in report   # total failed
    assert "FAIL" in report


def test_build_summary_report_all_pass():
    results = [_make_result("test_roas.py", 0, passed=5)]
    report = build_summary_report(results)
    assert "ALL TESTS PASSED" in report


# ---------------------------------------------------------------------------
# ExecutionResult tests
# ---------------------------------------------------------------------------

def test_execution_result_success_true_when_returncode_0():
    r = ExecutionResult(target="x.py", returncode=0, passed=2)
    assert r.success is True


def test_execution_result_success_false_when_returncode_1():
    r = ExecutionResult(target="x.py", returncode=1, failed=1)
    assert r.success is False


def test_execution_result_total():
    r = ExecutionResult(target="x.py", returncode=0, passed=3, failed=1, skipped=1)
    assert r.total == 5
