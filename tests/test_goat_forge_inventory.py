from pathlib import Path

from goat_forge.inventory import iter_skill_records, tree_digest


def make_skill(root: Path, dirname: str, frontmatter: str, body: str = "# Skill\n") -> Path:
    skill = root / dirname
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(frontmatter + body)
    return skill


def test_tree_digest_is_content_deterministic(tmp_path: Path):
    skill = make_skill(
        tmp_path,
        "alpha",
        "---\nname: alpha\ndescription: Use when alpha is needed\n---\n",
    )
    first = tree_digest(skill)
    (skill / "SKILL.md").touch()
    second = tree_digest(skill)
    assert first == second


def test_inventory_records_malformed_frontmatter_and_skips_containers(tmp_path: Path):
    make_skill(tmp_path, "broken", "---\nname:\n---\n")
    (tmp_path / "container-only").mkdir()

    records = iter_skill_records({"live": tmp_path})

    assert [record.relative_path for record in records] == ["broken"]
    assert records[0].frontmatter_status == "MALFORMED"
    assert records[0].name == "broken"


def test_inventory_preserves_duplicate_names_across_lanes(tmp_path: Path):
    live = tmp_path / "live"
    bundled = tmp_path / "bundled"
    make_skill(live, "one", "---\nname: duplicate\ndescription: Use when live\n---\n")
    make_skill(bundled, "two", "---\nname: duplicate\ndescription: Use when bundled\n---\n")

    records = iter_skill_records({"live": live, "bundled": bundled})
    assert [(r.source_lane, r.name) for r in records] == [
        ("bundled", "duplicate"),
        ("live", "duplicate"),
    ]


def test_inventory_records_symlink_without_following_external_content(tmp_path: Path):
    root = tmp_path / "root"
    skill = make_skill(root, "linked", "---\nname: linked\ndescription: Use when linked\n---\n")
    external = tmp_path / "outside.txt"
    external.write_text("secret-one")
    (skill / "outside-link").symlink_to(external)

    records = iter_skill_records({"live": root})
    before = records[0]
    external.write_text("secret-two")
    after = iter_skill_records({"live": root})[0]

    assert before.symlink_count == 1
    assert before.tree_sha256 == after.tree_sha256
    assert before.file_count == 1


def test_inventory_reads_folded_description_frontmatter(tmp_path: Path):
    root = tmp_path / "root"
    make_skill(
        root,
        "folded",
        "---\nname: folded\ndescription: >\n  Use when the skill has a folded\n  YAML description\n---\n",
    )

    record = iter_skill_records({"live": root})[0]

    assert record.frontmatter_status == "OK"
    assert record.description == "Use when the skill has a folded YAML description"


def test_write_inventory_emits_roundtrippable_jsonl_and_summary(tmp_path: Path):
    import json
    from goat_forge.inventory import write_inventory

    root = tmp_path / "root"
    make_skill(root, "alpha", "---\nname: alpha\ndescription: Use when alpha\n---\n")
    records = iter_skill_records({"live": root})
    jsonl = tmp_path / "inventory.jsonl"
    summary = tmp_path / "summary.json"

    write_inventory(records, jsonl, summary)

    row = json.loads(jsonl.read_text().strip())
    report = json.loads(summary.read_text())
    assert row["name"] == "alpha"
    assert report["total"] == 1
    assert report["by_lane"] == {"live": 1}
    assert report["frontmatter"] == {"OK": 1}


def test_inventory_marks_archived_live_packages(tmp_path: Path):
    root = tmp_path / "live"
    make_skill(root / ".archive", "old", "---\nname: old\ndescription: Use when old\n---\n")

    record = iter_skill_records({"live": root})[0]

    assert record.discovery_status == "ARCHIVED"


def test_inventory_records_top_level_discovery_symlink(tmp_path: Path):
    from goat_forge.inventory import iter_discovery_links

    root = tmp_path / "live"
    target = tmp_path / "canonical" / "alpha"
    make_skill(target.parent, target.name, "---\nname: alpha\ndescription: Use when alpha\n---\n")
    root.mkdir()
    (root / "alpha").symlink_to(target, target_is_directory=True)

    links = iter_discovery_links(root)
    assert [(link.name, link.target_path, link.target_exists) for link in links] == [
        ("alpha", str(target), True)
    ]


def test_write_discovery_links_emits_jsonl(tmp_path: Path):
    import json
    from goat_forge.inventory import iter_discovery_links, write_discovery_links

    root = tmp_path / "live"
    target = tmp_path / "canonical" / "alpha"
    make_skill(target.parent, target.name, "---\nname: alpha\ndescription: Use when alpha\n---\n")
    root.mkdir()
    (root / "alpha").symlink_to(target, target_is_directory=True)
    output = tmp_path / "links.jsonl"

    write_discovery_links(iter_discovery_links(root), output)

    row = json.loads(output.read_text().strip())
    assert row["name"] == "alpha"
    assert row["target_exists"] is True


def test_inventory_reads_chomped_folded_description_frontmatter(tmp_path: Path):
    root = tmp_path / "root"
    make_skill(
        root,
        "folded-chomped",
        "---\nname: folded-chomped\ndescription: >-\n  Use when folded YAML uses\n  a chomping indicator\n---\n",
    )

    record = iter_skill_records({"live": root})[0]
    assert record.description == "Use when folded YAML uses a chomping indicator"


def test_portable_path_collapses_home_prefix_without_touching_external_paths():
    from goat_forge.inventory import portable_path

    home = Path("/Users/example")
    inside = Path("/Users/example/.hermes/skills/alpha")
    outside = Path("/opt/shared/skill")

    assert portable_path(inside, home=home) == "~/.hermes/skills/alpha"
    assert portable_path(outside, home=home) == "/opt/shared/skill"


def test_linked_skill_inventory_handles_direct_and_container_targets(tmp_path: Path):
    from goat_forge.inventory import DiscoveryLink, iter_linked_skill_records

    direct = make_skill(
        tmp_path / "direct-root", "direct",
        "---\nname: direct\ndescription: Use when direct\n---\n",
    )
    container = tmp_path / "container"
    make_skill(
        container, "nested",
        "---\nname: nested\ndescription: Use when nested\n---\n",
    )
    links = [
        DiscoveryLink("direct-link", "/link/direct", str(direct), True),
        DiscoveryLink("container-link", "/link/container", str(container), True),
    ]

    records = iter_linked_skill_records(links)

    assert [(r.source_lane, r.discovery_status, r.name) for r in records] == [
        ("linked", "LINKED", "nested"),
        ("linked", "LINKED", "direct"),
    ]
