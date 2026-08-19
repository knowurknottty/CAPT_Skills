import json
from pathlib import Path
import subprocess
import sys


def test_inventory_cli_scans_explicit_roots(tmp_path: Path):
    roots = {}
    for lane in ("live", "bundled", "optional"):
        root = tmp_path / lane
        skill = root / f"{lane}-skill"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            f"---\nname: {lane}-skill\ndescription: Use when {lane}\n---\n# {lane}\n"
        )
        roots[lane] = root
    repo = tmp_path / "repo"
    repo.mkdir()
    jsonl = tmp_path / "inventory.jsonl"
    summary = tmp_path / "summary.json"
    links = tmp_path / "links.jsonl"

    command = [sys.executable, "scripts/goat_forge_inventory.py", "--repo-root", str(repo)]
    command += ["--live", str(roots["live"]), "--bundled", str(roots["bundled"])]
    command += ["--optional", str(roots["optional"]), "--jsonl", str(jsonl)]
    command += ["--summary", str(summary), "--links", str(links)]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)

    assert completed.returncode == 0, completed.stderr
    rows = [json.loads(line) for line in jsonl.read_text().splitlines()]
    report = json.loads(summary.read_text())
    assert [row["source_lane"] for row in rows] == ["bundled", "live", "optional"]
    assert report["total"] == 3
    assert links.exists()
