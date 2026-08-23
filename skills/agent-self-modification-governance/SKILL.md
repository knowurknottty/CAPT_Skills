---
name: agent-self-modification-governance
description: >
  Use when an agent can write skills, prompts, memory, configuration, or other
  artifacts that influence its own future behavior and those mutations need containment or audit.
version: 2.0.0
metadata:
  author: Inversion Labs
  role: future-behavior-mutation-governor
---

# Agent Self-Modification Governance

## Use when
- An autonomous/post-turn/background actor can alter its own future-behavior store.
- An unexpected skill/prompt/memory/config mutation must be attributed and contained.
- Approval, staging, journaling, rollback, or evidence requirements are being designed for self-modifying agents.

## Do not use when
- The task is ordinary skill content curation; use `skill-curation`.
- Historical sessions are only being mined for candidate lessons; use `cross-session-skill-harvest`.
- A normal user-directed repository edit does not change the actor's future behavioral authority.

## Authority and scope
Own **mutation authority, provenance, containment, recovery, and enforcement proof for stores that can change the actor's future behavior**. It does not decide what content is good; it decides whether an actor may mutate, whether the control actually enforces that authority, and how the previous state remains recoverable.

**Authorship is not permission.** Fields such as `authored_by`/`created_by` are historical facts. Permission/opt-in must come from an authority the mutating actor cannot grant to itself.

## Workflow
1. **Enumerate future-behavior stores and writers.** List every skill/prompt/memory/config/plugin surface that affects later agent behavior and every foreground/background/scheduled/post-turn code path that can write it. Containment is incomplete until all writer paths are mapped.
2. **Capture recovery state before control changes.** Record artifact identities, bytes/hashes, provenance metadata, permissions/opt-ins, mutation counters/timestamps, discovery status, and available version history/backups. Verify backups contain the relevant pre-incident state; existence alone proves nothing.
3. **Separate fact from authority.** Identify which fields describe provenance and which grant mutation rights. Remove any rule where an actor's own prior write or metadata stamp can create its later permission.
4. **Apply the narrow containment control.** Disable/revoke the offending writer or artifact through an authority outside the actor. Prefer reversible staging/quarantine outside runtime discovery. Preserve original bytes/evidence before moving or marking anything.
5. **Prove the guard fires.** Invoke the real writer path with the real actor/origin context and assert each mutating action is refused. A flag being set is not proof that the enforcement path consumes it.
6. **Run negative controls.** Prove legitimate user-directed mutation still works where authorized, unaffected peer scope remains appropriately available, and the containment harness itself did not modify unrelated artifacts.
7. **Sweep same-window mutations.** Inspect sibling artifacts and other writer paths in the incident window. Provenance from the same actor/window is a finding even if the content appears benign.
8. **Reject self-correction as authority.** If the autonomous actor rewrites the artifact after detection, preserve that revision too; do not adopt it as the trusted fix merely because it responds to the finding.
9. **Recompute receipts from live state.** Record before/after hashes, control used, actor/origin, intended versus actual changed files, guard test, negative controls, recoverability, and residual uncontained scope. Do not write receipts from memory.
10. **Redesign for durable governance.** Prefer explicit external opt-in, versioned/staged mutations, append-only mutation journal, evidence handles for durable guidance, scope binding, rate limits, and a review/promotion gate. See `references/self-modification-control-plane.md`.

## Failure and recovery
If pre-mutation content is unrecoverable, record that as a governance failure rather than inventing a prior state. If the proposed containment leaves the artifact active in discovery, use a different reversible mechanism that actually removes its behavioral authority. If one writer path bypasses the guard, containment is FAILED even when another path refuses correctly. If containment breaks legitimate foreground/user-authorized writes, narrow the control before declaring success.

## Evidence required
Containment evidence must identify the protected store, every known writer path, external permission source, pre/post artifact hashes, recoverability, real guard invocation, negative controls, same-window sweep, and residual risk. “Autonomous improvement disabled” is not a proof unless all mutation paths were exercised or otherwise shown to consume the control.

## Stop conditions
STOP on unknown writer paths, self-granted permission, missing recovery snapshot when a reversible snapshot is possible, artifact still active after supposed quarantine, bypassing writer path, failed negative controls, unverifiable receipt, or any attempt by the contained actor to promote its own corrective rewrite.
