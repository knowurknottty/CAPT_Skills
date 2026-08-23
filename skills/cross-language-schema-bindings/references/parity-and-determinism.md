# Parity and Determinism

## Deterministic generation
For identical canonical input and generator version, output should be byte-stable when the contract promises reproducibility.

Control these common drift sources:
- unordered type/field/enum traversal;
- timestamps and host-local metadata;
- absolute temporary/workspace paths;
- locale-dependent formatting;
- unstable map/dictionary ordering;
- stale generated/build output accidentally reused.

Generate into two clean roots and compare relative file sets plus bytes. Comparing absolute temporary paths creates false drift.

## Behavioral parity
Compile success is weaker than contract parity. Use the same positive and negative fixtures in every runtime and compare:
- acceptance/rejection;
- normalized output/defaults;
- discriminator/union selection;
- required/optional/null semantics;
- canonical error code/path/value representation when errors are observable.

Language-native repr/stringification often differs. If error messages are part of the parity surface, represent embedded values canonically rather than with language-specific debug repr.

## Dependency ordering
Some languages evaluate aliases/classes eagerly while others tolerate forward references. Resolve the contract dependency graph once in the normalized model and emit in an order valid for each target without changing semantic identity.

## Hermetic parity runners
A parity runner must create/build what it imports, or depend on a declared preceding build step. It must not pass locally only because a stale `dist/`, wheel, generated module, cache, or editable install happens to exist.
