---
name: codebase-archaeology
description: >
  Use when a large code/filesystem corpus must be inventoried, provenance-mapped,
  duplicate-analyzed, or canonicality-assessed without modifying source artifacts.
version: 2.0.0
metadata:
  author: Inversion Labs
  role: read-only-corpus-forensics
---

# Codebase Archaeology

## Use when
- Many repositories/directories may overlap, fork, copy, supersede, or depend on one another.
- The actual source of truth is uncertain or documentation conflicts with filesystem/git state.
- A preserve-everything mandate requires inventory and organization planning before mutation.
- A large filesystem needs bounded discovery rather than one unscoped recursive scan.

## Do not use when
- The task is to reconstruct runtime/software architecture from implementation evidence; use `forensic-architecture-reconstruction`.
- The task is to clean, move, merge, archive, reset, or delete repositories; archaeology is read-only.
- One specific halted agent/session artifact must be recovered; use a session-recovery workflow.

## Authority and scope
Own **discovery, corpus identity, lineage/provenance analysis, duplicate/divergence analysis, dependency/usage mapping, and evidence-qualified canonicality proposals**. Do not mutate discovered projects or convert a probable canonical candidate into an authoritative source merely because it is newest, largest, or best documented.

All writes go to one isolated evidence workspace outside discovered projects. Secret-bearing files are classified by path/type only; do not collect secret values.

## Workflow
1. **Freeze scope.** Record roots, exclusions, permissions, preserve rules, evidence workspace, and what counts as a project/repository/artifact. Capture a pre-run source-state fingerprint sufficient to detect accidental mutation.
2. **Bound discovery.** Enumerate shallow/top-level structure first, identify system/cache/vendor/build trees, then scan curated roots independently with per-root timeouts. Preserve partial results incrementally. See `references/bounded-discovery.md`.
3. **Build the corpus index.** For each candidate record path, type, size/LOC as appropriate, git identity, remote, branch, HEAD, dirty state, timestamps, entrypoints, manifests, and discovery confidence. Keep raw facts separate from interpretation.
4. **Resolve identity and lineage.** Compare remotes, commit ancestry, first/last commits, file/package hashes, submodules, copied directory structure, and distinctive content. Classify exact duplicate, snapshot/copy, fork, divergent sibling, generated artifact, worktree/submodule, archive, or unresolved.
5. **Map usage and dependencies.** Prefer manifest/import/config/submodule/launch/CI/runtime evidence over documentation mentions. Classify edges as `VERIFIED`, `INFERRED`, or `SPECULATIVE` and preserve the evidence that earned the label.
6. **Assess canonicality by subsystem.** Use `canonical-confirmed`, `canonical-probable`, `candidate`, `compatibility-layer`, `fork/copy`, `legacy`, `archive`, `experiment`, or `unknown`. Every non-unknown label requires evidence, counterevidence, confidence, and unresolved questions. See `references/canonicality-and-lineage.md`.
7. **Analyze duplication and divergence.** Hash comparable source/config files only after discovery is complete; distinguish generated/vendor/scaffolding noise from meaningful duplication. Same remote/SHA can support duplicate identity; same name never does.
8. **Draft organization, never execute it.** Propose canonical map, compatibility needs, migration order, rollback, and decisions requiring approval. Keep destructive or history-changing actions outside archaeology.
9. **Verify the archaeology.** Reconcile counts against raw discovery outputs, validate generated JSON/CSV/graphs, sample-check classifications, record inaccessible/excluded paths, and confirm source fingerprints did not change.

## Failure and recovery
If a scan times out, narrow the root and continue from preserved partial indexes rather than restarting an unbounded traversal. If two evidence sources conflict, keep both and lower confidence. If a classification would require reading secret contents, destructive checkout changes, installs, or runtime mutation, mark that evidence `BLOCKED` and continue with safer evidence. If the evidence workspace was accidentally created inside a target, stop writing, preserve it, and relocate subsequent output outside the corpus.

## Evidence required
The final report must distinguish **observed facts** from **inference**. For material lineage/canonicality claims retain the exact supporting path/command/hash/commit evidence, counterevidence, and confidence. Report coverage and exclusions so “all repos” is never claimed from a partial scan.

## Stop conditions
STOP before any move/delete/archive/merge/reset/clean/install or source-tree rewrite. Also stop a canonicality claim when lineage remains contradictory, a required root is inaccessible, or coverage cannot support the requested scope. Return the evidence map, unresolved conflicts, proposed next moves, and approvals required.
