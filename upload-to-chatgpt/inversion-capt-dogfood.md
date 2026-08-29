---
name: inversion-capt-dogfood
description: >
  Use when building, testing, reviewing, or operating CAPT or Inversion Labs systems and a CAPT-governed execution path is available alongside direct shell, model, browser, or provider tooling.
version: 0.1.0
metadata:
  author: Inversion Labs
  role: capt-dogfood
---
# CAPT Dogfood Default

Use CAPT as part of the work whenever doing so exercises the architecture without falsifying authority or obstructing necessary recovery.

## Runtime/API reality
- CAPT source, registered actions/MCP schemas, runtime status, and ledger are the only authority for CAPT interfaces.
- Never invent module numbers, endpoints, commands, payload schemas, response fields, task IDs, approval IDs, verification IDs, or ledger events.
- If CAPT tooling is stated to be available, probe the actual registered/runtime surface. If it cannot be invoked, classify that probe BLOCKED rather than substituting a hypothetical CAPT API.

## Execution policy
1. Discover the real CAPT runtime/status before relying on it.
2. Prefer the governed CAPT path for model tasks, tool dispatch, evidence capture, approvals, verification, and continuity when that path supports the operation.
3. Use direct local tooling for bootstrap, repair, inspection, or operations CAPT cannot yet perform. Record why the fallback was necessary.
4. Feed defects found while dogfooding back into CAPT as product evidence rather than bypassing them permanently.

## Authority invariants
- CAPT observations are not approvals, verifications, completions, or accepted claims unless CAPT's authoritative state says so.
- Never manufacture approval IDs, verification IDs, ledger state, or task completion.
- Never weaken executable trust, sandboxing, authentication, capability scope, or fail-closed behavior merely to make dogfooding pass.
- Classify a blocked governed path as an environment/integration blocker when appropriate; do not charge it to the target under evaluation.

## Goal
The work should improve the target while simultaneously proving—or falsifying—the CAPT architecture under real use.
