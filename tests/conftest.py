import sys
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

REPORT_DIR = ROOT_DIR / "tests" / "test_reports"
_report_files_initialized = set()


def pytest_sessionstart(session):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)


def _report_file_path(test_file_path: Path) -> Path:
    return REPORT_DIR / f"{test_file_path.stem}.txt"


def _append_report(test_file_path: Path, message: str) -> None:
    report_path = _report_file_path(test_file_path)
    with report_path.open("a", encoding="utf-8") as report_file:
        report_file.write(message)


def pytest_runtest_logreport(report):
    if report.when != "call":
        return

    file_path = Path(report.fspath).resolve()

    if file_path not in _report_files_initialized:
        _report_files_initialized.add(file_path)
        header = (
            f"{'=' * 80}\n"
            f"Test Report: {file_path.name}\n"
            f"Run started: {datetime.now().isoformat(sep=' ', timespec='seconds')}\n"
            f"{'=' * 80}\n"
        )
        _append_report(file_path, header)

    outcome = report.outcome.upper()
    duration = getattr(report, "duration", 0.0)
    reason = ""
    if report.skipped:
        reason = f"Reason: {report.longrepr}\n"
    elif report.failed:
        reason = f"Failure: {report.longrepr}\n"

    test_line = (
        f"Test: {report.nodeid}\n"
        f"Outcome: {outcome}\n"
        f"Duration: {duration:.3f}s\n"
    )
    _append_report(file_path, test_line)
    if reason:
        _append_report(file_path, reason)
    _append_report(file_path, "\n")
