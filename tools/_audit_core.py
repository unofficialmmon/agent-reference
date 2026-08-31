#!/usr/bin/env python3
"""Deterministic static audit for agent-reference.

This script intentionally validates repository structure and metadata only. It does
not claim that OpenCode, OMO Slim, Spec Kit, a model, or any Skill behaves correctly
at runtime.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
RECOGNIZED_SKILL_FIELDS = {"name", "description", "license", "compatibility", "metadata"}
OMO_BUILTIN_SKILLS = {
    "simplify",
    "codemap",
    "clonedeps",
    "deepwork",
    "verification-planning",
    "reflect",
    "worktrees",
    "oh-my-opencode-slim",
}
OMO_BUILTIN_AGENTS = {
    "orchestrator",
    "oracle",
    "librarian",
    "explorer",
    "designer",
    "fixer",
    "observer",
    "council",
}


@dataclass(frozen=True)
class Finding:
    level: str
    code: str
    message: str
    path: str | None = None


class Audit:
    def __init__(self) -> None:
        self.findings: list[Finding] = []
        self.metrics: dict[str, Any] = {}

    def add(self, level: str, code: str, message: str, path: Path | str | None = None) -> None:
        if isinstance(path, Path):
            try:
                path_text = path.relative_to(ROOT).as_posix()
            except ValueError:
                path_text = str(path)
        else:
            path_text = path
        self.findings.append(Finding(level, code, message, path_text))

    def error(self, code: str, message: str, path: Path | str | None = None) -> None:
        self.add("ERROR", code, message, path)

    def warn(self, code: str, message: str, path: Path | str | None = None) -> None:
        self.add("WARN", code, message, path)

    def info(self, code: str, message: str, path: Path | str | None = None) -> None:
        self.add("INFO", code, message, path)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def scalar(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    if value[0:1] in {"'", '"'} and value[-1:] == value[0:1]:
        try:
            parsed = ast.literal_eval(value)
            return str(parsed)
        except (ValueError, SyntaxError):
            return value[1:-1]
    return value


def parse_frontmatter(path: Path, audit: Audit) -> dict[str, Any] | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        audit.error("SKILL_FRONTMATTER", "SKILL.md must begin with YAML frontmatter.", path)
        return None
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        audit.error("SKILL_FRONTMATTER", "SKILL.md frontmatter is not terminated.", path)
        return None

    fm = lines[1:end]
    result: dict[str, Any] = {}
    i = 0
    while i < len(fm):
        line = fm[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        if line.startswith((" ", "\t")):
            audit.error("SKILL_FRONTMATTER", f"Unexpected indented top-level line: {line!r}", path)
            i += 1
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$", line)
        if not match:
            audit.error("SKILL_FRONTMATTER", f"Unsupported frontmatter line: {line!r}", path)
            i += 1
            continue
        key, raw = match.group(1), (match.group(2) or "")
        if key == "metadata":
            mapping: dict[str, str] = {}
            i += 1
            while i < len(fm) and (not fm[i].strip() or fm[i].startswith((" ", "\t"))):
                nested = fm[i]
                if nested.strip() and not nested.lstrip().startswith("#"):
                    nested_match = re.match(r"^\s+([^:]+):(?:\s*(.*))?$", nested)
                    if not nested_match:
                        audit.error("SKILL_METADATA", f"Unsupported metadata line: {nested!r}", path)
                    else:
                        nested_key = nested_match.group(1).strip()
                        nested_value = scalar(nested_match.group(2) or "")
                        mapping[nested_key] = nested_value
                i += 1
            result[key] = mapping
            continue

        if raw in {">", "|"} or raw == "":
            block: list[str] = []
            i += 1
            while i < len(fm) and (not fm[i].strip() or fm[i].startswith((" ", "\t"))):
                block.append(fm[i].strip())
                i += 1
            if raw == "|":
                result[key] = "\n".join(block).strip()
            else:
                result[key] = " ".join(part for part in block if part).strip()
            continue

        continued = [scalar(raw)]
        i += 1
        while i < len(fm) and (not fm[i].strip() or fm[i].startswith((" ", "\t"))):
            if fm[i].strip() and not fm[i].lstrip().startswith("#"):
                continued.append(fm[i].strip())
            i += 1
        result[key] = " ".join(part for part in continued if part).strip()

    return result


def strip_jsonc(text: str) -> str:
    output: list[str] = []
    i = 0
    in_string = False
    escaped = False
    while i < len(text):
        ch = text[i]
        nxt = text[i + 1] if i + 1 < len(text) else ""
        if in_string:
            output.append(ch)
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            i += 1
            continue
        if ch == '"':
            in_string = True
            output.append(ch)
            i += 1
            continue
        if ch == "/" and nxt == "/":
            i += 2
            while i < len(text) and text[i] not in "\r\n":
                i += 1
            continue
        if ch == "/" and nxt == "*":
            i += 2
            while i + 1 < len(text) and not (text[i] == "*" and text[i + 1] == "/"):
                i += 1
            i += 2
            continue
        output.append(ch)
        i += 1
    cleaned = "".join(output)
    return re.sub(r",\s*([}\]])", r"\1", cleaned)


def relative_file_set(directory: Path) -> set[str]:
    return {
        path.relative_to(directory).as_posix()
        for path in directory.rglob("*")
        if path.is_file()
    }


def iter_markdown_links(path: Path) -> Iterable[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for match in MD_LINK_RE.finditer(line):
            target = match.group(1).strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            target = target.split("#", 1)[0].split("?", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:", "#", "/")):
                continue
            if any(marker in target for marker in ("<", ">", "*", "{")):
                continue
            yield target


def find_skill_dirs() -> dict[str, Path]:
    result: dict[str, Path] = {}
    for skill_file in sorted((ROOT / "skills").glob("*/*/SKILL.md")):
        name = skill_file.parent.name
        if name in result:
            raise RuntimeError(f"duplicate directory name: {name}")
        result[name] = skill_file.parent
    return result


def audit_required_files(audit: Audit) -> None:
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
        "global/HISTORY.md",
        "project/AGENTS.template.md",
        "prompts/PROJECT_BOOTSTRAP.md",
        "prompts/PROJECT_REFRESH.md",
        "prompts/PROJECT_AUDIT.md",
        "prompts/CODEBASE_ONBOARD.md",
        "prompts/CHANGE_AUDIT.md",
        "templates/omo/ROUTING.md",
        "evaluation/README.md",
        "evaluation/agentrc.eval.jsonc",
        "tools/README.md",
        "tools/audit.py",
    ]
    for item in required:
        if not (ROOT / item).is_file():
            audit.error("REQUIRED_FILE", "Required repository file is missing.", item)
    license_dir = ROOT / "catalog/LICENSES"
    if not license_dir.is_dir() or not any(path.is_file() for path in license_dir.iterdir()):
        audit.error("LICENSE_MATERIAL", "catalog/LICENSES must contain preserved source license/evidence files.", license_dir)


def audit_skills(audit: Audit, lock: dict[str, Any]) -> tuple[dict[str, Path], set[str]]:
    try:
        skill_dirs = find_skill_dirs()
    except RuntimeError as exc:
        audit.error("SKILL_DUPLICATE", str(exc), ROOT / "skills")
        skill_dirs = {}

    lock_skills = lock.get("skills")
    if not isinstance(lock_skills, dict):
        audit.error("LOCK_SCHEMA", "catalog/skills.lock.json must contain an object named 'skills'.", ROOT / "catalog/skills.lock.json")
        lock_skills = {}

    on_disk = set(skill_dirs)
    in_lock = set(lock_skills)
    for name in sorted(on_disk - in_lock):
        audit.error("LOCK_MISSING_ENTRY", f"Skill '{name}' is present on disk but absent from the lockfile.", skill_dirs[name])
    for name in sorted(in_lock - on_disk):
        audit.error("LOCK_ORPHAN_ENTRY", f"Lockfile Skill '{name}' is absent from disk.", ROOT / "catalog/skills.lock.json")

    for name, directory in sorted(skill_dirs.items()):
        skill_file = directory / "SKILL.md"
        frontmatter = parse_frontmatter(skill_file, audit)
        if frontmatter is None:
            continue
        unknown = set(frontmatter) - RECOGNIZED_SKILL_FIELDS
        if unknown:
            audit.error("SKILL_FIELDS", f"OpenCode ignores unsupported frontmatter fields: {sorted(unknown)}", skill_file)
        if frontmatter.get("name") != name:
            audit.error("SKILL_NAME", f"Frontmatter name {frontmatter.get('name')!r} does not match directory '{name}'.", skill_file)
        if not NAME_RE.fullmatch(name) or len(name) > 64:
            audit.error("SKILL_NAME", f"Skill name '{name}' violates OpenCode naming constraints.", skill_file)
        description = str(frontmatter.get("description") or "").strip()
        if not description:
            audit.error("SKILL_DESCRIPTION", "Skill description is missing or empty.", skill_file)
        elif len(description) > 1024:
            audit.error("SKILL_DESCRIPTION", f"Skill description is {len(description)} characters; OpenCode allows at most 1024.", skill_file)
        metadata = frontmatter.get("metadata")
        if metadata is not None:
            if not isinstance(metadata, dict) or any(not isinstance(k, str) or not isinstance(v, str) for k, v in metadata.items()):
                audit.error("SKILL_METADATA", "metadata must be a string-to-string map for OpenCode.", skill_file)
        body_lines = skill_file.read_text(encoding="utf-8", errors="replace").count("\n") + 1
        if body_lines > 500:
            source_trust = (lock_skills.get(name) or {}).get("sourceTrust", "unknown")
            audit.warn("SKILL_LENGTH", f"SKILL.md has {body_lines} lines; progressive disclosure is recommended. Source trust: {source_trust}.", skill_file)

        entry = lock_skills.get(name)
        if not isinstance(entry, dict):
            continue
        for field in (
            "source",
            "sourceType",
            "revision",
            "reviewed",
            "license",
            "licenseEvidence",
            "placement",
            "sideEffects",
            "sourceTrust",
            "integrity",
            "hostCompatibility",
            "behaviorStatus",
            "activationGuidance",
            "operationalRisk",
            "redistributionStatus",
        ):
            if not entry.get(field):
                audit.error("LOCK_METADATA", f"Skill '{name}' is missing required lock metadata '{field}'.", ROOT / "catalog/skills.lock.json")
        if not isinstance(entry.get("review"), dict):
            audit.error("LOCK_REVIEW", f"Skill '{name}' is missing structured review metadata.", ROOT / "catalog/skills.lock.json")
        if entry.get("redistributionStatus") != "license-evidence-preserved-or-local" and not entry.get("knownIssues"):
            audit.error("LICENSE_EVIDENCE", f"Skill '{name}' has incomplete redistribution evidence without a recorded known issue.", ROOT / "catalog/skills.lock.json")
        if not isinstance(entry.get("knownIssues"), list):
            audit.error("LOCK_METADATA", f"Skill '{name}' must record knownIssues as a list.", ROOT / "catalog/skills.lock.json")
        expected_files = entry.get("files")
        if not isinstance(expected_files, dict):
            audit.error("LOCK_FILES", f"Skill '{name}' has no file hash map.", ROOT / "catalog/skills.lock.json")
            continue
        actual_files = relative_file_set(directory)
        expected_set = set(expected_files)
        for rel in sorted(actual_files - expected_set):
            audit.error("LOCK_UNTRACKED_FILE", f"Untracked Skill file: {name}/{rel}", directory / rel)
        for rel in sorted(expected_set - actual_files):
            audit.error("LOCK_MISSING_FILE", f"Tracked Skill file is missing: {name}/{rel}", directory / rel)
        for rel in sorted(actual_files & expected_set):
            expected_hash = str(expected_files[rel])
            if not expected_hash.startswith("sha256:"):
                audit.error("LOCK_HASH_FORMAT", f"Hash for {name}/{rel} is not prefixed with sha256:.", ROOT / "catalog/skills.lock.json")
                continue
            actual_hash = sha256(directory / rel)
            if actual_hash != expected_hash.removeprefix("sha256:"):
                audit.error("LOCK_HASH_MISMATCH", f"Hash mismatch for {name}/{rel}.", directory / rel)

        placement = entry.get("placement")
        category = directory.parent.name
        if category == "operational" and placement != "operational":
            audit.error("OPERATIONAL_PLACEMENT", f"Operational Skill '{name}' is not marked operational in the lockfile.", directory)
        if category != "operational" and placement == "operational":
            audit.error("OPERATIONAL_PLACEMENT", f"Skill '{name}' is marked operational but is stored under '{category}'.", directory)

    audit.metrics["skillsOnDisk"] = len(on_disk)
    audit.metrics["skillsInLock"] = len(in_lock)
    audit.metrics["trackedSkillFiles"] = sum(len((entry or {}).get("files", {})) for entry in lock_skills.values() if isinstance(entry, dict))
    audit.metrics["operationalSkills"] = sum(1 for entry in lock_skills.values() if isinstance(entry, dict) and entry.get("placement") == "operational")
    return skill_dirs, {name for name, entry in lock_skills.items() if isinstance(entry, dict) and entry.get("placement") == "operational"}


def audit_omo_templates(audit: Audit, skill_ids: set[str], operational_ids: set[str]) -> None:
    templates = sorted((ROOT / "templates/omo").glob("*.jsonc"))
    for path in templates:
        try:
            data = json.loads(strip_jsonc(path.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            audit.error("OMO_JSONC", f"Invalid JSONC: {exc}", path)
            continue
        if not isinstance(data, dict):
            audit.error("OMO_SCHEMA", "OMO template root must be an object.", path)
            continue
        extra_root = set(data) - {"$schema", "agents"}
        if extra_root:
            audit.error("OMO_SCOPE", f"Template contains non-routing root keys: {sorted(extra_root)}", path)
        agents = data.get("agents")
        if not isinstance(agents, dict) or not agents:
            audit.error("OMO_SCHEMA", "Template must define a non-empty root agents object.", path)
            continue
        for agent_name, config in agents.items():
            if agent_name not in OMO_BUILTIN_AGENTS:
                audit.error("OMO_AGENT", f"Unknown built-in agent '{agent_name}' in routing template.", path)
            if agent_name not in {"fixer", "designer"}:
                audit.warn("OMO_AGENT_SCOPE", f"Template routes project Skills to '{agent_name}'; review whether this is necessary.", path)
            if not isinstance(config, dict):
                audit.error("OMO_SCHEMA", f"Agent '{agent_name}' config must be an object.", path)
                continue
            extra = set(config) - {"skills"}
            if extra:
                audit.error("OMO_SCOPE", f"Agent '{agent_name}' contains non-Skill settings: {sorted(extra)}", path)
            skills = config.get("skills")
            if not isinstance(skills, list) or any(not isinstance(item, str) for item in skills):
                audit.error("OMO_SKILLS", f"Agent '{agent_name}' skills must be a string array.", path)
                continue
            if len(skills) != len(set(skills)):
                audit.error("OMO_SKILLS", f"Agent '{agent_name}' contains duplicate Skill IDs.", path)
            if "*" in skills:
                audit.error("OMO_SKILLS", f"Project routing template for '{agent_name}' must not grant wildcard Skill access.", path)
            for skill in skills:
                if skill not in skill_ids and skill not in OMO_BUILTIN_SKILLS:
                    audit.error("OMO_SKILL_UNKNOWN", f"Template references unknown Skill '{skill}'.", path)
                if skill in operational_ids:
                    audit.error("OMO_OPERATIONAL_ROUTE", f"Operational Skill '{skill}' must not be auto-routed.", path)
    audit.metrics["omoTemplates"] = len(templates)


def audit_prompt_boundaries(audit: Audit) -> None:
    read_only = {
        "PROJECT_AUDIT.md": ("read-only", "do not modify"),
        "CODEBASE_ONBOARD.md": ("read-only", "do not modify"),
        "CHANGE_AUDIT.md": ("read-only", "do not fix"),
    }
    for name, required_phrases in read_only.items():
        path = ROOT / "prompts" / name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8").lower()
        if not all(phrase in text for phrase in required_phrases):
            audit.error("PROMPT_BOUNDARY", f"Read-only prompt lacks explicit mutation boundary: {required_phrases}", path)
    for name in ("PROJECT_BOOTSTRAP.md", "PROJECT_REFRESH.md"):
        path = ROOT / "prompts" / name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8").lower()
        if "do not modify application source" not in text:
            audit.error("PROMPT_BOUNDARY", "Configuration prompt must explicitly prohibit application-source edits.", path)
        if "noop" not in text:
            audit.warn("PROMPT_NOOP", "Configuration prompt should define NOOP behavior when already aligned.", path)
    audit.metrics["conveniencePrompts"] = len(list((ROOT / "prompts").glob("*.md"))) - 1


def audit_markdown_links(audit: Audit, lock: dict[str, Any]) -> None:
    authored_roots = [ROOT, ROOT / "global", ROOT / "project", ROOT / "prompts", ROOT / "templates", ROOT / "evaluation", ROOT / "tools", ROOT / "catalog"]
    authored_files: set[Path] = set()
    for base in authored_roots:
        if base == ROOT:
            authored_files.update(path for path in ROOT.glob("*.md") if path.is_file())
        elif base.exists():
            authored_files.update(path for path in base.rglob("*.md") if path.is_file())
    for path in sorted(authored_files):
        for target in iter_markdown_links(path):
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                audit.warn("AUTHORED_LINK_EXTERNAL_PATH", f"Relative link escapes repository: {target}", path)
                continue
            if not resolved.exists():
                audit.error("AUTHORED_BROKEN_LINK", f"Missing authored relative link target: {target}", path)

    lock_skills = lock.get("skills", {}) if isinstance(lock.get("skills"), dict) else {}
    upstream_broken = 0
    local_broken = 0
    for skill_file in sorted((ROOT / "skills").glob("*/*/**/*.md")):
        if not skill_file.is_file():
            continue
        skill_name = skill_file.relative_to(ROOT / "skills").parts[1]
        source_trust = (lock_skills.get(skill_name) or {}).get("sourceTrust")
        for target in iter_markdown_links(skill_file):
            resolved = (skill_file.parent / target).resolve()
            try:
                resolved.relative_to((ROOT / "skills").resolve())
            except ValueError:
                continue
            if resolved.exists():
                continue
            if source_trust == "local-derived":
                local_broken += 1
                audit.error("LOCAL_SKILL_BROKEN_LINK", f"Missing local Skill link target: {target}", skill_file)
            else:
                upstream_broken += 1
    if upstream_broken:
        audit.info("UPSTREAM_BROKEN_LINKS", f"Retained {upstream_broken} unresolved relative links in byte-preserved upstream snapshots; see lockfile knownIssues.")
    audit.metrics["knownUpstreamBrokenLinks"] = upstream_broken
    audit.metrics["localBrokenLinks"] = local_broken



def audit_evaluation(audit: Audit) -> None:
    path = ROOT / "evaluation/agentrc.eval.jsonc"
    if not path.is_file():
        return
    try:
        data = json.loads(strip_jsonc(path.read_text(encoding="utf-8")))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        audit.error("EVAL_JSONC", f"Invalid evaluation JSONC: {exc}", path)
        return
    cases = data.get("cases") if isinstance(data, dict) else None
    if not isinstance(cases, list) or not cases:
        audit.error("EVAL_SCHEMA", "Evaluation file must contain a non-empty cases array.", path)
        return
    seen: set[str] = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            audit.error("EVAL_SCHEMA", f"Case {index} must be an object.", path)
            continue
        case_id = case.get("id")
        prompt = case.get("prompt")
        expectation = case.get("expectation")
        if not isinstance(case_id, str) or not case_id.strip():
            audit.error("EVAL_SCHEMA", f"Case {index} has no valid id.", path)
        elif case_id in seen:
            audit.error("EVAL_DUPLICATE", f"Duplicate case id '{case_id}'.", path)
        else:
            seen.add(case_id)
        if not isinstance(prompt, str) or not prompt.strip():
            audit.error("EVAL_SCHEMA", f"Case '{case_id or index}' has no prompt.", path)
        valid_expectation = (
            isinstance(expectation, str) and bool(expectation.strip())
        ) or (
            isinstance(expectation, list)
            and bool(expectation)
            and all(isinstance(item, str) and item.strip() for item in expectation)
        )
        if not valid_expectation:
            audit.error("EVAL_SCHEMA", f"Case '{case_id or index}' has no valid expectation.", path)
    audit.metrics["behavioralEvalCases"] = len(cases)


def audit_authored_markdown(audit: Audit) -> None:
    authored: set[Path] = set(path for path in ROOT.glob("*.md") if path.is_file())
    for folder in ("global", "project", "prompts", "templates", "evaluation", "tools", "catalog"):
        base = ROOT / folder
        if base.exists():
            authored.update(path for path in base.rglob("*.md") if path.is_file())
    for path in sorted(authored):
        text = path.read_text(encoding="utf-8", errors="replace")
        trailing = [idx for idx, line in enumerate(text.splitlines(), start=1) if line.rstrip() != line]
        if trailing:
            audit.warn("MARKDOWN_TRAILING_SPACE", f"Trailing whitespace on lines: {trailing[:8]}", path)
        fence_count = sum(1 for line in text.splitlines() if line.lstrip().startswith("```"))
        if fence_count % 2:
            audit.error("MARKDOWN_FENCE", f"Unbalanced fenced code blocks ({fence_count} fence lines).", path)


def audit_no_forbidden_artifacts(audit: Audit) -> None:
    for path in ROOT.rglob("*"):
        if path.is_symlink():
            audit.error("SYMLINK", "Repository archive must not contain symlinks.", path)
        if path.is_file() and (path.name.endswith((".pyc", ".pyo")) or "__pycache__" in path.parts):
            audit.error("GENERATED_ARTIFACT", "Python cache artifact must not be packaged.", path)


def load_lock(audit: Audit) -> dict[str, Any]:
    path = ROOT / "catalog/skills.lock.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        audit.error("LOCK_PARSE", f"Cannot parse lockfile: {exc}", path)
        return {}
    if not isinstance(data, dict):
        audit.error("LOCK_SCHEMA", "Lockfile root must be an object.", path)
        return {}
    return data


def run() -> Audit:
    audit = Audit()
    audit_required_files(audit)
    lock = load_lock(audit)
    skill_dirs, operational_ids = audit_skills(audit, lock)
    audit_omo_templates(audit, set(skill_dirs), operational_ids)
    audit_prompt_boundaries(audit)
    audit_evaluation(audit)
    audit_authored_markdown(audit)
    audit_markdown_links(audit, lock)
    audit_no_forbidden_artifacts(audit)
    audit.metrics["errors"] = sum(item.level == "ERROR" for item in audit.findings)
    audit.metrics["warnings"] = sum(item.level == "WARN" for item in audit.findings)
    audit.metrics["infos"] = sum(item.level == "INFO" for item in audit.findings)
    return audit


def print_text(audit: Audit) -> None:
    for finding in audit.findings:
        location = f" [{finding.path}]" if finding.path else ""
        print(f"{finding.level:<5} {finding.code}: {finding.message}{location}")
    print("\nMetrics")
    for key, value in sorted(audit.metrics.items()):
        print(f"- {key}: {value}")
    status = "PASS" if audit.metrics.get("errors", 0) == 0 else "FAIL"
    if status == "PASS" and audit.metrics.get("warnings", 0):
        status = "PASS_WITH_WARNINGS"
    print(f"\nResult: {status}")
    print("Scope: deterministic static repository checks only; host/model behavior is NOT RUN.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    args = parser.parse_args()
    audit = run()
    if args.json:
        status = "pass" if audit.metrics.get("errors", 0) == 0 else "fail"
        payload = {
            "status": status,
            "scope": "deterministic-static-only",
            "metrics": audit.metrics,
            "findings": [asdict(item) for item in audit.findings],
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print_text(audit)
    return 1 if audit.metrics.get("errors", 0) else 0


if __name__ == "__main__":
    sys.exit(main())
