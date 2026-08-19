---
name: inversion-interface-craft
description: >
  Use for Inversion Labs interface work combining Impeccable and Taste across marketing and product surfaces.
version: 0.1.0
metadata:
  author: Inversion Labs
  role: interface-owner
---

# Inversion Interface Craft

## Required handoff shape

A valid response under this skill contains these slots, in order:

1. **Ownership** — skill owner=`inversion-interface-craft`; production owner=`impeccable`. In the handoff write `Primary owner: impeccable` for every interface surface. `taste` is support. `design-taste-frontend` is conditional marketing support only; never a co-owner.
2. **Surface routing** — classify each route separately: marketing/Persuade vs product/operator/Operate, plus preservation level.
3. **Truth/assumption status** — audience, incumbent/preservation level, brand, platform, claims, and quantitative targets as `SUPPLIED / VERIFIED / ASSUMED / PROPOSED / UNKNOWN`.
4. **Precedence + direction** — include exactly `Precedence: brief/product truth > safety/accessibility/legal > interaction/platform contract > incumbent brand/content > taste > heuristics/novelty`, then state spine + one signature move.
5. **Evidence scope** — device classes, themes/modes, locales, and states from brief/repo/product truth or `UNKNOWN`.
6. **Evidence + bounded QA** — follow the exact `Evidence and finish` contract below.

If a slot is omitted, the handoff is incomplete. **Context economy:** ≤600 words; reference upstream playbooks instead of restating checklists/recipes. Surface decisions, exceptions, truth status, evidence scope, and proof.

## Route before styling

- **Landing, campaign, portfolio, editorial marketing, marketing redesign:** use `impeccable` + `taste`; load `design-taste-frontend` for Design Read, its three dials, anti-default vocabulary, and redesign heuristics.
- **Dashboard, admin, dense product UI, data table, multi-step workflow, editor, operator console:** use `impeccable` + `taste`. **Do not load `design-taste-frontend`.** After this routing statement, do not name or apply that marketing skill's native rules inside operator direction or evidence. State operator guidance positively from Impeccable, the product domain, or a design system.
- **Mixed product:** classify each surface independently. Landing can Persuade while its console Operates.

When `design-taste-frontend` participates, never paste its preflight wholesale. A check applies only when its predicate is established for this marketing surface. Dials and anti-defaults yield to the brief, product truth, accessibility, official systems, and Impeccable's medium contract.

Do not duplicate upstream playbooks here; load current Impeccable and let it own implementation mechanics.

## Working method

1. Run Impeccable context/setup and inspect incumbent product, brand, code, and interaction truth before changing code.
2. Use `taste` to establish quality bar, audience knowledge, attention budget, and spine. Unknown audience/domain beliefs are `ASSUMED`, never facts.
3. Choose mode; derive preservation from inspected incumbent truth. If incumbent evidence is absent, preservation is `UNKNOWN`; do not default UNKNOWN to `new-work`, refinement, or replacement. Resolve it by inspection first.
4. Apply the Inversion test: identify category cliché and fashionable anti-cliché; choose a third move only when it improves the surface's job.
5. Commit to one signature move. Keep navigation, forms, dense data, recovery states, and conventional affordances where convention carries usability.
6. Build and verify through Impeccable playbooks.

## Constraint integrity

Never invent product claims, KPIs, conversion claims, benchmarks, click/task thresholds, performance targets, or quantitative UX goals for specificity. Supplied/verified constraints are truth. Unsupplied goals are **PROPOSED/ILLUSTRATIVE** or qualitative. Numeric performance thresholds may appear only from a source actually loaded and named in the handoff; otherwise omit them. An internal spine is not permission to fabricate a measurable promise.

## Precedence

Explicit brief/product truth → safety/accessibility/legal → interaction/platform contract → incumbent brand/content constraints → domain-grounded `taste` → anti-slop heuristics/dials/novelty.

Product UI task completion and state legibility outrank expression. Marketing may carry more expression, but claims still require truth.

## Evidence and finish

Start exactly with: `Evidence scope: device classes=<value|UNKNOWN>; themes=<value|UNKNOWN>; locales=<value|UNKNOWN>; states=<value|UNKNOWN>`.

For each **UNKNOWN** dimension, **INVERSION OVERRIDE:** suspend only checks that depend on that dimension and mark them `PENDING SCOPE`; do not invent a default. Resolved dimensions and invariant evidence may proceed. First inspect sources; unresolved dimensions stay `UNKNOWN/UNVERIFIED`. Do not infer a stack, breakpoint, desktop/mobile matrix, theme, locale, or responsive rules from upstream examples. If every variant dimension is UNKNOWN, output `Finish evidence: PENDING SCOPE — resolve Evidence scope before enumerating variant-dependent checks.` **Still include the QA line below.**

After scope resolves, require evidence appropriate to observed variants: rendered result, overflow/layout, interaction/focus, required states, accessibility, supplied copy/data or labeled fixtures, working controls, and build/test/performance evidence when touched. Performance is measured or `UNVERIFIED`; "plausibly" is not evidence. Numeric performance thresholds appear only when an actually loaded brief/standard supplies them; otherwise omit them.

Always end exactly: `QA: inspect resolved shipped variants once → batch-fix → confirm once → STOP unless the fix creates a new defect or the brief changes.`
