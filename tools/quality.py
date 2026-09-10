#!/usr/bin/env python3
"""Maintainer-only policy/evidence checks. No runtime or installation changes."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
SHA = re.compile(r"[0-9a-f]{40}")
ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
REPO = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")
POLICIES = {"baseline", "external", "pilot", "hold", "retired"}
KINDS = {"host", "plugin", "integration", "companion"}
STATUSES = {"PASS", "PARTIAL", "FAIL", "BLOCKED", "NOT RUN"}
BEGIN = "<!-- tooling-policy:begin -->"
END = "<!-- tooling-policy:end -->"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)


def iso_date(value: Any) -> date:
    require(isinstance(value, str) and bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", value)), "Expected an ISO date YYYY-MM-DD")
    return date.fromisoformat(value)


def local_path(root: Path, value: Any) -> Path:
    require(text(value), "Expected a repository-relative path")
    p = Path(value)
    require(not p.is_absolute() and ".." not in p.parts, "Path escapes repository")
    resolved = (root / p).resolve()
    require(resolved.is_relative_to(root.resolve()), "Symlink escapes repository")
    require(resolved.is_file(), f"Missing evidence/reference file: {value}")
    return resolved


def validate_registry(data: Any, today: date) -> dict[str, dict[str, Any]]:
    require(isinstance(data, dict) and type(data.get("schemaVersion")) is int and data.get("schemaVersion") == 1, "Invalid tooling schemaVersion")
    require(data.get("scope") == "opencode-v1", "Tooling scope must remain opencode-v1")
    require(iso_date(data.get("policyReviewedAt")) <= today, "Future tooling policy review")
    require(text(data.get("notes")), "Tooling policy needs evidence limitations")
    tools = data.get("tools")
    require(isinstance(tools, list) and bool(tools), "Tooling registry is empty")
    result: dict[str, dict[str, Any]] = {}
    for tool in tools:
        require(isinstance(tool, dict), "Tool must be an object")
        ident = tool.get("id")
        require(isinstance(ident, str) and bool(ID.fullmatch(ident)), "Invalid tool id")
        require(ident not in result, f"Duplicate tool id: {ident}")
        require(text(tool.get("name")) and text(tool.get("rationale")), f"Missing tool description: {ident}")
        require(isinstance(tool.get("kind"), str) and isinstance(tool.get("policy"), str) and tool["kind"] in KINDS and tool["policy"] in POLICIES, f"Invalid policy/kind: {ident}")
        upstream = tool.get("upstream")
        require(upstream is None or (isinstance(upstream, str) and bool(REPO.fullmatch(upstream))), f"Invalid upstream: {ident}")
        if tool["policy"] in {"baseline", "external", "pilot"}:
            require(upstream is not None, f"Selected tool needs a reviewed upstream: {ident}")
        require((tool["policy"] == "external") == (tool["kind"] == "companion"), f"Companion/runtime policy mismatch: {ident}")
        result[ident] = tool
    return result


def tooling_table(data: dict[str, Any]) -> str:
    lines = [BEGIN, "| Tool | Policy | Integration |", "|---|---|---|"]
    for tool in data["tools"]:
        lines.append(f"| {tool['name']} | `{tool['policy']}` | `{tool['kind']}` |")
    lines.append(END)
    return "\n".join(lines)


def validate_evidence(data: Any, tools: dict[str, Any], root: Path, today: date) -> None:
    require(isinstance(data, dict) and type(data.get("schemaVersion")) is int and data.get("schemaVersion") == 1, "Invalid evidence schemaVersion")
    require(text(data.get("id")), "Evidence id is missing")
    kind = data.get("evidenceClass")
    require(isinstance(kind, str) and kind in {"historical-summary", "host-smoke"}, "Unknown evidence class")
    observed, recorded = iso_date(data.get("observedAt")), iso_date(data.get("recordedAt"))
    require(observed <= recorded <= today, "Invalid evidence chronology")
    source = data.get("source")
    require(isinstance(source, dict), "Evidence source is missing")
    local_path(root, source.get("path"))
    require(isinstance(source.get("revision"), str) and bool(SHA.fullmatch(source["revision"])), "Evidence source needs immutable revision")
    env = data.get("environment")
    require(isinstance(env, dict) and text(env.get("os")), "Evidence environment is missing")
    versions = env.get("versions")
    require(isinstance(versions, dict) and bool(versions), "Evidence tool versions are missing")
    require(all(k in tools and text(v) for k, v in versions.items()), "Unknown/unversioned evidence tool")
    require(isinstance(data.get("limitations"), list) and bool(data["limitations"]) and all(text(x) for x in data["limitations"]), "Evidence limitations are required")
    if kind == "host-smoke":
        require(text(env.get("model")), "Host smoke must identify the model")
        require(isinstance(env.get("repositoryRevision"), str) and bool(SHA.fullmatch(env["repositoryRevision"])), "Host smoke must identify the tested revision")
    checks = data.get("checks")
    require(isinstance(checks, list) and bool(checks), "Evidence checks are empty")
    seen: set[str] = set()
    for check in checks:
        require(isinstance(check, dict) and text(check.get("id")), "Invalid evidence check")
        require(check["id"] not in seen, "Duplicate evidence check")
        seen.add(check["id"])
        require(isinstance(check.get("tool"), str) and check["tool"] in versions, "Evidence check has no tested tool version")
        require(isinstance(check.get("status"), str) and check["status"] in STATUSES, "Unknown evidence status")
        if kind == "host-smoke" and check["status"] in {"PASS", "FAIL", "PARTIAL"}:
            local_path(root, check.get("artifact"))
        if check["status"] in {"NOT RUN", "BLOCKED"}:
            require(text(check.get("reason")), "Unexecuted check needs a reason")


def check_repository(root: Path = ROOT, today: date | None = None) -> dict[str, Any]:
    today = today or date.today()
    errors: list[str] = []
    records = 0
    tools: dict[str, Any] = {}
    try:
        registry = load_json(root / "catalog/tooling.json")
        tools = validate_registry(registry, today)
        readme = (root / "README.md").read_text(encoding="utf-8")
        require(readme.count(BEGIN) == 1 and readme.count(END) == 1, "README tooling projection markers missing/duplicated")
        projection = readme[readme.index(BEGIN):readme.index(END) + len(END)]
        require(projection == tooling_table(registry), "README tooling policy drift; regenerate the table from catalog/tooling.json")
        setup = (root / "prompts/OPENCODE_PLUGIN_SETUP.md").read_text(encoding="utf-8")
        require("catalog/tooling.json" in setup, "Setup prompt must use the canonical tooling registry")
    except (OSError, ValueError, TypeError) as exc:
        errors.append(str(exc))
    evidence_dir = root / "evaluation/evidence"
    paths = sorted(evidence_dir.glob("*.json"))
    if not paths:
        errors.append("No structured evidence records")
    for path in paths:
        try:
            record = load_json(path)
            validate_evidence(record, tools, root, today)
            require(record["id"] == path.stem, "Evidence filename/id mismatch")
            records += 1
        except (OSError, ValueError, TypeError) as exc:
            errors.append(f"{path.name}: {exc}")
    return {"status": "FAIL" if errors else "PASS", "scope": "static-policy-and-evidence-schema-only", "tools": len(tools), "evidenceRecords": records, "errors": errors, "hostBehavior": "NOT RUN"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tooling-table", action="store_true", help="Print the README projection; never modify files.")
    args = parser.parse_args()
    if args.tooling_table:
        registry = load_json(ROOT / "catalog/tooling.json")
        validate_registry(registry, date.today())
        print(tooling_table(registry))
        return 0
    result = check_repository()
    print(json.dumps(result, indent=2))
    return int(bool(result["errors"]))


if __name__ == "__main__":
    raise SystemExit(main())
