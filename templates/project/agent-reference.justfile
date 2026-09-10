# Optional facade for THIS reference repository, when copied to its root.
# Consumer projects must substitute their real native commands, not empty stubs.
set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @just --list

test:
    PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/tests -v

audit:
    python3 tools/audit.py

verify: test audit
    git diff --check
