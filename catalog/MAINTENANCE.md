# Catalog and tooling maintenance

## Independent signals, not one quality score

Keep source trust, immutable content hashes, runtime evidence, known issues, operational risk, review age, and upstream content status separate. No weighted aggregate can certify suitability. `skills.lock.json` already owns Skill review dates (`reviewed`) and provenance; never refresh dates simply because an automated check ran.

```bash
python3 tools/freshness.py
python3 tools/freshness.py --as-of 2026-09-10 --review-days 30
python3 tools/freshness.py --online
```

Offline mode reports `WITHIN_WINDOW`, `REVIEW_DUE`, or `UNKNOWN_REVIEW_DATE`. Thirty days is a configurable review reminder, not an expiry/security guarantee. Upstream is `NOT_CHECKED` offline and `NOT_APPLICABLE` for local/documentation-derived content, which still requires human review.

Online mode performs only bounded GitHub GETs. It compares the recorded upstream Skill subtree at the pinned revision with that subtree at the current default-branch head. `UNCHANGED` concerns upstream content only, not execution or deployed local bytes. `UPSTREAM_CHANGED` and `UPSTREAM_PATH_MISSING` require review, not automatic upgrades/deletion. Incomplete pins/paths are `UNCOMPARABLE`; network, rate-limit, malformed, truncated, or missing pinned-tree evidence is `UNKNOWN`, never current. Renamed repositories require explicit provenance review; redirects are refused. A changed repository HEAD alone does not imply a changed Skill.

Requests are cached per run, bounded by request count/timeout/response size, and stop on auth/rate/network failure. Optional `GITHUB_TOKEN` is sent only to the fixed GitHub API endpoint and is not logged. Output is JSON on stdout; the tool never writes snapshots, locks, selections, or user configuration. Exit codes: 0 complete report, 2 partial/unknown observations, 1 invalid input. Findings such as `REVIEW_DUE` are not silently promoted to test failures.

After a candidate is reviewed, use the existing full-directory snapshot replacement, attribution, lock hash, and exact APM mirror workflow. Do not patch vendor bytes or create an automatic updater.

## Tool policy

`tooling.json` owns approved roles and policy states, not machine installation or current compatibility. Historical smoke evidence lives under `evaluation/evidence/`; `historical-summary` explicitly means prior prose was transcribed without fresh raw logs. A new `host-smoke` requires model, tested revision, versions, and local redacted evidence artifacts for executed checks. The validator checks schema/references, not authenticity or runtime success.

After an explicit tool-policy review, update the registry and its checked README projection together:

```bash
python3 tools/quality.py --tooling-table
python3 tools/audit.py
```

The first command prints a table; replace only the README marker block. Setup reads the registry instead of maintaining a separate authoritative list. Human explanations elsewhere do not override it. Registry/evidence validation and CI artifacts contain no secrets; inspect/redact runtime logs before committing them.

The `catalog-freshness-report` workflow runs weekly, on relevant PRs, or manually. It only produces observations. Exit 2 (`PARTIAL`) becomes an explicit warning and summary, not a claim that upstreams passed; malformed input (exit 1) still fails the job. Test/audit gates never use that report-only exception.
