# macos-computer-use — GOAT Forge Verdict

**Decision:** PASS — promote hardened candidate.

## Deterministic evidence
- Static GOAT contract: PASS; 730-word activation payload.
- Pressure invariants: 10/10 PASS.
- Secret scan: gitleaks clean.
- Driver/tool schema is discovered at runtime; donor-era action names and focus claims are non-normative.
- Target app/window/control must be uniquely bound before input.
- Semantic/AX identity outranks coordinates; stale UI state forces recapture/rebinding.
- Consequential effects require postcondition proof and ambiguity-safe retry handling.
- Sensitive permission/auth/2FA/payment/privacy surfaces remain fail-closed.

## Independent governed review
- CAPT / local Qwen3.8 MTPLX: complete semantic review PASS; final `MANDATORY=NONE`.
- CAPT / OpenRouter Nemotron 3.5 Lightning: malformed simulated-runtime finding discarded; static-policy re-adjudication PASS; final `MANDATORY=NONE`.

## Residual risk
Actual GUI automation still depends on the active macOS driver, its granted OS permissions, and target-app accessibility behavior. This skill requires runtime discovery and does not claim universal non-interference or stable AX behavior.
