---
name: mcp-server-engineering
description: >
  Use when designing, implementing, or hardening a maintained MCP server whose tools/resources/prompts,
  transport, lifecycle, capability boundaries, errors, and client interoperability must be explicit and testable.
version: 2.0.0
metadata:
  author: Inversion Labs
  role: mcp-server-contract-engineering
---

# MCP Server Engineering

## Use when
- Building or refactoring an MCP server rather than a one-shot script.
- Tool/resource schemas, transport framing, lifecycle, concurrency, or client interoperability need deliberate design.
- Effectful tools need capability boundaries, receipts, auditability, or fail-closed behavior.
- A server appears correct in-process but fails under a real MCP client/transport.

## Do not use when
- The task is generic command-wrapper security; use `secure-command-execution` for that boundary.
- The task is only deployment/hosting resilience; use `deployment-resilience-verification`.
- The user needs an MCP client/host integration and no server behavior is changing.

## Authority and scope
Own **MCP surface design, tool/resource/prompt contracts, protocol/transport correctness, server lifecycle, concurrency semantics, error truthfulness, capability enforcement integration, real-client conformance, and server observability**. Do not broaden tool authority because the protocol can carry it, and do not encode deployment/provider policy into the protocol layer.

Prefer the maintained official SDK appropriate to the implementation environment and pin/test the supported protocol/SDK range. Do not copy protocol details from memory when the current SDK/spec can define them.

## Workflow
1. **Define the server contract.** Identify clients/hosts, chosen transport(s), protocol/SDK compatibility, server identity/version, startup/shutdown behavior, and whether each capability is read-only, mutating, external-effectful, or privileged.
2. **Design narrow surfaces.** Give every tool/resource/prompt a precise name, trigger/use case, typed input/output schema, bounded sizes, error model, and authority requirement. Prefer multiple explicit capabilities over one “run anything” escape hatch.
3. **Bind effects to policy.** Resolve roots, credentials, leases/approvals, executable profiles, network destinations, and effect class before execution. Delegate command shaping to `secure-command-execution`; filesystem/database/domain tools need equivalent positive boundaries.
4. **Make error semantics truthful.** Protocol-level success must not wrap a denied/failed operation as successful content. Return structured coded failures in the SDK's intended error/result channel and make clients able to distinguish denial, invalid input, unavailable dependency, timeout, conflict, and internal fault.
5. **Keep transport framing pure.** Protocol channels carry protocol frames only; diagnostics/logging use the designated side channel. For stdio, stray stdout is protocol corruption. For network transports, validate session/origin/auth/lifecycle according to the current transport contract.
6. **Choose concurrency semantics deliberately.** Assume clients may issue overlapping requests. Serialize only resources that require it; otherwise use per-resource locking/idempotency/transactions. Never rely on tests being sequential if the server contract is concurrent.
7. **Preflight fail-closed obligations.** If audit/backup/authorization/transaction preparation is required before a mutation, prove it can succeed before performing the effect. Post-hoc logging cannot make an unaudited mutation fail-closed.
8. **Verify postconditions.** A handler returning normally is not proof the requested effect occurred. Read back or query the authoritative state for material writes and return evidence/receipt identifiers rather than model-facing success prose alone.
9. **Test over a real transport/client.** Exercise initialize/discovery, representative calls, malformed/denied requests, concurrency, cancellation/timeouts, server restart where state matters, framing/logging, and client-visible error semantics. See `references/mcp-conformance-matrix.md`.
10. **Observe without leaking.** Correlate request/tool/receipt IDs, timings, result class, and bounded diagnostics while structurally redacting secrets. Never log raw credential-bearing environment or opaque user payloads by default.
## Failure and recovery
If protocol compatibility, authorization, preflight obligations, or transport integrity cannot be established, fail closed before the effect. A dropped client connection is not proof an effect did not occur: reconcile authoritative state and receipts before retrying. After restart, restore only explicitly durable state; never infer completion from handler entry or logs alone.

## Verification and evidence
Require evidence at the layer of the claim: schema/contract tests for surfaces, protocol traces for framing and lifecycle, authoritative read-back for effects, concurrency probes for ordering claims, and at least one supported real client/transport for interoperability. Keep protocol success, domain success, and verification status distinct.

## Stop conditions
STOP if the requested capability requires authority the server does not possess, if a required fail-closed control cannot be preflighted, if protocol/SDK behavior is materially uncertain and untested, or if postcondition evidence is unavailable for a consequential effect. Do not replace a blocked narrow capability with a broader executor.
