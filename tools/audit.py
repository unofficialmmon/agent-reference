#!/usr/bin/env python3
"""Deterministic static audit entry point for agent-reference.

The implementation remains in _audit_core.py; this entry point owns the current
required-file/deprecated-artifact policy so retired reference/runtime protocols
do not remain active through the preserved audit core.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Importing _audit_core would normally create tools/__pycache__/..., which the
# audit correctly treats as a generated artifact. Disable bytecode generation
# before importing the implementation so a normal audit run does not create its
# own failure condition.
sys.dont_write_bytecode = True

import _audit_core as core


ROOT = Path(__file__).resolve().parents[1]


def audit_required_files(audit: core.Audit) -> None:
    required = [
        "AGENTS.md",
        "README.md",
        "CHANGELOG.md",
        "LICENSE",
        "NOTICE",
        "catalog/SOURCES.md",
        "catalog/skills.lock.json",
        "global/AGENTS.md",
        "global/ENGINEERING.md",
        "global/MEMORY.md",
        "project/AGENTS.template.md",
        "prompts/README.md",
        "prompts/OPENCODE_PLUGIN_SETUP.md",
        "prompts/PROJECT_BOOTSTRAP.md",
        "prompts/PROJECT_REFRESH.md",
        "prompts/PROJECT_AUDIT.md",
        "prompts/CODEBASE_ONBOARD.md",
        "prompts/CHANGE_AUDIT.md",
        "templates/omo/ROUTING.md",
        "evaluation/README.md",
        "evaluation/agentrc.eval.jsonc",
        "tools/README.md",
        "tools/_audit_core.py",
        "tools/audit.py",
    ]
    for item in required:
        if not (ROOT / item).is_file():
            audit.error("REQUIRED_FILE", "Required repository file is missing.", item)

    deprecated = [
        (
            "global/HISTORY.md",
            "DEPRECATED_HISTORY",
            "Retired work-history artifact must not be active in agent-reference.",
        ),
        (
            ".opencode/history",
            "DEPRECATED_HISTORY",
            "Retired work-history artifact must not be active in agent-reference.",
        ),
        (
            ".opencode/memory",
            "DEPRECATED_SIMPLE_MEMORY",
            "Retired Simple Memory runtime state must not be active in agent-reference.",
        ),
    ]
    for item, code, message in deprecated:
        if (ROOT / item).exists():
            audit.error(code, message, item)

    license_dir = ROOT / "catalog/LICENSES"
    if not license_dir.is_dir() or not any(path.is_file() for path in license_dir.iterdir()):
        audit.error("LICENSE_MATERIAL", "catalog/LICENSES must contain preserved source license/evidence files.", license_dir)


def main() -> int:
    core.audit_required_files = audit_required_files
    return core.main()


if __name__ == "__main__":
    raise SystemExit(main())
