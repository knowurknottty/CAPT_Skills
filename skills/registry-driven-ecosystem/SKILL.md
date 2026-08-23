---
name: registry-driven-ecosystem
description: >
  Use when many consumers must derive consistent views from a versioned metadata registry
  with semantic validation, typed relationships, provenance, compatibility, and reproducible generation.
version: 2.0.0
metadata:
  author: Inversion Labs
  role: metadata-authority-architecture
---

# Registry-Driven Ecosystem

## Use when
- UI, CI, docs, release tooling, search, agents, or APIs duplicate the same project/system metadata.
- A living ecosystem needs one machine-readable authority with explicit provenance and relationship semantics.
- Hardcoded consumer arrays/config are drifting independently.
- The registry must evolve without breaking older readers/writers or hiding unknown/partial truth.

## Do not use when
- The registry is merely a cache/view of an authority owned elsewhere and should not become source of truth.
- The task is runtime architecture reconstruction; use `forensic-architecture-reconstruction` first.
- The problem is only one static config file with one consumer and no meaningful ecosystem semantics.

## Authority and scope
Own **registry schema, authored-vs-generated boundaries, identity, relationship ontology, provenance fields, compatibility/versioning, semantic validation, deterministic aggregation, and consumer contract**. Do not claim a registry field is true about the live world merely because it validates structurally, and do not let downstream presentation invent authoritative metadata absent from the registry.

The pattern is: **observed/curated reality → authored records with provenance → validated/generated aggregate → consumers**. Unknown is preferable to fabricated precision.

## Workflow
1. **Define identity and authority.** Choose stable record IDs, authored source files, generated aggregates, and which fields the registry truly owns versus mirrors from external authorities.
2. **Model semantic relationships.** Type edges by meaning rather than one generic links array. Dependency/extension/supersession edges may require acyclicity; integration/association edges may legitimately cycle; symmetric relations must validate both directions. See `references/relationship-and-provenance.md`.
3. **Attach field-level provenance where truth can drift.** Record source/authority, evidence state, verification time/version, and refresh policy for material fields. `curated`, `inferred`, `verified`, and `needs-confirmation` must remain distinguishable.
4. **Separate authored from generated artifacts.** Per-record metadata is authored; indexes/aggregates/search artifacts are regenerated deterministically. Generated files carry an explicit generated notice and are never hand-edited to bypass the source records.
5. **Version schema and compatibility.** Track schema version plus reader/writer compatibility separately. Breaking changes require an explicit migration path; reject unsupported future major versions rather than best-effort parsing unknown semantics.
6. **Validate semantics, not just JSON shape.** Check unique IDs, required/enum fields, relationship target/type rules, symmetry/acyclicity where applicable, provenance requirements, URL/reference classes, cross-record invariants, and generated-aggregate drift.
7. **Build reproducibly.** Sort deterministically, derive timestamps from reproducible inputs when artifacts are committed, and make regeneration+diff a verification gate. Equivalent authored inputs should yield byte-equivalent semantic output.
8. **Make consumers read the registry.** UI/docs/search/CI/release tooling consume the validated aggregate or a stable reader API. Consumer-specific presentation belongs downstream; it must not fork canonical project/system facts.
9. **Emit machine-readable verification.** Record schema/registry identity, validation results, source coverage, generated-artifact digest, unresolved fields/issues, and freshness limits so downstream automation can distinguish structural green from evidence completeness.
10. **Report truth scope precisely.** Say “consumer renders from a validated registry” when that is what is proven. Claim “live ecosystem synchronized/verified” only when external authorities were actually refreshed and reconciled.

## Failure and recovery
If generated output drifts, regenerate from authored records; do not patch the aggregate. If a relation fails because the ontology is too coarse, correct the edge type/schema rather than weakening every cycle rule. If external truth is unavailable, retain the last verified value only with visible freshness/provenance or mark it unknown; never silently refresh timestamps without refreshing evidence.

## Evidence required
Retain schema/compatibility version, authored-record identities, generation command/version, semantic-validation result, relationship/provenance checks, aggregate digest, consumer contract tests, unresolved/needs-confirmation fields, and external freshness scope. A structurally valid registry with unverified content is structurally valid—not globally truthful.

## Stop conditions
STOP when registry authority conflicts with a stronger external/system authority, stable identity cannot be defined, relationship semantics are ambiguous enough to produce false validation, a breaking schema change lacks migration, generated output cannot be reproduced, or consumers still contain competing authoritative copies. Report the exact authority/drift boundary rather than declaring a single source of truth prematurely.

Load `references/relationship-and-provenance.md` for ontology/provenance rules and `references/compatibility-and-generation.md` for migration and reproducibility gates.
