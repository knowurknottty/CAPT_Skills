# Reachability and Generation Traps

## Reachability before dead-code claims
A component absent from the public entrypoint may still be imported, called indirectly, registered dynamically, built as a library, loaded by configuration, or consumed by another runtime. Before `DEAD`, inspect import/reference closure, build inclusion, registry/config consumers, plugin/discovery mechanisms, and generated/runtime loading. `GHOST` is the converse: catalogued or documented with no backing implementation/reachable artifact.

## Count domains
Raw filesystem counts are not architecture counts. State exclusions for virtualenvs, package/vendor trees, build outputs, caches, generated artifacts, archives, and worktree duplicates. Report distinct counts when they answer different questions: source files, registered modules, compiler-known entrypoints, compiled artifacts, active runtime modules.

## Generation versus recency
Track at least four axes independently: lineage/generation, commit recency, deployment recency, and observed runtime use. A later commit to an older architecture does not make it the newest generation; an advanced experimental generation does not make it the active production runtime.

## Documentation chronology
A newer document is not automatically stronger evidence. Use dates to reconstruct how claims evolved, then verify each current architectural statement against higher-tier evidence.
