---
name: inversion-creative-critic
description: >
  Use to decide whether an Inversion Labs interface, video, visual system, or cross-medium package
  is good enough to ship without confusing polish, preference, inference, and proof.
version: 0.1.0
metadata:
  author: Inversion Labs
  role: acceptance-critic
---

# Inversion Creative Critic

This is an **acceptance gate**, not an art-direction generator.

## EARLY RETURN — unseen artifacts

If **no** relevant artifact/source/render is supplied or accessible, use **only** this output shape and STOP. If availability is mixed, evaluate each inspectable artifact normally, mark unavailable artifacts BLOCKED, and make the package decision BLOCKED whenever release acceptance depends on those missing artifacts.

1. `Decision: BLOCKED`
2. `Evidence states: VERIFIED / INFERRED / UNVERIFIED / BLOCKED`
3. Factual evidence rows exactly:
   - `Artifact availability=BLOCKED`
   - `Claim truth=UNVERIFIED`
   - `Web technical fitness=UNVERIFIED/BLOCKED — scope unresolved`
   - `Film technical fitness=UNVERIFIED/BLOCKED — scope unresolved`
   - `Cross-medium coherence=UNVERIFIED`
4. `Qualitative risks (INFERRED):` only risks supported by the user's description; do not claim a hierarchy, spine, state, claim, accessibility property, or render property is present/absent.
5. `Cross-medium criterion: shared identity; different composition per medium; status=UNVERIFIED.`
6. Decision-changing actions exactly, with **no parentheses/subchecks**:
   - obtain/access actual web artifact + resolved Evidence scope
   - obtain/access actual film/render + resolved Render/story scope
   - obtain governing brief/product truth
7. `Stop: one inspection → one batched correction → one confirmation → STOP; reopen only for new defect, changed brief/artifact, or explicit request.` **This is the final output line. Emit nothing after it.**

Do not enumerate breakpoints, devices, themes/locales, states, accessibility controls, audio/captions, players, render formats, or verification subchecks until the relevant medium owner resolves scope. A supplied remark such as “looks polished” supports only a qualitative INFERRED risk, never a VERIFIED technical/factual finding.

## Full acceptance path — only when artifacts are inspectable

Use `inversion-interface-craft` or `inversion-motion-craft` for medium evidence and `taste` for domain-grounded judgment.

Return:
1. **Decision** — `PASS / FIX / NO-GO / BLOCKED`.
2. **Evidence table** — factual/technical findings use only `VERIFIED / UNVERIFIED / BLOCKED`; qualitative judgments/risks use `INFERRED`.
3. **Truth + fitness** — job, claims, core interaction/render, accessibility/safety, hierarchy, required states, medium correctness.
4. **Craft + taste** — domain/audience fit, spine, signal-to-noise, identity coherence, medium fitness, novelty utility, calibrated finish.
5. **Cross-medium identity** when applicable — shared thesis/palette/type/voice/image treatment/motif with different composition per medium.
6. **Decision-changing actions** — smallest set that can change the decision.
7. **Stop condition** — one inspection → one batched correction → one confirmation → STOP.

### Evidence semantics

- **VERIFIED** — directly observed in supplied/accessed artifact, source, render, device/browser, test, metric, or authoritative supplied fact.
- **INFERRED** — qualitative aesthetic/usability/strategic judgment or risk; never factual claim truth or technical pass/fail.
- **UNVERIFIED** — relevant but not checked.
- **BLOCKED** — acceptance requires unavailable evidence.

A preference is never a VERIFIED defect.

### Decision semantics

- **PASS** — no release-critical VERIFIED defect; critical claims/evidence resolved; no remaining material defect that would weaken function, identity, or craft.
- **FIX** — bounded verified defects materially weaken function, identity, or craft.
- **NO-GO** — foundational mismatch, false/unsafe claim, broken core interaction/render, or wrong medium requires rework.
- **BLOCKED** — required acceptance evidence unavailable.
