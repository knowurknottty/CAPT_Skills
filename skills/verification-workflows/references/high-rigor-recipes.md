# High-Rigor Verification Recipes

## Fail-closed control efficacy

A wrapper named `strict`, `secure`, or `fail_closed` is not evidence. Prove the denial path:

1. Establish the normal mutation succeeds and identify its observable side effect.
2. Make the required safety dependency genuinely fail: audit sink unwritable, authorization denied, backup impossible, persistence unavailable, etc.
3. Attempt the guarded mutation through the normal public path.
4. Assert the operation reports refusal/failure **and** the forbidden side effect did not occur.
5. Restore the dependency and prove normal operation recovers.

A swallowed sink exception with a successful mutation is a failed control even if logs say “strict mode.”

## Frozen-spec conformance

When implementation must conform to frozen artifacts:

1. Build an authority map: which artifact owns each state, operation, schema, and invariant.
2. Trace every assertion to that authority. Do not add expectations because they seem ergonomic.
3. Record contradictions between frozen artifacts as findings.
4. Where names differ but semantics must interoperate, use one explicit compatibility mapping rather than silently renaming either authority.
5. Never patch the frozen spec to make implementation/tests green during conformance verification.

## Deterministic replay

When same logical input should produce an identical state/evidence chain:

- separate deterministic **ID** generation from deterministic **clock** generation;
- pin randomness/seeds and external input order;
- determine whether identifiers are opaque strings or structurally validated IDs before choosing a deterministic factory;
- exclude environmental values only when the contract explicitly says they are non-semantic;
- run at least two clean replays and compare canonical outputs/digests.

A shared counter for IDs and time hides causality: changes in allocation cadence shift timestamps and make replay failures hard to localize.

## Fresh-state verification

Use when prior state could rescue a broken artifact:

- record exact revision/artifact identity;
- create a clean process, checkout, install, database/store, cache, or build directory appropriate to the claim;
- install/build only from declared dependencies and source;
- run the same acceptance checks;
- preserve the clean-state failure before cleanup.

Working-tree PASS plus fresh-state FAIL is a blocker until the discrepancy is explained; it is not “environmental” by default.
