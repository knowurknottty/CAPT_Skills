---
name: inversion-parallel-work-splitting
description: >
  Use when two or more independent tasks, reviewers, models, terminals, agents, or research tracks can proceed concurrently without requiring shared mutable state.
version: 0.1.0
metadata:
  author: Inversion Labs
  role: parallel-orchestration
---
# Parallel Work Splitting

Parallelism is useful only when it reduces wall-clock work without creating merge ambiguity or duplicated authority.

## Decompose first
For each worker define: objective, owned files/artifacts, inputs, forbidden mutations, expected output, verification, and convergence point.

## Rules
- Parallelize independent discovery, tests, reviews, benchmarks, or disjoint implementation areas.
- Do not let two workers edit the same mutable files/branch unless a deliberate merge protocol exists.
- Give all workers the same immutable authority references when they must reason about the same system.
- Keep reviewer roles read-only unless explicitly assigning implementation.
- One integrator owns final adjudication and repository mutation.
- Preserve worker-specific evidence instead of collapsing it into a consensus summary too early.
- If one result invalidates another worker's assumptions, stop/rebase that track rather than combining incompatible outputs.

## Convergence
At the merge point: compare outputs, resolve contradictions against authoritative evidence, integrate once, run the combined verification suite, and record the exact terminal state.
