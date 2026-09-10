#!/usr/bin/env python3
"""Exercise an already installed ast-grep in disposable fixtures; no installer."""
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


def main():
    binary = shutil.which('ast-grep')
    if not binary:
        print(json.dumps({'status': 'BLOCKED', 'reason': 'ast-grep is not installed'}))
        return 2
    version = subprocess.run([binary, '--version'], check=True, capture_output=True, text=True, timeout=20).stdout.strip()
    with tempfile.TemporaryDirectory(prefix='agent-reference-ast-') as directory:
        source = Path(directory) / 'sample.ts'
        before = 'console.log(1);\nconst text = "console.log(2)";\n// console.log(3);\n'
        source.write_text(before, encoding='utf-8')
        common = [binary, 'run', '--lang', 'ts', '--pattern', 'console.log($A)']
        found = subprocess.run(common + ['--json', str(source)], capture_output=True, text=True, timeout=30, check=True)
        matches = json.loads(found.stdout)
        if not isinstance(matches, list) or len(matches) != 1:
            raise RuntimeError('AST search must match code once, not strings/comments')
        subprocess.run(common + ['--rewrite', 'console.info($A)', '--update-all', str(source)], check=True, capture_output=True, timeout=30)
        expected = before.replace('console.log(1)', 'console.info(1)')
        if source.read_text(encoding='utf-8') != expected:
            raise RuntimeError('Rewrite changed more than the matched code')
        after = subprocess.run(common + ['--json', str(source)], capture_output=True, text=True, timeout=30)
        if after.returncode not in (0, 1) or json.loads(after.stdout or '[]'):
            raise RuntimeError('Original AST pattern must no longer match')
    print(json.dumps({'status': 'PASS', 'tool': version, 'checks': ['structural-match', 'string-comment-exclusion', 'bounded-rewrite', 'post-rewrite-no-match'], 'openCodeHost': 'NOT RUN'}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
