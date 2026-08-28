# Change Audit Prompt

Audit the current working-tree change against the requested outcome and repository contracts. This is read-only: do not fix findings during the audit.

## Goal

Determine whether the change is correct, complete for the agreed scope, safely bounded, and honestly verified.

## Procedure

1. Capture `git status --short` and inspect the relevant diff without modifying it.
2. Reconstruct the requested outcome from the current conversation, issue/spec, or task artifacts. Do not broaden it. If the original request or acceptance criteria are unavailable, mark scope comparison `UNVERIFIED` and ask for the missing contract rather than guessing.
3. Separate task changes from pre-existing user changes when evidence permits.
4. Inspect only the nearest maintained contracts, source, tests, project `AGENTS.md`, and generated-source ownership needed to judge the diff.
5. Treat CodeGraph/search indexes as navigation aids; verify cited files/symbols against current source.
6. Check high-value failure classes:
   - requested behavior missing or partial;
   - unrelated scope or feature creep;
   - symptom/band-aid fix instead of root-cause correction;
   - fix in the wrong layer or ownership boundary;
   - special-case, fallback, retry, or validation accumulation masking invalid state;
   - unnecessary abstraction, wrapper, interface, configuration, or placeholder code;
   - generated code edited directly;
   - API/DB/auth/security/public-contract break;
   - dead or unreachable additions;
   - tests that do not exercise the changed behavior;
   - completion claims unsupported by fresh, relevant evidence.
7. If an active Spec Kit feature exists, compare the diff with its current `spec.md`, `plan.md`, and `tasks.md` where relevant. Do not invoke `/speckit.converge` from this read-only audit because it may update task artifacts.
8. Use existing validation output only when it was produced after the last relevant change and clearly applies to the current diff. Confirm each cited check actually covers the claim; a passing unrelated command is not proof. Run additional read-only/static checks only when needed to substantiate a finding.

## Output

Prioritize findings by correctness, contract/security/data risk, verification gap, then maintainability.

For each finding include:

- severity;
- exact file/symbol or evidence;
- why it matters;
- smallest correction direction, without implementing it.

Then report:

### Scope Match

`PASS`, `PARTIAL`, `FAIL`, or `UNVERIFIED`.

### Verification Evidence

What actually passed, failed, was not run, or was blocked, and which claims each check covers.

### Clean Findings

Important areas explicitly checked with no issue.

If there are no meaningful findings, say so directly. Do not invent style complaints to fill the report.
