from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
EXPECTED = {
    "inversion-creative-director": [
        "taste", "one primary", "precedence", "evidence", "inversion-interface-craft", "inversion-motion-craft"
    ],
    "inversion-interface-craft": [
        "impeccable", "design-taste-frontend", "dashboard", "marketing", "primary owner", "bounded"
    ],
    "inversion-motion-craft": [
        "hyperframes", "purposeful motion", "technical contract", "spine", "seam", "render"
    ],
    "inversion-creative-critic": [
        "VERIFIED", "INFERRED", "UNVERIFIED", "PASS", "FIX", "NO-GO", "stop"
    ],
}

errors = []
for name, needles in EXPECTED.items():
    path = SKILLS / name / "SKILL.md"
    if not path.exists():
        errors.append(f"MISSING {path}")
        continue
    text = path.read_text()
    m_name = re.search(r"(?m)^name:\s*(.+)$", text)
    m_desc = re.search(r"(?m)^description:\s*[>|\-]?\s*(.*)$", text)
    if not m_name or m_name.group(1).strip() != name:
        errors.append(f"{name}: bad/missing frontmatter name")
    if not m_desc:
        errors.append(f"{name}: missing description")
    body_words = len(re.findall(r"\b[\w'-]+\b", text))
    if body_words > 750:
        errors.append(f"{name}: too large ({body_words} words > 750)")
    for needle in needles:
        if needle.lower() not in text.lower():
            errors.append(f"{name}: missing contract token {needle!r}")

# Pack-level invariants: custom skills compose upstream owners; they never fork their mechanics.
all_text = "\n".join(
    (SKILLS / n / "SKILL.md").read_text()
    for n in EXPECTED if (SKILLS / n / "SKILL.md").exists()
)
if all_text:
    if "copy upstream" not in all_text.lower() and "do not duplicate" not in all_text.lower():
        errors.append("pack: no explicit anti-fork/drift rule")
    if "brief" not in all_text.lower() or "safety" not in all_text.lower() or "technical" not in all_text.lower():
        errors.append("pack: precedence lacks brief/safety/technical layers")

if errors:
    print("FAIL")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("PASS: Inversion Labs skill-pack structural contract")
