from datetime import datetime, timezone

import requests

POKEMON_COLOR = 0xFFCB05
MATCH_COLOR = 0x57F287   # Discord green
DEBRIEF_COLOR = 0x5865F2  # Discord blurple


def send(listing: dict, card_name: str, card_set: str, language: str, webhook_url: str) -> None:
    embed = {
        "title": f"🎴 New listing: {card_name}",
        "url": listing["url"],
        "color": MATCH_COLOR,
        "fields": [
            {"name": "📦 Set", "value": card_set, "inline": True},
            {"name": "💶 Price", "value": f"€{listing['price']:.2f}", "inline": True},
            {"name": "🏷️ Condition", "value": listing["condition"], "inline": True},
            {"name": "🌍 Language", "value": language.title(), "inline": True},
        ],
        "footer": {"text": "Vinted Delta Species Bot"},
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    if listing.get("thumbnail"):
        embed["thumbnail"] = {"url": listing["thumbnail"]}
    resp = requests.post(webhook_url, json={"embeds": [embed]}, timeout=10)
    resp.raise_for_status()


def send_debrief(matches: list, webhook_url: str) -> None:
    """Post one summary embed listing every new matched listing for this run."""
    timestamp = datetime.now(timezone.utc).strftime("%d %b %Y · %H:%M UTC")
    count = len(matches)

    lines = []
    for m in matches:
        lines.append(
            f"• **[{m['card_name']}]({m['listing']['url']})** ({m['card_set']}) "
            f"— €{m['listing']['price']:.2f} · {m['listing']['condition']}"
        )

    embed = {
        "title": f"🎴 {count} new listing{'s' if count > 1 else ''} · {timestamp}",
        "color": DEBRIEF_COLOR,
        "description": "\n".join(lines),
        "footer": {"text": "Vinted Delta Species Bot"},
    }
    resp = requests.post(webhook_url, json={"embeds": [embed]}, timeout=10)
    resp.raise_for_status()
