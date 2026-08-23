---
name: stacked-pr-decomposition
description: >
  Use when one oversized change set or pull request must be split into a dependency-correct,
  reviewable stack without losing files, changing semantics, or overstating independence.
version: 2.0.0
metadata:
  author: Inversion Labs
  role: change-set-decomposer
---

# Stacked PR Decomposition

## Use when
- One PR/change set is too large or heterogeneous for reliable review.
- A proposed split needs exact file/hunk ownership, dependency order, and equivalence proof.
- Reviewers need to know which layers can merge independently versus only stack cleanly.

## Do not use when
- Merging an accepted stack; use `frozen-baseline-integration` or the relevant integration workflow.
- The source is still changing materially.
- One PR is already coherent and reviewable.

## Authority and scope
Own **decomposition analysis, ownership boundaries, stack topology, optional construction of authorized replacement branches/PRs, and proof that the terminal stack represents the intended source delta**. Do not rewrite history, force-push, close the source PR, or publish replacements without explicit construction authority.

A stack may be **topologically valid** yet **semantically coupled**. Keep those claims separate.

## Hard gates
- Freeze exact source `BASE` and `HEAD` identities before accounting.
- Analysis is read-only until construction is explicitly authorized.
- Do not publish a replacement stack while source CI is non-terminal; if red, classify the actual failures as baseline-inherited, source-owned test defects, source-owned implementation defects, or infrastructure/verifier failures first.
- Frozen/protocol artifacts stay with their owning baseline unless an authorized rewrite explicitly changes that authority.

## Workflow
1. **Map the source delta.** Capture ordered commits and authoritative `git diff --name-status/--numstat BASE...HEAD`. Classify every path as added, modified, or deleted relative to `BASE`; do not infer “new” from commit position or filename.
2. **Build dependency graphs.** Track create-before-modify/topological constraints separately from semantic/runtime/test dependencies. A later PR editing a file created earlier is stack-valid but not independently mergeable.
3. **Assign ownership.** Give every changed path one primary semantic owner. For genuinely shared existing files, assign explicit non-overlapping hunks rather than duplicating the whole file across scopes. Inspect disputed files by behavior, imports, scripts, and CI ownership—not filename alone.
4. **Reconcile the manifest.** Programmatically prove unique paths/owners, added-modified-deleted counts, aggregate line accounting, locked ownership rules, and exact coverage of the source delta. If an asserted count conflicts with Git evidence, correct the assertion; never falsify Git classification.
5. **Choose boundaries.** Prefer coherent scopes with minimal cross-scope churn and clear rollback. If one commit mixes themes, distinguish a no-rewrite stack from an authorized history-rewrite option; never rewrite merely to make the plan aesthetically cleaner.
6. **Audit cross-scope coupling.** Before construction, find imports, subprocess launches, generated/config references, test fixtures, and required-CI dependencies that point to later scopes. Resolve required-gate coupling before publishing; defer only evidence-proven non-required gaps. See `references/accounting-and-coupling.md`.
7. **Construct only after approval.** Create each branch from the exact predecessor, materialize only its owned files/hunks, verify its diff against the manifest, and run the required local gates. Use isolated worktrees when practical.
8. **Prove remote identity.** Push branch first, confirm remote HEAD, then create/update the PR. For each PR verify required CI completed successfully for that exact head SHA.
9. **Audit the stack graph.** For every adjacent pair verify Git ancestry **and** that PR metadata names the immediate predecessor branch as its base. Correct metadata-only base errors without rewriting valid branch ancestry.
10. **Prove terminal equivalence.** Compare the terminal stack tree/delta to the frozen source candidate. Enumerate and justify intentional differences; unexplained residual diff blocks completion. See `references/construction-and-equivalence.md`.

## Evidence required
For each scope retain: predecessor/base, exact commits or source hunks, added/modified/deleted paths, shared-hunk ownership, semantic objective, dependencies, required verification and unsupported gaps, rollback boundary, local verification, remote head SHA, CI result, and independent-mergeability claims split into topological and semantic dimensions.

## Failure and recovery
If ownership cannot be made single-valued, stop construction and resolve the semantic boundary. If source CI is red, preserve and classify the failure before splitting. If a constructed branch requires a later scope to pass required CI, stop and change ownership/order rather than copying dependencies invisibly. If published PR metadata has the wrong base but ancestry is correct, repair metadata only; if ancestry is wrong, restack with preservation and force-with-lease safeguards.

## Stop conditions
STOP on unresolved source-CI failure, ambiguous ownership, required-gate cross-scope coupling, frozen-authority violation, source-delta accounting mismatch, unknown remote head identity, failed exact-SHA CI, ancestry/base mismatch, or unexplained terminal-tree divergence. Do not call the stack complete because the final branch “looks equivalent.”
