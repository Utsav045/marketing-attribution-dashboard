"""
Test Reporter Module

Purpose:
    Generate simple testing reports for the project.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict, List

from tests.runner.execution_handler import TestExecutionResult


def create_report_text(
    result: TestExecutionResult,
    discovered_files: List[Path] | None = None,
) -> str:
    """
    Create a markdown report from a pytest execution result.
    """

    status = "PASSED" if result.passed else "FAILED"

    discovered_files = discovered_files or []

    lines = [
        "# Automated Test Report",
        "",
        f"Generated At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Test Status",
        "",
        f"Overall Status: {status}",
        f"Return Code: {result.return_code}",
        "",
        "## Command Executed",
        "",
        "```bash",
        " ".join(result.command),
        "```",
        "",
        "## Discovered Test Files",
        "",
        f"Total Files: {len(discovered_files)}",
        "",
    ]

    for file_path in discovered_files:
        lines.append(f"- {file_path}")

    lines.extend(
        [
            "",
            "## Pytest Output",
            "",
            "```text",
            result.stdout.strip(),
            "```",
            "",
        ]
    )

    if result.stderr.strip():
        lines.extend(
            [
                "## Pytest Errors",
                "",
                "```text",
                result.stderr.strip(),
                "```",
                "",
            ]
        )

    return "\n".join(lines)


def save_report(
    report_text: str,
    output_path: str | Path = "docs/Testing_Reports.md",
) -> Path:
    """
    Save report text to a markdown file.
    """

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report_text, encoding="utf-8")

    return path


def create_summary_table(summary: Dict[str, object]) -> str:
    """
    Create markdown table from a summary dictionary.
    """

    lines = [
        "| Metric | Value |",
        "|---|---|",
    ]

    for key, value in summary.items():
        lines.append(f"| {key} | {value} |")

    return "\n".join(lines)


if __name__ == "__main__":
    print("Reporter module loaded successfully.")