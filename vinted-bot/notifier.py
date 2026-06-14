import requests

POKEMON_COLOR = 0xFFCB05


def send(listing: dict, card_name: str, card_set: str, language: str, webhook_url: str) -> None:
    embed = {
        "title": f"New listing: {card_name}",
        "url": listing["url"],
        "color": POKEMON_COLOR,
        "fields": [
            {"name": "Set", "value": card_set, "inline": True},
            {"name": "Price", "value": f"€{listing['price']:.2f}", "inline": True},
            {"name": "Condition", "value": listing["condition"], "inline": True},
            {"name": "Language", "value": language.title(), "inline": True},
        ],
        "footer": {"text": "Vinted Delta Species Bot"},
    }
    resp = requests.post(
        webhook_url,
        json={"embeds": [embed]},
        timeout=10,
    )
    resp.raise_for_status()
