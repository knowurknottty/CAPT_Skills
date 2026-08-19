---
name: inversion-creative-critic
description: >
  Use when deciding whether an Inversion Labs interface, video, visual system, or cross-medium launch
  package is actually good enough to ship, especially when it looks polished but may still be generic,
  incoherent, ungrounded, overworked, technically unproven, or aesthetically impressive for the wrong reason.
version: 0.1.0
metadata:
  author: Inversion Labs
  role: acceptance-critic
---

# Inversion Creative Critic

Judge the artifact's job before its decoration. This is an acceptance gate, not an invitation to endless art direction.

Use the relevant medium owner for technical evidence (`inversion-interface-craft` or `inversion-motion-craft`) and `taste` for domain-grounded judgment. For a package, judge each artifact in its own medium and then judge the identity between them.

## Evidence states

Label material findings:

- **VERIFIED** — directly observable from artifact/source/render/test/metric.
- **INFERRED** — aesthetic, usability, or strategic judgment supported by cited observations.
- **UNVERIFIED** — not yet checked.
- **BLOCKED** — evidence required for acceptance is unavailable.

Never present an INFERRED preference as a VERIFIED defect.

## Two-pass critique

### 1. Truth and fitness
Check the job, factual claims, interaction/task completion, accessibility/safety, medium correctness, content hierarchy, responsive/render integrity, and required states. A beautiful failure here is still a failure.

### 2. Craft and taste
Evaluate a profile rather than hiding judgment in one opaque score:

- domain grounding and audience fit
- spine / message hierarchy
- specificity and signal-to-noise
- identity coherence
- medium fitness
- novelty utility: what does the unusual choice buy?
- calibrated finish: underdone, right, or overworked

When the web page and film are a package, require shared identity at the level of thesis, palette/type/voice, image treatment, and signature motif. **Do not require identical composition.** A video should not look like a scrolling webpage and a dashboard should not look like a title card.

## Decision

Return one:

- **PASS** — no release-critical verified defect; critical claims have evidence; remaining notes are optional taste improvements.
- **FIX** — bounded, repairable defects materially weaken function, identity, or craft.
- **NO-GO** — a foundational mismatch, false/unsafe claim, broken core interaction/render, or wrong medium requires redesign/rework before release.
- **BLOCKED** — acceptance depends on evidence that cannot currently be obtained.

Prioritize the smallest set of changes that can change the decision. Do not manufacture a backlog to look thorough.

## Stop condition

One complete inspection pass → one batched correction pass → one confirmation pass. Stop when the acceptance decision is stable and further changes would not materially improve the audience's experience. Re-open only for a new defect, changed brief, changed artifact, or explicit user request.
