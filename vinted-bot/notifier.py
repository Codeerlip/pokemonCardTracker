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


def send_debrief(run_results: list, webhook_url: str) -> None:
    timestamp = datetime.now(timezone.utc).strftime("%d %b %Y · %H:%M UTC")
    total_listings = sum(r["listings_found"] for r in run_results)
    total_matches = sum(r["matches"] for r in run_results)
    seen = [r for r in run_results if r["listings_found"] > 0]

    lines = []

    if total_matches:
        lines.append(f"**✅ {total_matches} match{'es' if total_matches > 1 else ''} found**")
        for r in run_results:
            if r["matches"]:
                lines.append(f"> 🎴 **{r['card_name']}** — {r['card_set']}")
        lines.append("")

    lines.append("**📦 Card visibility this run**")
    if seen:
        for r in sorted(seen, key=lambda x: x["listings_found"], reverse=True):
            dots = "🟡" * min(r["listings_found"], 5)
            match_flag = "  ✅" if r["matches"] else ""
            lines.append(f"{dots} **{r['card_name']}** — {r['listings_found']} listing(s){match_flag}")
    else:
        lines.append("*No listings found this run.*")

    embed = {
        "title": f"📊 Run complete · {timestamp}",
        "color": DEBRIEF_COLOR,
        "description": "\n".join(lines),
        "footer": {
            "text": f"Vinted Delta Species Bot · {total_listings} listings scanned · {total_matches} match(es)"
        },
    }
    resp = requests.post(webhook_url, json={"embeds": [embed]}, timeout=10)
    resp.raise_for_status()
