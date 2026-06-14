import argparse
import json
import os
import time
import random
from pathlib import Path

import db
import vinted
import filters
import notifier


def load_config() -> dict:
    path = Path(__file__).parent / "config.json"
    with open(path) as f:
        return json.load(f)


def process_card(card: dict, cfg: dict, dry_run: bool) -> tuple[int, list]:
    queries = card["search_queries"]
    print(f"[main] searching {len(queries)} query/queries for: {card['name']}")
    listings = vinted.search_multi(queries)
    print(f"[main] found {len(listings)} unique listing(s) for {card['name']}")

    matches = []
    for listing in listings:
        if db.is_seen(listing["id"]):
            continue

        language = filters.detect_language(listing["title"], listing["description"])
        title_ok = filters.check_title_relevance(listing["title"], card["name"], card.get("set_number", ""))
        condition_ok = filters.check_condition(listing["condition"])
        price_ok = filters.check_price(listing["price"], card.get("max_price"))
        recency_ok = filters.check_recency(listing.get("created_at_ts"), cfg.get("max_listing_age_days", 30))

        if not title_ok or not condition_ok or not price_ok or not recency_ok:
            db.mark_seen(listing["id"])
            continue

        print(
            f"[main] MATCH — {listing['title']} | "
            f"€{listing['price']:.2f} | {listing['condition']} | lang:{language}"
        )
        matches.append({"card_name": card["name"], "card_set": card.get("set", ""), "listing": listing})

        if not dry_run:
            notifier.send(listing, card["name"], card.get("set", ""), language, cfg["discord_webhook_url"])

        db.mark_seen(listing["id"])

    print(f"[main] {len(matches)} new match(es) for {card['name']}")
    return len(listings), matches


def main() -> None:
    parser = argparse.ArgumentParser(description="Vinted Delta Species alert bot")
    parser.add_argument("--dry-run", action="store_true", help="Log matches without sending Discord messages")
    args = parser.parse_args()

    if args.dry_run:
        print("[main] DRY RUN — Discord notifications suppressed")

    cfg = load_config()
    cfg["discord_webhook_url"] = os.environ.get("DISCORD_WEBHOOK_URL") or cfg.get("discord_webhook_url", "")

    print("[main] --- starting poll cycle ---")
    all_matches = []
    for card in cfg["cards"]:
        found, matches = process_card(card, cfg, args.dry_run)
        db.record_sightings(card["name"], found)
        all_matches.extend(matches)
        time.sleep(random.uniform(3, 7))

    if all_matches and not args.dry_run:
        notifier.send_debrief(all_matches, cfg["discord_webhook_url"])

    print("[main] cycle complete")


if __name__ == "__main__":
    main()
