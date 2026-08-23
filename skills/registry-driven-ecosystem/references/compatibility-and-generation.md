# Compatibility and Generation

## Reader/writer compatibility
Reader and writer compatibility are separate capabilities. A reader may safely consume schema 2.x while a writer must not emit it. Record supported major/minor ranges or minimum reader/writer versions explicitly. Unsupported future major semantics fail closed with a migration requirement rather than being silently ignored.

## Migration discipline
A breaking schema change defines: source version, destination version, transformation, fields whose meaning changed, loss/unknown handling, rollback or preserved original, and validation proving migrated records satisfy both semantic intent and generated-consumer expectations.

## Deterministic generation
Generated aggregates should depend only on authored records, generator version/config, and explicit reproducible build inputs. Sort records/keys where order is not semantic; avoid wall-clock timestamps in committed output unless time itself is authoritative input. Regenerate twice or use regeneration+git-diff to detect nondeterminism/drift.

## Consumer seam
Consumers should depend on a stable registry reader/query contract rather than the generator's internal layout. This lets search/rendering providers evolve without creating a second metadata authority.
