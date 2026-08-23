# External Driver Authority-Boundary Threats

Adversarial coverage should be derived from the frozen contract, but these classes are commonly relevant:

- identity/driver/task/mission spoofing;
- forged policy, authorization, verification, evidence, claim, or completion objects;
- revoked/expired/stale capability use;
- scope escalation or cross-task replay;
- duplicate/conflicting observations and sequence rollback;
- path traversal, symlink escape, artifact substitution, receipt substitution;
- environment-variable or credential leakage;
- context sentinel exposure outside the authorized slice;
- unexpected network/subprocess/file writes;
- crash before/after side effect with unknown external state;
- replay after terminal/cancel state;
- adapter removal breaking the host/reference driver;
- dependency/version substitution changing semantics.

## Proof pattern
For every threat class, identify:
1. the protected invariant;
2. the external stimulus/forgery/failure;
3. the real boundary through which it is injected;
4. the host-side rejection/containment evidence;
5. the forbidden side effect that must remain absent.

A test that only asserts an error string without checking the forbidden effect may prove presentation, not enforcement.
