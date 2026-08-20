import re


MAX_CORE_WORDS = 750
_GENERIC_NAME_TOKENS = {
    "goat", "skill", "skills", "core", "contract", "workflow", "workflows",
    "agent", "toolkit", "guide", "framework", "system", "systems",
}


def _frontmatter_value(text: str, key: str) -> str:
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---\n", 4)
    if end < 0:
        return ""
    header = text[4:end]
    match = re.search(rf"(?m)^{re.escape(key)}:[ \t]*([^\n]*)$", header)
    if not match:
        return ""
    raw = match.group(1).strip()
    if raw in {">", "|", ">-", "|-", ">+", "|+"}:
        tail = header[match.end():].lstrip("\r\n").splitlines()
        parts = []
        for line in tail:
            if line.startswith((" ", "\t")):
                parts.append(line.strip())
            else:
                break
        return " ".join(part for part in parts if part)
    return raw.strip("\"'")


def _body(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---\n", 4)
    return text[end + 5:] if end >= 0 else text


def _has_heading(text: str, pattern: str) -> bool:
    return bool(re.search(rf"(?mi)^##+\s+.*(?:{pattern}).*$", text))


def validate_forge_candidate(text: str) -> list[str]:
    errors: list[str] = []
    name = _frontmatter_value(text, "name")
    description = _frontmatter_value(text, "description")
    body = _body(text)
    lower = body.lower()

    if not name:
        errors.append("missing frontmatter name")
    if not description.lower().startswith("use when"):
        errors.append("description must be a precise 'Use when ...' trigger")

    if not (
        _has_heading(body, r"do not use|when not to use")
        or "do not use when" in lower
    ):
        errors.append("missing negative trigger / do-not-use boundary")

    if not (
        _has_heading(body, r"authority|scope")
        or ("owns " in lower and "does not own" in lower)
    ):
        errors.append("missing authority and scope boundary")

    if not _has_heading(body, r"workflow|process|procedure|steps|execution"):
        errors.append("missing executable workflow/process")

    if not (
        _has_heading(body, r"failure|recovery|fallback")
        or any(token in lower for token in ("rollback", "retry", "fail closed"))
    ):
        errors.append("missing failure/recovery semantics")

    if not (
        _has_heading(body, r"verification|evidence|proof")
        or ("evidence" in lower and "verify" in lower)
    ):
        errors.append("missing verification/evidence requirement")

    if not (
        _has_heading(body, r"stop condition|stopping condition")
        or re.search(r"\bstop\b", lower)
    ):
        errors.append("missing stop condition")

    if re.search(r"(?i)guaranteed\s+to\s+(?:succeed|work)|always\s+succeeds|100%\s+(?:success|reliable)", body):
        errors.append("unsupported success theater / guarantee")

    word_count = len(re.findall(r"\b[\w'-]+\b", text))
    if word_count > MAX_CORE_WORDS:
        errors.append(f"SKILL.md core too large: {word_count} words > {MAX_CORE_WORDS}")

    if name:
        tokens = [
            token for token in re.split(r"[^a-z0-9]+", name.lower())
            if len(token) >= 4 and token not in _GENERIC_NAME_TOKENS
        ]
        if tokens and not any(re.search(rf"\b{re.escape(token)}\w*\b", lower) for token in tokens):
            errors.append("name/content mismatch: no distinctive name token appears in body")

    return errors
