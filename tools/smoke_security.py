#!/usr/bin/env python3
"""Run installed checkers on inert temporary fixtures, never on user source."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


def run(args: list[str], cwd: Path, expected: int = 0) -> subprocess.CompletedProcess:
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=180)
    if result.returncode != expected:
        # Do not echo findings, fixture contents or environment on failure.
        raise RuntimeError(f'{args[0]}: expected exit {expected}, got {result.returncode}')
    return result


def shellcheck(binary: str, root: Path) -> dict:
    clean, bad = root / 'clean.sh', root / 'bad.sh'
    clean.write_text('#!/bin/sh\nvalue="safe value"\nprintf "%s\\n" "$value"\n')
    bad.write_text('#!/bin/sh\nvalue="safe value"\nprintf "%s\\n" $value\n')
    run([binary, '--format=json', str(clean)], root)
    result = run([binary, '--format=json', str(bad)], root, 1)
    if not any(row['code'] == 2086 for row in json.loads(result.stdout)):
        raise RuntimeError('ShellCheck did not detect the intended unquoted expansion')
    return {'status': 'PASS', 'checks': ['clean-pass', 'SC2086-detected']}


def hadolint(binary: str, root: Path) -> dict:
    clean, bad = root / 'Dockerfile.clean', root / 'Dockerfile.bad'
    clean.write_text('FROM alpine:3.22.1\nUSER 10001\nCMD ["/bin/true"]\n')
    bad.write_text('FROM alpine:latest\nUSER 10001\nCMD ["/bin/true"]\n')
    run([binary, '--format', 'json', str(clean)], root)
    result = run([binary, '--format', 'json', str(bad)], root, 1)
    if not any(row['code'] == 'DL3007' for row in json.loads(result.stdout)):
        raise RuntimeError('Hadolint did not detect the intended floating image tag')
    return {'status': 'PASS', 'checks': ['clean-pass', 'DL3007-detected']}


def gitleaks(binary: str, root: Path) -> dict:
    repo = root / 'secret-fixture'
    repo.mkdir()
    # No real credential. Assemble an invalid synthetic token only in temp storage.
    sentinel = 'gh' + 'p_' + 'Ab3Cd4Ef5Gh6Ij7Kl8Mn9Op0Qr1St2Uv3Wx4'
    target = repo / 'sample.txt'
    target.write_text('public message\n')
    run(['git', 'init', '-q'], repo)
    run(['git', 'config', 'user.name', 'Fixture'], repo)
    run(['git', 'config', 'user.email', 'fixture@example.invalid'], repo)
    run(['git', 'add', '--', 'sample.txt'], repo)
    run(['git', '-c', 'core.hooksPath=/dev/null', 'commit', '-qm', 'clean baseline'], repo)
    report = root / 'gitleaks.json'
    args = [binary, 'git', '--staged', '--redact', '--no-banner', '--exit-code', '1', '--report-format', 'json', '--report-path', str(report), '.']
    run(args, repo)
    target.write_text('github_token=' + sentinel + '\n')
    run(['git', 'add', '--', 'sample.txt'], repo)
    target.write_text('public unstaged replacement\n')
    run(args, repo, 1)
    if not any(row.get('RuleID') == 'github-pat' for row in json.loads(report.read_text())):
        raise RuntimeError('Gitleaks did not detect the staged synthetic token')
    if sentinel in report.read_text():
        raise RuntimeError('Gitleaks report was not redacted')
    run(['git', 'add', '--', 'sample.txt'], repo)
    target.write_text('github_token=' + sentinel + '\n')
    run(args, repo)
    # Directory scanning sees the unstaged fixture, unlike the staged check.
    run([binary, 'dir', '--redact', '--no-banner', '--exit-code', '1', '.'], repo, 1)
    return {'status': 'PASS', 'checks': ['clean-index', 'staged-secret-clean-worktree-detected', 'clean-index-unstaged-secret-not-in-commit', 'directory-secret-detected', 'redacted-output']}


def trivy(binary: str, root: Path) -> dict:
    good, bad = root / 'trivy-good', root / 'trivy-bad'
    good.mkdir(); bad.mkdir()
    (good / 'Dockerfile').write_text('FROM alpine:3.22.1\nUSER 10001\nHEALTHCHECK CMD ["/bin/true"]\nCMD ["/bin/true"]\n')
    (bad / 'Dockerfile').write_text('FROM alpine:3.22.1\nUSER root\nHEALTHCHECK CMD ["/bin/true"]\nCMD ["/bin/true"]\n')
    output = root / 'trivy.json'
    # Built-in Dockerfile checks only: no claim of vulnerability DB or image scan.
    base = [binary, 'config', '--quiet', '--skip-check-update', '--misconfig-scanners', 'dockerfile', '--severity', 'HIGH,CRITICAL', '--include-non-failures', '--exit-code', '1', '--format', 'json', '--output', str(output)]
    run(base + [str(good)], root)
    parsed = json.loads(output.read_text())
    if not any(row.get('Class') == 'config' for row in parsed.get('Results', [])):
        raise RuntimeError('Trivy clean fixture scanned no configuration targets')
    run(base + [str(bad)], root, 1)
    parsed = json.loads(output.read_text())
    failures = [m for r in parsed.get('Results', []) for m in r.get('Misconfigurations', []) if m.get('Status') == 'FAIL']
    if not any('root' in (m.get('Title', '') + m.get('Description', '')).lower() for m in failures):
        raise RuntimeError('Trivy did not report the intended root-user misconfiguration')
    return {'status': 'PASS', 'checks': ['clean-config-target', 'root-user-detected'], 'vulnerabilityDatabase': 'NOT RUN', 'containerImage': 'NOT RUN'}


def main() -> int:
    checks = {'shellcheck': shellcheck, 'hadolint': hadolint, 'gitleaks': gitleaks, 'trivy': trivy}
    binaries = {name: shutil.which(name) for name in checks}
    missing = [name for name, path in binaries.items() if not path]
    if missing:
        print(json.dumps({'status': 'BLOCKED', 'missing': missing, 'scope': 'direct-fixtures-only'}))
        return 2
    results = {}
    with tempfile.TemporaryDirectory(prefix='agent-reference-security-') as directory:
        root = Path(directory)
        for name, check in checks.items():
            binary = binaries[name]
            flag = 'version' if name == 'gitleaks' else '--version'
            version = run([binary, flag], root).stdout.strip()
            results[name] = dict(check(binary, root), version=version)
    print(json.dumps({'status': 'PASS', 'scope': 'inert-local-fixtures-not-consumer-security-certification', 'results': results, 'workstationSetup': 'NOT RUN'}))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({'status': 'FAIL', 'reason': str(exc)}))
        raise SystemExit(1)
