#!/usr/bin/env python3
import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from goat_forge.inventory import (
    iter_discovery_links,
    iter_skill_records,
    write_discovery_links,
    write_inventory,
)
from goat_forge.paths import ForgePaths, validate_source_roots


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inventory GOAT Forge skill sources")
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--live", type=Path, default=Path.home() / ".hermes/skills")
    parser.add_argument("--bundled", type=Path, default=Path.home() / ".hermes/hermes-agent/skills")
    parser.add_argument("--optional", type=Path, default=Path.home() / ".hermes/hermes-agent/optional-skills")
    parser.add_argument("--jsonl", type=Path)
    parser.add_argument("--summary", type=Path)
    parser.add_argument("--links", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = ForgePaths(args.repo_root, args.live, args.bundled, args.optional)
    validate_source_roots(paths)
    records = iter_skill_records(
        {"live": args.live, "bundled": args.bundled, "optional": args.optional}
    )
    jsonl = args.jsonl or args.repo_root / "provenance/inventory.jsonl"
    summary = args.summary or args.repo_root / "provenance/inventory-summary.json"
    write_inventory(records, jsonl, summary)
    links_path = args.links or args.repo_root / "provenance/discovery-links.jsonl"
    write_discovery_links(iter_discovery_links(args.live), links_path)
    print(f"inventoried {len(records)} skill packages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
