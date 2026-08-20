import json
from pathlib import Path
import shutil
import subprocess
import sys

from goat_forge.inventory import iter_skill_records


def make_skill(root: Path, relative: str, name: str, body: str = "Use when needed.\n") -> Path:
    skill = root / relative
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: Use when {name} is needed\n---\n# {name}\n{body}"
    )
    return skill


def write_inventory(path: Path, records) -> None:
    path.write_text("\n".join(json.dumps(r.to_dict(), sort_keys=True) for r in records) + "\n")


def test_profile_cli_builds_deduplicated_expanded_inventory(tmp_path: Path):
    live = tmp_path / "live"
    alpha = make_skill(live, "alpha", "alpha")
    base = iter_skill_records({"live": live})
    base_path = tmp_path / "base.jsonl"
    write_inventory(base_path, base)

    profiles = tmp_path / "profiles"
    shutil.copytree(alpha, profiles / "author" / "skills" / "alpha")
    make_skill(profiles / "researcher" / "skills", "beta", "beta", "Unique beta.\n")
    make_skill(profiles / "author.bak.1" / "skills", "ignored", "ignored")
    nested = tmp_path / "nested"
    make_skill(nested, "gamma", "gamma", "Nested gamma.\n")

    variants = tmp_path / "variants.jsonl"
    projections = tmp_path / "projections.jsonl"
    merged = tmp_path / "expanded.jsonl"
    summary = tmp_path / "summary.json"
    completed = subprocess.run(
        [sys.executable, "scripts/goat_forge_profiles.py",
         "--base-inventory", str(base_path), "--profiles-root", str(profiles),
         "--nested", str(nested), "--variants", str(variants),
         "--projections", str(projections), "--merged", str(merged),
         "--summary", str(summary)],
        capture_output=True, text=True, check=False,
    )

    assert completed.returncode == 0, completed.stderr
    variant_rows = [json.loads(line) for line in variants.read_text().splitlines()]
    merged_rows = [json.loads(line) for line in merged.read_text().splitlines()]
    report = json.loads(summary.read_text())
    assert {row["name"] for row in variant_rows} == {"beta", "gamma"}
    assert len(merged_rows) == 3
    assert report["base_total"] == 1
    assert report["variant_total"] == 2
    assert report["expanded_total"] == 3
    assert report["active_profile_roots"] == 2
    assert report["included_nested_root"] is True
    assert report["base_matched_projection_groups"] == 1
    assert report["new_variant_groups"] == 2


def test_profile_cli_fails_closed_when_base_inventory_missing(tmp_path: Path):
    completed = subprocess.run(
        [sys.executable, "scripts/goat_forge_profiles.py",
         "--base-inventory", str(tmp_path / "missing.jsonl"),
         "--profiles-root", str(tmp_path / "profiles"),
         "--variants", str(tmp_path / "variants.jsonl"),
         "--projections", str(tmp_path / "projections.jsonl"),
         "--merged", str(tmp_path / "expanded.jsonl"),
         "--summary", str(tmp_path / "summary.json")],
        capture_output=True, text=True, check=False,
    )
    assert completed.returncode != 0
    assert "missing base inventory" in completed.stderr.lower()
