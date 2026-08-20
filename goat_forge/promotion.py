from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from typing import Callable

from goat_forge.forge_contract import validate_forge_candidate


SecretScanner = Callable[[Path], tuple[bool, str]]


@dataclass(frozen=True)
class EvalEvidence:
    static_contract: bool
    pressure_cases: bool
    semantic_review: bool

    @property
    def passed(self) -> bool:
        return self.static_contract and self.pressure_cases and self.semantic_review


@dataclass(frozen=True)
class PromotionDecision:
    state: str
    reason: str
    destination: str | None = None


def _frontmatter_name(text: str) -> str:
    match = re.search(r"(?m)^name:[ \t]*([^\n]+?)\s*$", text)
    return match.group(1).strip().strip("\"'") if match else ""


def gitleaks_scan(path: Path) -> tuple[bool, str]:
    executable = shutil.which("gitleaks")
    if executable is None:
        return False, "gitleaks unavailable; secret scan cannot be proven"
    with tempfile.TemporaryDirectory(prefix="goat-gitleaks-") as temporary:
        report = Path(temporary) / "report.json"
        completed = subprocess.run(
            [
                executable,
                "detect",
                "--no-git",
                "--source", str(path),
                "--report-format", "json",
                "--report-path", str(report),
                "--redact=100",
                "--no-banner",
                "--no-color",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode == 0:
            return True, "gitleaks clean"
        if completed.returncode == 1:
            count = 0
            try:
                findings = json.loads(report.read_text()) if report.exists() else []
                count = len(findings) if isinstance(findings, list) else 1
            except (OSError, json.JSONDecodeError):
                count = 1
            return False, f"secret scan found {count} finding(s)"
        return False, f"gitleaks failed closed with exit code {completed.returncode}"


def _validate_forge_path(forged_dir: Path, quarantine_root: Path) -> tuple[bool, str, str]:
    forge = forged_dir.expanduser().resolve(strict=False)
    quarantine = quarantine_root.expanduser().resolve(strict=False)
    try:
        relative = forge.relative_to(quarantine)
    except ValueError:
        return False, "candidate is outside the configured forge quarantine", ""
    parts = relative.parts
    if len(parts) != 3 or parts[0] != "forge" or parts[2] != "FORGED":
        return False, "candidate must come from quarantine/forge/<name>/FORGED", ""
    return True, "", parts[1]


def promote_candidate(
    forged_dir: Path,
    repo_root: Path,
    quarantine_root: Path,
    evidence: EvalEvidence,
    *,
    secret_scanner: SecretScanner = gitleaks_scan,
) -> PromotionDecision:
    valid_path, path_error, expected_name = _validate_forge_path(forged_dir, quarantine_root)
    if not valid_path:
        return PromotionDecision("NO-GO", path_error)

    forged = forged_dir.expanduser().resolve(strict=False)
    skill_md = forged / "SKILL.md"
    if not skill_md.is_file():
        return PromotionDecision("NO-GO", "forged candidate is missing SKILL.md")
    text = skill_md.read_text(errors="replace")
    name = _frontmatter_name(text)
    if not name or name != expected_name:
        return PromotionDecision(
            "FIX", f"frontmatter name/path mismatch: name={name!r} path={expected_name!r}"
        )

    contract_errors = validate_forge_candidate(text)
    if contract_errors:
        return PromotionDecision("FIX", "candidate contract failed: " + "; ".join(contract_errors))
    if not evidence.passed:
        return PromotionDecision("FIX", "evaluation evidence is incomplete or failing")

    secrets_ok, secret_summary = secret_scanner(forged)
    if not secrets_ok:
        return PromotionDecision("NO-GO", f"secret scan blocked promotion: {secret_summary}")

    repo = repo_root.expanduser().resolve(strict=False)
    destination = repo / "skills" / name
    if destination.exists() or destination.is_symlink():
        return PromotionDecision("BLOCKED", f"incumbent skill already exists: {destination}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{name}.promote-", dir=destination.parent))
    try:
        shutil.rmtree(temporary)
        shutil.copytree(forged, temporary, symlinks=True)
        os.replace(temporary, destination)
    except Exception:
        if temporary.exists():
            shutil.rmtree(temporary)
        raise
    return PromotionDecision("PASS", "all promotion gates passed", str(destination))
