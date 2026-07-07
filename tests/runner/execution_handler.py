"""
Test Execution Handler

Purpose:
    Execute pytest commands and collect results.
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class TestExecutionResult:
    """Container for test execution result."""

    command: List[str]
    return_code: int
    stdout: str
    stderr: str
    passed: bool


def run_pytest(
    test_path: str | Path = "tests",
    extra_args: Optional[List[str]] = None,
) -> TestExecutionResult:
    """
    Run pytest on a test path.

    Args:
        test_path: File or folder to test.
        extra_args: Extra pytest arguments.

    Returns:
        TestExecutionResult.
    """

    command = [sys.executable, "-m", "pytest", str(test_path)]

    if extra_args:
        command.extend(extra_args)

    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )

    return TestExecutionResult(
        command=command,
        return_code=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
        passed=completed.returncode == 0,
    )


def run_pytest_quiet(test_path: str | Path = "tests") -> TestExecutionResult:
    """
    Run pytest in quiet mode.
    """

    return run_pytest(test_path=test_path, extra_args=["-q"])


def run_pytest_verbose(test_path: str | Path = "tests") -> TestExecutionResult:
    """
    Run pytest in verbose mode.
    """

    return run_pytest(test_path=test_path, extra_args=["-v"])


def print_execution_result(result: TestExecutionResult) -> None:
    """
    Print result to terminal.
    """

    print("Command:")
    print(" ".join(result.command))
    print()

    print("Passed:")
    print(result.passed)
    print()

    print("Return code:")
    print(result.return_code)
    print()

    print("Output:")
    print(result.stdout)

    if result.stderr:
        print("Errors:")
        print(result.stderr)


if __name__ == "__main__":
    output = run_pytest_quiet("tests")
    print_execution_result(output)