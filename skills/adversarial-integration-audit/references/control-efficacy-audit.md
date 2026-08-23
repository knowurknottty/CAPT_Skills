# Control-Efficacy Audit

A green regression suite does not prove a security/safety control blocks the prohibited effect.

## Two-stage proof
1. **Decision-surface probe** — read the guard and enumerate what it inspects, normalizes, skips, short-circuits, or delegates. Generate cases from adjacent input families and representation changes, not just values already named in a denylist/test table.
2. **Real-boundary effect probe** — for any materially allowed case, invoke the actual public dispatch/tool/API surface inside an isolated harmless fixture and assert a forbidden side-effect sentinel remains absent.

## Strong evidence
- guard rejects the input for the intended reason;
- public surface also rejects/contains it;
- forbidden effect does not occur;
- legitimate negative-control behavior still works;
- audit fixture/source state is restored and verified.

## Common false proof
- looping over the same denylist the control uses;
- asserting only an error string/status;
- testing a shape no realistic caller can produce;
- validating sanitized logs without checking the original sensitive field/path;
- reproducing the author's test count and inferring exploit closure.

## Deleted-rule review
When a repair removes an over-broad rule, treat that deletion as a security-relevant change too. Enumerate the protections it previously supplied and test whether intended coverage remains through a narrower mechanism.
