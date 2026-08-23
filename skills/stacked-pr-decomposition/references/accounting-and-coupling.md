# Accounting and Coupling

## File accounting
For each proposed PR distinguish:
- **added**: absent at that PR's base and introduced by the scope;
- **modified**: present at that PR's base and changed by the scope;
- **deleted**: present at base and removed;
- **total touched**: distinct paths changed by that scope;
- **unique cumulative**: distinct paths represented by the stack so far.

A shared existing file touched by multiple scopes remains one unique path but must list each owned hunk separately. Per-PR line deltas need not sum naively when a file is created in one scope and edited later; terminal source-delta reconciliation is authoritative.

## Dependency classes
Keep separate graphs for:
1. **Git topology** — create-before-modify and branch ancestry.
2. **Semantic/runtime** — code/config behavior depends on earlier scope.
3. **Verification coupling** — a required test imports/spawns/reads a file owned by another scope.
4. **Release/frozen authority** — a file belongs to a fixed baseline or protocol layer.

A branch may be topologically valid while semantically coupled. A test dependency outside required CI is a documented deferred verification gap; the same dependency inside required CI is a construction blocker until ownership/order is corrected.

## Ownership rule
One path, one semantic owner unless a pre-existing shared file is explicitly split by non-overlapping hunks. Conditional rationales (“maybe”, “if needed”) mean ownership is unresolved and must fail manifest validation.
