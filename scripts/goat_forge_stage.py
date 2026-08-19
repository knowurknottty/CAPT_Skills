#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from goat_forge.inventory import SkillRecord
from goat_forge.staging import is_capt_candidate, stage_skill


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Quarantine GOAT Forge skill candidates")
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--inventory", type=Path)
    parser.add_argument("--lane", choices=("capt",), required=True)
    parser.add_argument(
        "--quarantine-root",
        type=Path,
        default=Path.home() / ".capt-skill-forge" / "quarantine",
    )
    return parser.parse_args()


def load_records(path: Path) -> list[SkillRecord]:
    return [SkillRecord(**json.loads(line)) for line in path.read_text().splitlines() if line]


def main() -> int:
    args = parse_args()
    repo = args.repo_root.resolve(strict=False)
    inventory = args.inventory or repo / "provenance/inventory.jsonl"
    records = load_records(inventory)
    selected = [record for record in records if is_capt_candidate(record)]
    staged = [
        stage_skill(record, args.lane, args.quarantine_root, repo)
        for record in selected
    ]
    lane_root = args.quarantine_root.expanduser() / args.lane
    manifest = lane_root / "MANIFEST.jsonl"
    rows = [
        {
            "package_id": item.package_id,
            "source_sha256": item.source_sha256,
            "staged_sha256": item.staged_sha256,
        }
        for item in staged
    ]
    manifest.write_text(
        "\n".join(json.dumps(row, sort_keys=True) for row in rows)
        + ("\n" if rows else "")
    )
    print(f"quarantined {len(staged)} {args.lane} skill packages")
    print(f"quarantine_root={args.quarantine_root.expanduser()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
