#!/usr/bin/env python3
"""Validate the Jira Assistant Claude Code plugin package structure."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    ".claude-plugin/plugin.json",
    "README.md",
    "skills/issue-investigator/SKILL.md",
    "skills/issue-investigator/references/"
    "jira-context-gathering.md",
    "skills/issue-investigator/references/"
    "repository-discovery.md",
    "skills/issue-investigator/references/"
    "dynamic-layer-investigation.md",
    "skills/issue-investigator/references/"
    "root-cause-verification.md",
    "skills/issue-investigator/references/"
    "solution-tradeoff-analysis.md",
    "skills/issue-investigator/references/"
    "testing-and-rollout.md",
    "skills/issue-investigator/references/"
    "investigation-report.md",
    "skills/issue-investigator/references/"
    "database-investigation.md",
    "skills/issue-investigator/references/"
    "observability-investigation.md",
    "tests/README.md",
    "tests/test-cases.md",
    "tests/expected-findings.md",
    "tests/validate_plugin.py",
]

REQUIRED_REFERENCES = [
    "jira-context-gathering.md",
    "repository-discovery.md",
    "dynamic-layer-investigation.md",
    "root-cause-verification.md",
    "solution-tradeoff-analysis.md",
    "testing-and-rollout.md",
    "investigation-report.md",
    "database-investigation.md",
    "observability-investigation.md",
]

REQUIRED_SKILL_SECTIONS = [
    "Phase 1: Resolve the Jira issue",
    "Phase 2: Understand impact and expected behavior",
    "Phase 3: Discover the repository",
    "Phase 4: Build and investigate hypotheses",
    "Phase 5: Dynamically investigate relevant layers",
    "Phase 6: Verify the root cause",
    "Phase 7: Design the solution",
    "Phase 8: Define validation and rollout",
]

ERRORS = []


def check(condition, message):
    if not condition:
        ERRORS.append(message)


def main():
    for relative_path in REQUIRED_FILES:
        check(
            (ROOT / relative_path).is_file(),
            f"Missing required file: {relative_path}",
        )

    manifest_path = ROOT / ".claude-plugin/plugin.json"

    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            check(
                isinstance(manifest, dict),
                "plugin.json must contain a JSON object",
            )

            if isinstance(manifest, dict):
                check(
                    manifest.get("name") == "jira-assistant-plugin",
                    "plugin.json name must be jira-assistant-plugin",
                )
                check(
                    isinstance(manifest.get("version"), str)
                    and bool(manifest["version"].strip()),
                    "plugin.json needs a non-empty version",
                )
                check(
                    isinstance(manifest.get("description"), str)
                    and bool(manifest["description"].strip()),
                    "plugin.json needs a non-empty description",
                )
        except (json.JSONDecodeError, OSError) as exc:
            ERRORS.append(f"Invalid plugin.json: {exc}")

    skill_path = (
        ROOT
        / "skills/issue-investigator/SKILL.md"
    )

    if skill_path.is_file():
        skill = skill_path.read_text(encoding="utf-8")

        check(
            skill.startswith("---\n"),
            "SKILL.md must start with YAML frontmatter",
        )

        frontmatter_match = re.match(
            r"\A---\n(.*?)\n---(?:\n|\Z)",
            skill,
            flags=re.DOTALL,
        )

        check(
            frontmatter_match is not None,
            "SKILL.md has missing or malformed frontmatter",
        )

        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)

            check(
                re.search(
                    r"(?m)^name:\s*issue-investigator\s*$",
                    frontmatter,
                ) is not None,
                "SKILL.md has an incorrect or missing skill name",
            )

            check(
                re.search(
                    r"(?m)^description:\s*\S.*$",
                    frontmatter,
                ) is not None,
                "SKILL.md needs a non-empty description",
            )

        for section in REQUIRED_SKILL_SECTIONS:
            check(
                section in skill,
                f"SKILL.md is missing section: {section}",
            )

        references_dir = skill_path.parent / "references"

        for reference in REQUIRED_REFERENCES:
            reference_path = references_dir / reference

            check(
                reference_path.is_file(),
                f"Missing reference: {reference}",
            )

            if reference_path.is_file():
                content = reference_path.read_text(encoding="utf-8")
                check(
                    bool(content.strip()),
                    f"Reference file is empty: {reference}",
                )

    if ERRORS:
        print("VALIDATION FAILED")
        for error in ERRORS:
            print(f"- {error}")
        return 1

    print("VALIDATION PASSED")
    print(f"Checked {len(REQUIRED_FILES)} required files.")
    print("Plugin manifest, skill metadata and reference files are present.")
    print("Note: this does not validate live Jira MCP connectivity.")
    return 0


if __name__ == "__main__":
    sys.exit(main())