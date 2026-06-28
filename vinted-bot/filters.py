import re
from datetime import datetime, timezone, timedelta

_SET_NUMBER_RE = re.compile(r'\b(\d+)\s*/\s*(\d+)\b')

# Standalone language codes/words that identify a non-English card edition.
# "fr" is safe as a whole word — no common Dutch or English word is exactly "fr".
# "de" and "nl" are intentionally excluded: "de" is a Dutch article and "nl"
# appears in URLs and other shorthand unrelated to card language.
_NON_ENGLISH_LANG_RE = re.compile(
    r'\b(?:ita|fra|ger|deu|por|spa|jpn|jap|kor|fr|'
    r'italiano|italiana|fran[cç]ais|fran[cç]aise|francese|deutsch|'
    r'espagnol|espagnola|portugu[eê]s|portuguesa|japonais|japonaise|'
    r'italian|french|german|spanish|portuguese|japanese|korean|'
    r'dutch|nederlands)\b',
    re.IGNORECASE | re.UNICODE,
)

DUTCH_MARKERS = {
    "nieuw", "gebruikt", "goede", "staat", "verzenden", "verzending",
    "ophalen", "betaling", "betalen", "kaart", "pokemon", "conditie",
    "nette", "lichte", "beschadiging", "zeer", "mooie",
}

ENGLISH_MARKERS = {
    "mint", "near", "excellent", "good", "played", "damaged",
    "shipping", "payment", "condition", "card", "listing", "buy",
    "sell", "offer", "trade", "graded", "sleeved",
}

# Maps Vinted NL condition labels (Dutch) to internal codes
_CONDITION_MAP: dict[str, str] = {
    "nieuw met prijskaartje": "new",
    "nieuw zonder prijskaartje": "new",
    "heel goed": "like_new",
    "goed": "good",
    "veelgebruikt": "satisfactory",
    "redelijk": "poor",
    "slecht": "poor",
    # English codes passed through as-is (for tests / future API changes)
    "new": "new",
    "like_new": "like_new",
    "good": "good",
    "satisfactory": "satisfactory",
    "poor": "poor",
}

ALLOWED_CONDITIONS = {"new", "like_new", "good"}


def check_no_foreign_language_tag(title: str, description: str = "") -> bool:
    """Returns False if the title or description contains a known non-English language tag."""
    return (
        _NON_ENGLISH_LANG_RE.search(title) is None
        and _NON_ENGLISH_LANG_RE.search(description) is None
    )


def detect_language(title: str, description: str) -> str:
    text = (title + " " + description).lower().split()
    words = set(text)
    dutch_hits = words & DUTCH_MARKERS
    english_hits = words & ENGLISH_MARKERS
    if dutch_hits and not english_hits:
        return "dutch"
    if english_hits and not dutch_hits:
        return "english"
    return "unknown"


def check_condition(condition: str) -> bool:
    normalised = _CONDITION_MAP.get(condition.lower(), condition.lower())
    return normalised in ALLOWED_CONDITIONS


def check_price(price: float, max_price: float | None) -> bool:
    """Returns True when max_price is None (no limit set) or price is within limit."""
    if max_price is None:
        return True
    return price <= max_price


def check_recency(created_at_ts: int | None, max_days: int = 30) -> bool:
    if not created_at_ts:
        # Vinted catalog API no longer returns date fields; pass listings through
        # when unknown — DB deduplication prevents repeat notifications.
        return True
    cutoff = datetime.now(timezone.utc) - timedelta(days=max_days)
    listing_date = datetime.fromtimestamp(created_at_ts, tz=timezone.utc)
    return listing_date >= cutoff


def check_title_relevance(title: str, card_name: str, set_number: str = "") -> bool:
    """Pokemon name must appear in the title, AND either:
    - the set number is present (both components for X/Y, bare number for singles), OR
    - an explicit set keyword ('delta', 'δ', 'species') appears AND the title
      does not contain a conflicting X/Y set number.
    Rarity markers (ex/gx/vmax/v) in the card name are optional.
    Delta keywords are NOT required when the set number itself is present —
    many valid listings omit 'delta species' and just state the card name and number."""
    _OPTIONAL = {"gx", "vmax", "v", "δ"}
    name_words = [w for w in card_name.lower().split() if w not in _OPTIONAL]
    title_lower = title.lower()

    if not all(w in title_lower for w in name_words):
        return False

    if set_number:
        parts = set_number.replace("/", " ").split()
        if len(parts) >= 2 and all(p in title_lower for p in parts):
            return True
        # If the title contains an explicit X/Y number that differs from ours,
        # it's a different card — reject even if "delta" appears in the title.
        m = _SET_NUMBER_RE.search(title_lower)
        if m:
            title_set = f"{m.group(1)}/{m.group(2)}"
            if title_set != set_number.lower():
                return False
        # For single-component set numbers the bare number is sufficient —
        # no delta keyword required (consistent with 2-part set number behaviour).
        if len(parts) == 1:
            return parts[0] in title_lower

    return any(kw in title_lower for kw in ("delta", "δ", "species"))
