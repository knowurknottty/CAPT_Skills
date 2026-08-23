---
name: skill-curation
description: >
  Use when a skill library needs evidence-based consolidation, trigger cleanup,
  deprecation, progressive-disclosure repair, or a decision about skill versus plugin scope.
version: 2.0.0
metadata:
  author: Inversion Labs
  role: skill-library-curator
---

# Skill Curation

## Use when
- Skill count/overlap makes discovery noisy or multiple skills compete for the same trigger.
- A reusable lesson needs to be placed into the right existing skill or support file.
- Thin/session-specific skills should be merged, deprecated, or re-scoped.
- A repeated executable behavior may belong in tooling/plugin code rather than prose guidance.

## Do not use when
- The task is merely to harvest possible lessons from sessions; use `cross-session-skill-harvest` first.
- Autonomous writers or self-modification authority must be contained; use `agent-self-modification-governance`.
- A project-specific rule belongs in repository instructions/configuration rather than a reusable skill.

## Authority and scope
Own **library taxonomy, trigger boundaries, consolidation/deprecation decisions, progressive disclosure, and authorized skill-pack changes**. Curation does not grant itself mutation authority. Any write still requires the surrounding repository/user governance, and an autonomous curator cannot authorize its own expansion merely by having created a skill previously.

## Workflow
1. **Inventory active discovery.** Count actual loadable skills, aliases/symlinks, duplicates, categories, descriptions, support files, size, and usage evidence. Distinguish live, bundled/upstream, archived, and externally managed sources.
2. **Map trigger collisions.** Compare names/descriptions and realistic user prompts. A healthy library gives a task one obvious primary owner; overlapping triggers need narrower boundaries, routing, merge, or deprecation.
3. **Classify the learning.** Decide whether new material is: project instruction, correction to an existing skill, supporting reference/template/script, new class-level skill, executable plugin/tooling, or transient/session evidence that should not become durable guidance.
4. **Prefer the smallest durable home.** Update an existing owner before creating another skill. Move bulky examples/history/API detail to references; keep trigger conditions and judgment-critical workflow in `SKILL.md`.
5. **Choose a disposition.** `KEEP`, `HARDEN`, `MERGE`, `SPLIT`, `DEPRECATE`, `ARCHIVE`, `CONVERT_TO_TOOL/PLUGIN`, or `CREATE`. Use evidence and routing quality, not a fixed library-size quota. See `references/curation-dispositions.md`.
6. **Preserve provenance.** Record donors, absorbed/superseded relationships, before/after triggers, and why information moved or was dropped. Never make a new umbrella silently erase unique behavior.
7. **Optimize discovery.** Descriptions should state **when to load**, not summarize the whole workflow. Include concrete task symptoms/keywords while avoiding triggers so broad they steal neighboring work.
8. **Validate progressive disclosure.** The activation payload should be compact; references should be linked and loadable; scripts/templates should exist and be reusable rather than prose pretending to be executable tooling.
9. **Test behavior, not formatting.** Run realistic positive, negative, collision, and adversarial prompts. Prove the intended skill is selected, neighboring skills are not falsely selected, and the body changes behavior where required.
10. **Mutate only through the authorized promotion path.** Apply changes in a versioned/staged workspace, run structural/secret/link/eval checks, then promote. Do not edit a live global library mid-task merely because a lesson was discovered.
11. **Verify the library after change.** Recount loadable skills, check broken references/aliases, search stale names, validate absorbed/deprecated pointers, and rerun collision prompts for affected neighbors.

## Failure and recovery
If the proper owner is uncertain, stage the lesson as unpromoted evidence rather than creating a skill. If merging would erase a distinct trigger or authority boundary, keep the skills separate. If a newly curated skill causes routing collisions, revert/disable the promotion and fix the trigger contract before further consolidation. If a source is externally managed or pinned, propose a local overlay/fork rather than mutating upstream in place.

## Evidence required
For each mutation retain the observed problem, candidate disposition, affected triggers/neighbors, donor provenance, before/after package identity, validation/eval results, and rollback. “Fewer skills” is not evidence of a healthier library; routing precision and preserved capability are.

## Stop conditions
STOP when mutation authority is absent, a merge would destroy unique capability, routing ownership cannot be made clear, an externally managed source would be overwritten, evaluation has not shown the change improves behavior, or provenance/rollback cannot be preserved.
