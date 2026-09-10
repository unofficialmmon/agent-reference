"""Deterministic contract tests, not model or OpenCode behavior certification."""
from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError, URLError

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import quality as q
import freshness as f
import eval_gate as e

TODAY = date(2026, 9, 10)
SHA_A, SHA_B, TREE_A, TREE_B = "a" * 40, "b" * 40, "c" * 40, "d" * 40


def registry():
    return copy.deepcopy(q.load_json(ROOT / "catalog/tooling.json"))


def evidence():
    return copy.deepcopy(q.load_json(ROOT / "evaluation/evidence/tool-stack-2026-09-02.json"))


def suite():
    return {"instructionFile": "global/AGENTS.md", "cases": [
        {"id": "test-one", "prompt": "Report the failed check.", "expectation": ["Report FAIL"], "workingDirectory": "."},
        {"id": "test-two", "prompt": "Preserve existing work.", "expectation": "No overwrite", "workingDirectory": "."}]}


def native():
    return {"model": "explicit-response-model", "judgeModel": "explicit-judge-model",
            "runMetrics": {"startedAt": "2026-09-09T12:00:00Z", "finishedAt": "2026-09-09T12:01:00Z", "durationMs": 60000},
            "results": [dict(case, withInstructions="Observed response B", withoutInstructions="Observed response A",
                             rationale="Observable criteria checked", verdict="pass", score=90) for case in suite()["cases"]]}


def entry():
    return {"source": "https://github.com/example/upstream", "sourceType": "external", "revision": SHA_A,
            "upstreamPath": "skills/example", "reviewed": "2026-09-03", "knownIssues": []}


class Reader:
    def __init__(self, current=TREE_A, truncated=False, pinned=TREE_A):
        self.current, self.truncated, self.pinned = current, truncated, pinned
        self.calls = []

    def get(self, path):
        self.calls.append(path)
        if "commits?" in path:
            return [{"sha": SHA_B}]
        value = self.pinned if SHA_A in path else self.current
        return {"truncated": self.truncated, "tree": [] if value is None else [
            {"path": "skills/example", "type": "tree", "sha": value}]}


class RegistryTests(unittest.TestCase):
    def test_current_registry(self):
        self.assertEqual(len(q.validate_registry(registry(), TODAY)), 16)

    def test_schema_bool_rejected(self):
        d = registry(); d["schemaVersion"] = True
        with self.assertRaises(ValueError): q.validate_registry(d, TODAY)

    def test_duplicate_tool(self):
        d = registry(); d["tools"].append(d["tools"][0])
        with self.assertRaises(ValueError): q.validate_registry(d, TODAY)

    def test_future_policy_review(self):
        d = registry(); d["policyReviewedAt"] = "2099-01-01"
        with self.assertRaises(ValueError): q.validate_registry(d, TODAY)

    def test_unknown_policy(self):
        d = registry(); d["tools"][0]["policy"] = "probably-safe"
        with self.assertRaises(ValueError): q.validate_registry(d, TODAY)

    def test_companion_cannot_be_runtime(self):
        d = registry(); d["tools"][0]["kind"] = "companion"
        with self.assertRaises(ValueError): q.validate_registry(d, TODAY)

    def test_active_tool_needs_upstream(self):
        d = registry(); d["tools"][0]["upstream"] = None
        with self.assertRaises(ValueError): q.validate_registry(d, TODAY)

    def test_duplicate_json_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "invalid.json"; p.write_text('{"status":"FAIL","status":"PASS"}')
            with self.assertRaises(ValueError): q.load_json(p)

    def test_invalid_calendar_date(self):
        with self.assertRaises(ValueError): q.iso_date("2026-02-30")

    def test_projection_and_evidence_integration(self):
        self.assertEqual(q.check_repository(ROOT, TODAY)["errors"], [])

    def test_projection_drift_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); (root / "catalog").mkdir()
            (root / "catalog/tooling.json").write_text(json.dumps(registry()))
            (root / "README.md").write_text(q.tooling_table(registry()).replace("baseline", "retired", 1))
            result = q.check_repository(root, TODAY)
            self.assertTrue(any("policy drift" in x for x in result["errors"]))


class EvidenceTests(unittest.TestCase):
    def validate(self, data):
        return q.validate_evidence(data, q.validate_registry(registry(), TODAY), ROOT, TODAY)

    def test_historical_limitations_preserved(self):
        d = evidence(); self.validate(d)
        self.assertIsNone(d["environment"]["model"])

    def test_unknown_status_rejected(self):
        d = evidence(); d["checks"][0]["status"] = "LIKELY PASS"
        with self.assertRaises(ValueError): self.validate(d)

    def test_duplicate_check_rejected(self):
        d = evidence(); d["checks"].append(d["checks"][0])
        with self.assertRaises(ValueError): self.validate(d)

    def test_future_observation_rejected(self):
        d = evidence(); d["observedAt"] = "2099-01-01"
        with self.assertRaises(ValueError): self.validate(d)

    def test_missing_tool_version_rejected(self):
        d = evidence(); d["environment"]["versions"].pop(d["checks"][0]["tool"])
        with self.assertRaises(ValueError): self.validate(d)

    def test_historical_record_not_promoted_to_fresh_smoke(self):
        d = evidence(); d["evidenceClass"] = "host-smoke"
        with self.assertRaises(ValueError): self.validate(d)

    def test_fresh_pass_needs_artifact(self):
        d = evidence(); d["evidenceClass"] = "host-smoke"
        d["environment"].update(model="known-model", repositoryRevision=SHA_A)
        with self.assertRaises(ValueError): self.validate(d)

    def test_blocked_needs_reason(self):
        d = evidence(); d["checks"][0]["status"] = "BLOCKED"
        with self.assertRaises(ValueError): self.validate(d)

    def test_missing_limitations(self):
        d = evidence(); d["limitations"] = []
        with self.assertRaises(ValueError): self.validate(d)

    def test_escape_path_rejected(self):
        with self.assertRaises(ValueError): q.local_path(ROOT, "../secret")


class FreshnessTests(unittest.TestCase):
    def test_offline_never_current(self):
        self.assertEqual(f.upstream_status(entry(), None)["status"], "NOT_CHECKED")

    def test_local_does_not_fetch(self):
        d = entry(); d["sourceType"] = "local-derived"; reader = Reader()
        self.assertEqual(f.upstream_status(d, reader)["status"], "NOT_APPLICABLE")
        self.assertEqual(reader.calls, [])

    def test_unrelated_head_change_not_skill_change(self):
        self.assertEqual(f.upstream_status(entry(), Reader())["status"], "UNCHANGED")

    def test_subtree_change_detected(self):
        self.assertEqual(f.upstream_status(entry(), Reader(current=TREE_B))["status"], "UPSTREAM_CHANGED")

    def test_removed_path(self):
        self.assertEqual(f.upstream_status(entry(), Reader(current=None))["status"], "UPSTREAM_PATH_MISSING")

    def test_missing_pin_is_unknown(self):
        self.assertEqual(f.upstream_status(entry(), Reader(pinned=None))["status"], "UNKNOWN")

    def test_truncated_tree_is_unknown(self):
        self.assertEqual(f.upstream_status(entry(), Reader(truncated=True))["status"], "UNKNOWN")

    def test_unpinned_revision_uncomparable(self):
        d = entry(); d["revision"] = "main"
        self.assertEqual(f.upstream_status(d, Reader())["status"], "UNCOMPARABLE")

    def test_unsafe_paths_and_sources(self):
        for key, value in [("source", "https://evil.example/o/r"), ("source", "https://github.com@evil.example/o/r"),
                           ("upstreamPath", "../secret"), ("upstreamPath", "/etc/passwd"), ("upstreamPath", "skills//a")]:
            with self.subTest(key=key, value=value):
                d = entry(); d[key] = value
                with self.assertRaises(ValueError): f.github_source(d)

    def test_review_window_boundary(self):
        d = entry(); d["reviewed"] = "2026-08-11"
        result = f.report({"skills": {"test": d}}, TODAY)
        self.assertEqual(result["skills"][0]["reviewStatus"], "REVIEW_DUE")

    def test_unknown_review_stays_unknown(self):
        d = entry(); d["reviewed"] = None
        result = f.report({"skills": {"test": d}}, TODAY)
        self.assertEqual(result["status"], "PARTIAL")
        self.assertIsNone(result["skills"][0]["reviewAgeDays"])

    def test_future_review_not_fresh(self):
        d = entry(); d["reviewed"] = "2099-01-01"
        self.assertEqual(f.report({"skills": {"test": d}}, TODAY)["status"], "PARTIAL")

    def test_invalid_review_window(self):
        with self.assertRaises(ValueError): f.report({"skills": {"test": entry()}}, TODAY, 0)

    def test_reader_request_budget(self):
        with self.assertRaisesRegex(ValueError, "budget"):
            f.GitHubReader(max_requests=0).get("/repos/o/r/commits")

    def test_network_failure_stops_further_requests(self):
        reader = f.GitHubReader()
        with patch.object(reader.opener, "open", side_effect=URLError("offline")) as request:
            for suffix in ("/repos/o/r/a", "/repos/o/r/b"):
                with self.assertRaisesRegex(ValueError, "unavailable"): reader.get(suffix)
            self.assertEqual(request.call_count, 1)

    def test_rate_limit_stops_further_requests(self):
        reader = f.GitHubReader()
        with patch.object(reader.opener, "open", side_effect=HTTPError("url", 429, "secret detail", {}, None)) as request:
            for suffix in ("/repos/o/r/a", "/repos/o/r/b"):
                with self.assertRaisesRegex(ValueError, "HTTP 429"): reader.get(suffix)
            self.assertEqual(request.call_count, 1)

    def test_redirect_refused(self):
        with self.assertRaises(ValueError): f.NoRedirect().redirect_request(None, None, 302, "", {}, "https://evil.example")

    def test_cached_success(self):
        reader = f.GitHubReader(); reader.cache["/repos/o/r/a"] = {"cached": True}
        self.assertEqual(reader.get("/repos/o/r/a"), {"cached": True})
        self.assertEqual(reader.requests, 0)


class EvalTests(unittest.TestCase):
    def test_complete_native_report_passes(self):
        self.assertEqual(e.gate(suite(), native())["status"], "PASS")

    def test_summary_envelope_not_native_results(self):
        self.assertEqual(e.gate(suite(), {"ok": True, "status": "success", "data": {"summary": "PASS"}})["status"], "FAIL")

    def test_missing_result_fails(self):
        d = native(); d["results"].pop()
        self.assertEqual(e.gate(suite(), d)["status"], "FAIL")

    def test_duplicate_result_fails(self):
        d = native(); d["results"].append(d["results"][0])
        self.assertEqual(e.gate(suite(), d)["status"], "FAIL")

    def test_unexpected_result_fails(self):
        d = native(); d["results"][0]["id"] = "unknown"
        self.assertEqual(e.gate(suite(), d)["status"], "FAIL")

    def test_unknown_verdict_fails(self):
        d = native(); d["results"][0]["verdict"] = "unknown"
        self.assertEqual(e.gate(suite(), d)["status"], "FAIL")

    def test_required_failure_cannot_average_out(self):
        d = native(); d["results"][0]["verdict"] = "fail"
        self.assertEqual(e.gate(suite(), d)["status"], "FAIL")

    def test_stale_suite_fails(self):
        d = native(); d["results"][0]["prompt"] = "old prompt"
        self.assertEqual(e.gate(suite(), d)["status"], "FAIL")

    def test_invalid_score_fails(self):
        for value in (float("nan"), float("inf"), True, 101, "100"):
            with self.subTest(value=value):
                d = native(); d["results"][0]["score"] = value
                self.assertEqual(e.gate(suite(), d)["status"], "FAIL")

    def test_empty_responses_fails(self):
        d = native(); d["results"][0]["withInstructions"] = ""
        self.assertEqual(e.gate(suite(), d)["status"], "FAIL")

    def test_future_report_fails(self):
        d = native(); d["runMetrics"]["finishedAt"] = "2099-01-01T00:00:00Z"
        self.assertEqual(e.gate(suite(), d)["status"], "FAIL")

    def test_timezone_required(self):
        with self.assertRaises(ValueError): e.timestamp("2026-09-09T00:00:00")

    def test_repository_suite_is_17_and_explicit(self):
        d = e.load_suite(ROOT / "evaluation/agentrc.eval.jsonc")
        self.assertEqual(len(d["cases"]), 17)
        self.assertEqual(d["instructionFile"], "global/AGENTS.md")

    def test_missing_instruction_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); p = root / "suite.json"; p.write_text(json.dumps(suite()))
            with self.assertRaises(ValueError): e.load_suite(p, root)

    def test_suite_duplicate_cases_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); (root / "global").mkdir(); (root / "global/AGENTS.md").write_text("Rules")
            d = suite(); d["cases"].append(d["cases"][0]); p = root / "suite.json"; p.write_text(json.dumps(d))
            with self.assertRaises(ValueError): e.load_suite(p, root)

    def test_context_revision_and_hash_binding(self):
        saved = {"schemaVersion": 1, "revision": SHA_A, "suiteSha256": "1" * 64, "instructionFile": "global/AGENTS.md",
                 "instructionSha256": "2" * 64, "capturedAt": "2026-09-09T11:59:00Z"}
        e.validate_context(saved, saved, native())
        for key in ("revision", "suiteSha256", "instructionSha256"):
            with self.subTest(key=key):
                changed = dict(saved); changed[key] = "different"
                with self.assertRaises(ValueError): e.validate_context(saved, changed, native())

    def test_context_cannot_be_backfilled_after_run(self):
        d = {"schemaVersion": 1, "revision": SHA_A, "suiteSha256": "1", "instructionFile": "global/AGENTS.md",
             "instructionSha256": "2", "capturedAt": "2026-09-09T12:10:00Z"}
        with self.assertRaises(ValueError): e.validate_context(d, d, native())

    def test_context_capture_requires_clean_checkout(self):
        with patch.object(e.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, " M global/AGENTS.md\n", "")):
            with self.assertRaisesRegex(ValueError, "clean checkout"):
                e.capture_context(ROOT / "evaluation/agentrc.eval.jsonc")

    def test_missing_native_report_cli_is_blocked(self):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        proc = subprocess.run([sys.executable, str(ROOT / "tools/eval_gate.py"), "--report", "/not-existing/report.json"], capture_output=True, text=True, env=env)
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(json.loads(proc.stdout)["status"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
