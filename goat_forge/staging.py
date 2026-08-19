from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
import shutil
import tempfile

from goat_forge.inventory import SkillRecord, tree_digest


@dataclass(frozen=True)
class StagedSkill:
    root: Path
    package_id: str
    source_sha256: str
    staged_sha256: str


def _safe_component(value: str) -> str:
    value = value.strip().lstrip(".") or "root"
    return re.sub(r"[^A-Za-z0-9._-]+", "-", value)


def staging_id(source_lane: str, relative_path: str) -> str:
    parts = [_safe_component(source_lane)]
    parts.extend(_safe_component(part) for part in Path(relative_path).parts)
    return "__".join(parts)


def _validate_quarantine(quarantine_root: Path, repo_root: Path) -> Path:
    quarantine = quarantine_root.expanduser().resolve(strict=False)
    repo = repo_root.expanduser().resolve(strict=False)
    if quarantine == repo or repo in quarantine.parents:
        raise ValueError(f"quarantine must remain outside repository: {repo}")
    return quarantine


def stage_skill(
    record: SkillRecord,
    lane: str,
    quarantine_root: Path,
    repo_root: Path,
) -> StagedSkill:
    if lane not in {"capt", "hermes", "forge"}:
        raise ValueError(f"unsupported quarantine lane: {lane}")
    quarantine = _validate_quarantine(quarantine_root, repo_root)
    source = Path(record.source_path).expanduser()
    if not source.is_dir():
        raise FileNotFoundError(source)
    current_digest = tree_digest(source)
    if current_digest != record.tree_sha256:
        raise ValueError(f"source changed since inventory: {source}")
    lane_root = quarantine / lane
    lane_root.mkdir(parents=True, exist_ok=True)
    package_id = staging_id(record.source_lane, record.relative_path)
    final_root = lane_root / package_id
    if final_root.exists() or final_root.is_symlink():
        raise FileExistsError(f"immutable quarantined package already exists: {final_root}")

    temporary = Path(tempfile.mkdtemp(prefix=f".{package_id}.tmp-", dir=lane_root))
    original = temporary / "original"
    try:
        shutil.copytree(source, original, symlinks=True)
        staged_digest = tree_digest(original)
        if staged_digest != record.tree_sha256:
            raise RuntimeError(f"quarantine digest mismatch for {source}")
        metadata = {
            "quarantine_lane": lane,
            "package_id": package_id,
            "source": record.to_dict(),
            "source_sha256": record.tree_sha256,
            "staged_sha256": staged_digest,
        }
        (temporary / "SOURCE.json").write_text(
            json.dumps(metadata, indent=2, sort_keys=True) + "\n"
        )
        os.replace(temporary, final_root)
        return StagedSkill(final_root, package_id, record.tree_sha256, staged_digest)
    except Exception:
        if temporary.exists():
            shutil.rmtree(temporary)
        raise


_CAPT_TOKEN = re.compile(
    r"(?i)(?:^|[-_/])(?:capt|capts|biocapt|frankencapt)(?:$|[-_/])"
)


def is_capt_candidate(record: SkillRecord) -> bool:
    if record.discovery_status != "LIVE" or record.frontmatter_status != "OK":
        return False
    haystack = f"{record.relative_path}/{record.name}"
    return bool(_CAPT_TOKEN.search(haystack))
