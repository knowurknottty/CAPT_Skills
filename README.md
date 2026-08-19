# Inversion Labs Craft Skills

A thin composition layer over upstream **Taste**, **Impeccable**, and **HyperFrames**.

The pack does not fork upstream mechanics. It adds the missing cross-skill contracts: ownership, precedence, Inversion reasoning, evidence states, cross-medium coherence, and bounded acceptance.

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

## Install

Run:

```bash
./scripts/install.sh
```

The installer symlinks the source-of-truth skills into the shared Agent Skills directory plus Claude and Hermes skill directories. It intentionally does not spray another copied skill into every agent-specific directory.

## Verify

```bash
python3 tests/validate_pack.py
python3 tests/behavioral_eval.py
```

The behavioral harness uses the local Ollama model `qwen3.5-defiant-fable:latest` and labels that evidence accordingly. Codex/Claude/Gemini smoke tests are recorded under `evals/` when available.
