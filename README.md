# Inversion Labs Craft Skills

**Current release: `v0.1.0`** — annotated tag peels to commit `080446e2e8b8774ece41285e50d1c9c903984ba2`.

A thin Inversion Labs composition layer over upstream **Taste**, **Impeccable**, and **HyperFrames**.

The pack does not fork upstream production mechanics. It adds the cross-skill contracts that were missing between them: ownership, precedence, Inversion reasoning, evidence states, cross-medium coherence, and bounded acceptance.

## Skills

- `inversion-creative-director` — cross-medium direction and routing.
- `inversion-interface-craft` — Impeccable-owned interface work with scoped Taste support.
- `inversion-motion-craft` — HyperFrames-owned video/motion with domain-grounded taste and purposeful motion.
- `inversion-creative-critic` — evidence-bearing acceptance across web, UI, motion, or packages.

## Core architecture

One artifact gets one production owner. Supporting skills advise; they do not co-own implementation.

Conflict precedence:

1. explicit brief / supplied truth
2. safety, accessibility, legal, privacy, data integrity
3. medium technical contract
4. incumbent brand / interaction / preservation constraints
5. domain-grounded taste
6. anti-slop heuristics, dials, trends, novelty

The Inversion test rejects both the category default and reflexive anti-default. Novelty must buy comprehension, memorability, trust, identity, or task performance.

## Local Agent Skills install

Run:

```zsh
./scripts/install.sh
```

The installer creates source-of-truth symlinks for the four Inversion skills in:

- `~/.agents/skills`
- `~/.claude/skills`
- `~/.hermes/skills`

It intentionally does not spray copied skill trees into every agent-specific directory.

### CAPT-managed use is a different path

`scripts/install.sh` is a convenience installer for ambient Agent Skills consumers. It is **not** CAPT's governed skill-ingestion mechanism.

Current CAPT Core supports both:

- immutable `pinned_external` authored-skill context, including this repository's `v0.1.0` release; and
- `managed_local` Agent Skills imported into CAPT-managed state with manifest/content/tree integrity binding, deterministic contextual selection, approval-time binding, and execution-time anti-drift checks.

For CAPT usage and current commands, see `knowurknottty/CAPT_core` → `docs/AUTHORED_SKILLS.md`. CAPT skill context remains guidance only and cannot grant filesystem, network, tool, provider, approval, or policy authority.

## Verify this pack

```zsh
python3 tests/validate_pack.py
python3 tests/final_post_smoke.py
python3 tests/cross_medium_smoke.py
python3 tests/grade_saved_outputs.py

# Optional baseline-vs-overlay comparison
python3 tests/behavioral_eval.py
```

The strict `v0.1.0` local release gate used Ollama `qwen3.5-defiant-fable:latest` as a small-model stress harness plus human semantic review: **interface 16/16, motion 49/49, director 17/17, critic 13/13**.

An independent larger local `qwen3.6-fable-fusion:latest` (27B Fable-Fusion) red-team found four material governance gaps; after bounded amendments, its second pass returned **RELEASE-CANDIDATE** with no BLOCKER or MATERIAL defects.

At the recorded release-integration check, HyperFrames v0.7.45 reported **9 current / 11 on-demand** skills, and installer symlink topology was verified across Agents, Claude, and Hermes roots. Those are evidence for the recorded release environment, not promises about a later upstream HyperFrames installation.

See [`RESEARCH.md`](RESEARCH.md) and [`evals/EVIDENCE.md`](evals/EVIDENCE.md) for the dated research and verification record.

## Provenance and update policy

`v0.1.0` is an immutable release input for consumers that pin it. A future pack update should be released/tagged and reverified rather than silently treating a moving `main` checkout as equivalent to the pinned release.

The current annotated tag is unsigned. Do not describe the tag itself as cryptographically signed provenance.

## Scope boundary

These skills improve creative direction and review behavior. They do not establish factual truth, accessibility conformance, runtime correctness, security, or release readiness by themselves. Those claims require their own evidence.
