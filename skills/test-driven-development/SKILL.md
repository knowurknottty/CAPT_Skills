---
name: test-driven-development
description: >
  Use when maintained code is being added, changed, refactored, or repaired and
  executable behavior can be specified before the production implementation.
version: 2.0.0
metadata:
  author: Inversion Labs
  role: behavior-first-implementation
---

# Test-Driven Development

## Use when
- Adding or changing maintained executable behavior.
- Fixing a proven defect after root-cause diagnosis.
- Refactoring behavior that must remain invariant.
- Designing an API whose contract can be expressed as observable examples.

## Do not use when
- The task is research, prose, static data curation, or another artifact with no executable behavior.
- Code is an explicitly disposable spike; discard the spike before production implementation begins.
- An active incident requires immediate containment or rollback. Contain first; do not call the mitigation a verified fix. Use TDD for the durable repair.

## Authority and scope
Own the **implementation loop for one observable behavior at a time**. Do not replace root-cause debugging, architecture decisions, acceptance testing, or release verification. Tests define externally meaningful behavior; they must not fossilize incidental implementation structure.

## Workflow
1. **Choose one vertical behavior slice.** State the smallest user/system-visible behavior that moves the artifact forward. Avoid writing a horizontal pile of speculative tests.
2. **RED — write one discriminating test.** Exercise the real seam when practical. Use mocks only where an external boundary cannot be made deterministic or safely exercised.
3. **Prove RED.** Run the narrow test and observe failure for the intended missing behavior—not syntax, fixture, environment, or unrelated failure. If it passes immediately, the test does not prove the new behavior is absent; repair the test or choose a different slice.
4. **GREEN — implement minimally.** Add only enough production code to satisfy the failing behavior. Do not bundle refactors, adjacent features, or speculative abstraction.
5. **Prove GREEN.** Re-run the exact RED command. Then run the smallest relevant regression set that can reveal collateral breakage.
6. **REFACTOR while green.** Remove duplication, improve names and structure, or extract abstractions without adding behavior. Re-run tests after each meaningful refactor step.
7. **Repeat vertically.** Let each completed slice teach the next interface/test. Edge cases become their own RED→GREEN cycles.

For defects, pair with `systematic-debugging`: prove the cause first, then encode the regression so the fix cannot silently return.

## Failure and recovery
If RED fails for the wrong reason, fix the test/harness before production code. If GREEN requires broad unrelated changes, stop and reconsider the slice or architecture. If a refactor breaks tests, revert to the last green state and take a smaller step. If a test requires pervasive mocking, treat that as coupling/design evidence rather than normalizing a fake test environment.

Never rewrite an assertion merely to make an unexpected implementation pass unless the intended contract itself changed and that change is explicitly justified.

## Verification
A TDD claim requires evidence that:
- the relevant test was observed failing for the intended reason before the production change;
- the same test passes after the bounded implementation;
- relevant existing tests still pass;
- the test asserts behavior rather than implementation trivia;
- any mocks/fakes are bounded to unavoidable external seams;
- refactoring occurred only from a green state.

Record the RED and GREEN commands/results when evidence durability matters.

## Stop conditions
STOP if the intended behavior is not clear enough to assert, the failure cannot distinguish missing behavior from harness failure, the proposed implementation exceeds the tested slice, or the only path to green is changing the expected result to match unapproved behavior.
