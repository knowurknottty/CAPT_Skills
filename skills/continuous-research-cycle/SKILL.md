---
name: continuous-research-cycle
description: >
  Use when a research program must run across repeated cycles or sessions while preserving
  state, verified source identity, unresolved questions, and marginal progress instead of restarting.
version: 2.0.0
metadata:
  author: Inversion Labs
  role: iterative-research-state-machine
---

# Continuous Research Cycle

## Use when
- Research recurs by schedule, daemon, automation, or multiple human/agent sessions.
- Each run must extend or correct prior findings rather than start from zero.
- The corpus has active threads, carry-over priorities, or citations whose identity must survive across cycles.
- Progress must be measured as net-new evidence, resolved uncertainty, or justified state change.

## Do not use when
- The task is a one-off deep investigation; use `deep-research`.
- The user wants only monitoring/notification with no persistent research state.
- A domain-specific protocol already owns the cycle schema; compose with it rather than replacing it.

## Authority and scope
Own **cycle continuity, checkpoint/schema integrity, carry-over priority handling, verified-source identity, marginal-value gating, and next-cycle handoff**. Do not decide domain truth merely because a prior cycle said it, and do not turn artifact re-validation into substitute research.

A cycle succeeds only by adding external evidence, correcting/resolving material uncertainty, advancing a decision, or explicitly finding no material change. File production alone is not progress.

## Workflow
1. **Resolve corpus and cycle identity.** Derive workspace/date/cycle from live state, not a hardcoded template. Detect duplicate IDs and interrupted runs before writing.
2. **Load the prior checkpoint.** Read the latest summary, active threads, source index, gaps, and next priorities. Confirm referenced artifacts exist and belong to this corpus/revision.
3. **Fingerprint the current schema.** Inspect recent artifacts first. Current field names, evidence classes, and status values outrank legacy examples. See `references/cycle-state-contract.md`.
4. **Choose this cycle's discriminating work.** Start from prior priorities unless new evidence invalidates them. If no carry-over exists, map covered territory and select a distinct unresolved dimension rather than re-deriving owned findings.
5. **Acquire net-new external evidence.** Prefer primary sources and re-open persistent claims when staleness matters. Lock source identity; never inherit an attribution string as proof. See `references/source-identity.md`.
6. **Analyze changes, not just facts.** State what this cycle adds, corrects, strengthens, weakens, or leaves unchanged relative to prior state. Keep inference separate from sourced observation.
7. **Write the smallest complete cycle artifacts.** Preserve the corpus's established structure while ensuring machine-readable evidence, synthesis, gaps, thread/status updates, and a next-cycle handoff exist where the corpus contract requires them.
8. **Verify artifact integrity.** Parse/validate structured outputs, derive prose counts from source data, and reconcile referenced files/IDs. Structural validation proves artifact integrity only; it is not the research result.
9. **Apply the marginal-value gate.** Require new evidence, a material correction, resolved uncertainty, or decision progress. Otherwise record `NO_MATERIAL_CHANGE` or silent delivery; do not pad the cycle with self-verification theater.
10. **Checkpoint and hand off.** Record active threads, claim/evidence changes, unresolved gaps, exact next-cycle priorities, and the state identity the next run must load. Persist only through the authorized corpus workflow.

## Failure and recovery
If an orphan evidence directory or partial cycle exists, preserve it, reconstruct the intended assignment from prior state, verify only load-bearing evidence afresh, then complete or explicitly abandon that cycle before allocating a new ID. If source identity conflicts, retract or downgrade the inherited claim instead of propagating it. If schema drift is detected, follow the newest verified corpus schema and document the migration boundary; never coerce current artifacts into a legacy shape merely to satisfy an old validator.

## Evidence required
Retain the cycle ID/time boundary, prior checkpoint identity, inherited priorities, source records used this run, net-new or corrected findings, claim/evidence status changes, artifact-validation result, marginal-value verdict, honest gaps, and explicit next-cycle priorities. A later run must be able to reconstruct why the cycle chose its work and what state it handed forward.

## Stop conditions
STOP when the live corpus cannot be identified, cycle numbering/state is contradictory, prior artifacts appear partially written and unreconciled, current schema cannot be distinguished from legacy examples, a material citation cannot be tied to its source identity, or the run has no legitimate research contribution and the delivery contract permits silence. Never manufacture novelty to keep an autonomous loop busy.

Load `references/cycle-state-contract.md` for checkpoint fields and interrupted-run recovery, and `references/source-identity.md` for citation identity, staleness, and re-verification discipline.
