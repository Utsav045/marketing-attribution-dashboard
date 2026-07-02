import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPORT_THRESHOLD = 80
ROOT_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = ROOT_DIR / "tests" / "test_reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)
PRECOMMIT_REPORT = REPORT_DIR / "precommit_report.txt"

report_lines: list[str] = []


def append_line(line: str = "") -> None:
    report_lines.append(line)


def append_report(message: str) -> None:
    for line in message.rstrip().splitlines():
        append_line(line)
    if message.endswith("\n"):
        append_line()


def run_command(command, cwd=None):
    result = subprocess.run(
        command,
        cwd=cwd or ROOT_DIR,
        shell=False,
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def format_timestamp(ts: datetime) -> str:
    return ts.strftime("%d-%m-%Y %I:%M %p")


def parse_pytest_counts(text: str) -> tuple[int, int, int]:
    passed_match = re.search(r"(?<!x)(\d+)\s+passed", text)
    failed_match = re.search(r"(?<!x)(\d+)\s+failed", text)
    passed = int(passed_match.group(1)) if passed_match else 0
    failed = int(failed_match.group(1)) if failed_match else 0
    total = passed + failed
    if total == 0:
        collected_match = re.search(r"collected\s+(\d+)\s+items", text)
        if collected_match:
            total = int(collected_match.group(1))
    return total, passed, failed


def short_text(text: str, max_lines: int = 3) -> str:
    lines = [line for line in text.splitlines() if line.strip()]
    return " ".join(lines[:max_lines]) if lines else "No details available."


def section_header(title: str) -> None:
    append_line("=" * 60)
    append_line(f"  {title}")
    append_line("-" * 60)


def run_compile() -> tuple[bool, str]:
    code, out, err = run_command([sys.executable, "-m", "compileall", "-q", "src"])
    details = out or err or "Compilation completed."
    return code == 0, details


def run_black_check() -> tuple[bool, str]:
    code, out, err = run_command(
        [
            sys.executable,
            "-m",
            "black",
            "--check",
            "--target-version",
            "py312",
            "src",
            "tests",
            "scripts",
        ]
    )
    details = out or err or "Black formatting check completed."
    return code == 0, details


def run_lint() -> tuple[bool, str]:
    code, out, err = run_command(
        [sys.executable, "-m", "ruff", "check", "src", "tests", "scripts"]
    )
    details = out or err or "Ruff lint check completed."
    return code == 0, details


def run_tests() -> tuple[bool, dict[str, object]]:
    code, out, err = run_command([sys.executable, "-m", "pytest", "-q"])
    combined = "\n".join([out, err]).strip()
    total, passed, failed = parse_pytest_counts(combined)
    if total == 0 and code == 0:
        total = passed = 1
    return code == 0, {
        "details": combined or "Pytest run completed.",
        "total": total,
        "passed": passed,
        "failed": failed,
    }


def parse_coverage_percentage(output: str) -> float | None:
    match = re.search(r"TOTAL\s+\d+\s+\d+\s+(\d+(?:\.\d+)?)%", output)
    if match:
        return float(match.group(1))
    return None


def run_coverage() -> tuple[bool, float | None, str]:
    code, out, err = run_command(
        [
            sys.executable,
            "-m",
            "pytest",
            "--cov=src",
            "--cov-report=term-missing",
            "-q",
        ]
    )
    details = out or err or "Coverage check completed."
    coverage_percent = parse_coverage_percentage(details)
    if coverage_percent is None:
        return False, None, details
    success = coverage_percent >= REPORT_THRESHOLD
    return success, coverage_percent, details


def security_scan() -> tuple[str, str]:
    try:
        code, out, err = run_command(
            [sys.executable, "-m", "bandit", "-r", "src", "-n", "5"]
        )
        details = out or err or "Security scan completed."
        status = "PASS" if code == 0 else "WARN"
        return status, details
    except FileNotFoundError:
        return (
            "WARN",
            "Bandit not installed. Install it in the venv to enable security scanning.",
        )


def render_summary(
    start: datetime,
    duration_seconds: float,
    results: dict[str, str],
    test_data: dict[str, object],
    lint_details: str,
    security_details: str,
    coverage_status: str,
    coverage_percent: float | None,
    quality_score: float,
) -> None:
    append_line("=" * 60)
    append_line("  PRE-COMMIT QUALITY REPORT")
    append_line("=" * 60)
    append_line("")
    append_line(f"  Date            : {format_timestamp(start)}")
    append_line(f"  Execution Time  : {int(duration_seconds)}s")
    append_line("")
    append_line("  -- Check Results ----------------------------------------")
    for name in ["Compile", "Lint", "Tests", "Coverage", "Security"]:
        status = results[name]
        if name == "Coverage" and coverage_percent is not None:
            status = f"{status} ({coverage_percent:.1f}%)"
        append_line(f"  {name:15}: [{status}]")
    append_line("")
    passed_checks = [name for name, status in results.items() if status == "PASS"]
    failed_checks = [
        name for name, status in results.items() if status not in ("PASS", "N/A")
    ]
    append_line("  -- Test Summary -----------------------------------------")
    append_line(
        f"  Passed Checks   : {', '.join(passed_checks) if passed_checks else 'None'}"
    )
    append_line(
        f"  Failed Checks   : {', '.join(failed_checks) if failed_checks else 'None'}"
    )
    append_line(
        f"  Tests Run       : {test_data['total']}  |  Passed: {test_data['passed']}  |  Failed: {test_data['failed']}"
    )
    append_line("")
    append_line("  -- Score ------------------------------------------------")
    append_line(f"  Quality Score   : {quality_score:.1f} / 100")
    append_line(f"  Threshold       : {REPORT_THRESHOLD} / 100")
    overall_status = "PASS" if quality_score >= REPORT_THRESHOLD else "FAIL"
    append_line(f"  Overall Status  : {overall_status}")
    append_line("")
    append_line("  +-- Failure Details -----------------------------------+")
    if "Lint" in failed_checks:
        append_line("  [X] LINT FAILED")
        append_line(f"      {short_text(lint_details, max_lines=3)}")
        append_line("")
    if "Tests" in failed_checks:
        append_line("  [X] TESTS FAILED")
        append_line(f"      Passed : {test_data['passed']} / {test_data['total']}")
        append_line(f"      Failed : {test_data['failed']} / {test_data['total']}")
        append_line("")
    if security_details and results["Security"] == "WARN":
        warnings = sum(
            1 for line in security_details.splitlines() if line.strip().startswith("-")
        )
        warnings = warnings or 1
        append_line(f"  [!] SECURITY WARNINGS ({warnings} issue(s))")
        for line in security_details.splitlines():
            if line.strip():
                append_line(f"      {line}")
        append_line("")
    if not failed_checks:
        append_line("  [OK] No blocking failures detected.")
        append_line("")
    append_line("  +-----------------------------------------------------+")
    append_line("")
    append_line("  -- Verdict ----------------------------------------------")
    if overall_status == "PASS":
        append_line("  [OK]  YOU ARE ALLOWED TO COMMIT")
    else:
        append_line("  [FAIL]  YOU ARE NOT ALLOWED TO COMMIT")


def main() -> int:
    start = datetime.now()

    compile_success, compile_details = run_compile()
    lint_success, lint_details = run_lint()
    tests_success, test_data = run_tests()
    if tests_success:
        coverage_success, coverage_percent, coverage_details = run_coverage()
        coverage_status = "PASS" if coverage_success else "FAIL"
    else:
        coverage_success = False
        coverage_percent = None
        coverage_status = "N/A"
    security_status, security_details = security_scan()

    tests_score = 40 if tests_success else 0
    lint_score = 20 if lint_success else 0
    security_score = 15 if security_status == "PASS" else 0
    coverage_score = 0.0
    if coverage_percent is not None:
        coverage_score = min(coverage_percent, REPORT_THRESHOLD) / REPORT_THRESHOLD * 25
    quality_score = tests_score + lint_score + security_score + coverage_score

    results = {
        "Compile": "PASS" if compile_success else "FAIL",
        "Lint": "PASS" if lint_success else "FAIL",
        "Tests": "PASS" if tests_success else "FAIL",
        "Coverage": coverage_status,
        "Security": security_status,
    }

    render_summary(
        start,
        (datetime.now() - start).total_seconds(),
        results,
        test_data,
        lint_details,
        security_details,
        coverage_status,
        coverage_percent,
        quality_score,
    )
    with PRECOMMIT_REPORT.open("a", encoding="utf-8") as report_file:
        report_file.write("\n".join(report_lines) + "\n")

    commit_allowed = compile_success and quality_score >= REPORT_THRESHOLD
    return 0 if commit_allowed else 1


if __name__ == "__main__":
    sys.exit(main())
