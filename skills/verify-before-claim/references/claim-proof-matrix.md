# Claim → Proof Matrix

Choose evidence that observes the property actually being claimed. A nearby proxy is useful diagnostic evidence, not proof of a broader claim.

| Claim surface | Direct proof | Common false substitute |
|---|---|---|
| UI interaction | Real user-path input/click plus observed state/DOM/accessibility result | Handler exists; synthetic JS invocation; screenshot before interaction |
| API behavior | Request against the claimed server/config plus status/body/side effect | Route exists in source; mocked controller test |
| CLI behavior | Real invocation plus exit code and stdout/stderr/side effect | Argument parser imports; help text renders |
| Build artifact | Clean build plus artifact identity; load/run when runtime behavior is claimed | Compiler exits 0 while stale artifact already exists |
| Pure function | Executed tests with non-trivial and boundary inputs | Type checking or source inspection |
| Integration | Real component boundary exercised end-to-end or via faithful conformance harness | Each component passes independently |
| Displayed data | Trace displayed value to the real source field/query/event for that state | Hardcoded/mock value that merely looks plausible |
| Persistence | Mutate, restart/reload through the real persistence boundary, observe retained state | In-memory value changed |
| Security control | Controlled adversarial/failure case proves the forbidden action is denied | Guard function exists in source |
| Performance | Measurement under declared workload/hardware/statistical method | Algorithm seems fast; one unrecorded run |
| Fresh install/clone | Reproduce from clean declared dependencies and exact source revision | Developer working tree passes |

## Scope dimensions

Record only dimensions that materially affect the claim, for example:

- source revision / artifact digest
- environment or deployment
- provider/account/permission set
- operating system/device/browser
- data fixture or production slice
- feature flags/configuration
- execution mode (unit, integration, E2E, packaged artifact)
- time/freshness when external state can change

Do not invent coverage. If only one dimension was exercised, classify only that dimension as VERIFIED.
