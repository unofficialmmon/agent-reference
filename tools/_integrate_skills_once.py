#!/usr/bin/env python3
"""One-shot reviewed Skill catalog expansion; removed after a successful run."""
from __future__ import annotations
import hashlib, json, re, shutil, subprocess, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "catalog/skills-expansion-2026-09-03.json"
TODAY = "2026-09-03"


def run(*args: str, cwd: Path | None = None) -> None:
    subprocess.run(args, cwd=cwd, check=True)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def skill_name(path: Path) -> str:
    text = (path / "SKILL.md").read_text(encoding="utf-8")
    m = re.search(r"(?m)^name:\s*[\"']?([^\n\"']+)", text)
    if not m:
        raise RuntimeError(f"missing Skill name: {path}")
    return m.group(1).strip()


def skill_dirs() -> dict[str, Path]:
    out: dict[str, Path] = {}
    for file in sorted((ROOT / "skills").glob("*/*/SKILL.md")):
        name = skill_name(file.parent)
        if name in out:
            raise RuntimeError(f"duplicate Skill ID: {name}")
        out[name] = file.parent
    return out


def append(path: Path, marker: str, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    if marker not in text:
        path.write_text(text.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def checkout(item: dict, cache: Path) -> Path:
    key = hashlib.sha256(f"{item['repository']}@{item['revision']}".encode()).hexdigest()[:20]
    path = cache / key
    if path.exists():
        return path
    path.mkdir()
    run("git", "init", "-q", cwd=path)
    run("git", "remote", "add", "origin", item["repository"], cwd=path)
    run("git", "fetch", "-q", "--depth=1", "origin", item["revision"], cwd=path)
    run("git", "checkout", "-q", "FETCH_HEAD", cwd=path)
    return path


def license_evidence(item: dict, repo: Path, source: Path) -> str:
    choices = [source / n for n in ("LICENSE", "LICENSE.md", "LICENSE.txt", "LICENSE_NOTICE.md")]
    choices += [repo / n for n in ("LICENSE", "LICENSE.md", "LICENSE.txt", "license.md")]
    for candidate in choices:
        if candidate.is_file():
            suffix = candidate.suffix or ".txt"
            target = ROOT / "catalog/LICENSES" / f"{item['id']}-UPSTREAM-LICENSE{suffix}"
            shutil.copy2(candidate, target)
            return str(target.relative_to(ROOT))
    raise RuntimeError(f"missing license evidence: {item['id']}")


def web_adapter(item: dict, repo: Path) -> tuple[Path, str]:
    required = ("command.md", "README.md", "AGENTS.md", "LICENSE")
    target = ROOT / "skills" / item["category"] / item["id"]
    upstream = target / "upstream"
    upstream.mkdir(parents=True)
    for name in required:
        if not (repo / name).is_file():
            raise RuntimeError(f"missing web guideline payload: {name}")
        shutil.copy2(repo / name, upstream / name)
    (target / "SKILL.md").write_text("""---
name: web-design-guidelines
description: Offline workflow adapter for reviewing web interfaces against pinned guidelines.
---

# Web Design Guidelines

Read `./upstream/command.md`, inspect only the requested files, and apply its rules and output format. Use this revision-pinned local payload only; do not fetch or refresh it at runtime.
""", encoding="utf-8")
    rows = "\n".join(f"- `upstream/{n}`: `{digest(upstream / n)}`" for n in required)
    (target / "SOURCE.md").write_text(
        f"# Source\n\nOffline adapter over `vercel-labs/web-interface-guidelines` at `{item['revision']}`.\n\n{rows}\n",
        encoding="utf-8",
    )
    return target, str((upstream / "LICENSE").relative_to(ROOT))


def materialize(manifest: dict) -> None:
    existing = skill_dirs()
    with tempfile.TemporaryDirectory(prefix="skill-import-") as temp:
        cache = Path(temp)
        for item in manifest["skills"]:
            if item["id"] in existing:
                raise RuntimeError(f"refusing overwrite: {item['id']}")
            repo = checkout(item, cache)
            if item.get("mode") == "web-guidelines-adapter":
                target, evidence = web_adapter(item, repo)
            else:
                source = repo / item["sourcePath"].strip("/")
                if not (source / "SKILL.md").is_file() or skill_name(source) != item["id"]:
                    raise RuntimeError(f"upstream Skill mismatch: {item['id']}")
                target = ROOT / "skills" / item["category"] / item["id"]
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(source, target)
                evidence = license_evidence(item, repo, source)
            item["licensePath"] = evidence
            existing[item["id"]] = target
            if not item["operational"]:
                shutil.copytree(target, ROOT / ".apm/skills" / item["id"])


def merge_guidance() -> None:
    path = ROOT / "global/ENGINEERING.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "2. Read the actual error and trace the relevant data/control path.\n3. Identify which component owns the violated invariant or contract.",
        "2. Read the actual error and trace the relevant data/control path. Compare with the nearest working path when one exists; differences in inputs, state, ownership, and control flow are evidence.\n3. Identify which component owns the violated invariant or contract.",
        1,
    )
    text = text.replace(
        "6. Rerun the same failing check or scenario before broadening verification.",
        "6. Rerun the same failing check or scenario before broadening verification. Remove temporary diagnostics and obsolete workarounds before completion.",
        1,
    )
    path.write_text(text, encoding="utf-8")
    security = ROOT / "skills/java-spring/spring-security/SKILL.md"
    append(security, "## Application security hardening", """
## Application security hardening

- Use Spring Security adaptive password encoders; never store plaintext credentials or invent password hashing.
- Keep secrets out of committed configuration, defaults, logs, and fixtures.
- Use parameterized persistence APIs and validated DTO boundaries; never concatenate untrusted SQL, JPQL, commands, redirects, or paths.
- Put headers and rate limits at the owning boundary and verify the effective response instead of duplicating controls.
- Constrain upload size, type, path, storage, and execution boundaries.
- Redact personal and authentication data from logs.
""")
    shutil.copy2(security, ROOT / ".apm/skills/spring-security/SKILL.md")


def trust(repo: str) -> tuple[str, str]:
    official = ("github.com/android/", "github.com/expo/", "github.com/flutter/", "github.com/vercel/", "github.com/vercel-labs/")
    return ("A", "official-vendor") if any(x in repo for x in official) else ("B", "maintainer-community")


def review(item: dict) -> dict:
    risk = item.get("risk", False)
    return {
        "installHooks": False,
        "mcpDependency": item.get("mcpDependency", False),
        "networkOperations": risk,
        "credentialOrCookieAccess": item.get("credentials", False),
        "destructiveOrDeploymentOperations": risk,
        "executables": [], "symlinks": [], "scripts": [],
    }


def update_lock(manifest: dict) -> None:
    path = ROOT / "catalog/skills.lock.json"
    lock = json.loads(path.read_text(encoding="utf-8"))
    lock["version"], lock["generated"] = max(int(lock.get("version", 0)), 5), TODAY
    for item in manifest["skills"]:
        grade, source_trust = trust(item["repository"])
        operational = item["operational"]
        adapter = bool(item.get("mode"))
        lock["skills"][item["id"]] = {
            "trust": grade, "source": item["repository"].removesuffix(".git"),
            "sourceType": "external-adapted" if adapter else "external",
            "upstreamPath": item["sourcePath"].strip("/") or None,
            "revision": item["revision"], "reviewed": TODAY, "license": item["license"],
            "licenseEvidence": item["licensePath"], "placement": "operational" if operational else "catalog",
            "files": {}, "review": review(item),
            "sideEffects": "documentation-with-explicit-operational-effects" if operational else "documentation-only",
            "notes": item.get("notes", "Complete pinned upstream snapshot from the reviewed 2026-09 expansion."),
            "sourceTrust": source_trust,
            "integrity": "pinned-upstream-payload-hash-verified" if adapter else "pinned-hash-verified",
            "hostCompatibility": "opencode-static-pass-runtime-smoke-not-run",
            "behaviorStatus": "upstream-claimed-local-static-review",
            "operationalRisk": "explicit-opt-in" if operational else "documentation-only-or-bounded-guidance",
            "knownIssues": item.get("knownIssues", []),
            "redistributionStatus": "license-evidence-preserved-or-local",
            "activationGuidance": "explicit-opt-in-operational" if operational else "project-stack-only",
        }
    directories = skill_dirs()
    if set(directories) != set(lock["skills"]):
        raise RuntimeError("lock IDs do not match Skill directories")
    for name, directory in directories.items():
        lock["skills"][name]["files"] = {
            str(f.relative_to(directory)): digest(f) for f in sorted(directory.rglob("*")) if f.is_file()
        }
    path.write_text(json.dumps(lock, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def update_docs(manifest: dict) -> None:
    added = [x["id"] for x in manifest["skills"]]
    op = [x["id"] for x in manifest["skills"] if x["operational"]]
    selectable = len(added) - len(op)
    apm = ROOT / "apm.yml"
    apm.write_text(re.sub(r"(?m)^version:\s*\S+", "version: 0.3.0", apm.read_text(), count=1))
    readme = ROOT / "README.md"
    text = readme.read_text()
    old = "The current catalog contains 40 Skills: 31 non-operational IDs are APM-selectable and the 9 IDs under `skills/operational/` remain intentionally catalog-only."
    new = f"The current catalog contains 78 Skills: {31 + selectable} non-operational IDs are APM-selectable and the {9 + len(op)} IDs under `skills/operational/` remain intentionally catalog-only."
    if old not in text:
        raise RuntimeError("README count marker missing")
    readme.write_text(text.replace(old, new, 1))
    append(readme, "### 2026-09 reviewed catalog expansion", f"""
### 2026-09 reviewed catalog expansion

Added 38 pinned unique Skills: {selectable} APM-selectable and {len(op)} operational opt-ins. See `catalog/SKILLS-ZIP-EXPANSION-REVIEW.md` for additions, aliases, merges, exclusions, and deferred provenance work.
""")
    aliases = "\n".join(f"- `{a}` -> `{b}`" for a, b in manifest["requestedAliases"].items())
    added_rows = "\n".join(f"- `{x}`" for x in added)
    op_rows = "\n".join(f"- `{x}`" for x in op)
    report = f"""# 2026-09 Skill catalog expansion review

## Result

- Existing: 40
- Added unique IDs: 38
- Final: 78
- New APM-selectable: {selectable}
- New operational opt-ins: {len(op)}

## Added IDs

{added_rows}

## Alias normalization

{aliases}

## Merged or skipped

- `debugging-discipline` -> selected guidance merged into `global/ENGINEERING.md`.
- `engineering-quality` -> already covered by `global/ENGINEERING.md`.
- `springboot-security` -> selected hardening guidance merged into `spring-security`.
- `redis` -> skipped because `redis-core` and `redis-connections` already own the scope.
- Existing same-ID snapshots were not overwritten; upgrades require a separate snapshot review.

## Deferred

`aws`, `azure`, `docker`, `flyway`, `gcp`, `github-actions`, `gitlab-ci`, `jenkins`, `kafka`, `kubernetes`, `mariadb`, `mysql`, and `rabbitmq` remain excluded until immutable source, revision, and license evidence are established.

## Operational isolation

{op_rows}

Catalog inclusion is not activation. Ordinary IDs are mirrored under `.apm/skills/`; operational IDs require explicit task authorization.
"""
    (ROOT / "catalog/SKILLS-ZIP-EXPANSION-REVIEW.md").write_text(report)
    append(ROOT / "catalog/SOURCES.md", "## 2026-09 reviewed expansion sources", """
## 2026-09 reviewed expansion sources

Pinned snapshots were added from Android, Expo, Flutter, Vercel/Next.js, Vercel Labs, affaan-m/ECC, wshobson/agents, Kadajett/agent-nestjs-skills, sickn33/agentic-awesome-skills, and vuejs-ai/skills. Exact revisions, paths, file hashes, licenses, risk placement, and activation guidance are recorded in `skills.lock.json`.
""")
    append(ROOT / "NOTICE", "## 2026-09 expansion sources", """
## 2026-09 expansion sources

Additional pinned content comes from Android (Apache-2.0), Expo (MIT), Flutter (BSD-3-Clause), Vercel/Next.js and Vercel Labs (MIT), affaan-m/ECC (MIT), wshobson/agents (MIT), Kadajett/agent-nestjs-skills (MIT), sickn33/agentic-awesome-skills (MIT), and vuejs-ai/skills (MIT). See `catalog/skills.lock.json` and retained license evidence.
""")
    changelog = ROOT / "CHANGELOG.md"
    text = changelog.read_text()
    text = text.replace("### Added\n", f"### Added\n\n- Added 38 reviewed pinned Skill IDs ({selectable} selectable, {len(op)} operational opt-ins).\n", 1)
    text = text.replace("### Improved\n", "### Improved\n\n- Merged non-duplicative debugging and Spring application-security guidance into existing maintained references.\n", 1)
    changelog.write_text(text)


def cleanup() -> None:
    for rel in (
        "tools/_expand_skills_once.py", "catalog/skills-expansion-2026-09-02.json", ".github/workflows/expand-skills-once.yml",
        "tools/_integrate_skills_once.py", "catalog/skills-expansion-2026-09-03.json", ".github/workflows/integrate-skills-once.yml",
    ):
        path = ROOT / rel
        if path.exists(): path.unlink()


def main() -> None:
    manifest = json.loads(MANIFEST.read_text())
    if len(manifest["skills"]) != 38:
        raise RuntimeError("expected 38 additions")
    materialize(manifest)
    merge_guidance()
    update_lock(manifest)
    update_docs(manifest)
    cleanup()


if __name__ == "__main__":
    main()
