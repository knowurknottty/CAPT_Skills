---
name: verify-before-claim
description: >
  Use when an empirical statement about an artifact, runtime, behavior, result,
  wiring, data, test status, or completion is about to be presented as fact.
version: 2.0.0
metadata:
  author: Inversion Labs
  role: claim-evidence-governor
---

# Verify Before Claim

## Use when
- Saying that code, a UI, API, CLI, build, integration, workflow, or deployment works.
- Reporting counts, states, outputs, wiring, performance, security properties, or completion.
- Handing work back with claims that a user could independently test.
- Reusing verification evidence from an earlier run, environment, commit, or session.

## Do not use when
- The statement is explicitly a proposal, hypothesis, estimate, preference, or future plan rather than an empirical claim.
- The task is to diagnose why something fails; use systematic debugging, then return here before claiming the repair works.
- No claim is being made beyond accurately quoting supplied evidence.

## Authority and scope
Own **claim status and evidence sufficiency**, not implementation. Never convert confidence, code inspection, compilation, a stale PASS flag, or another agent's assertion into runtime proof.

A claim is only as strong as the narrowest evidence that supports it. Evidence from one commit, environment, surface, account, device, data slice, or execution mode does not automatically generalize to another.

Use four evidence states:
- `VERIFIED` — directly observed evidence supports the exact claim in the declared scope.
- `INFERRED` — evidence supports a reasoned conclusion but does not directly observe the claimed property.
- `UNVERIFIED` — the claim has not been tested sufficiently.
- `BLOCKED` — verification cannot currently be performed; state why.

## Workflow
1. **Atomize the claim.** Rewrite broad language such as “everything works” into concrete falsifiable statements: target, behavior/property, scope, and expected observation.
2. **Choose proof before probing.** Define what observation would verify the claim and what result would falsify it. Prefer the user's actual interaction path over a nearby proxy.
3. **Verify the real target.** Exercise the artifact/environment being claimed: real click for an interaction, real request for an endpoint, real invocation for a CLI, real load/run for a shipped artifact, real source-backed value for displayed data.
4. **Capture evidence.** Record command/action, relevant target identity (commit/version/environment), result, exit/status code where applicable, and the smallest raw output needed to substantiate the claim.
5. **Match evidence to wording.** Narrow the claim whenever the evidence is narrower. Syntax check ≠ runtime behavior; unit test ≠ end-to-end integration; working tree ≠ clean clone; mock data ≠ live state.
6. **Falsify material claims.** For high-consequence or surprising results, test an edge, negative path, controlled failure, independent route, or fresh state that could reveal a false PASS.
7. **Classify each claim.** Mark it `VERIFIED`, `INFERRED`, `UNVERIFIED`, or `BLOCKED`. Never merge different scopes into one status.
8. **Preserve unexpected failure evidence before repair/cleanup.** Keep enough state to reproduce or investigate it; see `references/evidence-preservation-and-falsification.md`.
9. **Report exactly what is proven.** Separate verified facts from inference and residual unknowns. If nothing was verifiable, say so rather than substituting plausibility.

See `references/claim-proof-matrix.md` for surface-specific proof selection.

## Failure and recovery
If a verification tool fails, first determine whether the artifact failed or the verifier failed. Preserve the raw failure before retrying. If evidence is stale, re-run against the current target or downgrade the claim. If verification mutates state, record the pre-state and restore it when required. If a broad claim cannot be tested completely, split it into independently classified subclaims.

Never delete the only failing reproduction merely because a clean retry passes.

## Verification
A claim-verification pass is complete only when every published empirical claim has:
- a declared evidence state;
- target/scope identity sufficient to know what was tested;
- observed evidence appropriate to the property claimed;
- no known contradiction hidden by broader wording;
- preserved failure evidence when an unexpected result occurred.

For high-risk claims, include at least one falsification attempt or state why it was not possible.

## Stop conditions
STOP before saying `VERIFIED`, “works,” “wired,” “fixed,” “complete,” or equivalent when the real target was not exercised, evidence belongs to a different scope, a verifier failure is unresolved, contradictory evidence exists, or the only support is inspection/confidence. Report `UNVERIFIED` or `BLOCKED` instead.
