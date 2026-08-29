---
name: inversion-release-closure
description: >
  Use when work is described as done, ready, mergeable, shippable, release-candidate, or when the user asks what remains before integration or release.
version: 0.1.0
metadata:
  author: Inversion Labs
  role: release-closure
---
# Release Closure

"Tests passed earlier" is not a release gate. Closure must be performed against the exact terminal head being shipped.

## Gate sequence
1. Confirm repo, branch, exact HEAD, and clean/intentional working tree.
2. Re-run the complete relevant test suite from that head; record count and failures.
3. Run lint/static checks required by the repository.
4. Build/package from the exact head when the project ships artifacts.
5. Test the installed/built artifact, not only the editable source tree, when installation behavior matters.
6. Run adversarial/security/self-tests and real integration smokes required by the release contract.
7. Resolve Critical/Important reviewer findings and repeat affected gates after fixes.
8. Commit final evidence/docs only if they are part of the release, then re-run any gate whose artifact bytes or claims changed.
9. Push the exact head, verify the remote ref, inspect PR/CI/review state, and only then call it integration-ready.

## Claim discipline
Separate: IMPLEMENTED, LOCALLY VERIFIED, INSTALLED-ARTIFACT VERIFIED, REMOTE VERIFIED, CI VERIFIED, MERGED, RELEASED. Never collapse these states into "done."
