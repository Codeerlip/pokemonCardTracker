from datetime import datetime, timezone

import requests

POKEMON_COLOR = 0xFFCB05
MATCH_COLOR = 0x57F287   # Discord green
DEBRIEF_COLOR = 0x5865F2  # Discord blurple


def send_debrief(matches: list, webhook_url: str) -> None:
    """Post all matched listings in one webhook request (up to 10 embeds per POST)."""
    timestamp = datetime.now(timezone.utc).strftime("%d %b %Y · %H:%M UTC")
    count = len(matches)

    embeds = []

    # Header embed
    embeds.append({
        "title": f"🎴 {count} new listing{'s' if count > 1 else ''} · {timestamp}",
        "color": DEBRIEF_COLOR,
        "footer": {"text": "Vinted Delta Species Bot"},
    })

    # One embed per match (Discord max 10 embeds per POST, max 6000 chars total)
    for m in matches[:9]:  # reserve slot 0 for header
        listing = m["listing"]
        embed = {
            "title": f"{m['card_name']} ({m['card_set']})",
            "url": listing["url"],
            "color": MATCH_COLOR,
            "fields": [
                {"name": "💶 Price", "value": f"€{listing['price']:.2f}", "inline": True},
                {"name": "🏷️ Condition", "value": listing["condition"], "inline": True},
            ],
        }
        if listing.get("thumbnail"):
            embed["thumbnail"] = {"url": listing["thumbnail"]}
        embeds.append(embed)

    resp = requests.post(webhook_url, json={"embeds": embeds}, timeout=10)
    resp.raise_for_status()
