# Work History Reference

Optional rules for projects that keep AI handoff history. History is inactive by default.

## Activation

Read or update history only when:

- the user asks to view, resume, continue, update, summarize, or use history; or
- project `AGENTS.md` explicitly requires a history update after qualifying work.

History is active only when the project already contains `.ai/history/opencode/`. Do not create it automatically without explicit user intent.

## Layout

```text
.ai/history/opencode/
  current.md
  README.md
  work/
    <area>/
      index.md
      YYYY-MM-Wn.md
  daily/
    YYYY-MM/
      YYYY-MM-DD.md
```

- `current.md` — short resume pointer.
- `README.md` — local routing/format notes when needed.
- `work/<area>/index.md` — compact current summary of one work area.
- `work/<area>/YYYY-MM-Wn.md` — detailed weekly task log.
- `daily/...` — optional thin date index, not the source of truth.

Month-local weeks: `W1` days 1–7, `W2` 8–14, `W3` 15–21, `W4` 22–28, `W5` 29–month end.

## Reading order

For resume/history work, read the minimum context:

1. `current.md`.
2. `README.md` only when routing is missing or unclear.
3. Only work-area indexes named by `current.md` or required by the request.
4. Only referenced/current weekly files.
5. Older weekly or daily files only for explicit historical/date tracing.

Never scan all history by default.

## Update policy

Update only after qualifying tasks when history is active, unless the user opts out.

Qualifying work includes file edits, implementation, debugging, refactoring, API/DB/auth/security/build/deploy/config changes, multi-step design/doc restructuring, and useful commit candidates.

Do not update for simple Q&A, explanation-only work, read-only inspection, short snippets, one-off comparisons, or recommendations.

Update minimally:

1. `current.md`;
2. affected `work/<area>/index.md` when its summary changed;
3. current weekly file;
4. daily index only when useful/already maintained.

Record only handoff facts: goal, status, key decisions, changed files, validation result, remaining TODO, unverified boundaries, and useful commit candidate.

`current.md` is a pointer, not a journal. Keep it short and overwrite it with the latest resume state.

Never record full conversations, private reasoning, long terminal output, full diffs, repeated failure logs, secrets, credentials, cookies, private hosts, or personal data.

Never stage, commit, push, delete, reset, or rewrite history files unless explicitly requested.
