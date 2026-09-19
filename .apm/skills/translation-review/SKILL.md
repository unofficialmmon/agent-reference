---
name: translation-review
description: Meaning-preserving translation and translation review for technical, business, operational, and general prose. Use when translating a substantive passage or document, polishing an existing translation, checking source-versus-target fidelity, or producing natural target-language wording without weakening or exaggerating the source's certainty, criticism, constraints, or intent.
license: MIT
compatibility: opencode
metadata:
  source: "agent-reference translation and review policy"
  ownership: "agent-reference"
---

# Translation Review

Preserve what the source means, how strongly it says it, and what the target reader needs to understand. Prefer natural target-language communication over word-for-word structural copying, but never trade away facts, conditions, uncertainty, or intent for smooth prose.

## Establish the translation contract

Before translating, determine from the request and source:

- source and target language;
- intended audience and medium when relevant;
- domain and terminology that must remain stable;
- requested output shape, such as translated text only, bilingual comparison, or review notes;
- any explicit glossary, names, product terms, legal/technical terms, formatting, or length constraints.

Do not ask for information already evident from the source or request. Preserve the user's requested structure unless natural target-language grammar requires local restructuring.

## Choose the narrowest mode

Use the mode implied by the task; do not force the user to select one.

- **faithful** — contracts, requirements, specifications, policies, interfaces, technical instructions, or wording where semantic precision dominates style;
- **natural** — general prose where fluent target-language communication is primary while meaning and tone remain unchanged;
- **business** — email, meeting, report, proposal, or customer-facing prose where concise professional delivery matters without adding diplomacy that changes the message.

All modes use the same fidelity and review rules below.

## Translate meaning, not source syntax

Translate the semantic unit rather than mirroring each source word or clause mechanically.

- Reorder phrases when the target language requires it for clarity.
- Replace source-language idioms with an equivalent target-language expression when one exists.
- Keep technical identifiers, code, commands, URLs, version numbers, units, dates, amounts, and proper nouns accurate.
- Preserve lists, tables, headings, labels, placeholders, and code formatting unless the user requests a different presentation.
- Keep an established project or user glossary consistent. Do not invent alternate terminology merely for variety.
- When a term is genuinely ambiguous and the ambiguity affects the result, preserve the ambiguity or flag it briefly instead of silently choosing a stronger interpretation.

Do not add explanations, examples, claims, causes, or implications that the source does not contain merely to make the translation read better.

## Preserve strength, certainty, and intent

Match the source's communicative force.

- Do not introduce hedging that is absent from the source.
- Do not remove uncertainty, qualification, or conditional language that is present in the source.
- Do not soften criticism, refusal, obligation, prohibition, risk, or urgency solely to sound polite.
- Do not intensify neutral or uncertain language into a stronger accusation, guarantee, requirement, or conclusion.
- Preserve distinctions such as must/should/may, required/recommended/optional, confirmed/likely/possible, and supported/unsupported.
- Preserve negative scope precisely: not supported, not verified, not included, and not required are not interchangeable.

Natural phrasing may change sentence shape, but it must not change these semantics.

## Review against the source

After drafting, perform a source-versus-target pass before delivering the result. Check for:

1. **omissions** — every material source statement is represented;
2. **additions** — no material claim or rationale was invented;
3. **semantic distortion** — actors, actions, conditions, causality, time, scope, and negation match;
4. **terminology** — domain terms and repeated concepts are consistent;
5. **certainty and tone** — strength, uncertainty, criticism, politeness, and urgency remain equivalent;
6. **data fidelity** — names, numbers, dates, currency, units, versions, IDs, and references are unchanged unless conversion was explicitly requested;
7. **target-language quality** — the final wording reads as intentional target-language prose rather than a visible source-language skeleton.

When reviewing an existing translation, correct the target text rather than merely describing its problems unless the user asks for critique only.

## Handle unverifiable or source-specific terms

Do not silently guess a domain term whose exact rendering materially matters. Prefer, in order:

1. a glossary or terminology authority supplied by the user/project;
2. an authoritative maintained source available through an approved tool when current verification is necessary;
3. a conservative rendering that preserves the original term, optionally with a short clarification when useful.

Tool availability is not a reason to browse every translation. Use external lookup only when it materially improves a term, name, standard, or current product wording.

## Deliver the requested artifact

Return the requested translation or corrected translation as the primary output. Do not prepend a long translation-process explanation.

Include review notes only when they are requested or when a material ambiguity, source error, or terminology uncertainty cannot be resolved safely. Keep such notes separate from the translated artifact so the user can copy the translation directly.

For high-stakes legal, medical, regulatory, or safety text, preserve wording conservatively and state any unresolved ambiguity; do not present model translation as certified or professionally attested translation.
