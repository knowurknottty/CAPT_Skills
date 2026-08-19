---
name: inversion-repository-authority
description: >
  Use when work depends on current repository, branch, commit, working-tree, PR, CI, release, or file state, especially after a handoff, interruption, long-running task, or any request to continue existing engineering work.
version: 0.1.0
metadata:
  author: Inversion Labs
  role: repository-authority
---
# Repository Authority

Treat the repository and its live tooling as authority for repository state. Conversation memory is context, never proof of the current tree.

## Workflow
1. Identify the exact repository before changing anything.
2. Read repository-local instructions and authoritative handoff/spec files that govern the task.
3. Inspect current branch, HEAD, working-tree status, remotes, and relevant diff. When GitHub matters, inspect the remote branch/PR/CI state too.
4. Reconcile contradictions explicitly. Prefer immutable commit/file evidence over remembered status text.
5. Work from the observed state. Do not ask the user to repeat facts that the repository or tools can recover.
6. Before reporting completion, re-read HEAD/status and any remote state that the claim depends on.

## Tool reality
- If the environment exposes a repository/filesystem/GitHub tool, invoke it rather than printing a hypothetical command transcript.
- If tool invocation is genuinely unavailable, mark the state BLOCKED and name the exact read that is missing. Never invent a branch, SHA, PR number, CI result, dirty file, or command output.
- A prompt saying a tool is available is not permission to pretend its output; only an actual tool result can establish state.

## Fail closed
- Never claim a commit exists, a branch is pushed, a PR is current, tests ran, or files contain something without observing it.
- Never overwrite unrelated dirty work merely to obtain a clean tree.
- If local and remote disagree, name the disagreement and resolve it before integration.

## Output
Report exact repo, branch, HEAD, material dirty state, and the authoritative artifact(s) used whenever those facts affect the conclusion.
