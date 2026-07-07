"""
Execution Handler
Runs pytest programmatically for a given set of test paths
and captures structured results.
"""

import subprocess
import sys
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class ExecutionResult:
    """Result of a single pytest run."""
    target: str
    returncode: int
    passed: int = 0
    failed: int = 0
    errors: int = 0
    skipped: int = 0
    duration_seconds: float = 0.0
    output: str = ""
    error_lines: list[str] = field(default_factory=list)

    @property
    def success(self) -> bool:
        return self.returncode == 0

    @property
    def total(self) -> int:
        return self.passed + self.failed + self.errors + self.skipped


def run_pytest(
    target: str | Path,
    extra_args: list[str] | None = None,
    capture_output: bool = True,
) -> ExecutionResult:
    """
    Execute pytest on the given target path.

    Args:
        target: File or directory path to run pytest against.
        extra_args: Additional pytest CLI args (e.g. ['-v', '--tb=short']).
        capture_output: If True, capture stdout/stderr.

    Returns:
        ExecutionResult with parsed pass/fail counts.
    """
    target = str(target)
    cmd = [sys.executable, "-m", "pytest", target, "--tb=short", "-q"]
    if extra_args:
        cmd.extend(extra_args)

    proc = subprocess.run(
        cmd,
        capture_output=capture_output,
        text=True,
    )

    output = (proc.stdout or "") + (proc.stderr or "")
    result = ExecutionResult(
        target=target,
        returncode=proc.returncode,
        output=output,
    )

    # Parse summary line e.g. "3 passed, 1 failed in 0.45s"
    for line in output.splitlines():
        line_lower = line.lower()
        if "passed" in line_lower or "failed" in line_lower or "error" in line_lower:
            result.passed  = _parse_count(line, "passed")
            result.failed  = _parse_count(line, "failed")
            result.errors  = _parse_count(line, "error")
            result.skipped = _parse_count(line, "skipped")
            result.duration_seconds = _parse_duration(line)

        if "FAILED" in line or "ERROR" in line:
            result.error_lines.append(line.strip())

    return result


def run_pytest_for_modules(
    test_files: list[Path],
) -> list[ExecutionResult]:
    """
    Run pytest individually for each test file.

    Args:
        test_files: List of test file paths.

    Returns:
        List of ExecutionResult objects.
    """
    results = []
    for fp in test_files:
        print(f"  Running: {fp.name} ...", end=" ", flush=True)
        result = run_pytest(fp)
        status = "✓ PASS" if result.success else "✗ FAIL"
        print(status)
        results.append(result)
    return results


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _parse_count(line: str, keyword: str) -> int:
    """Extract integer count before a keyword in a pytest summary line."""
    import re
    match = re.search(rf"(\d+)\s+{keyword}", line, re.IGNORECASE)
    return int(match.group(1)) if match else 0


def _parse_duration(line: str) -> float:
    """Extract duration in seconds from a pytest summary line."""
    import re
    match = re.search(r"in\s+([\d.]+)s", line, re.IGNORECASE)
    return float(match.group(1)) if match else 0.0


if __name__ == "__main__":
    from discovery import discover_test_files

    print("Running all tests...\n")
    files = discover_test_files()
    results = run_pytest_for_modules(files)

    total_pass = sum(r.passed for r in results)
    total_fail = sum(r.failed + r.errors for r in results)
    print(f"\nSummary: {total_pass} passed, {total_fail} failed across {len(files)} files.")
