from pathlib import Path

from goat_forge.promotion import EvalEvidence, promote_candidate


def write_valid_skill(root: Path, name: str = "systematic-debugging") -> Path:
    forged = root / "forge" / name / "FORGED"
    forged.mkdir(parents=True)
    (forged / "SKILL.md").write_text(f"""---
name: {name}
description: Use when a technical failure needs controlled root-cause work.
---
# {name}
## Use when
Use when a technical failure requires this capability.
## Do not use when
Do not use when the task is unrelated.
## Authority and scope
Own only the named capability; do not widen scope.
## Workflow
1. Inspect.\n2. Execute one bounded step.\n3. Re-check.
## Failure and recovery
If blocked, rollback the probe and preserve evidence.
## Verification
Verify with observed evidence before claiming PASS.
## Stop conditions
STOP if evidence is unavailable or authority is exceeded.
""")
    return forged


def passed_evidence() -> EvalEvidence:
    return EvalEvidence(static_contract=True, pressure_cases=True, capt_qwen38_review=True, capt_nemotron_lightning_review=True)


def test_promotion_rejects_raw_quarantine_source(tmp_path: Path):
    quarantine = tmp_path / "quarantine"
    raw = quarantine / "hermes" / "pkg" / "original"
    raw.mkdir(parents=True)
    (raw / "SKILL.md").write_text("raw")
    repo = tmp_path / "repo"
    repo.mkdir()

    decision = promote_candidate(
        raw, repo, quarantine, passed_evidence(), secret_scanner=lambda _: (True, "clean")
    )
    assert decision.state == "NO-GO"
    assert "forge" in decision.reason.lower()


def test_promotion_blocks_failed_eval_or_secret_scan(tmp_path: Path):
    quarantine = tmp_path / "quarantine"
    forged = write_valid_skill(quarantine)
    repo = tmp_path / "repo"
    repo.mkdir()

    failed_eval = promote_candidate(
        forged,
        repo,
        quarantine,
        EvalEvidence(static_contract=True, pressure_cases=False, capt_qwen38_review=True, capt_nemotron_lightning_review=True),
        secret_scanner=lambda _: (True, "clean"),
    )
    assert failed_eval.state == "FIX"
    assert "evaluation" in failed_eval.reason.lower()

    secret = promote_candidate(
        forged,
        repo,
        quarantine,
        passed_evidence(),
        secret_scanner=lambda _: (False, "secret detector found 1 finding"),
    )
    assert secret.state == "NO-GO"
    assert "secret" in secret.reason.lower()


def test_promotion_blocks_incumbent_collision_without_explicit_replace(tmp_path: Path):
    quarantine = tmp_path / "quarantine"
    forged = write_valid_skill(quarantine)
    repo = tmp_path / "repo"
    incumbent = repo / "skills" / "systematic-debugging"
    incumbent.mkdir(parents=True)
    (incumbent / "SKILL.md").write_text("incumbent")

    decision = promote_candidate(
        forged, repo, quarantine, passed_evidence(), secret_scanner=lambda _: (True, "clean")
    )
    assert decision.state == "BLOCKED"
    assert "incumbent" in decision.reason.lower()


def test_promotion_copies_only_verified_forged_package(tmp_path: Path):
    quarantine = tmp_path / "quarantine"
    forged = write_valid_skill(quarantine)
    (forged / "references").mkdir()
    (forged / "references" / "method.md").write_text("safe reference")
    repo = tmp_path / "repo"
    repo.mkdir()

    decision = promote_candidate(
        forged, repo, quarantine, passed_evidence(), secret_scanner=lambda _: (True, "clean")
    )

    assert decision.state == "PASS"
    destination = repo / "skills" / "systematic-debugging"
    assert (destination / "SKILL.md").exists()
    assert (destination / "references" / "method.md").read_text() == "safe reference"
    assert not (repo / "quarantine").exists()


def test_promotion_requires_both_named_capt_reviewers(tmp_path: Path):
    quarantine = tmp_path / "quarantine"
    forged = write_valid_skill(quarantine)
    repo = tmp_path / "repo"
    repo.mkdir()

    missing_qwen = promote_candidate(
        forged, repo, quarantine,
        EvalEvidence(static_contract=True, pressure_cases=True, capt_qwen38_review=False, capt_nemotron_lightning_review=True),
        secret_scanner=lambda _: (True, "clean"),
    )
    assert missing_qwen.state == "FIX"

    missing_nemotron = promote_candidate(
        forged, repo, quarantine,
        EvalEvidence(static_contract=True, pressure_cases=True, capt_qwen38_review=True, capt_nemotron_lightning_review=False),
        secret_scanner=lambda _: (True, "clean"),
    )
    assert missing_nemotron.state == "FIX"
