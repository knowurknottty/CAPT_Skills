# Research synthesis — HyperFrames × Impeccable × Taste

Research date: 2026-08-19.

## Sources inspected

- HeyGen HyperFrames repository and current installed skills: `hyperframes`, `hyperframes-core`, `hyperframes-creative`, `hyperframes-animation`, `hyperframes-keyframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use`, and current `motion-doctrine`.
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

## Local integration findings

- The global skill population is large enough that `skills remove` reported 219 unique installed skills; Codex separately reported its 2% skill-description context budget exceeded and omitted 144 skill descriptions from model-visible discovery.
- Running the official HyperFrames v0.7.45 updater repaired its core set: post-update health is 9 current, 0 outdated, 0 core-missing; 11 optional workflow skills remain intentionally uninstalled/on-demand.
- Gemini reported duplicate HyperFrames registrations between `~/.agents/skills` and `~/.gemini/skills`.
- One unrelated local `substack` skill has malformed frontmatter and triggers a Codex loader error.
- The skills installer reported security alerts on current upstream `media-use`; therefore the Inversion motion overlay keeps `media-use` conditional rather than a default dependency.

These are ecosystem/topology issues, not defects in the four new skill contracts. The custom installer therefore uses symlinks and a minimal target set instead of copying the pack to every agent directory.
