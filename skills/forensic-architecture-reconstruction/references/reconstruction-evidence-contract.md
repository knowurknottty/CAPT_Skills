# Reconstruction Evidence Contract

For each material architectural claim record:
- `claim_id` and concise claim;
- system/repo/generation/runtime scope;
- authoritative revision/time boundary;
- evidence paths/commands/observations and source tier;
- status: `VERIFIED`, `INFERRED`, `UNRESOLVED`, or `CONTRADICTED`;
- counterevidence and competing claims;
- affected component/authority/pipeline;
- confidence and what would falsify or resolve the claim.

## Canonical blueprint fields
A reconstructed component should identify its role, owner/authority, inputs/outputs, callers/consumers, dependencies, state/persistence, process/runtime boundary, side effects, failure behavior, implementation location, build/deploy status, observed-runtime status when known, lineage/replacement, and unresolved contradictions.

## Runtime truth discipline
`source exists`, `build artifact exists`, `deployable`, `configured`, and `observed running` are distinct states. Likewise, `gate exists`, `gate is called`, `gate can deny`, and `denial prevents the protected side effect` are distinct enforcement claims. Never collapse these states into one “implemented” label.
