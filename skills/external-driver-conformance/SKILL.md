---
name: external-driver-conformance
description: >
  Use when a genuine external agent, harness, or executor must be proven to conform
  to a frozen driver boundary without inheriting the host system's governing authority.
version: 2.0.0
metadata:
  author: Inversion Labs
  role: external-executor-boundary-proof
---

# External Driver Conformance

## Use when
- A frozen driver/interface contract and authority matrix already exist.
- A real third-party/external executor must run through that boundary.
- The host must prove replaceability without trusting external outputs as authoritative.

## Do not use when
- The driver contract is still being designed.
- A local/reference driver is the only executor under test.
- The task is ordinary provider integration without a frozen authority boundary.

## Authority and scope
Own **proof that one genuine external executor can be adapted to the frozen driver contract while remaining a replaceable, untrusted execution component**. The adapter may translate work orders, lifecycle state, observations, artifacts, receipts, and errors. It must not mint host policy decisions, capability grants, verification verdicts, evidence authority, claims, or completion merely because the external run succeeded.

## Preconditions
- Frozen contract/schema/version and reference conformance suite are identified.
- Host-versus-driver authority is explicit and machine-testable where possible.
- External dependency/version is pinned reproducibly in an isolated environment.
- Sandbox/network/filesystem/environment permissions are enumerated before execution.

## Workflow
1. **Prove the baseline.** Run the unchanged reference-driver/conformance gates before adding the external adapter. Record contract revision and baseline results.
2. **Select one real executor.** Choose a candidate that can be installed and executed reproducibly under the required sandbox. Do not broaden scope by integrating several at once.
3. **Pin and isolate it.** Lock exact dependencies; use a dedicated environment/process identity; expose only allowlisted environment variables, filesystem roots, network targets, and subprocess capabilities.
4. **Build the thinnest adapter.** Translate host work order → external request and external result → untrusted host observation/artifact. Keep host authority types unreachable from the external process and adapter public API.
5. **Run a bounded real task.** Exercise actual external execution—not a mocked call—against a narrowly scoped target. Hash/fingerprint protected inputs before/after and keep writable staging separate where read-only behavior is promised.
6. **Test capability/lifecycle enforcement.** Prove expired/revoked/wrong-scope/wrong-driver/wrong-mission/max-use or analogous authorization failures are rejected at every dispatch/resume/reconcile boundary where the contract requires them.
7. **Minimize context.** Supply only the context required for the task; plant sentinel data outside the allowed slice and prove it is not exposed.
8. **Treat output as hostile input.** Reject forged authority objects, identity mismatch, sequence rollback, path/symlink escape, conflicting duplicates, receipt/artifact substitution, malformed output, and cross-task/cross-mission replay. See `references/authority-boundary-threats.md`.
9. **Exercise interruption and uncertainty.** Crash/interrupt the external process, restart the host/adapter, and prove the contract's idempotency/reconciliation semantics: no silent duplicate execution and no automatic retry when external state is indeterminate unless the frozen contract authorizes it.
10. **Prove removal and substitution.** Disable/remove the external adapter and confirm the host/reference path still works. Run an equivalent work order through reference and external drivers and compare host-level semantics, not model text.
11. **Re-run unchanged conformance.** The frozen reference suite must remain unchanged and green. Add external-specific adversarial tests without weakening baseline assertions.
12. **Verify fresh.** From a clean environment run schema/drift/build/static gates, reference conformance, external happy/negative paths, restart/reconciliation, removal/swap, full relevant suite, secret scan, and source-diff checks.

## Failure and recovery
If safe reproducible execution is impossible, return `BLOCKED` rather than weakening sandbox or contract. If the external framework demands authority outside the frozen driver boundary, reject that adapter or introduce an explicitly reviewed containment layer; do not widen host authority silently. If restart state is unknowable, preserve it as indeterminate and stop automatic replay.

## Evidence required
Retain frozen contract/version, reference baseline, external dependency lock, sandbox policy, real-run transcript/receipts, protected-input before/after fingerprints, negative authority tests, interruption/reconciliation evidence, removal/swap result, and fresh final suite output. External process exit 0 alone proves neither authority safety nor task completion.

## Stop conditions
STOP on frozen-contract drift, authority leakage, sandbox escape, context over-disclosure, forged authoritative output acceptance, unexplained duplicate/replay, indeterminate external state with unsafe retry, reference-suite regression, or inability to remove the external adapter cleanly.
