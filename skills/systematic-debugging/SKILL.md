---
name: systematic-debugging
description: >
  Use when a technical failure, regression, flaky behavior, performance anomaly,
  build break, or integration defect needs root-cause isolation before repair.
version: 2.0.0
metadata:
  author: Inversion Labs
  role: root-cause-debugger
---

# Systematic Debugging

## Use when
A system behaves differently from its intended or previously observed behavior and the cause is not already proven.

## Do not use when
- The task is feature design or implementation with no defect to diagnose.
- The user only wants an explanation of already-established behavior.
- A root cause is already demonstrated and the remaining work is only the bounded fix; hand off to the implementation/TDD owner.

## Authority and scope
Own **diagnosis and root-cause proof**. Do not widen product scope, bundle opportunistic refactors, or convert a plausible symptom into a claimed cause. A proposed fix is downstream of evidence, never a substitute for it.

**Iron law:** no fix before a falsifiable root-cause investigation.

## Workflow
1. **Create the feedback loop.** Reproduce the exact symptom with the tightest practical command, test, request replay, browser script, trace replay, harness, differential check, or high-repetition flake loop. The loop must be capable of going red for this defect and green when it is gone.
2. **Bound the failing layer.** Read the full error and recent changes. In multi-component systems, observe inputs/outputs and configuration at each boundary until the failure is localized. Trace bad values upstream to their first incorrect origin.
3. **Minimize the reproduction.** Remove inputs, state, configuration, callers, and steps one at a time while preserving the failure. Keep only load-bearing conditions.
4. **Compare with reality.** Find a working analogue or authoritative reference and enumerate differences without dismissing small ones.
5. **Rank falsifiable hypotheses.** Produce a small set of plausible causes. For each, state the observation that would support or falsify it. Test the cheapest discriminating hypothesis first.
6. **Probe one variable.** Prefer inspection/breakpoints over noisy instrumentation. If temporary logging is required, tag it so cleanup is mechanically searchable. Failed probes return to diagnosis; they do not accumulate into a patch pile.
7. **Prove the cause.** A hypothesis graduates to root cause only when the evidence explains the observed failure and predicts a discriminating result.
8. **Hand off the fix.** Create the smallest regression test that fails before the repair, implement one root-cause fix, then run focused and broader regression checks.

## Failure and recovery
If the defect cannot be reproduced, increase observability or reproduction rate rather than guessing. If a probe changes system state, restore the pre-probe state before the next hypothesis. If three materially different fix attempts fail, stop treating the problem as a local defect: return to the evidence map and explicitly test whether the architecture or assumed contract is wrong.

For flaky defects, report reproduction rate and confidence. `UNVERIFIED` is preferable to a convenient story.

## Verification
A debugging claim is complete only when evidence shows:
- the original symptom is reproducible or its prior evidence is preserved;
- the proposed root cause predicts the observed failure;
- a regression test/probe fails before and passes after the bounded fix, when technically possible;
- the focused check passes repeatedly enough for the failure mode;
- relevant broader checks show no introduced regression;
- temporary diagnostics are removed or intentionally retained.

## Stop conditions
STOP before proposing a fix when the symptom is not bounded, evidence contradicts the current hypothesis, the necessary environment cannot be observed, or the root cause remains speculative. STOP after three failed fixes and reopen the architectural assumptions instead of attempting fix four.
