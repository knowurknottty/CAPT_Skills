# Verification Mode Selection

Select modes by the property under test. More layers are not automatically better; each layer must observe a distinct failure class.

| Mode | Use when | Minimum evidence |
|---|---|---|
| Static/schema | Shape, type, syntax, migration, generated-binding or contract vocabulary matters | Parser/compiler/schema check against the authoritative artifact |
| Focused behavioral | One function/component behavior is in question | Real implementation exercised with discriminating inputs |
| Integration boundary | Correctness depends on IPC, network, database, provider, driver, serialization, or process handoff | Real boundary or faithful conformance harness with both sides observed |
| Controlled failure / fail-closed | A control promises denial, audit durability, backup, authorization, rollback, or refusal on dependency failure | Induce the dependency/control failure and prove the forbidden mutation does not occur |
| Persistence/restart | State must survive process death/reload or remain isolated across sessions | Write through normal path, restart/reopen, read through normal path |
| Concurrency | Correctness depends on ordering, locking, idempotency, races, or shared state | Coordinated concurrent schedule plus invariant checks; repeat enough to expose timing failure |
| Deterministic replay | Same logical inputs should produce the same evidence/state chain | Pin independent ID/random/clock sources and compare repeated outputs/digests |
| Fresh environment | Stale caches, build outputs, dependencies, or working-tree state could create false green | Clean process/checkout/install/build at exact revision |
| Security/adversarial | Input trust, permission, secrets, boundaries, or hostile state matter | Negative/unauthorized/malformed case through the real control surface |
| Release acceptance | Claim concerns shippability rather than local code only | Required lower layers + package/artifact identity + install/run/deploy path appropriate to release |

## Escalation rule

Start with the narrowest mode capable of falsifying the property. Escalate when:
- the property crosses a boundary the current mode cannot observe;
- a happy-path PASS leaves an important denial/failure path untested;
- stale state or environment can explain the result;
- nondeterminism materially affects confidence;
- the claimed scope is broader than the evidence scope.

Do not escalate merely to accumulate test count.