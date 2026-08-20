from collections import Counter
from dataclasses import asdict, dataclass
import re

from goat_forge.inventory import SkillRecord


@dataclass(frozen=True)
class ScoreIndex:
    exact_digest_counts: Counter[str]
    exact_name_counts: Counter[str]
    canonical_name_counts: Counter[str]


@dataclass(frozen=True)
class ScoreCard:
    name: str
    source_lane: str
    relative_path: str
    trigger_precision: int
    procedural_depth: int
    verification_discipline: int
    recovery_semantics: int
    composability: int
    security_fail_closed: int
    context_efficiency: int
    support_depth: int
    metadata_quality: int
    metadata_penalty: int
    duplication_penalty: int
    auto_score: int
    capability_leverage: int | None = None
    uniqueness: int | None = None
    review_state: str = "AUTO"

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def canonical_name(name: str) -> str:
    tokens = [t for t in re.split(r"[^a-z0-9]+", name.lower()) if t]
    kept = [
        t for t in tokens
        if not re.fullmatch(r"v?\d+(?:\.\d+)*", t)
        and t not in {"version"}
    ]
    return "-".join(kept)


def build_score_index(records: list[SkillRecord]) -> ScoreIndex:
    return ScoreIndex(
        exact_digest_counts=Counter(r.tree_sha256 for r in records),
        exact_name_counts=Counter(r.name.lower() for r in records),
        canonical_name_counts=Counter(canonical_name(r.name) for r in records),
    )


def _context_efficiency(text: str) -> int:
    words = len(re.findall(r"\b[\w'-]+\b", text))
    if 80 <= words <= 500:
        return 15
    if 50 <= words <= 800:
        return 11
    if 30 <= words <= 1200:
        return 7
    if words < 30:
        return 3
    return 0


def _keyword_score(text: str, keywords: tuple[str, ...], maximum: int) -> int:
    lower = text.lower()
    hits = sum(1 for keyword in keywords if keyword in lower)
    return min(maximum, hits * 2)


def score_skill(
    record: SkillRecord,
    text: str,
    *,
    index: ScoreIndex | None = None,
) -> ScoreCard:
    lower = text.lower()
    description = record.description.strip().lower()

    trigger = 0
    if description.startswith("use when"):
        trigger += 9
    elif "use when" in description:
        trigger += 6
    elif description:
        trigger += 2
    if re.search(r"(?mi)^##?\s+when to use", text):
        trigger += 4
    if "when not to use" in lower or "do not use" in lower:
        trigger += 2
    trigger = min(15, trigger)

    procedural = 0
    if re.search(r"(?mi)^##?\s+(workflow|process|procedure|implementation|steps)", text):
        procedural += 6
    numbered = len(re.findall(r"(?m)^\s*\d+[.)]\s+", text))
    bullets = len(re.findall(r"(?m)^\s*[-*]\s+", text))
    procedural += min(6, numbered)
    procedural += min(3, bullets // 3)
    procedural = min(15, procedural)

    verification = 6 if re.search(r"(?mi)^##?\s+verification", text) else 0
    verification += _keyword_score(
        text, ("verify", "evidence", "test", "assert", " pass", " fail", "proof"), 9
    )
    verification = min(15, verification)

    recovery = _keyword_score(
        text, ("recovery", "rollback", "retry", "fallback", "blocked", "fail closed", "failure"), 10
    )
    composability = _keyword_score(
        text, ("references/", "related skill", "delegate", "handoff", "dependency", "compose"), 10
    )
    security = _keyword_score(
        text, ("fail closed", "secret", "credential", "permission", "authority", "unsafe"), 5
    )
    context = _context_efficiency(text)

    support = 0
    if record.file_count >= 2:
        support += 4
    if record.file_count >= 5:
        support += 4
    if "references/" in lower or "scripts/" in lower or "templates/" in lower:
        support += 2
    support = min(10, support)
    metadata = 5 if record.frontmatter_status == "OK" else 0
    metadata_penalty = 0
    if record.frontmatter_status != "OK":
        metadata_penalty -= 15
    if len(record.description) > 500:
        metadata_penalty -= 5
    if re.search(r"(?i)(?:^|[-_])(20\d{2}|pr[-_]?\d+|issue[-_]?\d+)(?:$|[-_])", record.name):
        metadata_penalty -= 4

    duplication_penalty = 0
    if index is not None:
        exact_count = index.exact_digest_counts[record.tree_sha256]
        canonical_count = index.canonical_name_counts[canonical_name(record.name)]
        duplication_penalty -= min(16, max(0, exact_count - 1) * 8)
        duplication_penalty -= min(9, max(0, canonical_count - 1) * 3)

    positive = (
        trigger + procedural + verification + recovery + composability
        + security + context + support + metadata
    )
    auto_score = max(0, min(100, positive + metadata_penalty + duplication_penalty))

    return ScoreCard(
        name=record.name,
        source_lane=record.source_lane,
        relative_path=record.relative_path,
        trigger_precision=trigger,
        procedural_depth=procedural,
        verification_discipline=verification,
        recovery_semantics=recovery,
        composability=composability,
        security_fail_closed=security,
        context_efficiency=context,
        support_depth=support,
        metadata_quality=metadata,
        metadata_penalty=metadata_penalty,
        duplication_penalty=duplication_penalty,
        auto_score=auto_score,
    )
