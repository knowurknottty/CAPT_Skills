---
name: subagent-driven-development
description: >
  Use when an approved implementation plan contains multiple bounded tasks that
  can be assigned to fresh workers and independently reviewed before integration.
version: 2.0.0
metadata:
  author: Inversion Labs
  role: implementation-orchestrator
---

# Subagent-Driven Development

## Use when
- An implementation plan or equivalent frozen task specification already exists.
- Work can be decomposed into bounded tasks with explicit dependencies and ownership.
- Independent implementation/review contexts materially reduce contamination or missed requirements.
- Multiple tasks may run concurrently only when their state, files, and prerequisites do not conflict.

## Do not use when
- The design/spec is still unresolved; return to planning first.
- One bounded task is cheaper and clearer to execute directly.
- Tasks share mutable state or overlapping files that cannot be isolated safely.
- Delegation would merely fragment context without creating an independently verifiable unit of work.

## Authority and scope
Own **task orchestration, context packaging, review ordering, and integration gates**. Do not redesign the approved plan, let a worker silently change scope, or treat worker self-review as independent verification. The controller remains responsible for cross-task truth and may make bounded repairs when that is safer than redispatch; any such repair inherits the same tests/review gates.

## Workflow
1. **Parse the plan once.** Extract every task, required artifact, dependency, acceptance condition, and explicit non-goal. Build a dependency DAG; do not rely on worker discovery for plan semantics.
2. **Define ownership.** For each task record files/surfaces it may mutate, prerequisites, expected outputs, test commands, and integration position. Serialize tasks with overlapping mutable authority unless isolation proves they cannot conflict.
3. **Create the context packet.** Give the worker the complete task specification plus only the project context needed to execute it: relevant contracts, paths, conventions, constraints, and verification commands. Never make the worker reconstruct critical requirements from a giant plan or chat history.
4. **Dispatch a fresh implementer.** Require the task's applicable process discipline (for maintained code, normally TDD), exact evidence, and a concise handoff listing changed artifacts, commands/results, assumptions, and unresolved risk.
5. **Spec-compliance review first.** An independent reviewer compares the result to the frozen task: required behavior, paths/interfaces, non-goals, and absence of scope creep. Any gap returns to implementation and is re-reviewed.
6. **Quality review second.** Only after spec PASS, independently inspect correctness, maintainability, security, error handling, tests, project conventions, and hidden coupling. Material findings must be fixed and re-reviewed.
7. **Integrate topologically.** Merge/apply completed tasks in dependency order. Revalidate assumptions invalidated by earlier integrations; do not carry stale PASS states forward blindly.
8. **Run final integration verification.** Exercise the complete plan-level behavior and review the aggregate diff/state, not just each task in isolation.

## Failure and recovery
If a worker discovers missing requirements, stop that task and escalate the question instead of inventing product truth. If two tasks collide on files/state, freeze parallel work and serialize or re-plan the boundary. If a worker fails repeatedly, preserve its evidence and dispatch a fresh diagnostic context rather than stacking guesses. If reviewers disagree, return to the frozen specification and observed behavior; authority is not decided by vote.

A task that cannot be independently verified is not a good subagent boundary. Merge or reshape it before continuing.

## Verification
Per-task completion requires:
- implementation evidence from the real artifact/environment;
- spec-compliance PASS from a context independent of the implementer;
- quality/security PASS or explicitly accepted residual findings;
- tests/checks appropriate to the changed surface;
- no unexplained mutation outside task ownership.

Plan completion additionally requires dependency-order integration, aggregate diff/state review, and final end-to-end verification.

## Stop conditions
STOP when the plan is not authoritative enough to delegate, ownership overlaps cannot be isolated, a prerequisite is unverified, a reviewer has unresolved material findings, integration invalidates a prior task assumption, or the final integrated system has not been verified.
