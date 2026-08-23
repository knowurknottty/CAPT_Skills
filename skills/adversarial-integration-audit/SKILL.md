---
name: adversarial-integration-audit
description: >
  Use when a pull request, integration branch, frozen baseline, or claimed security fix
  needs an independent falsification-oriented audit against exact repository evidence.
version: 2.0.0
metadata:
  author: Inversion Labs
  role: independent-integration-red-team
---

# Adversarial Integration Audit

## Use when
- A prior session/author claims a PR or integration is correct, minimal, frozen, or merge-ready.
- A security/control repair must be shown to stop the prohibited effect, not merely pass tests.
- A claimed baseline/freeze anchor or REQUIRED-vs-independent change boundary needs recomputation.

## Do not use when
- You are the implementing agent still changing the branch; finish implementation first.
- The task is ordinary verification strategy rather than independent adversarial review; use `verification-workflows`.
- The task is to execute a split/merge plan; this audit may recommend one but remains read-only unless separately authorized.

## Authority and scope
Own **independent recomputation, falsification, baseline/diff integrity, minimal-boundary classification, control-efficacy testing, and audit verdicts**. Treat prior reports—including your own—as claims, not evidence. Do not modify production source, tags, history, PR state, or frozen artifacts during the audit.

## Workflow
1. **Freeze the audit identities.** Record authoritative base/freeze ref, candidate head, merge base, PR metadata, tree identities, and required checks. Fetch first when remote state matters.
2. **Recompute scope from Git.** Enumerate every changed path/mode/submodule/symlink/permission and relevant config/lock/build metadata. Do not copy file counts or scope labels from the author's report.
3. **Validate the baseline/freeze.** Prove tag/ref object, target commit/tree, manifest/content hashes using the correct hash domain, and whether candidate ancestry actually descends from the claimed base.
4. **Classify each change.** Mark `REQUIRED`, `INDEPENDENT_HARDENING`, `EVIDENCE/DOC`, `OUT_OF_SCOPE`, or `UNRESOLVED`. A change is REQUIRED only when removing it breaks the accepted contract/build/test/runtime invariant or the frozen authority directly requires it—not because it is useful or adjacent.
5. **Audit configuration and supply-chain effects.** Check scripts, dependency/lock changes, install hooks, generated outputs, permissions, environment assumptions, and CI coverage. State what cannot be verified from repository contents alone.
6. **Test verification sufficiency.** Re-run the narrowest trustworthy checks and identify properties the current tests cannot observe. Classify gaps as acceptable, recommended, or blocker based on claimed scope/risk.
7. **Prove security-control efficacy when applicable.** Read the guard's decision surface, generate bypass classes that are not simply members of its own denylist, probe the guard, then escalate material allowed cases through the real public surface. Assert the forbidden side effect remains absent, not just that an error occurred. See `references/control-efficacy-audit.md`.
8. **Attack the audit's own assumptions.** Try alternate base interpretation, stale/current target differences, removed-rule regressions, input encodings/representations, and values the original tests did not enumerate. A non-reproduction becomes “not reproduced under current conditions,” not proof the historical claim was false.
9. **Derive the minimal correction/split only after findings.** If required and independent work are mixed, propose a non-destructive ownership/split plan with exact paths/hunks and proof obligations. Do not execute it during read-only audit.
10. **Issue an evidence-graded verdict.** For every material claim use `VERIFIED`, `INFERRED`, `NOT_VERIFIABLE`, or `FAILED/BLOCKER`, with command/artifact evidence and residual uncertainty.

## Failure and recovery
If the audit probe writes temporary state, confine it outside the source tree when possible, preserve the result needed for evidence, then restore/verify the source tree unchanged. If a control-efficacy probe could create material side effects, use an isolated fixture/sandbox and a harmless sentinel. If repository evidence contradicts a prior report, preserve both and correct the claim rather than “fixing” code to fit the report.

## Evidence required
Retain exact base/head identities, recomputed changed-path inventory, baseline/freeze proofs, per-change classifications, verification gaps, control-efficacy probes where relevant, and the final evidence-graded finding matrix. Reproducing test counts proves regression status only; it does not prove a claimed security control prevents the prohibited effect.

## Stop conditions
STOP on ambiguous base/freeze authority, unexpected source mutation, evidence requiring destructive history/tag changes, material control bypass, REQUIRED-vs-independent ambiguity that changes integration scope, or any blocker the current authorization does not permit you to repair. Return the smallest evidence-backed correction and wait for implementation authority.
