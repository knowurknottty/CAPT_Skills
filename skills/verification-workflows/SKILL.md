---
name: verification-workflows
description: >
  Use when a code, system, integration, control, or release needs a deliberate
  multi-layer verification strategy rather than one isolated proof check.
version: 2.0.0
metadata:
  author: Inversion Labs
  role: verification-strategist
---

# Verification Workflows

## Use when
- A change spans multiple components or evidence layers.
- A frozen specification must be tested for implementation conformance.
- A safety/security control must be proven effective under real failure.
- Stateful behavior needs restart, replay, concurrency, or persistence verification.
- A merge/release decision needs evidence beyond one local happy-path test.

## Do not use when
- One empirical claim only needs direct proof; use `verify-before-claim`.
- The root cause of a failing behavior is unknown; use `systematic-debugging` first.
- A specialist conformance/security/release skill already owns the exact domain; use this only to coordinate missing verification layers.

## Authority and scope
Own **verification strategy, layer selection, adversarial coverage, and evidence topology**. Do not change the specification being verified, repair production code during a read-only audit, or reinterpret failing evidence into PASS. `verify-before-claim` owns the final claim/evidence status; this skill supplies the verification program that generates that evidence.

Verification depth is risk-driven, not ritual-driven. Use the cheapest layer that can falsify the property, then add layers only where a lower layer cannot observe the relevant boundary or failure mode.

## Workflow
1. **Map authority and properties.** Identify the authoritative spec/contracts, target revision/environment, behaviors or controls to verify, and which artifact owns each truth. Record contradictions instead of silently normalizing them.
2. **Select verification modes.** Choose only the modes needed for the risk: static/schema, focused behavioral test, integration boundary, controlled failure/fail-closed, persistence/restart, concurrency, deterministic replay, fresh environment/reproducibility, security/adversarial, or release acceptance. See `references/verification-modes.md`.
3. **Capture the baseline.** Record target identity, relevant configuration, pre-change state, and the command/probe that currently demonstrates the property or defect. Preserve failing evidence before mutation.
4. **Run the narrow positive path.** Prove the intended behavior at the smallest layer that exercises the real implementation rather than a mock of the property under test.
5. **Attack the assumption.** Induce the failure, boundary, conflicting input, stale state, race, permission denial, process restart, or alternate environment most likely to create a false PASS. Controls are not verified until their denial/failure path is exercised when technically possible.
6. **Cross the real boundary.** If the property concerns IPC, persistence, provider/driver behavior, packaging, restart continuity, or deployment, exercise that boundary explicitly. Unit success cannot substitute.
7. **Check reproducibility when material.** Use fresh process/clone/install/build, deterministic replay, repeated runs, or independent implementation path when stale state or hidden nondeterminism could explain success.
8. **Reconcile evidence.** Map every result back to the exact property and authority source. A failure may identify a runtime defect, test defect, spec divergence, environment blocker, or verifier defect; classify before changing anything.
9. **Hand off claim status.** Feed exact evidence and residual gaps to `verify-before-claim`; do not broaden the scope of PASS.

## Failure and recovery
If the verifier itself fails, preserve its output and distinguish verifier failure from target failure. If a verification step mutates state, restore or recreate the baseline before the next discriminating run. If a controlled failure reveals that a supposedly fail-closed control still permits the side effect, treat the control as failed—not partially verified. If frozen artifacts conflict, add an explicit compatibility mapping or record the divergence; never edit the frozen authority to make the test green.

## Verification
A verification workflow is complete only when:
- every tested property maps to an authority source and evidence layer;
- the selected layer can actually observe that property;
- material denial/failure paths were exercised or explicitly BLOCKED;
- stateful/cross-process claims include the relevant boundary or restart when required;
- contradictory evidence is preserved and classified;
- final PASS scope excludes untested dimensions.

Load `references/high-rigor-recipes.md` for fail-closed controls, frozen-spec conformance, replay, and clean-environment verification.

## Stop conditions
STOP when the authority source is ambiguous, the test is proving a mock instead of the claimed property, a destructive verification lacks recovery, frozen truth would need to be edited to obtain green, contradictory evidence is unexplained, or required boundary/failure testing is unavailable. Report the blocked layer rather than promoting a weaker check into full verification.
