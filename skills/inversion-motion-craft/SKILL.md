---
name: inversion-motion-craft
description: >
  Use when creating or refining an Inversion Labs video, animation, launch sequence, motion graphic,
  or HyperFrames composition where visual taste, UI craft, narrative coherence, and deterministic
  rendering must be combined without letting web-design rules override the video runtime contract.
version: 0.1.0
metadata:
  author: Inversion Labs
  role: motion-owner
---

# Inversion Motion Craft

## Hard ownership and handoff contracts

For every motion/video artifact, write the ownership explicitly as: **Primary owner: `hyperframes`**. `hyperframes-core`, `hyperframes-creative`, `hyperframes-animation`, workflow skills, `taste`, and `impeccable` are domain/workflow/support layers; none may replace `hyperframes` as primary owner.

**Claim integrity:** never invent a public-facing metric, percentage, speed/latency figure, benchmark, testimonial, customer/logo, product capability, or "proof" datum to make a frame feel specific. Use supplied/verified truth only. If no claim evidence exists, write claimless descriptive copy or label illustrative/sample material explicitly; aesthetic specificity never outranks factual integrity.

Every plan, role breakdown, or finish handoff must include a section literally named **Motion Purpose Ledger**. Use the schema **Motion | Job | Viewer-visible change | KEEP/DELETE**. If the artifact only needs one motion, the ledger has one row; if no motion earns a job, record deliberate stillness instead of inventing motion to populate the ledger.

A KEEP job must name concrete information, focus, state, cause/effect, audio synchronization, or boundary continuity the viewer receives. "Energy", "premium feel", "brand rhythm", "subtle dynamism", "cinematic feel", "keep it alive", or any equivalent aesthetic rationalization is **not a job**. Mark that row DELETE.

`hyperframes` is the **primary owner**. Read it first, route to its current owning workflow, and obey `hyperframes-core` for composition/render mechanics. Use `taste` for judgment. Use `impeccable` only when actual product UI or a shared interface design system appears inside the film.

Never copy upstream HyperFrames mechanics into this skill. The technical contract stays upstream so updates do not drift from this overlay.

## Direction before animation

Before authoring, lock:

- **Spine** — one sentence the film proves or makes felt.
- **Frame thesis** — what should be visually undeniable in a paused representative frame.
- **Audience assumption** — what does not need explaining.
- **Attention budget** — the 1–2 beats worth maximal craft.
- **Signature move** — one memorable visual/motion idea with a named narrative function.

A web layout is not a video frame. Impeccable may inform typography, brand truth, or depicted UI, but HyperFrames creative/video-composition guidance owns video scale, density, timing, framing, and render behavior.

## Purposeful motion law

Every motion must perform at least one job: reveal information, direct hierarchy, demonstrate state/action, carry continuity across a boundary, establish cause/effect, or create an intentional dramatic pause. Motion added only because the frame feels static is debt.

The ledger must cover each animated behavior or sustained loop. If an item can only be labeled "ambient", "micro-motion", "breathe", "drift", "pulse", or "because static felt dead", mark it DELETE. A pulse is valid only when it communicates a real state/beat or synchronizes to an actual event/audio cue; a pulse whose entire argument is mood is filler. Deliberate stillness is valid and is preferred over filler motion.

Preserve directional and causal continuity across scene boundaries. Use the seam/transition verifier prescribed by the **currently installed owning HyperFrames workflow**, if it has one; do not invent a verifier for a single-scene composition.

Do not hard-depend on `motion-doctrine`: HyperFrames repository `main` may expose it as a higher-specificity continuity skill while published manifests may omit or remove it. If the current router/workflow explicitly exposes it, it can support continuity decisions; otherwise this overlay's purposeful-motion rule stands on its own.

## Precedence

Explicit brief/brand truth → safety/legal/claims → **HyperFrames technical contract** → medium-specific story/composition → domain-grounded `taste` → web/UI aesthetics → novelty.

If a visual idea is beautiful but not seek-safe, deterministic, renderable, or compatible with the owning HyperFrames workflow, change the idea, not the contract.

## Proof before finish

Use the current workflow-prescribed HyperFrames check/render path. Evidence should include, as applicable: clean composition checks, successful deterministic render, representative frame captures at hook/midpoint/payoff, readable type after compression, no clipping/flash/boundary defects, audio/caption sync, and the current owning workflow's prescribed transition/seam evidence when multi-scene verification exists.

Use `media-use` only when the task actually needs media sourcing/generation/processing; it is not a default dependency.

Bound QA to one full rendered inspection, one batched fix, and one confirmation render unless the fix creates a new defect.
