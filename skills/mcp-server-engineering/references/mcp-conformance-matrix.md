# MCP Conformance Matrix

Use this as a minimum test matrix; adapt cases to the current MCP specification, SDK, transport, and server authority model.

| Area | Required proof |
| --- | --- |
| Initialization | Supported protocol negotiation succeeds; unsupported versions fail truthfully. |
| Discovery | Tools/resources/prompts expose the intended names and schemas only. |
| Validation | Malformed, oversized, unknown, and unauthorized requests fail before effects. |
| Errors | Denial, invalid input, dependency failure, timeout, conflict, and internal fault remain distinguishable to the client. |
| Transport | Protocol frames are uncontaminated; diagnostics stay on their designated channel. |
| Effects | Required approvals/leases/audit/transaction preflight precede mutation; material writes receive authoritative read-back. |
| Concurrency | Overlapping calls preserve declared ordering, isolation, idempotency, and resource-lock semantics. |
| Cancellation | Cancellation/timeout does not create a false claim that an ambiguous effect never occurred. |
| Restart | Only declared durable state survives; interrupted effects reconcile before retry. |
| Observability | Request/tool/receipt correlation exists without raw secrets or unbounded payload logging. |
| Real client | At least one supported external MCP client exercises discovery, success, denial/failure, and representative effects over the real transport. |

A passing in-process handler test is not sufficient evidence for transport interoperability.