# Research synthesis — HyperFrames × Impeccable × Taste

Research date: 2026-08-19.

## Sources inspected

- HeyGen HyperFrames repository plus current installed core/domain skills: `hyperframes`, `hyperframes-core`, `hyperframes-creative`, `hyperframes-animation`, `hyperframes-keyframes`, `hyperframes-cli`, `hyperframes-registry`, `hyperframes-audio`, and `media-use`. Repository-main `motion-doctrine` was inspected as research input but is not a current published runtime dependency in the local v0.7.45 manifest.
- pbakaus/Impeccable current upstream skill, version 4.1.1, including craft-floor and bounded verification behavior.
- Hmbown/taste v0.1.0, including domain modes, anti-patterns, and evaluation rubric.
- Leonxlnx/taste-skill current `design-taste-frontend`, including Design Read, variance/motion/density dials, redesign protocol, and pre-flight rules.

## What each upstream should keep owning

### HyperFrames

Best at deterministic video production: composition/runtime contract, seek-safe timing, render loop, media/time ownership, and specialized video workflows. Repository `main` also contains a `motion-doctrine` continuity model with vector continuity, causal motion, seam verification, and a ban on idle wobble; however, the locally installed HyperFrames CLI v0.7.45 manifest marks that skill removed. The Inversion overlay therefore adopts the durable principle (motion performs a job; continuity matters) without hard-depending on that optional skill.

Do not transplant web-layout rules into this runtime. Video scale, timing, frame density, scene continuity, and render correctness remain HyperFrames concerns.

### Impeccable

Best at production interface craft: surface modes, design direction, implementation, audit, responsive/device inspection, state coverage, accessibility, copy, and bounded visual QA. It is a production owner, not merely a style checklist.

Do not fork its large command/reference system. Keep the custom layer thin so upstream improvements remain upstream.

### Hmbown Taste

Best general judgment substrate: ground in the real domain, establish a quality bar, identify assumed knowledge and attention budget, commit to a spine, exclude what does not earn its place, and stop at the right level of finish.

It deliberately does not provide production mechanics. That is a strength when used as a support layer.

### Leon Taste / design-taste-frontend

Best at fast brief inference for marketing surfaces: explicit Design Read, controllable variance/motion/density, anti-default vocabulary, redesign audit, and strong preflight pressure against generated-looking landing pages.

Its own scope explicitly excludes dashboards, dense product UI, data tables, and multi-step product work. Several preflight rules are intentionally absolute for its target aesthetic domain; they are unsafe as universal rules across product UI or other media.

## Collisions found

1. **Marketing Taste vs product UI** — applying `design-taste-frontend` globally can push expressive landing-page heuristics into operator surfaces it explicitly excludes.
2. **HyperFrames ambient-motion tension** — generic creative guidance says decoratives should breathe/drift/pulse, while repository-main `motion-doctrine` bans idle wobble. Because the published CLI manifest marks that skill removed, the custom overlay resolves the principle itself: motion must perform a communicative or continuity job; filler wobble is rejected.
3. **Web aesthetic vs render contract** — a beautiful web-inspired effect can still be wrong if it violates HyperFrames seek safety, deterministic rendering, timing, or composition ownership.
4. **Taste vs verification** — subjective judgment can improve direction but cannot prove accessibility, rendering, interaction state, or runtime correctness.
5. **Polish loops** — all three systems can encourage iteration; Impeccable's current bounded-QA rule is the safest default for cost and convergence.
6. **Evidence-scope leakage** — generic preflight lists can invent device/theme coverage (for example, demanding mobile plus both themes when the product truth never said they ship). Evidence must be scoped to known shipped variants; unknown stays unverified.
7. **Claim laundering** — a model can turn an internal creative spine, render property, or aesthetic number into public-facing "proof." Internal direction is not product truth; unsupplied copy stays proposed and metrics require supplied/verified evidence.
8. **Exclusion rationalization** — models may correctly say a marketing skill is out-of-scope for dashboards, then "borrow its spirit" anyway. Excluded skills have zero authority on that surface; coincidentally similar choices must be re-derived from the actual owner/domain.

## Inversion Labs additions

The custom pack adds only the missing layer:

- one production owner per artifact
- explicit conflict precedence
- first-order default vs fashionable anti-default vs useful inversion
- one load-bearing signature move instead of novelty everywhere
- `VERIFIED / INFERRED / UNVERIFIED / BLOCKED` creative ClaimGuard states
- `PASS / FIX / NO-GO / BLOCKED` acceptance semantics
- cross-medium identity without forcing identical composition
- bounded inspect → batch-fix → confirm QA
- Motion Purpose Ledger: every animated behavior gets a viewer-visible job or is deleted
- evidence-scope declaration before acceptance
- claim-status separation between internal creative direction and approved public truth

## Local integration findings

- The global skill population is large enough that `skills remove` reported 219 unique installed skills; Codex separately reported its 2% skill-description context budget exceeded and omitted 144 skill descriptions from model-visible discovery.
- Running the official HyperFrames v0.7.45 updater repaired its core set: post-update health is 9 current, 0 outdated, 0 core-missing; 11 optional workflow skills remain intentionally uninstalled/on-demand.
- Gemini reported duplicate HyperFrames registrations between `~/.agents/skills` and `~/.gemini/skills`.
- One unrelated local `substack` skill has malformed frontmatter and triggers a Codex loader error.
- The skills installer reported security alerts on current upstream `media-use`; therefore the Inversion motion overlay keeps `media-use` conditional rather than a default dependency.

These are ecosystem/topology issues, not defects in the four new skill contracts. The custom installer therefore uses symlinks and a minimal target set instead of copying the pack to every agent directory.

## Verification evidence

- `tests/validate_pack.py` enforces frontmatter, compactness (<750 words/skill), required ownership/precedence tokens, and anti-fork behavior.
- `tests/final_post_smoke.py` runs fresh local Qwen inference against real upstream skill text plus the overlays. Current strict small-model results: interface **16/16**, motion **49/49**.
- `tests/cross_medium_smoke.py` separately gates the governor/acceptance surfaces: director **17/17**, critic **13/13**.
- The behavioral checks cover sole ownership, skill-owner vs production-owner authority, product-vs-marketing scope, precedence, bounded QA, per-dimension evidence scope, no marketing-rule leakage into operator UI, HyperFrames technical precedence, Motion Purpose Ledger, claim provenance, render/story scope, proposed continuity boundaries, partial BLOCKED handling, internal-vs-public copy status, and rejection of invented public metrics/state/cue/product truth.
- Human review remains required because regex scores previously missed semantic leaks such as "borrow the anti-default rule anyway," mood-only motion justified as "brand rhythm," fabricated "100% deterministic" public proof, `SUPPLIED[assumed]`, UNKNOWN→default render scope, invented product capability/state stories, and cross-media constraint leakage. Those failures hardened the contracts rather than weakening the graders.
- Independent 27B red-team: `qwen3.6-fable-fusion:latest` first identified ownership terminology ambiguity, all-or-nothing BLOCKED handling, overconstrained proposed continuity, and all-dimension evidence freezing. The accepted amendments were regression-locked in `tests/validate_pack.py`; the second 27B pass returned **RELEASE-CANDIDATE** with zero BLOCKER/MATERIAL findings.
- Release integration check: `hyperframes doctor` reports v0.7.45 latest; `hyperframes skills check` reports **9 current, 11 on-demand**. Optional Kokoro/MusicGen and a stopped Docker daemon are non-dependencies for this pack. Installer symlinks resolve exactly to this repository in `~/.agents/skills`, `~/.claude/skills`, and `~/.hermes/skills`.
- Codex, Claude, and Gemini behavioral runners were attempted but were externally blocked during this pass (Codex usage limit, Claude Vertex quota, Gemini backend/client eligibility). Those are recorded as blockers, not passing tests.
