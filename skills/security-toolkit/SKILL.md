---
name: security-toolkit
description: >
  Use when a security task spans multiple trust boundaries or security disciplines and needs threat triage,
  evidence preservation, authority control, specialist routing, remediation ordering, and verification.
version: 2.0.0
metadata:
  author: Inversion Labs
  role: security-triage-and-governance
---

# Security Toolkit

## Use when
- A security incident/audit crosses code, credentials, processes, supply chain, deployment, or public-source evidence.
- The right specialist workflow is unclear and choosing the wrong one could destroy evidence or broaden authority.
- Findings from multiple security lanes must be reconciled into one risk/remediation/verification plan.
- Active unauthorized effects may require containment before deeper analysis.

## Do not use when
- One narrow boundary already has a specialist: use `secure-command-execution` for command wrappers and `adversarial-integration-audit` for independent integration falsification.
- The task is ordinary code quality, generic debugging, or deployment verification without a security claim.
- The task is specifically MCP server protocol/surface hardening; use `mcp-server-engineering` for that contract.
- The requester lacks authority for containment, credential access, private-system investigation, or identity-sensitive reconnaissance.

## Authority and scope
Own **security triage, trust-boundary mapping, evidence-preservation policy, containment decision criteria, specialist routing, cross-lane finding reconciliation, remediation priority, and security-verification closure**. Do not grant credentials, expand system authority, attribute identity from weak evidence, or perform destructive containment merely because a security concern exists.

## Workflow
1. **Freeze scope and authority.** Name assets, principals, trust boundaries, allowed effects, time window, sensitive data, and explicit exclusions. Separate owner authorization from technical capability.
2. **Classify the situation.** Distinguish active incident, suspected compromise, preventive audit, supply-chain/forensic inquiry, credential exposure, and public-source reconnaissance. State what is observed versus hypothesized.
3. **Contain only when justified.** For an active harmful effect, use the smallest authorized control that stops further damage while preserving recoverability. Capture volatile evidence first unless delay materially increases harm. Never kill processes by broad name/pattern alone; bind containment to verified process identity/lineage and any exact respawn mechanism.
4. **Route specialist work.** Use the routing matrix in `references/security-routing-matrix.md`. Compose specialist skills rather than copying their mechanics into this router.
5. **Investigate evidence-first.** Prefer read-only acquisition before mutation. Record source, time, scope, hashes/identifiers, acquisition method, and limitations. Scanner output, model output, deleted refs, force-push history, or username matches are leads—not self-verifying conclusions.
6. **Reconcile findings.** For each finding separate vulnerable condition, reachable path, prerequisites, demonstrated effect, impacted assets, confidence, and unresolved alternatives. Deduplicate findings that share one root cause.
7. **Remediate minimally.** Preserve evidence and rollback paths; fix the authority/control boundary rather than hiding a symptom. Credential rotation, process termination, configuration changes, history rewrite, or production mutation require their own authority.
8. **Verify efficacy.** Re-run the prohibited/hostile path where safe, add deterministic regression evidence, and verify the negative property at the relevant boundary. A patched file, clean scanner, green CI job, or terminated PID alone is not control-efficacy proof.
9. **Close with residual risk.** Record what was fixed, what remains unverified, recovery/monitoring needs, and which security claims are actually supported.

## Domain invariants
- Secrets stay as credential references or appropriately protected secret material; never copy raw credentials into prompts, logs, reports, fixtures, or commits.
- A username/account-name match is not identity proof. Public-source correlation must preserve uncertainty and authorization boundaries.
- Repository deletion, force-push, unusual process activity, or dependency drift is not compromise by itself; establish provenance and causal evidence.
- Containment success means the prohibited effect stops and does not immediately reappear through the identified supervisor/respawn path; it does not prove root cause removal.

## Failure and recovery
If authority, scope, evidence integrity, or system identity is uncertain, remain read-only or quarantine the affected artifact and mark the finding `UNRESOLVED`; do not improvise broader access. If containment may have altered evidence, record the mutation and preserve pre/post state. If remediation fails, restore the last known-good state only when its provenance and safety are established; otherwise isolate and escalate the unresolved boundary.

## Evidence required
Keep a security ledger that ties each material claim to observed evidence, exact asset/revision/process identity, acquisition time/method, and verification status. Consequential remediation needs before/after evidence plus a control-efficacy test. Preserve contradictory evidence and distinguish `OBSERVED`, `INFERRED`, `REPRODUCED`, `REMEDIATED`, `VERIFIED`, and `UNRESOLVED`.

## Stop conditions
STOP if requested investigation or containment exceeds granted authority, if evidence acquisition would materially destroy the evidence needed to adjudicate the claim, if a secret cannot be handled without exposure, if identity attribution would exceed the available evidence, or if a high-impact remediation lacks rollback/recovery proof. Do not turn a blocked security lane into an unrestricted shell, credential, surveillance, or production-access path.
