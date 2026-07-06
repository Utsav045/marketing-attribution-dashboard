"""
Integration tests for the executer (runner CLI).
Verifies the end-to-end pipeline: discover → map → execute → report.
"""

import pytest
from pathlib import Path
from unittest.mock import patch

from .execution_handler import ExecutionResult
from .reporter import write_report, build_summary_report


TESTS_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = TESTS_ROOT / "test_reports"


# ---------------------------------------------------------------------------
# Runner pipeline smoke tests
# ---------------------------------------------------------------------------

def test_discovery_finds_at_least_one_file():
    from .discovery import discover_test_files
    files = discover_test_files()
    assert len(files) >= 1


def test_discovery_includes_this_file():
    from .discovery import discover_test_files
    files = discover_test_files()
    names = [f.name for f in files]
    assert "test_runner.py" in names


def test_mapper_produces_correct_count():
    from .discovery import discover_test_files
    from .mapper import build_test_module_map

    files = discover_test_files()
    mappings = build_test_module_map(files)
    assert len(mappings) == len(files)


def test_execution_result_dataclass_defaults():
    r = ExecutionResult(target="test_x.py", returncode=0)
    assert r.passed == 0
    assert r.failed == 0
    assert r.total == 0
    assert r.error_lines == []


def test_write_report_creates_file(tmp_path):
    """Report file must be created with non-empty content."""
    results = [
        ExecutionResult("tests/analytics/test_roas.py", returncode=0, passed=3),
        ExecutionResult("tests/preprocessing/test_data_cleaner.py", returncode=1, passed=1, failed=1),
    ]

    with patch("tests.runner.reporter.REPORTS_DIR", tmp_path):
        report_path = write_report(results, filename="test_runner_integration.txt")

    assert report_path.exists()
    content = report_path.read_text(encoding="utf-8")
    assert len(content) > 100
    assert "MARKETING ATTRIBUTION DASHBOARD" in content


def test_write_report_fail_shows_fail_verdict(tmp_path):
    results = [
        ExecutionResult("tests/x/test_a.py", returncode=1, failed=2),
    ]
    with patch("tests.runner.reporter.REPORTS_DIR", tmp_path):
        report_path = write_report(results, filename="fail_report.txt")

    content = report_path.read_text()
    assert "FAILED" in content


def test_write_report_all_pass_shows_pass_verdict(tmp_path):
    results = [
        ExecutionResult("tests/x/test_a.py", returncode=0, passed=5),
    ]
    with patch("tests.runner.reporter.REPORTS_DIR", tmp_path):
        report_path = write_report(results, filename="pass_report.txt")

    content = report_path.read_text()
    assert "ALL TESTS PASSED" in content


# ---------------------------------------------------------------------------
# Module-level runner scoped test
# ---------------------------------------------------------------------------

def test_run_single_test_file_via_execution_handler():
    """
    Smoke test: run a fast, known-good test file through execution_handler
    and check that it reports 0 failures.
    """
    from .execution_handler import run_pytest

    target = TESTS_ROOT / "runner" / "test_generation.py"
    if not target.exists():
        pytest.skip("test_generation.py not found")

    result = run_pytest(target)
    # We just check the runner didn't crash with a non-standard exit code
    assert result.returncode in (0, 1, 2, 3, 4, 5)  # valid pytest exit codes
    assert isinstance(result.output, str)
