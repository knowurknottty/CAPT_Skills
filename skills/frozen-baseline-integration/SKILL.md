---
name: frozen-baseline-integration
description: >
  Use when an already-reviewed dependency stack must be landed onto an authoritative
  target branch without rewriting proven layer identities or duplicating content.
version: 2.0.0
metadata:
  author: Inversion Labs
  role: proof-preserving-stack-integrator
---

# Frozen Baseline Integration

## Use when
- A linear/partially linear stack has been reviewed and accepted for integration.
- Layer SHAs or evidence artifacts are part of the proof and must remain in ancestry.
- Child PRs need sequential retargeting as predecessors land.
- Concurrent merges may have already superseded some stack content.

## Do not use when
- The stack still needs decomposition or ownership redesign; use `stacked-pr-decomposition`.
- The implementation itself needs rewriting to pass review.
- Merge authority has not been granted.

## Authority and scope
Own **proof-preserving integration order, remote-target reconciliation, supersession detection, retargeting, merge execution when authorized, and verification that every accepted layer survives in the integrated target**. Do not squash/rebase/force-push proven layers merely for convenience, and do not modify frozen implementation/contracts during merge-only integration.

## Hard gates
- Fetch first; the authoritative remote target ref, not a stale local checkout, defines the current baseline.
- Record every remote layer head and prove the intended ancestry/dependency chain before mutation.
- If proof depends on layer SHAs, use a non-rewriting merge method that preserves those SHAs in target ancestry.
- Revalidate target and candidate immediately before each merge because concurrent integration can change both necessity and diff.

## Workflow
1. **Snapshot remote truth.** Fetch/prune; record target SHA, layer remote SHAs, PR states, bases, head SHAs, mergeability, and required checks. Verify expected ancestry with Git, not branch names or PR metadata alone.
2. **Confirm accepted scope.** Compare the accepted top implementation layer to the frozen review/evidence boundary. Integration must not introduce unreviewed files or later/deferred scopes.
3. **Detect supersession.** Before landing a layer, determine whether its exact content is already contained in the target or another merged layer. Prove containment by ancestry and/or file/tree/diff equivalence. Close/note truly superseded PRs rather than merging duplicate content.
4. **Land one layer.** Merge the earliest remaining accepted layer with a proof-preserving method allowed by repository policy. Do not delete evidence branches as a side effect unless separately authorized.
5. **Re-fetch and prove.** Record the new target SHA; prove the landed layer head is an ancestor of the target and run the smallest layer-relevant smoke/contract gate. Stop on any failure.
6. **Retarget the next child.** Once its predecessor is in the target, update PR base metadata to the target only if branch ancestry is already correct; confirm the resulting PR diff contains only that layer's residual delta. Metadata repair must not masquerade as ancestry repair.
7. **Repeat sequentially.** Re-run supersession, remote-head, ancestry, diff, and check-state gates before every child merge. Never assume the stack stayed unchanged while earlier layers landed.
8. **Integrate evidence/docs separately.** If accepted review/evidence documents are part of delivery, use a small explicit documentation change; redact unnecessary machine-local paths and secret-bearing artifacts.
9. **Verify integrated target fresh.** From a clean worktree/checkout at the final remote target SHA, run the required generated-artifact drift, build/type/lint, layer/runtime, security/secret, replay/state, and repository checks appropriate to the release. Fresh output replaces historical test counts.
10. **Freeze only if authorized.** If the workflow calls for a tag/freeze marker, first prove the name is unused, create it at the verified target SHA, and record included/deferred scope. Never overwrite an existing freeze marker silently.

## Failure and recovery
If target moves concurrently, fetch and recompute the next merge rather than continuing from stale assumptions. If ancestry breaks or a layer head changed materially, stop and return to review. If a candidate is already contained, preserve its evidence and disposition it as superseded rather than duplicating content. If post-merge verification fails, stop the stack and use the repository's non-rewriting revert/repair path; do not continue layering failures.

## Evidence required
Retain pre/post target SHA, every layer head, ancestry results, supersession proof, PR base/head metadata, merge commit/result, per-layer smoke evidence, final clean-target verification, and any deferred scope. `main` containing the code is not enough when the accepted proof requires specific layer identities in ancestry.

## Stop conditions
STOP on changed/unreviewed layer heads, broken ancestry, unclear supersession, merge conflicts requiring implementation edits, failed required checks, stale remote identity, duplicate-content risk, or any step that would require rewriting a proven SHA. Report the last verified target and the exact layer requiring correction.

See `references/supersession-and-retargeting.md` for containment and metadata/ancestry distinctions.
