---
name: goat-skill-router-core-contract
description: >
  Use when a task plausibly matches multiple GOAT skills or needs an explicit owner,
  bounded support roles, and proof-bearing completion semantics before execution.
version: 2.0.0
metadata:
  author: Inversion Labs
  role: routing-governor
---

# GOAT Skill Router Core Contract

## Use when
- Multiple skills could plausibly own the same task.
- A broad task must be decomposed without creating parallel authority.
- A high-risk execution needs explicit evidence, rollback, and completion gates.
- A worker needs a portable handoff contract before delegation.

## Do not use when
- One narrow skill is already the obvious owner and no cross-skill coordination is needed.
- The request is pure explanation, brainstorming, or discussion with no governed execution.
- The target artifact cannot be identified or inferred well enough to route safely.

## Authority and scope
Own **routing and execution-contract formation only**. Select exactly one primary skill. Select zero to two support skills that advise the primary without becoming co-owners. Never invent a domain rule, silently widen task scope, replace the primary skill's technical workflow, or treat tool availability as authority.

Precedence: explicit user brief and supplied truth > safety/legal/privacy/data integrity > primary domain/runtime contract > incumbent artifact constraints > support-skill advice > heuristics.

## Workflow
1. **Resolve the target.** Identify the artifact, environment, requested outcome, constraints, and material unknowns.
2. **Generate candidates.** List only skills whose trigger conditions materially match the task.
3. **Choose one owner.** Pick the skill whose named responsibility best covers the requested outcome. If ownership is ambiguous, prefer the narrower class-level contract; do not stack broad umbrellas.
4. **Bound support.** Add at most two support skills and state the exact advisory job each performs.
5. **Form the execution contract.** Record assumptions, target artifact, primary owner, support roles, hard gates, verification evidence required, rollback/recovery requirement, residual risk, and next move.
6. **Execute through the owner.** The router does not duplicate child procedures.
7. **Adjudicate completion.** Return `PASS`, `FIX`, `NO-GO`, or `BLOCKED` from observed evidence, not confidence language.

## Failure and recovery
If no single owner fits, return `BLOCKED: ownership unresolved` and identify the missing capability instead of selecting several primaries. If a support skill conflicts with the primary or higher-precedence truth, discard the support advice. If evidence or rollback required for a high-risk action is unavailable, stop before the side effect. Preserve completed evidence and resume from the last verified gate rather than rerunning successful work blindly.

## Verification
A routed task is valid only when:
- exactly one primary owner is named;
- no more than two support skills are named with bounded roles;
- the target artifact and material assumptions are explicit;
- completion criteria identify observable evidence;
- high-risk mutation includes a viable recovery/rollback path;
- any final success claim cites observed evidence or remains explicitly `UNVERIFIED`/`BLOCKED`.

## Stop conditions
STOP when ownership remains ambiguous, the target is materially unknown, a hard gate fails, required current authority cannot be verified, rollback is impossible for a high-risk mutation, or the primary skill returns `NO-GO`/`BLOCKED`.

## Output contract
Return: `target → assumptions → primary_owner → support_roles → hard_gates → evidence_required → recovery → decision → residual_risk → next_move`.
