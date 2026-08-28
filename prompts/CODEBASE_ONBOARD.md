# Codebase Onboard Prompt

Map an unfamiliar repository so another engineering task can begin with the right context. This is a read-only discovery task.

## Goal

Produce a concise onboarding brief grounded in maintained source and configuration. Do not create permanent documentation unless explicitly requested.

## Inspect

Read only what is needed to establish:

- project purpose;
- languages, runtimes, frameworks, package/build tools;
- main modules/domains and ownership;
- important entry points and request/data flow;
- API, persistence, auth/security, IPC, and external boundaries when present;
- generated code and its source of truth;
- build, test, lint, format, and local-run commands that actually exist;
- the most useful files to read next for the likely work.

Prefer current maintained source, tests, manifests, and authoritative contracts over historical or deleted material. Do not infer architecture from directory names. Treat CodeGraph/search indexes as navigation aids and confirm important symbols/files against the current filesystem.

## Constraints

- Read only. Do not modify source, docs, configuration, history, or generated files.
- Do not run the application or full test suite unless runtime verification was explicitly requested.
- Do not create a documentation framework, architecture folder, or multiple generated reports by default.
- Do not turn onboarding into code review, refactoring, or speculative redesign.
- Mark uncertain or conflicting findings as uncertain.

## Output

### Purpose and Stack

Short factual summary.

### Structure and Ownership

Only the important modules/domains and boundaries.

### Key Flows

A few important execution/data paths when they can be proven.

### Contracts and Generated Boundaries

Only those that exist.

### Developer Commands

Commands discovered in repository configuration/docs. Distinguish commands merely found from commands actually executed.

### Start Here

Three to seven concrete files/directories worth reading next, with one-line reasons.

### Unknowns

Material questions the repository did not answer.
