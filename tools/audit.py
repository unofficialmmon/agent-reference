#!/usr/bin/env python3
"""Deterministic static audit entry point for agent-reference.

The implementation remains in _audit_core.py; this entry point owns current
required/deprecated artifact policy plus APM packaging mirror checks.
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


def _audit_prompt_mirror(audit: core.Audit, source: str, packaged: str) -> None:
    source_path = ROOT / source
    packaged_path = ROOT / packaged
    if not source_path.is_file() or not packaged_path.is_file():
        return
    if core.sha256(source_path) != core.sha256(packaged_path):
        audit.error(
            "APM_PROMPT_DRIFT",
            f"APM prompt mirror must be byte-identical to {source}.",
            packaged_path,
        )


def _audit_apm_skill_mirrors(audit: core.Audit) -> None:
    mirror_root = ROOT / ".apm/skills"
    try:
        canonical = core.find_skill_dirs()
    except RuntimeError as exc:
        audit.error("APM_SKILL_SOURCE", str(exc), ROOT / "skills")
        canonical = {}

    operational = {
        name for name, directory in canonical.items() if directory.parent.name == "operational"
    }
    expected = set(canonical) - operational

    if not mirror_root.is_dir():
        audit.error(
            "APM_SKILL_ROOT",
            "APM producer Skill root .apm/skills is missing.",
            mirror_root,
        )
        audit.metrics["apmDeployableSkills"] = 0
        audit.metrics["apmExpectedDeployableSkills"] = len(expected)
        audit.metrics["apmExcludedOperationalSkills"] = len(operational)
        return

    published: dict[str, Path] = {}
    for child in sorted(mirror_root.iterdir()):
        if child.is_symlink():
            audit.error(
                "APM_SKILL_SYMLINK",
                "APM Skill mirrors must be real packaged directories, not symlinks.",
                child,
            )
            continue
        if not child.is_dir():
            audit.error(
                "APM_SKILL_ENTRY",
                "Only Skill directories are allowed directly under .apm/skills.",
                child,
            )
            continue
        if not (child / "SKILL.md").is_file():
            audit.error(
                "APM_SKILL_ENTRY",
                "APM Skill directory must contain SKILL.md.",
                child,
            )
            continue
        published[child.name] = child

    published_ids = set(published)
    for name in sorted(expected - published_ids):
        audit.error(
            "APM_SKILL_MISSING",
            f"Non-operational catalog Skill '{name}' is not exposed as an APM primitive.",
            canonical[name],
        )
    for name in sorted(published_ids & operational):
        audit.error(
            "APM_SKILL_OPERATIONAL",
            f"Operational Skill '{name}' must remain catalog-only and must not be exposed through .apm/skills.",
            published[name],
        )
    for name in sorted(published_ids - set(canonical)):
        audit.error(
            "APM_SKILL_UNKNOWN",
            f"APM exposes unknown Skill '{name}' that has no canonical catalog source.",
            published[name],
        )

    for name in sorted(expected & published_ids):
        source = canonical[name]
        mirror = published[name]
        for path in mirror.rglob("*"):
            if path.is_symlink():
                audit.error(
                    "APM_SKILL_SYMLINK",
                    f"APM Skill '{name}' contains a symlink; mirrors must preserve real files.",
                    path,
                )

        source_files = core.relative_file_set(source)
        mirror_files = core.relative_file_set(mirror)
        for rel in sorted(source_files - mirror_files):
            audit.error(
                "APM_SKILL_MIRROR_MISSING",
                f"APM mirror for '{name}' is missing canonical file '{rel}'.",
                mirror / rel,
            )
        for rel in sorted(mirror_files - source_files):
            audit.error(
                "APM_SKILL_MIRROR_EXTRA",
                f"APM mirror for '{name}' contains non-canonical file '{rel}'.",
                mirror / rel,
            )
        for rel in sorted(source_files & mirror_files):
            if core.sha256(source / rel) != core.sha256(mirror / rel):
                audit.error(
                    "APM_SKILL_DRIFT",
                    f"APM mirror for '{name}' drifted from canonical source file '{rel}'.",
                    mirror / rel,
                )

    audit.metrics["apmDeployableSkills"] = len(published_ids)
    audit.metrics["apmExpectedDeployableSkills"] = len(expected)
    audit.metrics["apmExcludedOperationalSkills"] = len(operational)


def audit_required_files(audit: core.Audit) -> None:
    required = [
        "AGENTS.md",
        "README.md",
        "CHANGELOG.md",
        "LICENSE",
        "NOTICE",
        "apm.yml",
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
        "prompts/APM_SETUP.md",
        "prompts/AGENT_SYNC.md",
        ".apm/prompts/apm-setup.prompt.md",
        ".apm/prompts/agent-sync.prompt.md",
        ".apm/prompts/test-setup.prompt.md",
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
        audit.error(
            "LICENSE_MATERIAL",
            "catalog/LICENSES must contain preserved source license/evidence files.",
            license_dir,
        )

    _audit_prompt_mirror(audit, "prompts/APM_SETUP.md", ".apm/prompts/apm-setup.prompt.md")
    _audit_prompt_mirror(audit, "prompts/AGENT_SYNC.md", ".apm/prompts/agent-sync.prompt.md")
    _audit_apm_skill_mirrors(audit)


def main() -> int:
    core.audit_required_files = audit_required_files
    return core.main()


if __name__ == "__main__":
    raise SystemExit(main())
