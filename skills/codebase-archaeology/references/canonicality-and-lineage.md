# Canonicality and Lineage Evidence

Canonicality is a claim about authority for a subsystem; lineage is a claim about origin/history. Keep them separate.

## Evidence ladder
Strong evidence includes:
- explicit runtime/build/deploy references to the candidate;
- commit ancestry and shared history;
- remote identity plus matching commit graph;
- pinned submodule/worktree relationships;
- current entrypoint/CI/package wiring;
- direct reverse imports/config references.

Weaker evidence includes README claims, names, directory mtimes, file counts, or “looks newer.” Use those as clues, not proof.

## Required record
For each material classification capture:
- candidate/subsystem;
- proposed label;
- evidence;
- counterevidence;
- confidence;
- unresolved questions;
- migration/compatibility risk if organization is later approved.

## Common traps
- Same directory name does not prove shared lineage.
- Same snapshot/hash does not prove which copy is authoritative.
- Newest commit does not necessarily mean latest architecture generation.
- Registry rows can be stale or refer to a different entity class than assumed.
- Documentation can describe intended state rather than runtime state.
- A dirty tree may contain the only current work even when another clone has a newer clean commit.

When evidence conflicts, prefer `unknown` or `canonical-probable` over forced certainty.
