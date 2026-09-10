#!/usr/bin/env python3
"""Validate native AgentRC results; never invoke a model or infer host health."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True
from _audit_core import strip_jsonc
from quality import ROOT, local_path, load_json, require, text, unique_object


def load_suite(path: Path, root: Path = ROOT) -> dict[str, Any]:
    suite = json.loads(strip_jsonc(path.read_text(encoding="utf-8")), object_pairs_hook=unique_object)
    require(isinstance(suite, dict), "Eval suite must be an object")
    instruction = local_path(root, suite.get("instructionFile"))
    require(bool(instruction.read_text(encoding="utf-8").strip()), "Instruction-under-test is empty")
    cases = suite.get("cases")
    require(isinstance(cases, list) and bool(cases), "Eval suite is empty")
    seen: set[str] = set()
    for case in cases:
        require(isinstance(case, dict) and text(case.get("id")), "Invalid eval case id")
        require(case["id"] not in seen, "Duplicate eval case id")
        seen.add(case["id"])
        require(text(case.get("prompt")), "Eval case prompt is empty")
        expectation = case.get("expectation")
        require(text(expectation) or (isinstance(expectation, list) and bool(expectation) and all(text(x) for x in expectation)), "Eval expectation is empty/invalid")
        directory = case.get("workingDirectory", ".")
        require(isinstance(directory, str) and not Path(directory).is_absolute() and ".." not in Path(directory).parts, "Eval working directory escapes repository")
        target = (root / directory).resolve()
        require(target.is_relative_to(root.resolve()) and target.is_dir(), "Eval working directory is missing/unsafe")
    return suite


def capture_context(suite_path: Path, root: Path = ROOT) -> dict[str, Any]:
    suite = load_suite(suite_path, root)
    def git(*args: str) -> str:
        return subprocess.run(["git", "-C", str(root), *args], check=True,
                              capture_output=True, text=True, timeout=10).stdout.strip()
    require(not git("status", "--porcelain", "--untracked-files=normal"), "Native evaluation requires a clean checkout; write artifacts outside it")
    instruction = local_path(root, suite["instructionFile"])
    return {"schemaVersion": 1, "revision": git("rev-parse", "HEAD"),
            "suiteSha256": hashlib.sha256(suite_path.read_bytes()).hexdigest(),
            "instructionFile": suite["instructionFile"],
            "instructionSha256": hashlib.sha256(instruction.read_bytes()).hexdigest(),
            "capturedAt": datetime.now(timezone.utc).isoformat()}


def validate_context(saved: Any, current: dict[str, Any], report: Any) -> None:
    require(isinstance(saved, dict), "Run context must be an object")
    for key in ("schemaVersion", "revision", "suiteSha256", "instructionFile", "instructionSha256"):
        require(type(saved.get(key)) is type(current[key]) and saved.get(key) == current[key], f"Run context mismatch: {key}")
    require(isinstance(report, dict) and isinstance(report.get("runMetrics"), dict), "Native run metrics are missing")
    require(timestamp(saved.get("capturedAt")) <= timestamp(report["runMetrics"].get("startedAt")), "Context must be captured before the native run")


def timestamp(value: Any) -> datetime:
    require(text(value), "Run timestamp is missing")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(parsed.tzinfo is not None, "Run timestamps require a timezone")
    return parsed


def gate(suite: dict[str, Any], report: Any) -> dict[str, Any]:
    errors: list[str] = []
    results: list[Any] = []
    try:
        require(isinstance(report, dict), "Native report must be an object; --json stdout is not the --output result artifact")
        require(text(report.get("model")) and text(report.get("judgeModel")), "Model/judge provenance is missing")
        metrics = report.get("runMetrics")
        require(isinstance(metrics, dict), "Native run metrics are missing")
        started, finished = timestamp(metrics.get("startedAt")), timestamp(metrics.get("finishedAt"))
        require(started <= finished <= datetime.now(timezone.utc) + timedelta(minutes=1), "Invalid native run chronology")
        duration = metrics.get("durationMs")
        require(type(duration) in {int, float} and math.isfinite(duration) and duration >= 0, "Invalid native run duration")
        results = report.get("results")
        require(isinstance(results, list), "Native results array is missing")
        expected = {case["id"]: case for case in suite["cases"]}
        seen: set[str] = set()
        for result in results:
            require(isinstance(result, dict) and text(result.get("id")), "Invalid result record")
            ident = result["id"]
            require(ident in expected, f"Unexpected eval result: {ident}")
            require(ident not in seen, f"Duplicate eval result: {ident}")
            seen.add(ident)
            case = expected[ident]
            require(result.get("prompt") == case["prompt"] and result.get("expectation") == case["expectation"], f"Stale/different suite result: {ident}")
            require(text(result.get("withInstructions")) and text(result.get("withoutInstructions")), f"Missing comparison response: {ident}")
            require(text(result.get("rationale")), f"Missing judge rationale: {ident}")
            score = result.get("score")
            require(type(score) in {int, float} and math.isfinite(score) and 0 <= score <= 100, f"Invalid judge score: {ident}")
            if result.get("verdict") != "pass":
                errors.append(f"{ident}: {result.get('verdict', 'missing')} (requires pass)")
        missing = sorted(set(expected) - seen)
        require(not missing, f"Missing eval cases: {', '.join(missing)}")
    except (ValueError, TypeError, KeyError) as exc:
        errors.append(str(exc))
    count = len(results) if isinstance(results, list) else 0
    return {"status": "FAIL" if errors else "PASS", "scope": "native-agentrc-policy-response-evaluation-only", "expectedCases": len(suite["cases"]), "receivedCases": count, "errors": errors, "openCodeHostBehavior": "NOT RUN"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", type=Path, default=ROOT / "evaluation/agentrc.eval.jsonc")
    parser.add_argument("--report", type=Path)
    parser.add_argument("--context", type=Path)
    parser.add_argument("--capture-context", action="store_true")
    args = parser.parse_args()
    try:
        suite = load_suite(args.suite)
        require(not args.capture_context or (args.report is None and args.context is None), "Context capture cannot also validate a report")
        if args.capture_context:
            print(json.dumps(capture_context(args.suite), indent=2))
            return 0
        if args.report is None:
            require(args.context is None, "--context requires --report")
            print(json.dumps({"status": "PASS", "scope": "suite-schema-and-instruction-file-only", "cases": len(suite["cases"]), "modelBehavior": "NOT RUN"}, indent=2))
            return 0
        if not args.report.is_file():
            print(json.dumps({"status": "BLOCKED", "reason": "Native AgentRC report was not produced", "modelBehavior": "NOT RUN"}))
            return 2
        require(args.context is not None, "--report requires the pre-run --context record")
        native = load_json(args.report)
        validate_context(load_json(args.context), capture_context(args.suite), native)
        result = gate(suite, native)
        print(json.dumps(result, indent=2))
        return int(result["status"] != "PASS")
    except (OSError, ValueError, TypeError, subprocess.SubprocessError) as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc), "modelBehavior": "NOT RUN"}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
