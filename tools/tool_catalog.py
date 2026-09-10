#!/usr/bin/env python3
"""Validate selected tools and optionally observe upstreams. Never install or edit."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timezone
from typing import Any
from urllib.parse import urlsplit

sys.dont_write_bytecode = True
from quality import ROOT, ID, REPO, SHA, iso_date, load_json, require, text, validate_registry
from freshness import GitHubReader

CATALOGS = {
    "agent-capabilities.json": "agent-capabilities",
    "automation-tools.json": "project-automation",
    "developer-tools.json": "developer-cli",
}
POLICIES = {"baseline", "conditional", "optional", "pilot", "operational"}
ACTIVATIONS = {"on-demand", "project-evidence", "user-choice", "explicit-opt-in"}
INTERFACES = {"mcp", "cli", "ci", "bot", "hook", "task", "runtime", "build-plugin"}
INSTALLS = {"remote-or-official-binary", "reuse-or-remote", "official-package", "official-python-tool", "official-npm-package", "github-workflow", "github-app-or-approved-runner", "native-build-plugin"}


def validate_tools(data: Any, scope: str, today: date) -> dict[str, Any]:
    require(isinstance(data, dict) and type(data.get("schemaVersion")) is int and data["schemaVersion"] == 1, "Invalid tool catalog schema")
    require(data.get("scope") == scope, "Tool catalog scope mismatch")
    require(iso_date(data.get("policyReviewedAt")) <= today, "Future tool policy review")
    require(isinstance(data.get("tools"), list) and bool(data["tools"]), "Empty tool catalog")
    result = {}
    for tool in data["tools"]:
        require(isinstance(tool, dict), "Tool must be an object")
        ident = tool.get("id")
        require(isinstance(ident, str) and bool(ID.fullmatch(ident)) and ident not in result, "Invalid or duplicate tool id")
        for key, choices in (("policy", POLICIES), ("activation", ACTIVATIONS), ("interface", INTERFACES), ("install", INSTALLS)):
            require(isinstance(tool.get(key), str) and tool[key] in choices, f"Invalid {key}: {ident}")
        require(text(tool.get("name")) and text(tool.get("purpose")), f"Missing description: {ident}")
        repo = tool.get("upstream")
        require(isinstance(repo, str) and bool(REPO.fullmatch(repo)) and all(p not in {".", ".."} for p in repo.split("/")), f"Unsafe upstream: {ident}")
        require(text(tool.get("docs")), f"Missing official documentation: {ident}")
        url = urlsplit(tool["docs"])
        require(url.scheme == "https" and bool(url.hostname) and not url.username and not url.password, f"Unsafe documentation URL: {ident}")
        if tool["policy"] in {"pilot", "operational"}:
            require(tool["activation"] == "explicit-opt-in", f"Unsafe automatic activation: {ident}")
        result[ident] = dict(tool, scope=scope)
    return result


def load_tools(root=ROOT, today: date | None = None) -> dict[str, Any]:
    today = today or date.today()
    runtime = validate_registry(load_json(root / "catalog/tooling.json"), today)
    tools = {k: dict(v, scope="opencode-v1") for k, v in runtime.items()}
    for filename, scope in CATALOGS.items():
        rows = validate_tools(load_json(root / "catalog" / filename), scope, today)
        require(not (tools.keys() & rows.keys()), "Duplicate tool id across catalogs")
        tools.update(rows)
    return tools


def timestamp(value: Any, today: date) -> date:
    require(isinstance(value, str), "Missing upstream timestamp")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(parsed.tzinfo is not None, "Unzoned upstream timestamp")
    day = parsed.astimezone(timezone.utc).date()
    require(day <= today, "Future upstream timestamp")
    return day


def observe(tool: dict[str, Any], reader: Any | None, today: date, review_days: int) -> dict[str, Any]:
    repo = tool.get("upstream")
    if repo is None:
        return {"status": "NOT_APPLICABLE", "reason": "No reviewed upstream identity for historical held/retired entry"}
    if reader is None:
        return {"status": "NOT_CHECKED", "reason": "Offline validation only"}
    try:
        require(isinstance(repo, str) and bool(REPO.fullmatch(repo)) and all(p not in {".", ".."} for p in repo.split("/")), "Unsafe upstream")
        meta = reader.get(f"/repos/{repo}")
        require(isinstance(meta, dict) and text(meta.get("full_name")), "Malformed upstream metadata")
        if meta["full_name"].lower() != repo.lower():
            return {"status": "RENAMED", "canonical": meta["full_name"], "reason": "Review identity; no automatic redirect or policy rewrite"}
        require(type(meta.get("archived")) is bool and type(meta.get("disabled")) is bool, "Missing archival flags")
        result = {"canonical": meta["full_name"], "archived": meta["archived"], "disabled": meta["disabled"], "pushedAt": meta.get("pushed_at")}
        if meta["archived"] or meta["disabled"]:
            return dict(result, status="ARCHIVED" if meta["archived"] else "DISABLED")
        require(text(meta.get("default_branch")), "Missing default branch")
        commits = reader.get(f"/repos/{repo}/commits?per_page=1")
        require(isinstance(commits, list) and len(commits) == 1 and isinstance(commits[0], dict), "Missing default-branch commit")
        commit = commits[0]
        require(isinstance(commit.get("sha"), str) and bool(SHA.fullmatch(commit["sha"])), "Invalid upstream commit")
        committed = commit["commit"]["committer"]["date"]
        activity = timestamp(committed, today)
        result.update(defaultBranch=meta["default_branch"], commit=commit["sha"], committedAt=committed)
        try:
            release = reader.get(f"/repos/{repo}/releases/latest")
        except ValueError as exc:
            if str(exc) != "GitHub API HTTP 404":
                raise
            release = None
        if release is not None:
            require(isinstance(release, dict) and release.get("draft") is False and release.get("prerelease") is False and text(release.get("tag_name")), "Malformed stable release")
            published = timestamp(release.get("published_at"), today)
            activity = max(activity, published)
            result["release"] = {"tag": release["tag_name"], "publishedAt": release["published_at"]}
        else:
            result["release"] = None
        result["status"] = "RECENT_ACTIVITY" if (today - activity).days < review_days else "REVIEW_DUE"
        return result
    except (ValueError, TypeError, KeyError, IndexError, OSError):
        return {"status": "UNRESOLVED", "reason": "Metadata, network, rate limit, redirect or release lookup could not be verified"}


def report(tools: dict[str, Any], today: date, reader=None, review_days: int = 180) -> dict[str, Any]:
    require(type(review_days) is int and review_days > 0, "Review days must be a positive integer")
    rows = [{"id": ident, "scope": tool["scope"], "upstream": tool.get("upstream"), "observation": observe(tool, reader, today, review_days)} for ident, tool in sorted(tools.items())]
    partial = any(row["observation"]["status"] == "UNRESOLVED" for row in rows)
    return {"schemaVersion": 1, "status": "PARTIAL" if partial else "REPORTED", "asOf": today.isoformat(), "online": reader is not None, "reviewDays": review_days, "scope": "maintenance-observation-not-security-or-runtime-certification", "installation": "NOT RUN", "tools": rows}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--online", action="store_true")
    parser.add_argument("--review-days", type=int, default=180)
    args = parser.parse_args()
    try:
        today = datetime.now(timezone.utc).date()
        result = report(load_tools(today=today), today, GitHubReader(max_requests=160) if args.online else None, args.review_days)
        print(json.dumps(result, indent=2))
        return 2 if result["status"] == "PARTIAL" else 0
    except (OSError, ValueError, TypeError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
