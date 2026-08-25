# Security Routing Matrix

Use the narrowest lane that owns the security boundary. This router coordinates; it does not replace specialists.

| Security question | Primary lane | Required boundary |
|---|---|---|
| User/agent input reaches a CLI or child process | `secure-command-execution` | Positive argv/cwd/env/stdin capability grammar; no authority grant |
| Claimed integration/security repair needs independent falsification | `adversarial-integration-audit` | Read-only independent recomputation and efficacy test |
| Maintained MCP server surface/protocol is changing | `mcp-server-engineering` | MCP contracts, transport, lifecycle, errors, concurrency, real-client proof |
| Live artifact/rollback/degraded behavior is the claim | `deployment-resilience-verification` | Source-to-live provenance plus failure/recovery proof |
| Repository history/canonical source is uncertain | `codebase-archaeology` | Read-only lineage/provenance; no canonicality by recency |
| Architecture/security control reachability is disputed | `forensic-architecture-reconstruction` | Executable/config/build/runtime evidence hierarchy |
| Credential exposure/rotation | secret-management procedure | Credential references; rotation only with authority and exposure evidence |
| Active unauthorized mutation/process | incident containment procedure | Exact process/supervisor identity, minimal stop control, pre/post evidence |
| OSS/supply-chain compromise hypothesis | forensic acquisition | Read-only source/ref/package provenance; hypothesis != compromise |
| Username/public-account correlation | authorized public-source research | Public evidence only; username match != person identity |

A task may require several lanes. Preserve each lane's authority boundary and reconcile findings afterward; do not create one super-tool with the union of all permissions.
