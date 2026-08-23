---
name: repository-hygiene
description: >
  Use when Git repository state must be cleaned or repaired without losing
  unrelated work, rewriting history unnecessarily, or conflating index state with disk state.
version: 2.0.0
metadata:
  author: Inversion Labs
  role: repository-state-surgeon
---

# Repository Hygiene

## Use when
- Tracked generated/vendor/secret-bearing artifacts should stop being tracked.
- Dirty working-tree state must be classified before a scoped repair or commit.
- A worktree, stash, ignored path, or detached HEAD may contain unique work.
- Hygiene changes need isolated verification and a reversible commit boundary.

## Do not use when
- Repository identity/canonicality is uncertain; run `codebase-archaeology` first.
- The task is to decompose or integrate a PR stack; use the dedicated integration skills.
- The root cause of a failing runtime/test is unknown; use `systematic-debugging`.

## Authority and scope
Own **Git/index/worktree hygiene, preservation of unrelated work, scoped cleanup, reversible commit separation, and proof that a hygiene mutation changed only intended repository state**. Do not silently discard untracked changes, stashes, orphan commits, ignored files, or pre-existing modifications. Prefer the narrowest Git operation that changes the required state.

Filesystem presence and Git tracking are separate properties. An index-only repair must not be implemented as disk deletion.

## Workflow
1. **Capture repository state.** Record branch/HEAD, remotes, `git status --short`, staged/unstaged diffs, untracked/ignored paths relevant to the repair, stashes, and worktrees. Mark pre-existing unrelated state explicitly.
2. **Define the mutation set.** Name the exact paths and Git property to change: tracked→untracked, ignored rule, generated artifact removal, staged-set correction, worktree cleanup, etc. Refuse broad cleanup whose target set is not enumerated.
3. **Preserve unique work.** Before removing a worktree, stash, or suspicious path, prove whether its commits are reachable and whether it contains dirty state. Preserve unreachable commits/diffs before cleanup. See `references/worktree-and-stash-preservation.md`.
4. **Choose the least destructive operation.** For tracking-only repairs, change the index (`git rm --cached`/equivalent) while preserving disk state. Avoid history rewriting when a normal commit/revert can represent the change.
5. **Separate concerns.** Keep audit/evidence, hygiene mutation, source/test fixes, and unrelated user work in distinct commits or unstaged sets. Do not hide functional changes inside a cleanup commit.
6. **Verify the staged delta before commit.** Confirm every staged path is intended, deletion/addition modes match the plan, expected tracking counts changed, and preserved disk content still exists when required.
7. **Verify reconstruction/ignore behavior.** Confirm ignore rules actually match the target and that a fresh dependency/build reconstruction works where the repair removes tracked generated/vendor content.
8. **Verify at the commit identity.** Use an isolated/detached worktree or clean checkout at the candidate SHA when dirty local state could contaminate verification. Run the maintained checks needed to prove the hygiene change did not break the repository.
9. **Reconcile residual dirt.** After the hygiene commit, re-run status and classify every remaining path as pre-existing, required follow-up, evidence-only, generated, unrelated, or unresolved. Do not sweep residual dirt into the commit merely to make status clean.
10. **Record rollback.** Name the exact commit/revert or index restoration path and any preserved orphan/stash evidence.

## Failure and recovery
If staged paths exceed the declared mutation set, unstage/restore the index and reclassify before continuing. If an apparently disposable worktree contains unreachable or dirty work, STOP cleanup and preserve it. If clean-checkout verification fails, preserve that state and hand the failure to `systematic-debugging`; do not broaden hygiene changes to chase the failure. If a secret is already committed, stop treating it as ordinary hygiene and invoke the repository's secret-rotation/history-remediation procedure.

## Evidence required
Retain before/after tracking counts or path sets, staged diff summary, commit SHA, residual dirty-state classification, reconstruction/test results where applicable, and the rollback method. A clean `git status` is not itself proof of correctness; it can also mean work was lost.

## Stop conditions
STOP when the mutation target is ambiguous, unrelated dirty state cannot be separated safely, a worktree/stash may contain unique work, the requested cleanup requires destructive history rewriting without explicit authority, or verification at the candidate commit fails. Report what is preserved and what decision is required.
