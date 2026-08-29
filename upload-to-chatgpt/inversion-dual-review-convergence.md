---
name: inversion-dual-review-convergence
description: >
  Use when substantial architecture, security, evaluation, release, or high-risk implementation work benefits from two independent reviewers or local-model critics before integration.
version: 0.1.0
metadata:
  author: Inversion Labs
  role: review-convergence
---
# Dual Review Convergence

Use independent reviewers to create adversarial diversity, then converge on one evidence-backed implementation—not two mutually reinforcing opinions.

## Review design
1. Freeze the exact base/head or artifact digest under review.
2. Give both reviewers the same immutable evidence world but different attack surfaces.
   - Reviewer A: architecture, implementation, authority, security, concurrency, compatibility.
   - Reviewer B: epistemics, statistics, benchmark validity, hidden assumptions, false confidence, evaluator self-validity.
3. Reviewers are read-only. They report Critical/Important findings with exact evidence and required correction.
4. Do not let either reviewer see the other's reasoning before its independent pass completes.
5. Adjudicate every material finding against source/tests/spec. Reject false positives explicitly.
6. Convert surviving findings into RED tests where executable, fix them, then run the full relevant regression suite.
7. Re-review the exact fix head. Integration fails closed until both focused passes are clean or remaining disagreement is explicitly accepted by the user.

## Never
Do not count reviewer agreement as proof. Do not average conflicting claims. Deterministic repository evidence outranks persuasive model prose.
