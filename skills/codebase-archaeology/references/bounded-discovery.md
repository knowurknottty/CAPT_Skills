# Bounded Discovery

Large filesystem archaeology fails when discovery, content search, and hashing are fused into one unbounded traversal.

## Pattern
1. Enumerate the requested roots shallowly first.
2. Identify obvious vendor/cache/build/system trees and record exclusions rather than silently skipping them.
3. Build an explicit curated root list.
4. Scan one root at a time with a bounded runtime and append results after every completed root.
5. Separate discovery from expensive analysis: first enumerate candidates; then inspect git/manifests; then hash only the relevant file classes.
6. Preserve timeout/permission failures as coverage gaps.

## Guardrails
- Never report complete coverage unless every requested root is either scanned or explicitly classified as inaccessible/excluded.
- Avoid a single giant exclusion regex; test exclusions against known-positive targets.
- Distinguish repositories, worktrees, submodules, vendor copies, build artifacts, and ordinary directories before counting.
- For duplicate analysis, exclude generated/vendor noise and record the comparison scope.
- Hashing is evidence of content identity, not lineage by itself.

## Recovery
When a root exceeds the bound, split it at the next directory level and continue. Do not discard completed partial output or restart the same doomed unbounded command.
