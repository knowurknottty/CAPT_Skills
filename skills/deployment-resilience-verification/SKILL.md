---
name: deployment-resilience-verification
description: >
  Use when a release or deployment must be proven from source revision through artifact,
  deployment, startup/serving, degraded-mode behavior, live provenance, and rollback/recovery.
version: 2.0.0
metadata:
  author: Inversion Labs
  role: deployment-resilience-verifier
---

# Deployment Resilience Verification

## Use when
- A build/deploy pipeline is green but the live artifact may be stale, incomplete, or serving a different revision.
- Availability depends on startup/boot/runtime dependencies that can fail or degrade.
- A release needs explicit artifact identity, live-state proof, rollback, or recovery evidence.
- A deployment incident requires distinguishing source/build/pipeline/hosting/cache/runtime layers.

## Do not use when
- The task is generic multi-layer verification with no deployment boundary; use `verification-workflows`.
- The branch/repository itself is not release-ready; use repository/integration skills first.
- The task is to design application fallback UX rather than verify deployment resilience; use the appropriate product/interface skill.

## Authority and scope
Own **source-to-artifact provenance, deployment-path verification, live revision identity, startup/serving probes, dependency-failure/degraded-mode tests, cache/routing diagnosis, and rollback/recovery proof**. Do not change release policy, credentials, DNS/hosting topology, or production code merely to make verification green without separate authority.

A successful CI deploy job proves only that the job succeeded. Deployment verification must separately prove what artifact was built, what revision/environment received it, what users can retrieve/run, and how the system behaves when important deployment dependencies fail.

## Workflow
1. **Freeze release identity.** Record source revision/tree, build configuration, target environment/project, expected routes/services, and the acceptance/rollback contract. If remote state matters, fetch/reconcile before testing.
2. **Trace the real build path.** Identify actual source entrypoints, generated steps, dependencies, packaging rules, and final artifact. Prove the artifact is newly produced from the intended revision rather than stale output rescued by local caches.
3. **Stamp provenance.** Embed or otherwise expose an immutable release/build identifier that can be compared with source and deployment records. Avoid provenance that can be edited independently of the artifact it claims to identify.
4. **Verify the deployment path.** Confirm the target environment received the intended artifact and no competing integration/pipeline is deploying another branch or artifact to the same destination.
5. **Probe live behavior.** Exercise the actual public/local deployment surface appropriate to the product: HTTP routes, package install/start, service readiness, health/readiness, CLI invocation, desktop launch, or mobile startup. Compare live revision/provenance with the expected artifact.
6. **Test dependency failure/degraded mode.** Break or withhold deployment/runtime dependencies whose failure could trap users or produce false healthy status. Verify bounded degradation/failover/fail-open/fail-closed behavior according to the product contract—not one universal fallback policy.
7. **Test cache/routing ambiguity.** Where CDN/cache/proxy/DNS/preview/custom-domain layers exist, probe canonical and alternate routes with cache-busting or direct origins as appropriate. Distinguish stale observer/cache evidence from a genuinely stale deployment.
8. **Verify rollback/recovery.** Prove the documented rollback/redeploy/restart/recovery action targets the correct artifact/environment and restores an accepted state. Do not wait for an incident to discover the rollback path is theoretical.
9. **Run release acceptance.** Combine artifact identity, live probes, degraded-mode tests, observability, and rollback evidence. Use `verify-before-claim` for the exact final status and `verification-workflows` when additional layers are required.

## Failure and recovery
If the live revision disagrees with source, stop changing application code and isolate the layer: uncommitted source, wrong build entrypoint, stale generated artifact, failed/competing pipeline, wrong target, cache/proxy, DNS/custom domain, or runtime bootstrap. Missing production credentials/authority is `BLOCKED`; do not bypass the deployment path with an ungoverned alternate. Preserve failed live/build evidence before retrying.

## Evidence required
Retain source revision/tree, build command/config, artifact digest/identity, deployment target/run identity, live provenance result, acceptance probes, dependency-failure results, cache/routing checks where relevant, and rollback/recovery evidence. A local build PASS is not live-deployment evidence; a live page response is not proof of source identity without provenance.

## Stop conditions
STOP when the source revision or deployment target is ambiguous, the artifact cannot be tied to source, credentials/production authority are missing, competing deploy paths are unresolved, a degraded-mode test risks uncontrolled production harm, live provenance disagrees with the intended revision, or rollback cannot be demonstrated safely. Return the failing layer and exact evidence instead of redeploying repeatedly.

Load `references/deployment-proof-matrix.md` for evidence layers and `references/failure-and-fallback-tests.md` for degraded-mode test design.
