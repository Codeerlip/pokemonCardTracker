from datetime import datetime, timezone, timedelta

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
        return True
    cutoff = datetime.now(timezone.utc) - timedelta(days=max_days)
    listing_date = datetime.fromtimestamp(created_at_ts, tz=timezone.utc)
    return listing_date >= cutoff


def check_title_relevance(title: str, card_name: str, set_number: str = "") -> bool:
    """Pokemon name must appear in the title, AND either:
    - the set number components both appear (e.g. '13' and '113'), OR
    - an explicit set keyword ('delta', 'δ', 'species') appears.
    Rarity markers (ex/gx/vmax/v) in the card name are optional."""
    _OPTIONAL = {"ex", "gx", "vmax", "v", "δ"}
    name_words = [w for w in card_name.lower().split() if w not in _OPTIONAL]
    title_lower = title.lower()

    if not all(w in title_lower for w in name_words):
        return False

    if set_number:
        parts = set_number.replace("/", " ").split()
        if all(p in title_lower for p in parts):
            return True

    return any(kw in title_lower for kw in ("delta", "δ", "species"))
