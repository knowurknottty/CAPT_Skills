from goat_forge.forge_contract import validate_forge_candidate


def valid_skill() -> str:
    return """---
name: systematic-debugging
description: Use when a technical failure needs root-cause isolation before a fix.
---
# Systematic Debugging

## Use when
A reproducible technical failure needs investigation.

## Do not use when
The task is purely explanatory and no failure is being diagnosed.

## Authority and scope
Own root-cause diagnosis. Do not expand product scope or rewrite unrelated code.

## Workflow
1. Reproduce the failure.
2. Bound the failing layer.
3. Form one falsifiable hypothesis.
4. Test the smallest discriminating change.

## Failure and recovery
If reproduction is unstable, gather diagnostics and mark the cause UNVERIFIED. Roll back failed probes before the next hypothesis.

## Verification
Require a failing-before / passing-after regression or equivalent observed evidence before claiming the defect fixed.

## Stop conditions
STOP when the root cause is unproven, required evidence is unavailable, or the proposed fix exceeds authorized scope.
"""


def test_valid_candidate_passes_contract():
    assert validate_forge_candidate(valid_skill()) == []


def test_contract_rejects_missing_negative_triggers_and_authority():
    text = valid_skill().replace(
        "## Do not use when\nThe task is purely explanatory and no failure is being diagnosed.\n\n",
        "",
    ).replace(
        "## Authority and scope\nOwn root-cause diagnosis. Do not expand product scope or rewrite unrelated code.\n\n",
        "",
    )
    errors = validate_forge_candidate(text)
    assert any("negative trigger" in error for error in errors)
    assert any("authority" in error for error in errors)


def test_contract_rejects_missing_recovery_verification_and_stop_conditions():
    text = valid_skill()
    for block in (
        "## Failure and recovery\nIf reproduction is unstable, gather diagnostics and mark the cause UNVERIFIED. Roll back failed probes before the next hypothesis.\n\n",
        "## Verification\nRequire a failing-before / passing-after regression or equivalent observed evidence before claiming the defect fixed.\n\n",
        "## Stop conditions\nSTOP when the root cause is unproven, required evidence is unavailable, or the proposed fix exceeds authorized scope.\n",
    ):
        text = text.replace(block, "")
    errors = validate_forge_candidate(text)
    assert any("recovery" in error for error in errors)
    assert any("verification" in error for error in errors)
    assert any("stop condition" in error for error in errors)


def test_contract_rejects_unsupported_success_theater():
    text = valid_skill() + "\nThis workflow is guaranteed to succeed every time.\n"
    errors = validate_forge_candidate(text)
    assert any("unsupported success" in error for error in errors)


def test_contract_rejects_bloated_core_and_non_trigger_description():
    text = valid_skill().replace(
        "description: Use when a technical failure needs root-cause isolation before a fix.",
        "description: A comprehensive debugging framework.",
    )
    text += "\n" + ("unbounded detail " * 800)
    errors = validate_forge_candidate(text)
    assert any("description" in error for error in errors)
    assert any("too large" in error for error in errors)


def test_contract_rejects_obvious_name_content_mismatch():
    text = valid_skill().replace("name: systematic-debugging", "name: database-migration-safety")
    text = text.replace("# Systematic Debugging", "# Marketing Copy")
    errors = validate_forge_candidate(text)
    assert any("name/content mismatch" in error for error in errors)
