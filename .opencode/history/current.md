# Current handoff

- Goal: maintain bounded `apm-setup` and `agent-sync` convenience prompts for Microsoft APM adoption and updates.
- Status: both prompts implemented and validated; future APM updates belong to `/agent-sync`.
- Changed: `prompts/APM_SETUP.md`, `prompts/AGENT_SYNC.md`, and their minimal `prompts/README.md` index entries.
- Validation: `python3 tools/audit.py` passed with existing warnings; `git diff --check` and prompt-specific checks passed.
- Remaining: OpenCode/OMO behavioral discovery was not run; no runtime command was introduced.
- Last updated: 2026-08-31
