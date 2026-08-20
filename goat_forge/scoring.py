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
    discovery_penalty: int
    duplication_penalty: int
    auto_score: int
    capability_leverage: int | None = None
    uniqueness: int | None = None
    review_state: str = "AUTO"

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _bounded(value: int) -> int:
    return max(0, min(10, value))


def canonical_name(name: str) -> str:
    value = name.casefold().strip()
    value = re.sub(r"(?:[-_.](?:v|ver|version)?\d+(?:\.\d+)*)$", "", value)
    value = re.sub(r"(?:[-_.](?:copy|backup|old|legacy))$", "", value)
    return value


def build_score_index(records: list[SkillRecord]) -> ScoreIndex:
    return ScoreIndex(
        Counter(record.tree_sha256 for record in records),
        Counter(record.name.casefold() for record in records),
        Counter(canonical_name(record.name) for record in records),
    )


def _has(text: str, pattern: str) -> bool:
    return re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE) is not None


def _trigger_precision(record: SkillRecord, text: str) -> int:
    score = 0
    joined = f"{record.description}\n{text}"
    if _has(joined, r"\buse when\b|^#{1,4}\s+when to use\b"):
        score += 3
    if _has(joined, r"\bdo not use\b|\bwhen not to use\b|\bnot for\b|\bshould not trigger\b"):
        score += 4
    if _has(joined, r"\brequires?\b|\bonly when\b|\bif and only if\b|\bprecondition"):
        score += 2
    if _has(joined, r"\b(any|every|all) (task|request|problem)s?\b|\banything\b|\bwhenever\b"):
        score -= 4
    return _bounded(score)


def _procedural_depth(text: str) -> int:
    score = 0
    if _has(text, r"^#{1,4}\s+(workflow|procedure|process|steps|method)\b"):
        score += 3
    numbered = len(re.findall(r"(?m)^\s*\d+[.)]\s+", text))
    score += min(4, numbered)
    if _has(text, r"\bif\b.*\bthen\b|\bgate\b|\bdecision\b|\bstop when\b"):
        score += 2
    if _has(text, r"\bprerequisite|precondition|input contract\b"):
        score += 1
    return _bounded(score)


def _verification_discipline(text: str) -> int:
    score = 0
    if _has(text, r"^#{1,4}\s+(verification|validation|testing|acceptance)\b"):
        score += 3
    if _has(text, r"\bevidence\b|\bassert\b|\btest(s|ed|ing)?\b|\bexit code\b"):
        score += 3
    if _has(text, r"\bbefore (claim|calling|declaring|completion)|\bprove\b|\bproof\b"):
        score += 2
    if _has(text, r"\bPASS\b|\bFAIL\b|\bNO[-_ ]?GO\b|\bverified\b"):
        score += 2
    return _bounded(score)


def _recovery_semantics(text: str) -> int:
    score = 0
    if _has(text, r"^#{1,4}\s+(failure|recovery|rollback|error handling)\b"):
        score += 2
    if _has(text, r"\brollback\b|\bretry\b|\brecover\b|\bresume\b|\bcleanup\b"):
        score += 4
    if _has(text, r"\bfail closed\b|\bblocked\b|\bblocker\b"):
        score += 2
    if _has(text, r"\bescalate\b|\bstop\b|\babort\b|\brevert\b"):
        score += 2
    return _bounded(score)


def _composability(text: str) -> int:
    score = 0
    if _has(text, r"\bauthority\b|\bscope\b|\bownership\b|\bprimary owner\b"):
        score += 3
    if _has(text, r"\bdelegate\b|\bcompose\b|\bupstream\b|\bhandoff\b|\brouter\b"):
        score += 3
    if _has(text, r"\bdoes not own\b|\bdo not exceed\b|\bboundar(y|ies)\b"):
        score += 2
    if _has(text, r"\bconflict\b|\bprecedence\b|\bpriority\b"):
        score += 2
    return _bounded(score)


def _security_fail_closed(text: str) -> int:
    score = 0
    if _has(text, r"\bsecurity\b|\bsafety\b|\bthreat\b"):
        score += 2
    if _has(text, r"\bapproval\b|\bpermission\b|\bauthori[sz]ed\b|\bleast privilege\b"):
        score += 2
    if _has(text, r"\bfail closed\b|\bdeny by default\b"):
        score += 2
    if _has(text, r"\bsecret\b|\bcredential\b|\bsandbox\b|\buntrusted\b"):
        score += 2
    if _has(text, r"\bdestructive\b|\bside effect\b|\beffect boundary\b"):
        score += 2
    return _bounded(score)


def _context_efficiency(text: str) -> int:
    words = len(re.findall(r"\b[\w'-]+\b", text))
    if words <= 750:
        return 10
    if words <= 1500:
        return 8
    if words <= 3000:
        return 5
    if words <= 6000:
        return 2
    return 0


def _support_depth(record: SkillRecord, text: str) -> int:
    if record.file_count <= 1:
        score = 0
    elif record.file_count <= 3:
        score = 2
    elif record.file_count <= 5:
        score = 4
    else:
        score = 6
    if _has(text, r"\breferences?/|\bscripts?/|\bexamples?/"):
        score += 4
    return _bounded(score)


def _metadata_quality(record: SkillRecord) -> tuple[int, int]:
    if record.frontmatter_status == "OK":
        penalty = 0
        score = 5
    elif record.frontmatter_status == "MISSING":
        penalty = -10
        score = 0
    else:
        penalty = -15
        score = 0
    description = record.description.strip()
    if 12 <= len(description) <= 600:
        score += 3
    if re.search(r"\buse when\b", description, re.IGNORECASE):
        score += 2
    return _bounded(score), penalty


def _discovery_penalty(record: SkillRecord) -> int:
    return {
        "ARCHIVED": -15,
        "BACKUP": -20,
        "HUB_INTERNAL": -15,
    }.get(record.discovery_status, 0)


def _duplication_penalty(record: SkillRecord, index: ScoreIndex | None) -> int:
    if index is None:
        return 0
    penalty = 0
    digest_count = index.exact_digest_counts[record.tree_sha256]
    name_count = index.exact_name_counts[record.name.casefold()]
    canonical_count = index.canonical_name_counts[canonical_name(record.name)]
    if digest_count > 1:
        penalty -= min(24, 12 * (digest_count - 1))
    if name_count > 1:
        penalty -= min(12, 4 * (name_count - 1))
    if canonical_count > 1:
        penalty -= min(15, 3 * (canonical_count - 1))
    return penalty


def score_skill(record: SkillRecord, text: str, *, index: ScoreIndex | None = None) -> ScoreCard:
    trigger = _trigger_precision(record, text)
    procedure = _procedural_depth(text)
    verification = _verification_discipline(text)
    recovery = _recovery_semantics(text)
    composability = _composability(text)
    security = _security_fail_closed(text)
    context = _context_efficiency(text)
    support = _support_depth(record, text)
    metadata, metadata_penalty = _metadata_quality(record)
    discovery_penalty = _discovery_penalty(record)
    duplication_penalty = _duplication_penalty(record, index)
    structural = sum((trigger, procedure, verification, recovery, composability,
                      security, context, support, metadata))
    normalized = round(structural * 100 / 90)
    auto_score = max(0, min(100, normalized + metadata_penalty + discovery_penalty + duplication_penalty))
    return ScoreCard(
        name=record.name,
        source_lane=record.source_lane,
        relative_path=record.relative_path,
        trigger_precision=trigger,
        procedural_depth=procedure,
        verification_discipline=verification,
        recovery_semantics=recovery,
        composability=composability,
        security_fail_closed=security,
        context_efficiency=context,
        support_depth=support,
        metadata_quality=metadata,
        metadata_penalty=metadata_penalty,
        discovery_penalty=discovery_penalty,
        duplication_penalty=duplication_penalty,
        auto_score=auto_score,
    )


def rank_score_cards(cards: list[ScoreCard]) -> list[ScoreCard]:
    return sorted(
        cards,
        key=lambda card: (
            -card.auto_score,
            card.name.casefold(),
            card.source_lane.casefold(),
            card.relative_path.casefold(),
        ),
    )
