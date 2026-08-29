---
name: inversion-durable-handoff
description: >
  Use when ending or transferring a long-running task, starting a new chat, approaching a context/tool cutoff, pausing overnight, or when the user asks for a handoff or Treasure Chest checkpoint.
version: 0.1.0
metadata:
  author: Inversion Labs
  role: durable-handoff
---
# Durable Handoff

A handoff must let a fresh agent recover the work from authoritative artifacts without trusting conversational recollection.

## Include
- exact repository and relevant subproject
- branch and exact HEAD
- base/head or PR when review scope matters
- authoritative spec/workflow/checkpoint paths
- what is implemented versus merely planned
- current verification results with exact commands/counts where available
- open Critical/Important findings, blockers, and known dirty state
- work that remains, ordered by dependency
- exact next safe action
- explicit things that must not be re-done or falsely assumed

## Persistence
When repository changes are part of the task and a durable handoff file belongs in the project, write and commit it. Otherwise produce a copy-ready new-chat prompt that names the immutable repository artifacts the next agent must read first.

## Rule
Do not make conversation memory the only location of a material decision, blocker, release gate, or authority boundary.
