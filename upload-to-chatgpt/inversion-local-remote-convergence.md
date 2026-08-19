---
name: inversion-local-remote-convergence
description: >
  Use when a task spans a local filesystem or terminal and GitHub, including branch work, PR preparation, release closure, handoffs, CI investigation, or any workflow where local and remote state can diverge.
version: 0.1.0
metadata:
  author: Inversion Labs
  role: local-remote-convergence
---
# Local / Remote Convergence

Treat local and GitHub state as different authorities that must be reconciled, not interchangeable copies.

## Authority split
- Local machine: working tree, uncommitted changes, local tests/builds, local processes and artifacts.
- GitHub: published refs, PR metadata/diff, review threads, CI/status checks, remote commit existence.

## Workflow
1. Inspect both sides before changing shared history or claiming synchronization.
2. Record local branch/HEAD and remote branch/PR head.
3. Make local changes in an isolated branch when practical.
4. Verify locally before publishing.
5. Push without force unless force is explicitly required and justified.
6. Verify through GitHub that the expected commit is actually the remote head.
7. Re-check PR/CI/review state after the push before saying integration is ready.

## Fail closed
A local commit is not "on GitHub." A pushed branch is not "merged." A green local test is not green CI. A PR that existed earlier is not assumed current. Name the exact layer supporting each claim.
