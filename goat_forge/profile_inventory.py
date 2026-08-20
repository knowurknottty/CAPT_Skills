from dataclasses import asdict, dataclass, replace
from pathlib import Path

from goat_forge.inventory import SkillRecord, iter_skill_records


@dataclass(frozen=True)
class ProfileProjection:
    tree_sha256: str
    profiles: tuple[str, ...]
    source_paths: tuple[str, ...]
    base_match: bool
    selected_source_path: str | None

    def to_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["profiles"] = list(self.profiles)
        data["source_paths"] = list(self.source_paths)
        return data


@dataclass(frozen=True)
class ProfileVariantInventory:
    records: tuple[SkillRecord, ...]
    projections: tuple[ProfileProjection, ...]


def discover_profile_roots(profiles_root: Path) -> dict[str, Path]:
    roots: dict[str, Path] = {}
    if not profiles_root.is_dir():
        return roots
    for profile in sorted(profiles_root.iterdir(), key=lambda path: path.name):
        if not profile.is_dir() or ".bak." in profile.name:
            continue
        skills = profile / "skills"
        if not skills.is_dir():
            continue
        if next(skills.rglob("SKILL.md"), None) is None:
            continue
        roots[profile.name] = skills
    return roots


def inventory_profile_variants(
    profile_roots: dict[str, Path],
    known_records: list[SkillRecord] | tuple[SkillRecord, ...],
) -> ProfileVariantInventory:
    known_digests = {record.tree_sha256 for record in known_records}
    grouped: dict[str, list[tuple[str, SkillRecord]]] = {}
    for profile, root in sorted(profile_roots.items()):
        for record in iter_skill_records({profile: root}):
            grouped.setdefault(record.tree_sha256, []).append((profile, record))

    records: list[SkillRecord] = []
    projections: list[ProfileProjection] = []
    for digest, entries in grouped.items():
        ordered = sorted(entries, key=lambda item: (item[0], item[1].relative_path, item[1].source_path))
        profiles = tuple(sorted({profile for profile, _ in ordered}))
        source_paths = tuple(sorted({record.source_path for _, record in ordered}))
        base_match = digest in known_digests
        selected_source_path: str | None = None
        if not base_match:
            profile, selected = ordered[0]
            selected_source_path = selected.source_path
            records.append(
                replace(
                    selected,
                    source_lane="profile",
                    relative_path=f"{profile}/{selected.relative_path}",
                    discovery_status="PROFILE",
                )
            )
        projections.append(
            ProfileProjection(
                tree_sha256=digest,
                profiles=profiles,
                source_paths=source_paths,
                base_match=base_match,
                selected_source_path=selected_source_path,
            )
        )

    records.sort(key=lambda record: (record.relative_path, record.name.casefold(), record.tree_sha256))
    projections.sort(key=lambda item: (item.base_match, item.profiles, item.source_paths, item.tree_sha256))
    return ProfileVariantInventory(tuple(records), tuple(projections))
