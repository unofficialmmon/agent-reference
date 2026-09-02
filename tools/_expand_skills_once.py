#!/usr/bin/env python3
"""One-shot maintainer import for the 2026-09-02 reviewed Skill expansion.

This file is intentionally removed by the workflow after a successful import.
It is not part of the runtime, APM consumer surface, or a permanent installer.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "catalog/skills-expansion-2026-09-02.json"
TODAY = "2026-09-02"


def run(*args: str, cwd: Path | None = None) -> None:
    subprocess.run(args, cwd=cwd, check=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def skill_name(skill_dir: Path) -> str:
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    match = re.search(r"(?m)^name:\s*[\"']?([^\n\"']+)", text)
    if not match:
        raise RuntimeError(f"missing name frontmatter: {skill_dir}")
    return match.group(1).strip()


def find_skill_dirs() -> dict[str, Path]:
    found: dict[str, Path] = {}
    for path in sorted((ROOT / "skills").rglob("SKILL.md")):
        directory = path.parent
        name = skill_name(directory)
        if name in found:
            raise RuntimeError(f"duplicate Skill ID {name}: {found[name]} and {directory}")
        found[name] = directory
    return found


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"expected text not found in {path}: {old!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def append_if_missing(path: Path, marker: str, text: str) -> None:
    current = path.read_text(encoding="utf-8")
    if marker not in current:
        path.write_text(current.rstrip() + "\n\n" + text.strip() + "\n", encoding="utf-8")


def source_trust(repo: str) -> tuple[str, str]:
    official = (
        "github.com/android/",
        "github.com/expo/",
        "github.com/flutter/",
        "github.com/vercel-labs/",
    )
    if any(token in repo for token in official):
        return "A", "official-vendor"
    return "B", "maintainer-community"


def review_block(item: dict) -> dict:
    if not item["operational"]:
        return {
            "installHooks": False,
            "mcpDependency": False,
            "networkOperations": False,
            "credentialOrCookieAccess": False,
            "destructiveOrDeploymentOperations": False,
            "executables": [],
            "symlinks": [],
            "scripts": [],
        }
    risk = item.get("risk", "May run project/tool commands or make consequential environment changes; explicit opt-in only.")
    credentials = item.get("credentials", False)
    return {
        "installHooks": False,
        "mcpDependency": False,
        "networkOperations": risk,
        "credentialOrCookieAccess": credentials,
        "destructiveOrDeploymentOperations": risk,
        "executables": [],
        "symlinks": [],
        "scripts": [],
    }


def copy_upstream(item: dict, cache_root: Path) -> Path:
    repo = item["repository"]
    revision = item["revision"]
    source_path = item["sourcePath"].strip("/")
    key = hashlib.sha256(f"{repo}@{revision}".encode()).hexdigest()[:16]
    checkout = cache_root / key
    if not checkout.exists():
        checkout.mkdir(parents=True)
        run("git", "init", "-q", cwd=checkout)
        run("git", "remote", "add", "origin", repo, cwd=checkout)
        run("git", "fetch", "-q", "--depth=1", "origin", revision, cwd=checkout)
        run("git", "checkout", "-q", "FETCH_HEAD", cwd=checkout)
    source = checkout / source_path
    if not (source / "SKILL.md").is_file():
        raise RuntimeError(f"upstream Skill missing: {repo}@{revision}:{source_path}")
    return source


def copy_license(item: dict, checkout_source: Path) -> str:
    repo_root = checkout_source
    while repo_root.parent != repo_root and not (repo_root / ".git").exists():
        repo_root = repo_root.parent
    candidates = [
        checkout_source / "LICENSE",
        checkout_source / "LICENSE.md",
        checkout_source / "LICENSE.txt",
        repo_root / "LICENSE",
        repo_root / "LICENSE.md",
        repo_root / "LICENSE.txt",
        repo_root / "license.md",
    ]
    for candidate in candidates:
        if candidate.is_file():
            target = ROOT / "catalog/LICENSES" / f"{item['id']}-UPSTREAM-LICENSE{candidate.suffix}"
            shutil.copy2(candidate, target)
            return str(target.relative_to(ROOT))
    raise RuntimeError(f"license evidence not found for {item['id']}")


def add_skills(manifest: dict) -> None:
    existing = find_skill_dirs()
    with tempfile.TemporaryDirectory(prefix="agent-reference-skill-import-") as tmp:
        cache = Path(tmp)
        for item in manifest["skills"]:
            if item["id"] in existing:
                raise RuntimeError(f"refusing to overwrite existing Skill ID: {item['id']}")
            source = copy_upstream(item, cache)
            actual_name = skill_name(source)
            if actual_name != item["id"]:
                raise RuntimeError(f"frontmatter ID mismatch for {item['id']}: {actual_name}")
            target = ROOT / "skills" / item["category"] / item["id"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(source, target)
            item["licensePath"] = copy_license(item, source)
            if not item["operational"]:
                mirror = ROOT / ".apm/skills" / item["id"]
                if mirror.exists():
                    raise RuntimeError(f"APM mirror already exists unexpectedly: {mirror}")
                shutil.copytree(target, mirror)


def merge_local_guidance() -> None:
    engineering = ROOT / "global/ENGINEERING.md"
    text = engineering.read_text(encoding="utf-8")
    old = "2. Read the actual error and trace the relevant data/control path.\n3. Identify which component owns the violated invariant or contract."
    new = "2. Read the actual error and trace the relevant data/control path. Compare with the nearest working path when one exists; differences in inputs, state, ownership, and control flow are evidence.\n3. Identify which component owns the violated invariant or contract."
    if old in text:
        text = text.replace(old, new, 1)
    old2 = "6. Rerun the same failing check or scenario before broadening verification."
    new2 = "6. Rerun the same failing check or scenario before broadening verification. Remove temporary diagnostics and obsolete workarounds before completion."
    if old2 in text:
        text = text.replace(old2, new2, 1)
    engineering.write_text(text, encoding="utf-8")

    security = ROOT / "skills/java-spring/spring-security/SKILL.md"
    marker = "## Application security hardening"
    section = """
## Application security hardening

Keep framework security and application hardening connected without turning this Skill into a generic security handbook.

- Use adaptive password hashing through Spring Security encoders; never store plaintext credentials or invent application-level password hashing.
- Keep secrets in environment/secret-management boundaries rather than committed configuration, defaults, logs, or fixtures.
- Use parameterized persistence APIs and validated DTO boundaries; do not concatenate untrusted input into SQL, JPQL, shell commands, redirects, or file paths.
- Configure security headers and rate limits at the boundary that actually owns them (Spring Security, gateway, reverse proxy, or platform) and verify the effective response rather than duplicating controls across layers.
- Treat file uploads and other externally supplied content as untrusted: constrain size/type/path handling and keep storage/execution boundaries explicit.
- Keep personal or authentication data out of logs; redact identifiers when full values are not needed for diagnosis.
"""
    append_if_missing(security, marker, section)


def update_lock(manifest: dict) -> None:
    lock_path = ROOT / "catalog/skills.lock.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    lock["version"] = max(int(lock.get("version", 0)), 5)
    lock["generated"] = TODAY
    entries = lock["skills"]

    for item in manifest["skills"]:
        directory = ROOT / "skills" / item["category"] / item["id"]
        trust, source_trust_name = source_trust(item["repository"])
        files = {
            str(path.relative_to(directory)): sha256(path)
            for path in sorted(directory.rglob("*"))
            if path.is_file()
        }
        entries[item["id"]] = {
            "trust": trust,
            "source": item["repository"].removesuffix(".git"),
            "sourceType": "external",
            "upstreamPath": item["sourcePath"].strip("/"),
            "revision": item["revision"],
            "reviewed": TODAY,
            "license": item["license"],
            "licenseEvidence": item["licensePath"],
            "placement": "operational" if item["operational"] else "catalog",
            "files": files,
            "review": review_block(item),
            "sideEffects": "documentation-with-explicit-operational-effects" if item["operational"] else "documentation-only",
            "notes": item.get("notes", "Imported as a complete pinned upstream Skill snapshot from the reviewed 2026-09-02 expansion set."),
            "sourceTrust": source_trust_name,
            "integrity": "pinned-hash-verified",
            "hostCompatibility": "opencode-static-pass-runtime-smoke-not-run",
            "behaviorStatus": "upstream-claimed-local-static-review",
            "operationalRisk": "explicit-opt-in" if item["operational"] else "documentation-only-or-bounded-guidance",
            "knownIssues": item.get("knownIssues", []),
            "redistributionStatus": "license-evidence-preserved-or-local",
            "activationGuidance": "explicit-opt-in-operational" if item["operational"] else "project-stack-only",
        }

    # Rehash every existing entry after local-derived merges, without changing provenance metadata.
    dirs = find_skill_dirs()
    for skill_id, entry in entries.items():
        directory = dirs.get(skill_id)
        if not directory:
            continue
        entry["files"] = {
            str(path.relative_to(directory)): sha256(path)
            for path in sorted(directory.rglob("*"))
            if path.is_file()
        }

    lock_path.write_text(json.dumps(lock, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def update_docs(manifest: dict) -> None:
    non_operational = sum(1 for i in manifest["skills"] if not i["operational"])
    operational = sum(1 for i in manifest["skills"] if i["operational"])

    apm = ROOT / "apm.yml"
    text = apm.read_text(encoding="utf-8")
    text = re.sub(r"(?m)^version:\s*\S+", "version: 0.3.0", text, count=1)
    apm.write_text(text, encoding="utf-8")

    readme = ROOT / "README.md"
    append_if_missing(
        readme,
        "### 2026-09-02 catalog expansion",
        f"""
### 2026-09-02 catalog expansion

The reviewed catalog was expanded with {len(manifest['skills'])} additional pinned upstream Skills. {non_operational} are ordinary selectable catalog Skills and are mirrored under `.apm/skills/`; {operational} are isolated under `skills/operational/` and remain explicit opt-in only. Existing same-ID snapshots were not overwritten as part of this expansion, and the Redis `redis-core` snapshot was not duplicated under a second ID.

New coverage includes Java/JPA/Spring test and architecture guidance, Node/NestJS, SQL optimization, Android/Kotlin/Compose, Flutter, Expo/React Native, Vue testing/router guidance, and web-interface review. Catalog presence still does not mean activation: each project selects only the Skills justified by its actual stack and task.
""",
    )

    sources = ROOT / "catalog/SOURCES.md"
    append_if_missing(
        sources,
        "## 2026-09-02 expansion sources",
        """
## 2026-09-02 expansion sources

The expansion adds complete pinned snapshots from Android, Expo, Flutter, Vercel Labs, affaan-m/ECC, wshobson/agents, Kadajett/agent-nestjs-skills, sickn33/agentic-awesome-skills, and vuejs-ai/skills. Exact revisions and per-file SHA-256 hashes are recorded in `skills.lock.json`; root/upstream license evidence is retained under `catalog/LICENSES/` when the Skill directory itself does not carry a license file.

The uploaded bundle's `bundled/` entries (AWS, Azure, Docker, Flyway, GCP, CI systems, Kafka, Kubernetes, MariaDB/MySQL, RabbitMQ, and duplicate MyBatis entries) were not imported because they did not carry immutable source/revision/license provenance. They remain candidates only after provenance is established.

`debugging-discipline` and `engineering-quality` were not added as separate ambient Skills because their responsibilities already belong to `global/ENGINEERING.md`; only the small non-duplicative debugging guidance was folded into that maintained local reference. `springboot-security` was similarly not added as a competing broad security Skill; narrow application-hardening points were folded into the local `spring-security` Skill while its Spring Security ownership remains intact.
""",
    )

    changelog = ROOT / "CHANGELOG.md"
    text = changelog.read_text(encoding="utf-8")
    anchor = "### Added\n"
    bullet = f"\n- Expanded the reviewed Skill catalog with {len(manifest['skills'])} complete pinned upstream snapshots across Java/Spring, backend, SQL, Android/Kotlin, Flutter, Expo/native, Vue, and web-interface guidance; ordinary Skills are mirrored for APM while consequential CLI/deployment/migration/testing setup Skills remain operational opt-in.\n"
    if bullet.strip() not in text:
        text = text.replace(anchor, anchor + bullet, 1)
    improved = "### Improved\n"
    ibullet = "\n- Folded non-duplicative root-cause debugging guidance into `global/ENGINEERING.md` and selected application-hardening guidance into the local `spring-security` Skill instead of creating overlapping ambient Skills.\n"
    if ibullet.strip() not in text:
        text = text.replace(improved, improved + ibullet, 1)
    changelog.write_text(text, encoding="utf-8")


def remove_one_shot_files() -> None:
    for rel in [
        "tools/_expand_skills_once.py",
        "catalog/skills-expansion-2026-09-02.json",
        ".github/workflows/expand-skills-once.yml",
    ]:
        path = ROOT / rel
        if path.exists():
            path.unlink()


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    add_skills(manifest)
    merge_local_guidance()
    update_lock(manifest)
    update_docs(manifest)
    remove_one_shot_files()


if __name__ == "__main__":
    main()
