---
name: inversion-motion-craft
description: >
  Use for Inversion Labs HyperFrames motion combining taste with deterministic runtime constraints.
version: 0.1.0
metadata:
  author: Inversion Labs
  role: motion-owner
---

# Inversion Motion Craft

## Required handoff shape

Return these slots, in order:

1. `Primary owner: hyperframes | Claim status: Spine/Frame thesis = INTERNAL; public copy = SUPPLIED / APPROVED / PROPOSED`
2. **Bounded roles** — HyperFrames layers plus `taste`; `impeccable` only for actual in-film product UI/shared interface systems.
3. **Precedence + creative direction** — exactly: `Precedence: brief/brand truth > safety/legal/claims > HyperFrames technical contract > video story/composition > taste > web/UI aesthetics > novelty`, then spine, frame thesis, attention budget, signature move, and audience status. If no audience source is loaded write exactly `Audience assumption: ASSUMED`; otherwise `Audience assumption: SUPPLIED[source=<exact source>]`.
4. **Render/story scope** — `duration=<STATUS[source]|UNKNOWN>; aspect=<STATUS[source]|UNKNOWN>; resolution=<STATUS[source]|UNKNOWN>; audio=<STATUS[source]|UNKNOWN>; sustained-motion-basis=<SUPPLIED[source]|VERIFIED[source]|NONE>; product-state-basis=<SUPPLIED[source]|VERIFIED[source]|NONE>`. Extract explicit values first. Example: `8-second` → `duration=SUPPLIED[user:8-second]`; no audio statement → `audio=UNKNOWN`. Framework defaults are not sources. With no real state/event/audio/continuity source use `sustained-motion-basis=NONE`; with no supplied product capability/state/story use `product-state-basis=NONE`.
5. **Motion Purpose Ledger** — `Motion | Job=<ENUM> | Viewer-visible change | Basis=STATUS[source] | KEEP/DELETE`. Job ENUM is exactly `REVEAL_INFO / DIRECT_HIERARCHY / DEMONSTRATE_STATE / CONTINUITY / CAUSE_EFFECT / SYNC_REAL_CUE / PAUSE_READABILITY`; Basis STATUS is exactly `SUPPLIED / VERIFIED / PROPOSED`.
6. **Verification evidence + bounded QA** — emit pending lines for UNKNOWN fields, then always emit `Invariant finish gate: workflow-prescribed HyperFrames check + deterministic render must pass; no clipping/flash/boundary defects at resolved scope.` Final line exactly: `QA: one rendered inspection → one batched fix → confirmation render → STOP unless the fix creates a new defect.`

`Primary owner` appears exactly once. Supporting skills are layers, never co-owners. If any slot is missing, the handoff is incomplete.

Read `hyperframes` first; `hyperframes-core` owns composition/render mechanics. Do not copy upstream mechanics here.

## Truth and direction

Use supplied/verified truth only. Never invent metrics, benchmarks, testimonials, customers/logos, capabilities, or organization/product descriptors. Without a supplied descriptor, write `Spine: PROPOSED INTERNAL — <formal/emotional aim>`; do not use factual predicates such as `Inversion Labs is/does/builds...`. **Visual authority/craft is not evidence of product truth.** Unsupplied public copy stays **PROPOSED**.

Attention budget: qualitative beats or resolved-duration windows; no percentages.

## Purposeful motion law

**INVERSION OVERRIDE:** generic advice to keep decoratives breathing/drifting/pulsing is superseded. Static is valid.

Ledger rows cover animated behavior or deliberate stillness, not static styling. For every KEEP row:
- `Basis=SUPPLIED[source=...]` or `VERIFIED[source=...]` must cite exact observed user/repo/product/audio/continuity evidence. `assumed`, `none`, `internal`, `signature move`, `render/check/test`, `taste/filter`, or a framework rule are invalid sources. Tests verify implementation; they do not earn creative intent.
- `Basis=PROPOSED[creative-direction]` may justify a **one-shot** reveal/removal/reframe/transition that changes scene information or composition. It cannot justify a sustained/looping modulation or a claimed product state.
- A technical/render contract constrains **how**, but cannot be the creative Basis for **why** an element exists.

`NONE` scope values are **gates, never ledger evidence**; never write `Basis=...NONE`. If both sustained-motion and product-state basis are NONE, KEEP Job values are `REVEAL_INFO / DIRECT_HIERARCHY / PAUSE_READABILITY`, plus `CONTINUITY` only for a named proposed/observed scene boundary. Use identity-only fallback: supplied brand name/mark/assets, abstract geometry, and explicitly PROPOSED non-claim copy/form. Do not reference an unsupplied brand promise, capability, feature, problem/solution, intervention, product behavior/state, or value proposition. Pulse/breathe/drift/shimmer/oscillation/beat-sync/loop, `DEMONSTRATE_STATE`, `CAUSE_EFFECT`, and `SYNC_REAL_CUE` are DELETE without matching authority. `CONTINUITY` may use `Basis=PROPOSED[creative-direction]` only when its viewer-visible change names a concrete **proposed scene/seam/cut/handoff boundary**; once that boundary exists in an artifact it should become VERIFIED.

Deliberate stillness may KEEP only as `Job=PAUSE_READABILITY` with `Basis=PROPOSED[creative-direction]`. `CONTINUITY` requires a named scene/seam/cut/handoff boundary in the viewer-visible change; a merely static background is styling, not a ledger row.

If a job exposes a claim/capability/metric, that truth must be supplied/verified or the row becomes non-claim context/identity or DELETE.

For multi-scene work, use the seam verifier prescribed by the installed owning workflow; do not invent one or hard-depend on unpublished `motion-doctrine`.

## Proof before finish

UNKNOWN never means absent. Emit `aspect-dependent evidence=PENDING SCOPE`, `resolution-dependent evidence=PENDING SCOPE`, and/or `audio-dependent evidence=PENDING SCOPE` as applicable. Never claim legibility/compression at unknown resolution, fit at unknown aspect, or sync for unknown audio.
