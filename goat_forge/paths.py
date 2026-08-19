from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class ForgePaths:
    repo_root: Path
    hermes_live: Path
    hermes_bundled: Path
    hermes_optional: Path
    quarantine_root: Path = field(
        default_factory=lambda: Path.home() / ".capt-skill-forge" / "quarantine"
    )


def validate_source_roots(paths: ForgePaths) -> None:
    for field in ("repo_root", "hermes_live", "hermes_bundled", "hermes_optional"):
        path = getattr(paths, field)
        if not path.is_dir():
            raise FileNotFoundError(f"{field}: {path}")
