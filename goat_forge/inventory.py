from collections import Counter
from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
import re
from typing import Iterable


@dataclass(frozen=True)
class SkillRecord:
    source_lane: str
    source_path: str
    relative_path: str
    name: str
    description: str
    file_count: int
    byte_count: int
    symlink_count: int
    tree_sha256: str
    frontmatter_status: str
    discovery_status: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def portable_path(path: Path, *, home: Path | None = None) -> str:
    home = home or Path.home()
    try:
        relative = path.relative_to(home)
    except ValueError:
        return str(path)
    return "~/" + relative.as_posix()


@dataclass(frozen=True)
class DiscoveryLink:
    name: str
    link_path: str
    target_path: str
    target_exists: bool

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _tree_entries(root: Path) -> Iterable[Path]:
    stack = [root]
    while stack:
        current = stack.pop()
        for child in sorted(current.iterdir(), key=lambda p: p.name, reverse=True):
            yield child
            if child.is_dir() and not child.is_symlink():
                stack.append(child)


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(_tree_entries(root), key=lambda p: p.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix().encode()
        if path.is_symlink():
            digest.update(b"L\0" + rel + b"\0" + path.readlink().as_posix().encode() + b"\0")
        elif path.is_file():
            digest.update(b"F\0" + rel + b"\0")
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
        elif path.is_dir():
            digest.update(b"D\0" + rel + b"\0")
    return digest.hexdigest()


def _frontmatter(text: str, fallback_name: str) -> tuple[str, str, str]:
    if not text.startswith("---\n"):
        return fallback_name, "", "MISSING"
    end = text.find("\n---\n", 4)
    if end < 0:
        return fallback_name, "", "MALFORMED"
    header = text[4:end]
    name_match = re.search(r"(?m)^name:\s*([^\n]+?)\s*$", header)
    if not name_match or not name_match.group(1).strip():
        return fallback_name, "", "MALFORMED"
    name = name_match.group(1).strip().strip("\"'")
    desc_match = re.search(r"(?m)^description:[ \t]*([^\n]*)$", header)
    description = ""
    if desc_match:
        raw = desc_match.group(1).strip()
        if raw in {">", "|", ">-", "|-", ">+", "|+"}:
            tail = header[desc_match.end():].lstrip("\r\n").splitlines()
            folded = []
            for line in tail:
                if line.startswith((" ", "\t")):
                    folded.append(line.strip())
                else:
                    break
            description = " ".join(part for part in folded if part)
        else:
            description = raw.strip("\"'")
    return name, description, "OK"


def _stats(root: Path) -> tuple[int, int, int]:
    file_count = byte_count = symlink_count = 0
    for path in _tree_entries(root):
        if path.is_symlink():
            symlink_count += 1
        elif path.is_file():
            file_count += 1
            byte_count += path.stat().st_size
    return file_count, byte_count, symlink_count


def iter_skill_records(source_roots: dict[str, Path]) -> list[SkillRecord]:
    records: list[SkillRecord] = []
    for lane, root in sorted(source_roots.items()):
        for skill_md in sorted(root.rglob("SKILL.md")):
            skill_root = skill_md.parent
            relative = skill_root.relative_to(root).as_posix()
            try:
                text = skill_md.read_text(errors="replace")
            except OSError:
                text = ""
            name, description, status = _frontmatter(text, skill_root.name)
            file_count, byte_count, symlink_count = _stats(skill_root)
            records.append(
                SkillRecord(
                    source_lane=lane,
                    source_path=portable_path(skill_root.resolve(strict=False)),
                    relative_path=relative,
                    name=name,
                    description=description,
                    file_count=file_count,
                    byte_count=byte_count,
                    symlink_count=symlink_count,
                    tree_sha256=tree_digest(skill_root),
                    frontmatter_status=status,
                    discovery_status=_discovery_status(lane, relative),
                )
            )
    return records


def write_inventory(
    records: list[SkillRecord],
    jsonl_path: Path,
    summary_path: Path,
    source_roots: dict[str, Path] | None = None,
) -> None:
    jsonl_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(record.to_dict(), sort_keys=True) for record in records]
    jsonl_path.write_text("\n".join(lines) + ("\n" if lines else ""))
    counts = Counter(r.source_lane for r in records)
    by_lane = dict(sorted(counts.items()))
    summary: dict[str, object] = {
        "total": len(records),
        "by_lane": by_lane,
        "frontmatter": dict(sorted(Counter(r.frontmatter_status for r in records).items())),
    }
    if source_roots is not None:
        summary["by_lane"] = {lane: counts.get(lane, 0) for lane in sorted(source_roots)}
        summary["scanned_roots"] = {lane: str(path) for lane, path in sorted(source_roots.items())}
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")


def _discovery_status(lane: str, relative_path: str) -> str:
    if lane == "live":
        if relative_path == ".archive" or relative_path.startswith(".archive/"):
            return "ARCHIVED"
        if relative_path == ".curator_backups" or relative_path.startswith(".curator_backups/"):
            return "BACKUP"
        if relative_path == ".hub" or relative_path.startswith(".hub/"):
            return "HUB_INTERNAL"
    return lane.upper()


def iter_discovery_links(root: Path) -> list[DiscoveryLink]:
    links: list[DiscoveryLink] = []
    for path in sorted(root.iterdir(), key=lambda p: p.name):
        if not path.is_symlink():
            continue
        raw_target = path.readlink()
        target = (path.parent / raw_target).resolve(strict=False)
        links.append(DiscoveryLink(path.name, portable_path(path), portable_path(target), target.exists()))
    return links


def write_discovery_links(links: list[DiscoveryLink], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(link.to_dict(), sort_keys=True) for link in links]
    output_path.write_text("\n".join(lines) + ("\n" if lines else ""))


def iter_linked_skill_records(links: list[DiscoveryLink]) -> list[SkillRecord]:
    records: list[SkillRecord] = []
    seen: set[Path] = set()
    for link in sorted(links, key=lambda item: item.name):
        target = Path(link.target_path).expanduser()
        if not target.exists():
            continue
        direct = target / "SKILL.md"
        skill_files = [direct] if direct.is_file() else sorted(target.rglob("SKILL.md"))
        for skill_md in skill_files:
            skill_root = skill_md.parent.resolve(strict=False)
            if skill_root in seen:
                continue
            seen.add(skill_root)
            try:
                text = skill_md.read_text(errors="replace")
            except OSError:
                text = ""
            name, description, status = _frontmatter(text, skill_root.name)
            files, bytes_, symlinks = _stats(skill_root)
            suffix = skill_root.relative_to(target).as_posix() if skill_root != target else ""
            relative = link.name + (f"/{suffix}" if suffix else "")
            records.append(
                SkillRecord(
                    source_lane="linked",
                    source_path=portable_path(skill_root),
                    relative_path=relative,
                    name=name,
                    description=description,
                    file_count=files,
                    byte_count=bytes_,
                    symlink_count=symlinks,
                    tree_sha256=tree_digest(skill_root),
                    frontmatter_status=status,
                    discovery_status="LINKED",
                )
            )
    return records
