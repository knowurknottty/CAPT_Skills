---
name: inversion-continuation-recovery
description: >
  Use when the user says continue, resume, pick this back up, proceed from the handoff, or when a chat/tool/context cutoff means prior execution state may be stale or incomplete.
version: 0.1.0
metadata:
  author: Inversion Labs
  role: continuation-recovery
---
# Continuation Recovery

A continuation request is an instruction to recover authoritative state and resume work, not an invitation to reconstruct state from memory.

## Recovery order
1. Use any explicit handoff identifiers: repo, branch, commit, PR, file, task ID, reviewer marker.
2. Inspect the live local working tree and recent tool/process state when available.
3. Inspect the remote repository/PR/CI state when the task crosses GitHub.
4. Read the task's authoritative spec, checkpoint, workflow, or evidence files.
5. Compare recovered state with the remembered objective and identify the smallest next unfinished unit.
6. Resume execution immediately.

## Tool reality
- When local/GitHub tools are available, recovery means calling them now; do not substitute an example shell session.
- When they cannot actually be invoked, stop at BLOCKED state recovery and list the required reads. Never fabricate recovered branch names, SHAs, PRs, review comments, or divergences.

## Rules
- Do not make the user restate information that tools can recover.
- Do not assume a previously reported test, build, reviewer result, branch head, or approval is still current.
- Preserve dirty work and active sessions unless the task explicitly supersedes them.
- If recovery finds a different state than the handoff claimed, trust the live evidence and report the divergence.

## Output
Keep the recovery report compact: authoritative state, divergence if any, then the work performed next.
