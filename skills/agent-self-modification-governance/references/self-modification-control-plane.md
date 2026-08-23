# Self-Modification Control Plane

A durable design separates four concepts:

1. **Authorship/provenance** — who created or changed the artifact.
2. **Permission** — who is allowed to mutate it now.
3. **Promotion/activation** — whether a candidate mutation influences future behavior.
4. **Recovery/audit** — how prior state and mutation history can be reconstructed.

The mutating actor may contribute provenance but must not be the sole authority for permission or promotion.

## Strong controls
- external/user/admin opt-in distinct from `created_by`/`authored_by`;
- candidate writes land outside live discovery by default;
- immutable or version-controlled originals;
- append-only/hash-chained mutation journal or equivalent tamper-evident history;
- before/after artifact digests and actor/origin identity;
- evidence handle attached to durable technique claims;
- scope binding to the task/project that generated the proposal;
- rate/volume limits and explicit high-risk review;
- atomic promotion with rollback;
- all autonomous writer paths consume the same policy decision.

## Control-efficacy test
For each writer path:
1. bind the real autonomous actor/origin;
2. attempt a real mutation under denied policy;
3. assert refusal and unchanged target digest;
4. run an authorized foreground mutation as a negative control;
5. check an unrelated artifact to prove the policy is scoped rather than a global kill switch.

A sidecar flag, UI toggle, or policy object that is never consulted by one writer path is decorative containment.
