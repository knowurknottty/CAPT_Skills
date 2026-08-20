#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from goat_forge.inventory import SkillRecord
from goat_forge.scoring import build_score_index, rank_score_cards, score_skill


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rank GOAT Forge skill candidates")
    parser.add_argument("--inventory", type=Path, default=ROOT / "provenance/inventory.jsonl")
    parser.add_argument("--json", type=Path, default=ROOT / "evals/goat-forge/ranking.json")
    parser.add_argument("--markdown", type=Path, default=ROOT / "evals/goat-forge/ranking.md")
    return parser.parse_args()


def load_records(path: Path) -> list[SkillRecord]:
    return [
        SkillRecord(**json.loads(line))
        for line in path.read_text().splitlines()
        if line.strip()
    ]


def load_skill_text(record: SkillRecord) -> str:
    root = Path(record.source_path).expanduser()
    skill_md = root / "SKILL.md"
    if not skill_md.is_file():
        raise FileNotFoundError(f"missing skill source: {skill_md}")
    return skill_md.read_text(errors="replace")


def build_report(records: list[SkillRecord]) -> dict[str, object]:
    index = build_score_index(records)
    cards = [score_skill(record, load_skill_text(record), index=index) for record in records]
    ranked = rank_score_cards(cards)
    rows = [
        {
            "rank": rank,
            "score": card.to_dict(),
        }
        for rank, card in enumerate(ranked, start=1)
    ]
    return {
        "schema_version": "1.0.0",
        "review_state": "AUTO",
        "promotion_authority": False,
        "total": len(rows),
        "ranking": rows,
    }


def write_json(report: dict[str, object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")


def write_markdown(report: dict[str, object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# GOAT Forge Automatic Ranking",
        "",
        "This is **automatic structural triage only**. It does not authorize promotion.",
        "Capability leverage and true uniqueness require semantic review and remain unset here.",
        "",
        "| Rank | Skill | Lane | Auto | Trigger | Procedure | Verify | Recovery | Compose | Security | Context | Dup Penalty |",
        "|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in report["ranking"]:
        score = row["score"]
        lines.append(
            f"| {row['rank']} | `{score['name']}` | {score['source_lane']} | "
            f"{score['auto_score']} | {score['trigger_precision']} | {score['procedural_depth']} | "
            f"{score['verification_discipline']} | {score['recovery_semantics']} | "
            f"{score['composability']} | {score['security_fail_closed']} | "
            f"{score['context_efficiency']} | {score['duplication_penalty']} |"
        )
    path.write_text("\n".join(lines) + "\n")


def main() -> int:
    args = parse_args()
    try:
        records = load_records(args.inventory)
        report = build_report(records)
        write_json(report, args.json)
        write_markdown(report, args.markdown)
    except (OSError, ValueError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(f"ranked {report['total']} skill packages (AUTO only)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
