import json
from pathlib import Path
import subprocess
import sys

from goat_forge.inventory import SkillRecord, tree_digest


def make_record(root: Path, name: str, text: str, *, status: str = "LIVE") -> SkillRecord:
    skill = root / name
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(text)
    return SkillRecord(
        source_lane="live", source_path=str(skill), relative_path=name,
        name=name, description=f"Use when {name} is needed", file_count=1,
        byte_count=(skill / "SKILL.md").stat().st_size, symlink_count=0,
        tree_sha256=tree_digest(skill), frontmatter_status="OK",
        discovery_status=status,
    )


def test_score_cli_ranks_active_skills_and_excludes_archives(tmp_path: Path):
    source = tmp_path / "source"
    strong = make_record(source, "strong", """# Strong\n## When to Use\nUse when needed.\n## Workflow\n1. Inspect.\n2. Fix.\n## Verification\nVerify tests and evidence before PASS.\n## Failure Recovery\nRollback, retry, or fail closed when blocked.\n""")
    weak = make_record(source, "weak", "# Weak\nUse when needed.\n")
    archived = make_record(source, "old", "# Old\nUse when needed.\n", status="ARCHIVED")
    inventory = tmp_path / "inventory.jsonl"
    inventory.write_text("\n".join(json.dumps(r.to_dict()) for r in (weak, archived, strong)) + "\n")
    repo = tmp_path / "repo"
    (repo / "skills" / "strong").mkdir(parents=True)
    (repo / "skills" / "strong" / "SKILL.md").write_text("incumbent")
    output_json = tmp_path / "ranking.json"
    output_md = tmp_path / "ranking.md"

    completed = subprocess.run([
        sys.executable, "scripts/goat_forge_score.py",
        "--repo-root", str(repo), "--inventory", str(inventory),
        "--json", str(output_json), "--markdown", str(output_md),
    ], capture_output=True, text=True, check=False)

    assert completed.returncode == 0, completed.stderr
    rows = json.loads(output_json.read_text())
    assert [row["name"] for row in rows] == ["strong", "weak"]
    assert rows[0]["auto_score"] > rows[1]["auto_score"]
    assert rows[0]["candidate_state"] == "INCUMBENT"
    assert rows[1]["candidate_state"] == "AUTO"
    assert "old" not in output_md.read_text()
