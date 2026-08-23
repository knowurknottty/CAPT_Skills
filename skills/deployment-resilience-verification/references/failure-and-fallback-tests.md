# Failure and Fallback Tests

Choose failures from the deployment/runtime contract rather than a fixed web-only matrix.

## Candidate failure classes
- missing/unreachable runtime dependency or provider;
- corrupt/missing generated asset or package resource;
- process startup exception, readiness timeout, or slow initialization;
- stale cache/proxy route serving an older artifact;
- dependency permission/auth failure;
- network partition or origin failure where failover exists;
- invalid config/environment value;
- recovery/restart after abrupt termination.

For each class define: injection method, safe isolation boundary, expected degraded state, forbidden effect, user-visible/system-visible signal, timeout, recovery action, and post-recovery acceptance probe.

“Resilient” does not always mean fail-open. Security-sensitive mutations may need fail-closed; interactive presentation may need a static/degraded experience; redundant services may fail over. Verify the product's declared policy and make the degraded state observable rather than silently masking it.
