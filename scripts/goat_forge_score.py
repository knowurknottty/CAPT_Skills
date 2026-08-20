#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from goat_forge.inventory import SkillRecord
from goat_forge.scoring import build_score_index, score_skill

ACTIVE_STATUSES = {"LIVE", "BUNDLED", "OPTIONAL", "LINKED"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score GOAT Forge candidates")
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--inventory", type=Path)
    parser.add_argument("--json", type=Path)
    parser.add_argument("--markdown", type=Path)
    return parser.parse_args()


def load_records(path: Path) -> list[SkillRecord]:
    return [SkillRecord(**json.loads(line)) for line in path.read_text().splitlines() if line]


def incumbent_names(repo_root: Path) -> set[str]:
    skills = repo_root / "skills"
    if not skills.is_dir():
        return set()
    return {path.parent.name for path in skills.glob("*/SKILL.md")}


def main() -> int:
    args = parse_args()
    repo = args.repo_root.resolve(strict=False)
    inventory = args.inventory or repo / "provenance/inventory.jsonl"
    records = [r for r in load_records(inventory) if r.discovery_status in ACTIVE_STATUSES]
    index = build_score_index(records)
    incumbents = incumbent_names(repo)

    rows: list[dict[str, object]] = []
    for record in records:
        skill_md = Path(record.source_path).expanduser() / "SKILL.md"
        try:
            text = skill_md.read_text(errors="replace")
        except OSError:
            text = ""
        row = score_skill(record, text, index=index).to_dict()
        row["source_path"] = record.source_path
        row["candidate_state"] = "INCUMBENT" if record.name in incumbents else "AUTO"
        rows.append(row)

    rows.sort(key=lambda row: (-int(row["auto_score"]), str(row["name"]), str(row["source_lane"])))
    output_json = args.json or repo / "evals/goat-forge/ranking.json"
    output_md = args.markdown or repo / "evals/goat-forge/ranking.md"
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(rows, indent=2, sort_keys=True) + "\n")
    lines = [
        "# GOAT Forge Structural Ranking",
        "",
        "Structural triage only. `capability_leverage` and `uniqueness` require semantic review.",
        "",
        "| Rank | Score | Skill | Lane | State | Trigger | Verify | Recovery | Context |",
        "|---:|---:|---|---|---|---:|---:|---:|---:|",
    ]
    for rank, row in enumerate(rows, 1):
        lines.append(
            f"| {rank} | {row['auto_score']} | `{row['name']}` | {row['source_lane']} | "
            f"{row['candidate_state']} | {row['trigger_precision']} | "
            f"{row['verification_discipline']} | {row['recovery_semantics']} | "
            f"{row['context_efficiency']} |"
        )
    output_md.write_text("\n".join(lines) + "\n")
    print(f"scored {len(rows)} active skill packages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
