#!/usr/bin/env python3
"""
KnowledgeCraft repository-wide deterministic validation runner.

Runs:
1. Root skill-structure validation via validate_skills.py
2. Every deterministic Python test suite discovered under:
   .opencode/skills/*/scripts/test_*.py

The runner is intentionally discovery-based so new skill test suites are picked up
automatically without editing this file.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


@dataclass
class CommandResult:
    label: str
    command: list[str]
    cwd: Path
    returncode: int
    stdout: str
    stderr: str
    test_count: int | None = None


def repo_root_from_script() -> Path:
    # scripts/check_all.py -> repository root
    return Path(__file__).resolve().parent.parent


def run_command(
    label: str,
    command: Sequence[str],
    cwd: Path,
) -> CommandResult:
    proc = subprocess.run(
        list(command),
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=os.environ.copy(),
    )

    combined = "\n".join(part for part in (proc.stdout, proc.stderr) if part)
    test_count = parse_test_count(combined)

    return CommandResult(
        label=label,
        command=list(command),
        cwd=cwd,
        returncode=proc.returncode,
        stdout=proc.stdout,
        stderr=proc.stderr,
        test_count=test_count,
    )


def parse_test_count(output: str) -> int | None:
    """
    Count tests from common unittest / pytest summary formats.

    Preference:
    - unittest: "Ran 19 tests in ..."
    - pytest: "19 passed"
    """
    unittest_matches = re.findall(r"\bRan\s+(\d+)\s+tests?\b", output)
    if unittest_matches:
        return int(unittest_matches[-1])

    pytest_matches = re.findall(r"\b(\d+)\s+passed\b", output)
    if pytest_matches:
        return int(pytest_matches[-1])

    return None


def discover_skills(root: Path) -> list[Path]:
    skills_root = root / ".opencode" / "skills"
    if not skills_root.is_dir():
        return []

    return sorted(
        path.parent
        for path in skills_root.glob("*/SKILL.md")
        if path.is_file()
    )


def discover_test_suites(root: Path) -> list[Path]:
    skills_root = root / ".opencode" / "skills"
    if not skills_root.is_dir():
        return []

    return sorted(
        path
        for path in skills_root.glob("*/scripts/test_*.py")
        if path.is_file()
    )


def suite_label(root: Path, test_path: Path) -> str:
    try:
        rel = test_path.relative_to(root)
    except ValueError:
        rel = test_path
    return str(rel).replace("\\", "/")


def print_result_output(result: CommandResult) -> None:
    if result.stdout.strip():
        print(result.stdout.rstrip())
    if result.stderr.strip():
        print(result.stderr.rstrip())


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run all deterministic KnowledgeCraft repository checks."
    )
    parser.add_argument(
        "--verbose-output",
        action="store_true",
        help="Print stdout/stderr for passing suites as well as failures.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Repository root. Defaults to the parent directory of this script's folder.",
    )
    args = parser.parse_args()

    root = (args.root or repo_root_from_script()).resolve()

    print("KnowledgeCraft Repository Validation")
    print("=" * 36)
    print(f"Repository: {root}")
    print()

    validation_script = root / "validate_skills.py"
    skills_root = root / ".opencode" / "skills"

    preflight_errors: list[str] = []
    if not validation_script.is_file():
        preflight_errors.append(f"Missing root validator: {validation_script}")
    if not skills_root.is_dir():
        preflight_errors.append(f"Missing skills directory: {skills_root}")

    if preflight_errors:
        print("PREFLIGHT: FAIL")
        for error in preflight_errors:
            print(f"- {error}")
        print()
        print("KNOWLEDGECRAFT CHECK: FAIL")
        return 2

    skills = discover_skills(root)
    tests = discover_test_suites(root)

    print(f"Skills discovered:            {len(skills)}")
    print(f"Deterministic test suites:    {len(tests)}")
    print()

    # 1. Root skill-structure validator.
    root_validation = run_command(
        label="Skill structure",
        command=[sys.executable, str(validation_script)],
        cwd=root,
    )

    structure_ok = root_validation.returncode == 0
    print(f"Skill structure:              {'PASS' if structure_ok else 'FAIL'}")

    if args.verbose_output or not structure_ok:
        print_result_output(root_validation)
        print()

    # 2. All discovered deterministic skill test suites.
    suite_results: list[CommandResult] = []

    for test_path in tests:
        label = suite_label(root, test_path)
        result = run_command(
            label=label,
            command=[sys.executable, test_path.name],
            cwd=test_path.parent,
        )
        suite_results.append(result)

        status = "PASS" if result.returncode == 0 else "FAIL"
        count_text = (
            f" ({result.test_count} tests)"
            if result.test_count is not None
            else ""
        )
        print(f"[{status}] {label}{count_text}")

        if args.verbose_output or result.returncode != 0:
            print_result_output(result)
            print()

    failed_suites = [r for r in suite_results if r.returncode != 0]
    known_test_count = sum(
        r.test_count for r in suite_results if r.test_count is not None
    )
    unknown_count_suites = sum(
        1 for r in suite_results if r.test_count is None
    )

    overall_ok = structure_ok and not failed_suites

    print()
    print("Summary")
    print("-" * 36)
    print(f"Skills discovered:            {len(skills)}")
    print(f"Skill structure:              {'PASS' if structure_ok else 'FAIL'}")
    print(f"Deterministic test suites:    {len(suite_results)}")
    print(f"Tests counted:                {known_test_count}")

    if unknown_count_suites:
        print(
            "Suites without parsed count:  "
            f"{unknown_count_suites} "
            "(suite PASS/FAIL still enforced)"
        )

    print(f"Failed suites:                {len(failed_suites)}")

    if failed_suites:
        print()
        print("Failed:")
        for result in failed_suites:
            print(f"- {result.label}")

    print()
    print(f"KNOWLEDGECRAFT CHECK: {'PASS' if overall_ok else 'FAIL'}")

    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
