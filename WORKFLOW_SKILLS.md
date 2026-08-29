# Inversion Labs Workflow Skill Pack

Ten composable skills remove recurring engineering-agent friction without creating a monolithic system prompt.

## Portable forms

- Canonical: `skills/<skill-name>/SKILL.md`
- Flat Markdown copies: `upload-to-chatgpt/<skill-name>.md`

## Composition examples

- **"continue" after a cutoff:** continuation-recovery + repository-authority + local-remote-convergence
- **"just apply it":** execute-now
- **CAPT implementation:** capt-dogfood + truth-discipline
- **major architecture review:** dual-review-convergence + truth-discipline
- **ship/merge/release:** release-closure + repository-authority + local-remote-convergence + truth-discipline
- **new chat / overnight handoff:** durable-handoff + repository-authority
- **Qwen + Sol + multiple terminals:** parallel-work-splitting plus the domain skill for each worker

## Design constraints

Each skill has a narrow `Use when...` trigger. Skills compose rather than duplicate one giant workflow. Repository/runtime evidence outranks conversation memory; deterministic proof outranks reviewer prose; clear reversible authorization should result in execution rather than another approval loop.
