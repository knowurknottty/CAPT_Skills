from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ROOT / "evals/local-qwen/final-results.json",
    ROOT / "evals/local-qwen/cross-medium-results.json",
]

failed = False
for path in FILES:
    if not path.exists():
        print(f"MISSING {path}")
        failed = True
        continue
    data = json.loads(path.read_text())
    for name, result in data.items():
        checks = result.get("checks", result)
        bad = [key for key, value in checks.items() if value is not True]
        passed = result.get("passed", sum(value is True for value in checks.values()))
        total = result.get("total", len(checks))
        ok = not bad and passed == total == len(checks)
        print(f"{name}: {passed}/{total} {'PASS' if ok else 'FAIL'}")
        if not ok:
            print("  failed checks:", bad)
            failed = True

sys.exit(1 if failed else 0)
