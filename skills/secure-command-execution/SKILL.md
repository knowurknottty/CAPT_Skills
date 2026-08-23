---
name: secure-command-execution
description: >
  Use when an already-authorized tool must execute a local CLI or child process
  without turning caller-controlled arguments, paths, environment, or logs into a broader capability.
version: 2.0.0
metadata:
  author: Inversion Labs
  role: command-execution-safety-boundary
---

# Secure Command Execution

## Use when
- A tool forwards structured user/agent input to a CLI or child process.
- A command wrapper needs positive capability rules instead of a denylist.
- Execution crosses trust boundaries through argv, cwd, environment, stdin, files, or logs.
- A high-impact command surface needs reproducible refusal and postcondition evidence.

## Do not use when
- The caller lacks authority to perform the operation; authorization must be decided upstream.
- The task requires arbitrary interactive shell semantics; redesign or isolate that capability explicitly.
- A specialist sandbox/container policy already owns the execution boundary; compose with it rather than bypassing it.

## Authority and scope
Own **command shaping, capability grammar, process-boundary sanitization, execution constraints, secret-safe observability, and postcondition evidence**. Do not grant new authority, infer consent, broaden filesystem/network scope, or convert a rejected operation into an alternate command that succeeds.

The default unit is a structured process invocation: exact executable + validated argv + bounded cwd + explicit environment + optional stdin. Do not concatenate untrusted strings into a shell command unless shell syntax is the explicitly authorized capability.

## Workflow
1. **Bind authority first.** Record the requested operation, target, actor/lease/approval if applicable, allowed effect class, and whether shell interpretation is itself authorized. Missing authority is `BLOCKED`, not a parsing problem.
2. **Choose a positive capability profile.** Define allowed executable(s), subcommands/operation shapes, flags, positional types, cwd roots, stdin shape, environment keys, network/filesystem effects, and resource limits. Unknown syntax is denied. See `references/command-capability-profile.md`.
3. **Parse before policy.** Tokenize or accept argv structurally; validate each field according to its semantic role. Reject ambiguous abbreviations, option smuggling, control characters/confusables where meaningful, traversal/cwd escape, config injection, and unexpected shell metacharacter interpretation.
4. **Canonicalize once at the boundary.** Normalize paths/identifiers using the platform contract, resolve against the authorized root, then compare the object actually passed to the process. Avoid validate-one-representation/execute-another gaps.
5. **Construct the child environment positively.** Start from the minimum required keys rather than inheriting everything. Remove loader/config/hook/proxy/credential variables that can alter execution unless the capability profile explicitly requires them.
6. **Apply trusted controls in precedence-safe positions.** Forced no-hook/no-pager/no-plugin/read-only flags are useful only when the target CLI actually gives them precedence over caller input. Test this; do not assume ordering semantics.
7. **Execute without an implicit shell.** Prefer direct process APIs with argv arrays, bounded cwd, timeout, output limits, and controlled stdin. Capture exit status and termination reason.
8. **Redact structurally.** Preserve operation identity and diagnostic shape while scrubbing credentials/secrets recursively inside structured args, URLs, headers, stdin summaries, and child output. Never log raw secret-bearing payloads merely to prove execution.
9. **Verify the intended postcondition and forbidden effects.** A zero exit code is evidence about process completion, not proof of the requested state or absence of unauthorized side effects.

## Failure and recovery
On grammar rejection, report the rejected capability class without suggesting a bypass. On timeout/resource exhaustion, terminate only the owned child/process group and classify the outcome as incomplete. On ambiguous path/environment/config semantics, fail closed and require a narrower profile. If execution partially mutates state, use the operation-specific recovery/rollback contract; this skill must not invent destructive cleanup.

## Evidence required
Record the capability-profile ID/version, executable identity when material, sanitized argv shape, bounded cwd, environment-policy result, exit/termination status, postcondition evidence, and any residual effect that could not be observed. Logs are evidence only if their redaction path was itself exercised.

## Stop conditions
STOP when authority is missing, the requested syntax lies outside the positive grammar, canonicalization cannot prove the target stays in scope, safe environment construction is unknown, shell interpretation would broaden capability, secret-safe logging cannot be maintained, or a required postcondition/rollback cannot be observed. Return the blocked boundary; do not fall back to a more permissive executor.
