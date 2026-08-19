# Verification evidence

## RED

Before the custom skills existed, `tests/validate_pack.py` failed on all four missing skill contracts.

The first local upstream-only semantic run against `qwen3.5-defiant-fable:latest` exposed real composition gaps:

- mixed interface case: 2/5 under the initial behavioral checks
- motion case without the repo-main-only `motion-doctrine`: 3/5 under the initial behavioral checks

Human review then drove additional adversarial fixes for support-skill leakage, co-ownership wording, filler-motion rationalization, and invented public-facing metrics.

## GREEN

Final saved-output grading after those fixes:

- interface: 5/5
- motion: 7/7
- structural pack validation: PASS
- package discovery: exactly 4 skills

The local semantic checks are **Qwen 9.2B behavioral smoke tests**, not substitutes for Codex/Claude production validation.

## External runner status

External behavioral runners were attempted and preserved as machine-local logs:

- Codex 0.144.3: blocked by current usage-credit limit. It also reported the skill-description context budget exceeded and an unrelated malformed `substack` skill.
- Claude Code 2.1.179: blocked by Vertex 429 quota exhaustion.
- Gemini CLI 0.46.0: blocked by service/client eligibility failure and also reported duplicate skill registrations.

No blocked runner is counted as passing evidence.

## Upstream health

After running the official HyperFrames v0.7.45 updater, `hyperframes skills check` reported 9 current, 0 outdated, and 0 core-missing. Optional workflow skills remain on-demand.
