# GOAT Skill Forge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a provenance-preserving pipeline that inventories Hermes skills, stages CAPT skills separately, ranks GOAT candidates, forges stronger variants one-by-one, and promotes only verified winners into the canonical CAPT_Skills library.

**Architecture:** `CAPT_Skills` stays canonical. Raw source skills are copied into non-discoverable staging with hashes and provenance; deterministic tooling produces inventory and score artifacts; each candidate gets an isolated forge workspace and behavioral eval; only promoted skills enter `skills/` and the existing symlink installer. The dirty primary checkout must never be modified; execution happens in an isolated git worktree.

**Tech Stack:** Python 3.12+, stdlib (`pathlib`, `hashlib`, `json`, `shutil`, `re`, `subprocess`), pytest, zsh, git.

**Spec:** `docs/superpowers/specs/2026-08-19-goat-skill-forge-design.md`

## Global Constraints

- Local filesystem via RDC is authoritative for source discovery.
- GitHub is authoritative for committed forge state.
- Preserve every staged original byte-for-byte and record SHA-256 provenance before transformation.
- Raw staged skills must never be linked into live discovery roots.
- Existing canonical Inversion craft skills are incumbents and cannot be silently overwritten.
- A skill is promoted only after structural, trigger, adversarial, and baseline-vs-forged verification passes.
- Optimize capability density and trigger precision; do not reward verbosity.
- Never modify `/Users/knowurknot/inversion-labs-skills` while it contains unrelated dirty work.

---

### Task 1: Isolated Forge Worktree + Filesystem Contract

**Files:**
- Create: `goat_forge/__init__.py`
- Create: `goat_forge/paths.py`
- Test: `tests/test_goat_forge_paths.py`

**Interfaces:**
- Produces: `ForgePaths(repo_root: Path, hermes_live: Path, hermes_bundled: Path, hermes_optional: Path)` and `validate_source_roots(paths) -> None`.

- [ ] Write failing tests proving the canonical repo root, staging roots, and three Hermes source roots resolve independently and that missing roots fail closed.
- [ ] Run `pytest tests/test_goat_forge_paths.py -v` and confirm RED.
- [ ] Implement `ForgePaths` and strict existence/type validation with no implicit source creation.
- [ ] Run the test and confirm GREEN.
- [ ] Commit `feat: define GOAT forge filesystem contract`.

### Task 2: Provenance Inventory

**Files:**
- Create: `goat_forge/inventory.py`
- Create: `scripts/goat_forge_inventory.py`
- Test: `tests/test_goat_forge_inventory.py`
- Output: `provenance/inventory.jsonl`

**Interfaces:**
- Consumes: validated `ForgePaths`.
- Produces: `SkillRecord` with source lane, absolute source path, relative path, name, description, file count, byte count, SHA-256 tree digest, frontmatter status, and discovery status.

- [ ] Write tests using temporary skill fixtures for deterministic tree hashing, malformed frontmatter, symlink recording, duplicate names, and non-SKILL container directories.
- [ ] Run inventory tests and confirm RED.
- [ ] Implement deterministic recursive enumeration and hashing without following symlinks outside the source package.
- [ ] Run tests and confirm GREEN.
- [ ] Run the inventory against `~/.hermes/skills`, `~/.hermes/hermes-agent/skills`, and `~/.hermes/hermes-agent/optional-skills`; save JSONL plus a summary report.
- [ ] Commit `feat: add provenance-preserving Hermes skill inventory`.

### Task 3: CAPT Staging + Hermes GOAT Candidate Staging

**Files:**
- Create: `goat_forge/staging.py`
- Create: `scripts/goat_forge_stage.py`
- Test: `tests/test_goat_forge_staging.py`
- Create directories: `staging/capt/`, `staging/hermes/`, `staging/forge/`

**Interfaces:**
- Produces: `stage_skill(record, lane, destination_root) -> StagedSkill` and immutable `SOURCE.json` beside each staged package.

- [ ] Write failing tests proving byte-for-byte copy, hash equality, collision-safe source naming, refusal to overwrite an existing immutable original, and no staging path under `skills/`.
- [ ] Run staging tests and confirm RED.
- [ ] Implement staging with copy-to-temp + digest verification + atomic rename.
- [ ] Identify CAPT-specific skills by package path/name plus CAPT metadata, manually review ambiguous matches, then stage all accepted CAPT packages into `staging/capt`.
- [ ] Stage only ranked Hermes GOAT candidates into `staging/hermes`; do not stage the entire 385-skill live tree blindly.
- [ ] Run tests and digest reconciliation, then commit `feat: add immutable GOAT skill staging lanes`.

### Task 4: GOAT Ranking Engine

**Files:**
- Create: `goat_forge/scoring.py`
- Create: `scripts/goat_forge_score.py`
- Test: `tests/test_goat_forge_scoring.py`
- Output: `evals/goat-forge/ranking.json` and `evals/goat-forge/ranking.md`

**Interfaces:**
- Produces: `ScoreCard` with capability leverage, uniqueness, trigger precision, procedural depth, verification discipline, recovery semantics, composability, security/fail-closed behavior, context efficiency, duplication penalty, and final bounded score.

- [ ] Write tests proving duplicate/near-duplicate penalties, malformed-frontmatter penalties, context-bloat penalties, and strong verification/recovery bonuses.
- [ ] Run scoring tests and confirm RED.
- [ ] Implement explainable deterministic structural scoring; keep semantic judgment fields explicit rather than pretending they are objective measurements.
- [ ] Generate the first full ranking and manually inspect the top cohort against source text.
- [ ] Record `AUTO`, `HUMAN_REVIEWED`, and `PROMOTION_CANDIDATE` states separately.
- [ ] Commit `feat: rank Hermes GOAT skill candidates`.

### Task 5: Per-Skill GOAT Forge Contract

**Files:**
- Create: `goat_forge/forge_contract.py`
- Create: `tests/test_goat_forge_contract.py`
- Create per candidate: `staging/forge/<skill>/BASELINE.md`, `FORGED/SKILL.md`, `CHANGELOG.md`, `EVAL.md`

**Interfaces:**
- Produces: `ForgeReview` covering semantic name contract, positive and negative triggers, authority boundaries, prerequisites, workflow, decision gates, failure taxonomy, recovery, evidence requirements, stopping conditions, composition rules, context efficiency, and unresolved blockers.

- [ ] Write failing contract tests that reject missing negative triggers, unsupported success claims, absent failure/recovery semantics, accidental authority expansion, and name/content mismatch.
- [ ] Run tests and confirm RED.
- [ ] Implement contract validation.
- [ ] For each promotion candidate, read the original plus relevant neighboring/upstream skills, classify `HARDEN`, `REWRITE`, `SPLIT`, `MERGE`, or `RETIRE`, then forge exactly one candidate at a time.
- [ ] Preserve useful upstream mechanics and remove duplicated or contradictory guidance rather than inflating prose.
- [ ] Commit each forged skill independently so any candidate can be reverted without disturbing others.

### Task 6: Behavioral Evals + Promotion

**Files:**
- Create: `goat_forge/promotion.py`
- Create: `scripts/goat_forge_promote.py`
- Create: `tests/test_goat_forge_promotion.py`
- Extend: `scripts/install.sh`
- Extend: `tests/validate_pack.py`

**Interfaces:**
- Produces: `PromotionDecision(PASS|FIX|NO_GO|BLOCKED)` with evidence paths; promotion copies only the verified forged package into `skills/<name>`.

- [ ] Write failing tests proving raw staged packages cannot be promoted, incumbent name collisions require explicit replacement evidence, and failed evals block installer exposure.
- [ ] Add positive-trigger, should-not-trigger, ambiguous-input, tool-failure, hallucination-trap, premature-success, conflicting-instruction, and baseline-vs-forged cases per skill.
- [ ] Require structural PASS + behavioral PASS + no unresolved material red-team finding before promotion.
- [ ] Promote candidates one-by-one and add only promoted names to installer exposure.
- [ ] Run `pytest -q`, `python3 tests/validate_pack.py`, existing pack smokes, and GOAT forge evals.
- [ ] Commit `feat: gate GOAT skill promotion on behavioral evidence`.

### Task 7: Release Reconciliation

**Files:**
- Create: `GOAT_FORGE_REPORT.md`
- Update: `README.md`

**Interfaces:**
- Produces a final table of source path, source digest, disposition, forged digest, eval evidence, promotion state, and live discovery targets.

- [ ] Re-hash every promoted source and forged package and reconcile against provenance records.
- [ ] Verify no raw `staging/` path is symlinked from `~/.agents/skills`, `~/.claude/skills`, or `~/.hermes/skills`.
- [ ] Verify promoted symlinks resolve exactly to canonical `CAPT_Skills/skills/<name>`.
- [ ] Record retired/merged/split candidates explicitly so disappearance is never ambiguous.
- [ ] Run the complete regression suite and capture exact commands/results in `GOAT_FORGE_REPORT.md`.
- [ ] Commit `docs: publish GOAT forge reconciliation report`.