"""
Test Reporter
Formats and writes human-readable test run reports to tests/test_reports/.
"""

from __future__ import annotations

import datetime
from pathlib import Path
from .execution_handler import ExecutionResult


REPORTS_DIR = Path(__file__).resolve().parents[1] / "test_reports"


def _header(title: str, width: int = 70) -> str:
    line = "=" * width
    return f"\n{line}\n  {title}\n{line}"


def format_result_block(result: ExecutionResult) -> str:
    """Format a single ExecutionResult into a readable text block."""
    status = "PASS ✓" if result.success else "FAIL ✗"
    name = Path(result.target).name
    lines = [
        f"\n  [{status}] {name}",
        f"    Passed : {result.passed}",
        f"    Failed : {result.failed}",
        f"    Errors : {result.errors}",
        f"    Skipped: {result.skipped}",
        f"    Duration: {result.duration_seconds:.2f}s",
    ]
    if result.error_lines:
        lines.append("    Failures:")
        for err in result.error_lines[:10]:  # cap at 10 lines
            lines.append(f"      ✗ {err}")
    return "\n".join(lines)


def build_summary_report(results: list[ExecutionResult]) -> str:
    """
    Build a complete summary report string from all ExecutionResults.

    Returns:
        Multi-line string ready to write to a .txt file.
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_files = len(results)
    total_passed = sum(r.passed for r in results)
    total_failed = sum(r.failed + r.errors for r in results)
    total_skipped = sum(r.skipped for r in results)
    total_tests = total_passed + total_failed + total_skipped
    files_ok = sum(1 for r in results if r.success)
    files_fail = total_files - files_ok
    total_duration = sum(r.duration_seconds for r in results)

    lines = [
        _header("MARKETING ATTRIBUTION DASHBOARD — TEST REPORT"),
        f"  Generated : {now}",
        f"  Test Files: {total_files}  (✓ {files_ok} passed, ✗ {files_fail} failed)",
        f"  Tests Run : {total_tests}  (✓ {total_passed} passed, ✗ {total_failed} failed, ⊘ {total_skipped} skipped)",
        f"  Duration  : {total_duration:.2f}s",
        "",
        _header("PER-FILE RESULTS"),
    ]

    for result in results:
        lines.append(format_result_block(result))

    if total_failed > 0:
        lines.append(_header("FAILED TEST DETAILS"))
        for result in results:
            if not result.success and result.output:
                lines.append(f"\n  --- {Path(result.target).name} ---")
                # Show last 40 lines of output (most relevant)
                tail = result.output.strip().splitlines()[-40:]
                lines.extend(f"  {ln}" for ln in tail)

    overall = "ALL TESTS PASSED ✓" if total_failed == 0 else f"{total_failed} TEST(S) FAILED ✗"
    lines.append(_header(overall))

    return "\n".join(lines) + "\n"


def write_report(
    results: list[ExecutionResult],
    filename: str = "test_all.txt",
) -> Path:
    """
    Write the summary report to tests/test_reports/<filename>.

    Args:
        results: List of ExecutionResult objects.
        filename: Output filename (default 'test_all.txt').

    Returns:
        Path to the written report file.
    """
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / filename
    content = build_summary_report(results)
    report_path.write_text(content, encoding="utf-8")
    print(f"\n[INFO] Report written → {report_path}")
    return report_path


def print_summary(results: list[ExecutionResult]) -> None:
    """Print a compact summary to stdout."""
    print(build_summary_report(results))


if __name__ == "__main__":
    # Demo with dummy data
    from .execution_handler import ExecutionResult

    dummy = [
        ExecutionResult("tests/analytics/test_roas.py", 0, passed=4, duration_seconds=0.3),
        ExecutionResult("tests/preprocessing/test_data_cleaner.py", 1, passed=2, failed=1, duration_seconds=0.5),
    ]
    print_summary(dummy)
