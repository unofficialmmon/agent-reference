#!/usr/bin/env python3
"""Read-only Skill review/upstream report. Never installs or rewrites snapshots."""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import PurePosixPath
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

sys.dont_write_bytecode = True
from quality import ROOT, REPO, SHA, iso_date, load_json, require

MAX_BYTES = 16 * 1024 * 1024


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("GitHub API redirect refused; review renamed upstream explicitly")


class GitHubReader:
    """Bounded public-repository GETs; optional token is never printed."""
    def __init__(self, timeout: int = 10, max_requests: int = 100):
        self.timeout = timeout
        self.max_requests = max_requests
        self.requests = 0
        self.cache: dict[str, Any] = {}
        self.unavailable: str | None = None
        self.opener = build_opener(NoRedirect())

    def get(self, suffix: str) -> Any:
        require(suffix.startswith("/repos/") and not any(c in suffix for c in "\r\n"), "Invalid GitHub API path")
        if suffix in self.cache:
            value = self.cache[suffix]
            if isinstance(value, Exception):
                raise value
            return value
        if self.unavailable:
            raise ValueError(self.unavailable)
        if self.requests >= self.max_requests:
            raise ValueError("GitHub API request budget exhausted")
        self.requests += 1
        headers = {"Accept": "application/vnd.github+json", "User-Agent": "agent-reference-freshness", "X-GitHub-Api-Version": "2022-11-28"}
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        try:
            request = Request("https://api.github.com" + suffix, headers=headers, method="GET")
            with self.opener.open(request, timeout=self.timeout) as response:
                raw = response.read(MAX_BYTES + 1)
            require(len(raw) <= MAX_BYTES, "GitHub response exceeds bounded reader size")
            value = json.loads(raw)
            self.cache[suffix] = value
            return value
        except HTTPError as exc:
            message = f"GitHub API HTTP {exc.code}"
            if exc.code in {401, 403, 429}:
                self.unavailable = message
        except (URLError, OSError, TimeoutError):
            message = "GitHub API network unavailable"
            self.unavailable = message
        except (ValueError, UnicodeError):
            message = "Invalid or redirected GitHub API response"
        error = ValueError(message)
        self.cache[suffix] = error
        raise error


def github_source(entry: dict[str, Any]) -> tuple[str, str, str]:
    source = entry.get("source")
    require(isinstance(source, str), "Missing upstream source")
    parts = urlsplit(source)
    require(parts.scheme == "https" and parts.netloc == "github.com" and not parts.query and not parts.fragment, "Only canonical HTTPS github.com source roots are supported")
    repo = parts.path.strip("/")
    require(bool(REPO.fullmatch(repo)) and not any(p in {".", ".."} for p in repo.split("/")), "Invalid GitHub owner/repository")
    revision = entry.get("revision")
    require(isinstance(revision, str) and bool(SHA.fullmatch(revision)), "Upstream revision is not an immutable 40-character SHA")
    path = entry.get("upstreamPath")
    require(isinstance(path, str) and bool(path) and not path.startswith("/") and "\\" not in path, "Missing/invalid upstream Skill path")
    require(not any(p in {"", ".", ".."} for p in path.split("/")), "Unsafe upstream Skill path")
    return repo, revision, PurePosixPath(path).as_posix()


def subtree_sha(reader: Any, repo: str, revision: str, path: str) -> str | None:
    tree = reader.get(f"/repos/{repo}/git/trees/{revision}?recursive=1")
    require(isinstance(tree, dict) and tree.get("truncated") is False, "Incomplete/truncated upstream tree")
    require(isinstance(tree.get("tree"), list), "Missing upstream tree inventory")
    require(all(isinstance(item, dict) and isinstance(item.get("path"), str) for item in tree["tree"]), "Malformed upstream tree entry")
    matches = [item for item in tree["tree"] if item.get("path") == path]
    require(len(matches) <= 1, "Ambiguous upstream tree path")
    if not matches:
        return None
    item = matches[0]
    require(item.get("type") in {"tree", "blob"} and isinstance(item.get("sha"), str) and bool(SHA.fullmatch(item["sha"])), "Invalid upstream tree object")
    return item["sha"]


def upstream_status(entry: dict[str, Any], reader: Any | None) -> dict[str, Any]:
    if entry.get("sourceType") in {"local-derived", "official-doc-derived"}:
        return {"status": "NOT_APPLICABLE", "reason": "Local/documentation-derived content still needs human review"}
    if reader is None:
        return {"status": "NOT_CHECKED", "reason": "Offline mode; review age does not prove upstream freshness"}
    try:
        repo, revision, path = github_source(entry)
    except (ValueError, TypeError):
        return {"status": "UNCOMPARABLE", "reason": "Canonical GitHub source, immutable revision, or upstream path is missing/unsupported"}
    try:
        commits = reader.get(f"/repos/{repo}/commits?per_page=1")
        require(isinstance(commits, list) and len(commits) == 1 and isinstance(commits[0], dict), "Missing upstream head")
        head = commits[0].get("sha")
        require(isinstance(head, str) and bool(SHA.fullmatch(head)), "Invalid upstream head revision")
        pinned = subtree_sha(reader, repo, revision, path)
        require(pinned is not None, "Pinned upstream Skill path is absent")
        current = subtree_sha(reader, repo, head, path)
        status = "UPSTREAM_PATH_MISSING" if current is None else "UNCHANGED" if current == pinned else "UPSTREAM_CHANGED"
        return {"status": status, "checkedAt": datetime.now(timezone.utc).isoformat(), "headRevision": head, "pinnedSubtree": pinned, "headSubtree": current}
    except (ValueError, TypeError, KeyError, OSError) as exc:
        return {"status": "UNKNOWN", "reason": str(exc)}


def report(lock: Any, as_of: date, review_days: int = 30, reader: Any | None = None) -> dict[str, Any]:
    require(isinstance(lock, dict) and isinstance(lock.get("skills"), dict) and bool(lock["skills"]), "Lock needs a nonempty skills object")
    require(type(review_days) is int and review_days > 0, "review-days must be a positive integer")
    rows = []
    for ident, entry in sorted(lock["skills"].items()):
        require(isinstance(entry, dict), f"Invalid lock entry: {ident}")
        require(isinstance(entry.get("knownIssues", []), list), f"Invalid knownIssues: {ident}")
        try:
            reviewed = iso_date(entry.get("reviewed"))
            require(reviewed <= as_of, "Review date is after the report date")
            age = (as_of - reviewed).days
            review = "REVIEW_DUE" if age >= review_days else "WITHIN_WINDOW"
        except (ValueError, TypeError):
            age, review = None, "UNKNOWN_REVIEW_DATE"
        rows.append({"id": ident, "reviewed": entry.get("reviewed"), "reviewAgeDays": age, "reviewStatus": review, "sourceTrust": entry.get("sourceTrust"), "behaviorStatus": entry.get("behaviorStatus"), "operationalRisk": entry.get("operationalRisk"), "knownIssueCount": len(entry.get("knownIssues", [])), "upstream": upstream_status(entry, reader)})
    upstream = Counter(row["upstream"]["status"] for row in rows)
    reviews = Counter(row["reviewStatus"] for row in rows)
    partial = bool(upstream.get("UNKNOWN") or reviews.get("UNKNOWN_REVIEW_DATE"))
    return {"schemaVersion": 1, "status": "PARTIAL" if partial else "REPORTED", "scope": "read-only-catalog-status-not-quality-certification", "asOf": as_of.isoformat(), "reviewDays": review_days, "online": reader is not None, "reviewCounts": dict(reviews), "upstreamCounts": dict(upstream), "skills": rows}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--online", action="store_true", help="Explicitly query public GitHub trees; no update/install.")
    parser.add_argument("--as-of", type=iso_date, default=date.today())
    parser.add_argument("--review-days", type=int, default=30)
    args = parser.parse_args()
    try:
        require(not args.online or args.as_of == date.today(), "Online observations must use today's date")
        result = report(load_json(ROOT / "catalog/skills.lock.json"), args.as_of, args.review_days, GitHubReader() if args.online else None)
        print(json.dumps(result, indent=2))
        return 2 if result["status"] == "PARTIAL" else 0
    except (OSError, ValueError, TypeError) as exc:
        print(json.dumps({"status": "ERROR", "message": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
