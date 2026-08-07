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

    # Header embed with compact summary of all matches. Capped to the same 9 matches
    # that get detail embeds below — Discord limits a single POST to 6000 characters
    # of combined embed text, and an uncapped summary can exceed that on a large
    # first-run backfill (e.g. right after adding several new cards to the tracker).
    summary_lines = [
        f"• {m['card_name']} · {m['card_set']} · €{m['listing']['price']:.2f}"
        for m in matches[:9]
    ]
    if count > 9:
        summary_lines.append(f"…and {count - 9} more")
    embeds.append({
        "title": f"🎴 {count} new listing{'s' if count > 1 else ''} · {timestamp}",
        "description": "\n".join(summary_lines),
        "color": DEBRIEF_COLOR,
        "footer": {"text": "Vinted Delta Species Bot"},
    })

    # One embed per match (Discord max 10 embeds per POST, reserve slot 0 for header)
    shown = matches[:9]
    overflow = len(matches) - len(shown)
    for m in shown:
        listing = m["listing"]
        embed = {
            "title": f"{m['card_name']} ({m['card_set']})",
            "url": listing["url"],
            "color": MATCH_COLOR,
            "fields": [
                {"name": "💶 Price", "value": f"€{listing['price']:.2f}", "inline": True},
                {"name": "🏷️ Condition", "value": listing["condition"], "inline": True},
                {"name": "🔗 Link", "value": f"[View on Vinted]({listing['url']})", "inline": False},
            ],
        }
        if listing.get("thumbnail"):
            embed["thumbnail"] = {"url": listing["thumbnail"]}
        embeds.append(embed)

    if overflow:
        embeds[0]["footer"]["text"] += f" · +{overflow} more not shown (first-run backfill)"

    resp = requests.post(webhook_url, json={"embeds": embeds}, timeout=10)
    resp.raise_for_status()
