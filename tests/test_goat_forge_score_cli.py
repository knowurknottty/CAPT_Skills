import json
from pathlib import Path
import subprocess
import sys

from goat_forge.inventory import SkillRecord, tree_digest


def make_record(root: Path, name: str, body: str) -> SkillRecord:
    skill = root / name
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: Use when {name} is needed\n---\n{body}"
    )
    return SkillRecord(
        source_lane="live",
        source_path=str(skill),
        relative_path=name,
        name=name,
        description=f"Use when {name} is needed",
        file_count=1,
        byte_count=(skill / "SKILL.md").stat().st_size,
        symlink_count=0,
        tree_sha256=tree_digest(skill),
        frontmatter_status="OK",
        discovery_status="LIVE",
    )


def test_score_cli_writes_deterministic_auto_ranking(tmp_path: Path):
    source = tmp_path / "source"
    strong = make_record(
        source,
        "strong-skill",
        "## When to Use\nUse when a failure needs isolation.\n"
        "## Do Not Use\nDo not use for feature design.\n"
        "## Workflow\n1. Reproduce.\n2. Isolate.\n"
        "## Verification\nRequire test evidence before PASS.\n"
        "## Recovery\nFail closed; rollback and retry safely.\n",
    )
    weak = make_record(source, "weak-skill", "Use this for any task whenever useful.\n")
    inventory = tmp_path / "inventory.jsonl"
    inventory.write_text(
        "\n".join(json.dumps(r.to_dict(), sort_keys=True) for r in (weak, strong)) + "\n"
    )
    output_json = tmp_path / "ranking.json"
    output_md = tmp_path / "ranking.md"
    completed = subprocess.run(
        [sys.executable, "scripts/goat_forge_score.py", "--inventory", str(inventory),
         "--json", str(output_json), "--markdown", str(output_md)],
        capture_output=True, text=True, check=False,
    )
    assert completed.returncode == 0, completed.stderr
    report = json.loads(output_json.read_text())
    assert report["schema_version"] == "1.0.0"
    assert report["review_state"] == "AUTO"
    assert report["promotion_authority"] is False
    assert [row["score"]["name"] for row in report["ranking"]] == [
        "strong-skill", "weak-skill"
    ]
    assert [row["rank"] for row in report["ranking"]] == [1, 2]
    markdown = output_md.read_text()
    assert "automatic structural triage" in markdown.lower()
    assert "does not authorize promotion" in markdown.lower()
    assert "strong-skill" in markdown
    assert "weak-skill" in markdown


def test_score_cli_fails_closed_when_inventory_source_is_missing(tmp_path: Path):
    missing = make_record(tmp_path / "source", "missing-skill", "Use when needed.\n")
    Path(missing.source_path).rename(tmp_path / "moved-away")
    inventory = tmp_path / "inventory.jsonl"
    inventory.write_text(json.dumps(missing.to_dict()) + "\n")
    completed = subprocess.run(
        [sys.executable, "scripts/goat_forge_score.py", "--inventory", str(inventory),
         "--json", str(tmp_path / "ranking.json"),
         "--markdown", str(tmp_path / "ranking.md")],
        capture_output=True, text=True, check=False,
    )
    assert completed.returncode != 0
    assert "missing skill source" in completed.stderr.lower()
