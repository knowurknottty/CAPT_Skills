---
name: forensic-architecture-reconstruction
description: >
  Use when a complex or multi-generation system's documented architecture may have drifted
  from implementation and the actual runtime, authority, dataflow, and lineage must be reconstructed from evidence.
version: 2.0.0
metadata:
  author: Inversion Labs
  role: architecture-forensics
---

# Forensic Architecture Reconstruction

## Use when
- The user asks what a complex system actually is, how it really works, or which architecture is canonical.
- Multiple repos/generations/runtimes/docs disagree about ownership, modules, pipelines, or current behavior.
- Architectural drift, duplicate implementations, ghost systems, or documented-but-unimplemented controls are plausible.
- A future simplification/migration decision needs an evidence-grade reconstruction first.

## Do not use when
- The task is inventory/provenance/duplicate mapping only; use `codebase-archaeology`.
- The task is a normal PR/code review or independent integration audit.
- The architecture is already frozen and only implementation conformance must be verified; use `verification-workflows`.
- The user is asking to redesign/optimize the system before reconstruction; treat optimization as a separate phase.

## Authority and scope
Own **architecture claim reconstruction, runtime/control/dataflow mapping, authority-source resolution, implementation-vs-documentation drift, reachability/status classification, cross-generation lineage, and evidence-graded canonical blueprints**. Do not edit production code/specs, declare one source canonical by recency alone, or turn reconstruction findings into an implementation plan unless separately authorized.

## Evidence hierarchy
Resolve claims by observable evidence strength: runtime behavior/compiled artifacts/executable code/tests → config/registries/entrypoints/dependencies → current specs → historical notes → roadmap/marketing. The hierarchy establishes what exists/executes, not what *should* be correct. Record contradictions.

## Workflow
1. **Freeze the boundary.** Identify candidate repos/generations, revisions, runtime surfaces, time boundary, and required questions. Reuse `codebase-archaeology` output rather than rescanning blindly.
2. **Build an authority map.** For lifecycle, state, schemas, routing, governance, persistence, modules, runtime selection, and interfaces, identify claimed owners and artifacts that actually exercise authority.
3. **Map executable architecture.** Trace real entrypoints through components, process boundaries, state stores, providers, IPC/network edges, side effects, and return paths. Separate build availability, deployability, and observed runtime activity.
4. **Reconstruct module/reachability status.** Classify components as `ACTIVE`, `REACHABLE_LIBRARY`, `BUILD_ONLY`, `TEST_ONLY`, `EXPERIMENTAL`, `SUPERSEDED`, `GHOST`, `DEAD`, or `UNRESOLVED`. Never infer dead code from naming or non-entrypoint status alone; compute references/import/call/build reachability where material.
5. **Reconcile competing generations.** Track lineage and distinguish architectural generation, commit recency, deployment/runtime use, and source-of-truth status. “Newest commit” and “most advanced generation” are separate claims.
6. **Test architectural claims.** For every load-bearing claim—module count, feature parity, persistence, acceleration, governance enforcement, deterministic replay, compiled path, fail-closed control—trace the real implementation and verify the observable property. Presence is not enforcement; source is not build output; registry entry is not runtime reachability.
7. **Map drift and contradictions.** For each conflict, record competing claim, evidence on each side, likely origin/time boundary, current consequence, and status (`VERIFIED`, `INFERRED`, `UNRESOLVED`, `CONTRADICTED`).
8. **Use independent passes where ambiguity is high.** Partition architecture/runtime/dependency/history/control questions so reviewers do not inherit conclusions, then reconcile against evidence. Independence is a tool for variance reduction, not a ritual requiring arbitrary agent counts.
9. **Produce the reconstruction.** Emit only needed blueprints: architecture graph, authority map, runtime matrix, module/lineage registry, stateflow maps, contradiction ledger, and unresolved questions. See `references/reconstruction-evidence-contract.md`.
10. **Separate reconstruction from evolution.** Recommendations may identify consequences or investigation priorities, but redesign, deletion, consolidation, migration, and implementation belong to a separately authorized optimization/planning phase.

## Failure and recovery
If evidence collection mutates a target, stop, preserve the mutation evidence, restore only through an authorized/reversible method, and re-establish the baseline before continuing. If two high-tier artifacts disagree, do not average them: identify whether they represent different runtime paths, versions, scopes, or a genuine contradiction. If a count depends on filesystem discovery, exclude vendored/build/worktree copies explicitly and show the counting domain.

## Evidence required
Retain revision/runtime identities, authority-source map, executable entrypoint/dataflow evidence, component reachability/status rationale, cross-generation lineage, claim-verification probes, contradiction ledger, independent-review disagreements when used, and unresolved boundaries. Every canonical statement must be traceable to evidence or marked inferred/unresolved.

## Stop conditions
STOP when the target generation/runtime cannot be disambiguated, source coverage is too incomplete to establish an authority map, a supposedly read-only pass changes the target unexpectedly, high-tier evidence remains contradictory on a load-bearing claim, or the requested “canonical architecture” would require choosing a desired future design rather than reconstructing present/past reality. Report the exact ambiguity instead of manufacturing a blueprint.

Load `references/reconstruction-evidence-contract.md` for claim/status fields and `references/reachability-and-generation.md` for dead-code and version traps.
