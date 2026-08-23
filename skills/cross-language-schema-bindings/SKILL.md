---
name: cross-language-schema-bindings
description: >
  Use when one data contract must generate or validate equivalent bindings in
  multiple languages with deterministic output, behavioral parity, and drift detection.
version: 2.0.0
metadata:
  author: Inversion Labs
  role: multi-language-contract-compiler
---

# Cross-Language Schema Bindings

## Use when
- The same contract must exist in two or more languages/runtimes.
- Hand-maintained language models are drifting or one language has become an accidental source of truth.
- Generated types, validators, discriminated unions, versioning, or extension boundaries require reproducibility proof.

## Do not use when
- Only one runtime consumes the contract.
- An existing IDL/compiler already provides the required bindings and parity guarantees without a custom layer.
- The task is ordinary serialization without a shared semantic contract.

## Authority and scope
Own **canonical contract representation, normalized semantic model, deterministic binding generation, validation semantics, and cross-language parity/drift proof**. No generated language owns semantics independently; emitter convenience must not add, remove, weaken, or reinterpret contract rules.

## Workflow
1. **Freeze the canonical contract source.** Use the repository's mandated IDL/schema. If none exists and the payload is JSON-native, JSON Schema 2020-12 is a strong default. Version semantic contract changes deliberately; do not bump versions for formatting/generator-only changes.
2. **Normalize once.** Parse all source files into one language-neutral semantic model: types, fields, requiredness, defaults, enums, unions/discriminators, constraints, references, extension points, and version metadata. Resolve dependencies and traversal order deterministically.
3. **Make extension boundaries explicit.** Prefer closed objects/unions for trust-sensitive contracts; allow unknown/extension maps only where the canonical contract names that extensibility.
4. **Emit each language from the same model.** One emitter per target language may adapt syntax/idioms but not semantics. Dependency ordering, aliases, nullability/optionality, enum values, discriminator behavior, defaults, and constraint rules must derive from the shared model.
5. **Canonicalize observable validation output.** When parity includes errors, normalize paths, error codes, and embedded values so language-specific string representation does not create false drift. See `references/parity-and-determinism.md`.
6. **Generate reproducibly.** Sort unordered inputs; exclude timestamps, hostnames, absolute paths, locale-sensitive rendering, and insertion-order effects. Generate twice into separate temporary roots and compare relative paths plus bytes.
7. **Run shared fixtures.** Positive and negative fixture vectors must be consumed by every target runtime. Compare accept/reject decisions and canonicalized outputs/errors, not merely successful compilation.
8. **Prove hermetic consumers.** Parity/conformance runners must build or locate their own generated/runtime artifacts from declared dependencies; they cannot rely on stale local build output.
9. **Detect repository drift.** Regenerate in CI and compare only generator-owned artifacts against the repository's declared generated-output policy. If generated files are committed, any unexpected diff is a failure; if generated files are ephemeral, validate package/build output instead.
10. **Gate contract evolution.** For a semantic schema change, regenerate every language, run reproducibility plus parity plus downstream conformance, and verify version/backward-compatibility policy before merge.

## Failure and recovery
If one language cannot represent a construct directly, encode an explicit documented lowering in the shared model or revise the canonical contract; do not silently weaken that language's validator. If generated output differs between clean runs, isolate nondeterministic input/order before accepting the generator. If parity fails only in messages/formatting, determine whether that text is contractually observable before changing semantics.

## Evidence required
Retain canonical contract revision, generator/tool revision, normalized-model version, target-language versions, reproducibility diff result, shared fixture results per runtime, generated-artifact drift result, and compatibility/version decision. A green compiler in each language does not prove semantic parity.

## Stop conditions
STOP on nondeterministic generation, unexplained language-level semantic divergence, stale build artifacts required for parity, unreviewed version skew, or any emitter that must invent semantics absent from the canonical contract. Report the exact construct/runtime that cannot conform.
