#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from goat_forge.inventory import SkillRecord
from goat_forge.profile_inventory import discover_profile_roots, inventory_profile_variants


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inventory deduplicated Hermes profile variants")
    parser.add_argument("--base-inventory", type=Path, default=ROOT / "provenance/inventory.jsonl")
    parser.add_argument("--profiles-root", type=Path, default=Path.home() / ".hermes/profiles")
    parser.add_argument("--nested", type=Path, default=Path.home() / ".hermes/.hermes/skills")
    parser.add_argument("--variants", type=Path, default=ROOT / "provenance/profile-variants.jsonl")
    parser.add_argument("--projections", type=Path, default=ROOT / "provenance/profile-projections.jsonl")
    parser.add_argument("--merged", type=Path, default=ROOT / "provenance/inventory-expanded.jsonl")
    parser.add_argument("--summary", type=Path, default=ROOT / "provenance/inventory-expanded-summary.json")
    return parser.parse_args()


def load_records(path: Path) -> list[SkillRecord]:
    if not path.is_file():
        raise FileNotFoundError(f"missing base inventory: {path}")
    return [
        SkillRecord(**json.loads(line))
        for line in path.read_text().splitlines()
        if line.strip()
    ]


def write_jsonl(rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(row, sort_keys=True) for row in rows)
        + ("\n" if rows else "")
    )


def main() -> int:
    args = parse_args()
    try:
        base = load_records(args.base_inventory)
        profile_roots = discover_profile_roots(args.profiles_root)
        active_profile_roots = len(profile_roots)
        included_nested = False
        if args.nested.is_dir() and next(args.nested.rglob("SKILL.md"), None) is not None:
            profile_roots = dict(profile_roots)
            profile_roots["nested"] = args.nested
            included_nested = True
        result = inventory_profile_variants(profile_roots, base)
    except (OSError, ValueError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    variants = [record.to_dict() for record in result.records]
    projections = [projection.to_dict() for projection in result.projections]
    merged_records = list(base) + list(result.records)
    write_jsonl(variants, args.variants)
    write_jsonl(projections, args.projections)
    write_jsonl([record.to_dict() for record in merged_records], args.merged)

    base_matched = sum(1 for projection in result.projections if projection.base_match)
    summary = {
        "base_total": len(base),
        "variant_total": len(result.records),
        "expanded_total": len(merged_records),
        "projection_groups": len(result.projections),
        "base_matched_projection_groups": base_matched,
        "new_variant_groups": len(result.projections) - base_matched,
        "active_profile_roots": active_profile_roots,
        "included_nested_root": included_nested,
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(
        f"expanded {len(base)} base packages with {len(result.records)} "
        f"deduplicated profile/nested variants"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
