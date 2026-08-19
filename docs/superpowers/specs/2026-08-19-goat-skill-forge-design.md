# GOAT Skill Forge — Design

Date: 2026-08-19
Status: approved architecture, pre-implementation
Branch: `feat/goat-skill-forge-r1`

## Mission

Build a provenance-preserving skill curation and hardening pipeline for the local Hermes skill library and CAPT skill corpus. The forge must identify genuinely high-value skills, preserve originals immutably, stage candidates outside live discovery, improve each skill according to the semantic contract implied by its name, verify behavior adversarially, and promote only proven variants into the canonical `CAPT_Skills` library.

The objective is not to maximize installed skill count. It is to maximize capability density, trigger precision, behavioral reliability, and composability while minimizing context-budget waste, duplicate authority, drift, and unverified rewrites.

## Source-of-truth model

`CAPT_Skills` remains the canonical source of truth. Approved skills continue to be linked outward to runtime-specific discovery roots rather than copied independently into each agent environment.

Raw imports never enter live discovery.

Known runtime targets remain:

- `~/.agents/skills`
- `~/.claude/skills`
- `~/.hermes/skills`

The local filesystem, inspected through Remote Desktop Commander, is authoritative for discovering the actual Hermes library and CAPT skill folders. GitHub is authoritative for committed forge state.

## Inputs

### Hermes

Search the authorized local filesystem for all Hermes skill roots, then enumerate candidate skill packages and their associated files. Hermes candidates are curated before entering the forge.

### CAPT

Search the authorized local filesystem for the requested `CAPT_skills` / `CAPT_Skills` folders rather than assuming a path. Every discovered CAPT skill candidate is copied into a dedicated staging lane before review.

### Existing canonical pack

The four existing Inversion Labs craft skills are incumbents, not raw candidates. They remain protected from accidental replacement and are evaluated as part of collision detection and composition analysis.

## Repository layout

```text
CAPT_Skills/
  skills/                         # promoted canonical skills only
  staging/
    hermes/
      <skill>/
        original/                 # immutable imported snapshot
        candidate/                # forge working copy
    capt/
      <skill>/
        original/
        candidate/
    rejected/                     # intentionally non-promoted candidates
  provenance/
    manifest.jsonl                # append-only import/promotion records
    collisions.json               # duplicate/overlapping authority analysis
  evals/
    <skill>/
      cases.yaml                  # positive, negative, adversarial cases
      baseline/                   # original outputs/results
      candidate/                  # forged outputs/results
      verdict.md                  # evidence-bearing promotion verdict
  scripts/
    inventory_skills.py
    validate_skill.py
    score_skill.py
    detect_collisions.py
    promote_skill.py
```

Generated names may be adjusted after filesystem inspection if an incumbent repository convention is stronger, but the separation between canonical skills, staging, provenance, evaluations, and promotion tooling is invariant.

## Import invariants

Every imported skill receives a provenance record before transformation.

Required record fields:

- stable import ID
- source type: `hermes` or `capt`
- absolute source path
- source package name
- discovery timestamp
- source file inventory
- SHA-256 digest for every imported file
- aggregate package digest
- symlink targets when applicable
- detected frontmatter metadata
- dependency/reference files
- duplicate/collision candidates
- import status

`original/` is immutable after import. All transformations occur in `candidate/`.

A later rediscovery of the same package digest must be idempotent and must not silently overwrite provenance.

## GOAT candidate ranking

Hermes skills are scored before staging as forge candidates. CAPT skills are all staged, then scored.

Ranking dimensions:

1. capability leverage
2. uniqueness versus installed alternatives
3. trigger precision
4. procedural depth
5. verification rigor
6. failure and recovery handling
7. tool/environment awareness
8. composability and authority boundaries
9. security/fail-closed behavior where relevant
10. context efficiency
11. testability
12. maintainability/upstream drift risk

Penalties:

- duplicate authority
- broad trigger capture
- obsolete tooling assumptions
- unverifiable success claims
- prose inflation without behavioral value
- hidden destructive effects
- malformed metadata
- copied upstream mechanics with no reason to fork
- contradictions with higher-authority canonical skills

The score is a triage signal, not proof. Promotion requires behavioral evidence.

## Skill semantic contract

The skill name is treated as a semantic promise. A forged skill must be the strongest defensible implementation of the capability named, not merely a more elaborate prompt.

For each candidate, the forge must determine:

- what task class the name promises to solve
- when the skill should trigger
- when it explicitly should not trigger
- what authority it owns
- what authority it delegates
- what evidence it must inspect before acting
- what operations it may perform
- what success means
- how success is verified
- how failure is classified and recovered
- when it must stop

A rewrite that increases length without improving these properties is rejected.

## Forge procedure per skill

### 1. Read the whole package

Inspect `SKILL.md`, referenced documents, scripts, examples, assets, tests, install metadata, and sibling skills that materially overlap.

### 2. Establish baseline

Record current strengths, defects, ambiguities, trigger collisions, missing failure modes, and expected behavior on a small representative evaluation set.

### 3. Decide transformation class

One of:

- `PRESERVE` — already excellent; only metadata or verification hardening allowed
- `HARDEN` — retain architecture, close material gaps
- `REFACTOR` — preserve mission, materially restructure behavior
- `MERGE` — capability is better represented by composition with another skill
- `SPLIT` — package contains multiple independent authorities
- `RETIRE` — duplicate, obsolete, unsafe, or lower-value than an incumbent

No candidate is rewritten gratuitously.

### 4. Forge

Where applicable, the forged variant should include:

- exact positive and negative triggers
- scope and authority boundaries
- prerequisites/environment checks
- explicit workflow
- decision gates
- tool-selection logic
- failure taxonomy
- recovery paths
- evidence requirements
- anti-patterns
- bounded delegation/composition rules
- verification before completion claims
- stop conditions
- progressive disclosure into references/scripts when useful

### 5. Adversarial review

Attack the candidate for ambiguity, over-triggering, under-triggering, invented assumptions, unsafe effects, context bloat, authority collision, stale tooling, and unverifiable completion.

### 6. Behavioral comparison

Run the same evaluation cases against original and candidate when an executable model/runtime path is available. Human semantic review remains required when automated graders can miss meaning-level regressions.

### 7. Verdict

Issue exactly one lifecycle verdict:

- `PROMOTE`
- `REWORK`
- `PRESERVE_ORIGINAL`
- `MERGE`
- `SPLIT`
- `RETIRE`
- `BLOCKED`

Promotion requires recorded evidence.

## Evaluation model

Each skill should receive evaluation cases appropriate to its claimed capability.

Minimum categories where applicable:

- canonical should-trigger case
- canonical should-not-trigger case
- ambiguous trigger case
- incomplete-input case
- contradictory-input case
- tool unavailable/failure case
- stale-state case
- destructive-effect boundary case
- hallucination trap
- premature-success trap
- conflicting-skill authority case
- stopping-condition case

Evaluation distinguishes structural validity from behavioral quality. A valid frontmatter file is not a proven skill.

## Promotion gate

A candidate can enter `skills/<name>` only when all applicable gates pass:

1. provenance complete
2. package structurally valid
3. no unresolved name collision
4. trigger contract is bounded
5. authority/composition contract is explicit
6. safety/effect boundaries are correct
7. evaluation suite passes or all blockers are explicitly accepted
8. candidate is behaviorally superior or materially safer than baseline, unless verdict is `PRESERVE`
9. no regression against incumbent canonical skills
10. promotion verdict is recorded

Promotion is atomic: canonical skill + evaluation verdict + provenance update move together.

## Discovery-budget discipline

The system must actively resist skill-count inflation.

Promotion decisions consider total model-visible description budget. Near-duplicate skills should be composed, merged, routed through a narrower governor, or left staged/on-demand rather than all exposed simultaneously.

A skill may be valuable yet deliberately remain staged/on-demand if live registration would reduce overall system performance.

## Collision handling

Collision analysis operates at three levels:

- exact duplicate: same or near-identical package
- semantic overlap: different names claiming substantially the same task class
- authority conflict: separate skills that can issue contradictory instructions over the same artifact/action

The forge must prefer explicit ownership and routing over multiple co-equal skills.

Existing canonical production-owner contracts in `CAPT_Skills` have incumbent authority unless an explicit reviewed migration changes them.

## Security and trust

Imported skills are untrusted instructions until reviewed.

The forge must inspect for:

- commands with destructive effects
- credential access or exfiltration behavior
- broad filesystem/network operations
- implicit auto-approval
- hidden persistence/install behavior
- instructions that override user intent or higher-priority governance
- scripts or references that materially expand effect surface

No imported script is executed merely because the skill tells the agent to execute it.

## Verification and truthfulness

The forge never claims a skill is improved because prose changed.

Evidence states:

- `VERIFIED` — inspected or executed evidence supports the claim
- `INFERRED` — strong structural/semantic reasoning supports it, not yet executed
- `UNVERIFIED` — plausible but not tested
- `BLOCKED` — required evidence cannot currently be obtained

Promotion reports must distinguish these states.

## Initial execution sequence

Once RDC is online:

1. confirm allowed filesystem roots and shell
2. search for Hermes skill roots and `CAPT_skills`/`CAPT_Skills`
3. enumerate package topology and symlinks
4. locate the local checkout of `CAPT_Skills`
5. verify git status and branch safety
6. generate inventory and digests without modifying sources
7. detect duplicates/collisions
8. create staging directories in the canonical repo
9. import immutable CAPT snapshots
10. rank Hermes candidates and import the high-value set
11. establish evaluation harness
12. forge candidates one at a time
13. promote only after per-skill evidence gates

## Non-goals

This phase does not:

- blindly install every discovered skill
- overwrite source libraries
- rewrite every skill for stylistic consistency
- treat more tokens as higher quality
- expose staging folders to runtime discovery
- replace upstream production mechanics without evidence
- claim behavioral improvement from structural validation alone

## Success criteria

The forge is successful when:

- every imported candidate has reproducible provenance
- originals remain immutable
- live skill discovery contains only promoted canonical skills
- each promoted skill has bounded triggers and explicit authority
- each promoted skill has an evidence-bearing verdict
- duplicates and authority collisions are reduced rather than multiplied
- the resulting library has greater capability density without worsening discovery-budget pressure
- a later reviewer can reconstruct exactly what changed, why, and what evidence justified promotion
