# Evidence Preservation and Falsification

## Preserve before repair

When an unexpected failure appears, preserve the state that made it observable before cleanup, retry, restart, broad process killing, cache deletion, dependency reinstall, or patching.

Minimum durable capture when relevant:
- exact command/action and UTC time
- complete stdout/stderr before filtering
- exit/status code
- source revision and working-tree state
- relevant tool/runtime versions and configuration identity
- artifact/file hashes for evidence that may change
- process/service state when runtime ownership matters
- the failing input/fixture/request/trace needed to reproduce

Store evidence somewhere that the cleanup path will not erase. If an unsafe cleanup already destroyed evidence, record that loss explicitly; do not reconstruct certainty after the fact.

## Falsification ladder

For a material PASS, ask what cheapest observation could prove it wrong:

1. **Negative input** — invalid/unauthorized/boundary input should fail in the intended way.
2. **Controlled dependency failure** — make the log sink, persistence layer, network, provider, or downstream service genuinely fail and observe fail-closed/recovery behavior.
3. **Fresh state** — clean clone/install/build, empty cache, process restart, or newly initialized store where stale state cannot rescue the artifact.
4. **Independent path** — verify through a second interface or observer that does not share the same mocked seam.
5. **Replay/repetition** — repeat flaky, timing-sensitive, or probabilistic behavior enough to characterize stability rather than report a lucky run.
6. **Contradictory case** — choose an input near the claimed boundary where an overbroad implementation would reveal itself.

A failed falsification attempt is evidence. It is not permission to delete the failure and repeat until green.

## Evidence freshness

Evidence becomes stale when the property-bearing target changes: source revision, binary, config, dependency lock, environment, provider behavior, schema, or other material state. Re-run only the checks whose assumptions were invalidated; do not ritualistically repeat unrelated successful evidence.
