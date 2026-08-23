---
name: cross-session-skill-harvest
description: >
  Use when repeated lessons across prior sessions, incidents, or agent runs should be
  extracted into evidence-backed candidate skill patterns without mutating the live library.
version: 2.0.0
metadata:
  author: Inversion Labs
  role: learning-pattern-harvester
---

# Cross-Session Skill Harvest

## Use when
- The same problem class, correction, or successful technique appears across multiple sessions/runs.
- A project wants durable learning from historical agent work without importing session-specific noise.
- A skill library needs candidate patterns supported by real prior outcomes and failures.

## Do not use when
- Only one current task needs a note or handoff.
- The intended destination/disposition is already known and only curation is needed; use `skill-curation`.
- The request is to autonomously edit/register live skills; harvesting does not own mutation.

## Authority and scope
Own **historical discovery, episode clustering, extraction of reusable patterns, provenance/confidence, portability analysis, and candidate-learning packets**. Do not create, patch, register, install, or delete live skills. Harvest output is evidence for curation/promotion—not self-authorization.

## Workflow
1. **Define the harvest question.** Name the problem class/capability and time/source scope. Do not search the entire history merely hoping for “something useful.”
2. **Discover candidate episodes broadly.** Search session indexes, handoffs, governed memory/evidence, incident reports, and version-control artifacts using several synonymous problem/outcome terms. Record coverage limits and inaccessible sources.
3. **Build episode records.** For each relevant run capture source identity/date, problem signature, attempted methods, observed failures, successful technique, verification evidence, user correction, environment/tool dependencies, and final outcome. Never treat a retrospective summary as stronger than the underlying run evidence.
4. **Cluster by reusable mechanism.** Group episodes because the same causal/workflow pattern recurs—not because they share a project name or keyword. A cross-session pattern requires evidence from at least two distinct episodes; single-source lessons remain `PROVISIONAL`.
5. **Compare success and failure.** Identify what changed between failed and successful attempts, which constraints were load-bearing, and which commands/details were incidental. Preserve negative examples that explain when the pattern should not activate.
6. **Generalize carefully.** Remove project names, exact paths, one-off IDs, stale tool failures, temporary infrastructure facts, and private/session-specific data. Keep the class-level trigger, invariant, decision logic, failure recovery, and proof method.
7. **Test portability.** Ask whether the proposed pattern survives a different repo/runtime/tool provider. Mark dependencies as intrinsic or adapter-specific. If removing today's environment makes the pattern meaningless, keep it as a project reference rather than a skill candidate.
8. **Falsify the pattern.** Search the historical corpus for counterexamples: episodes where the proposed rule would have failed, over-triggered, or caused harm. Narrow the trigger/claim until the evidence supports it.
9. **Score confidence without inventing sources.** Base confidence on episode independence, evidence quality, recurrence, counterexamples, and portability. Never pad source counts to satisfy a rubric.
10. **Emit a candidate packet.** Include proposed capability/trigger, supporting episodes, counterevidence, distilled workflow/invariants, known exclusions, suggested disposition/owner, privacy/redaction notes, confidence, and unresolved questions. See `references/harvest-candidate-schema.md`.
11. **Hand off to curation.** `skill-curation` decides update/merge/split/create/reference/plugin disposition. Live mutation requires the normal promotion/governance path.

## Failure and recovery
If search coverage is incomplete, label the harvest partial rather than claiming ecosystem-wide recurrence. If episodes disagree, split the cluster or reduce confidence. If a source contains secrets/private data, record only the minimal provenance needed and redact sensitive content from the candidate packet. If the only support is unverified agent prose, return `INSUFFICIENT_EVIDENCE` rather than canonizing it.

## Evidence required
A candidate must cite the distinct episode records that support it, at least one verified success or correction when available, material counterexamples, and the reasoning that separates intrinsic technique from environment-specific detail. Cross-session recurrence is not proven by one session repeated in several summaries.

## Stop conditions
STOP before live mutation. Also stop/return provisional evidence when fewer than two distinct episodes support the pattern, historical coverage is too incomplete to justify recurrence, counterexamples invalidate the generalized trigger, or private/source material cannot be safely minimized.
