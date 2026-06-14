import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "seen_listings.db"


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS seen_listings "
        "(id TEXT PRIMARY KEY, seen_at TEXT DEFAULT (datetime('now')))"
    )
    conn.execute(
        "CREATE TABLE IF NOT EXISTS card_sightings "
        "(card_name TEXT PRIMARY KEY, total_seen INTEGER NOT NULL DEFAULT 0, "
        "runs_checked INTEGER NOT NULL DEFAULT 0)"
    )
    conn.commit()
    return conn


def is_seen(listing_id: str) -> bool:
    with _connect() as conn:
        row = conn.execute(
            "SELECT 1 FROM seen_listings WHERE id = ?", (listing_id,)
        ).fetchone()
    return row is not None


def mark_seen(listing_id: str) -> None:
    with _connect() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO seen_listings (id) VALUES (?)", (listing_id,)
        )
        conn.commit()


def record_sightings(card_name: str, count: int) -> None:
    with _connect() as conn:
        conn.execute(
            "INSERT INTO card_sightings (card_name, total_seen, runs_checked) VALUES (?, ?, 1) "
            "ON CONFLICT(card_name) DO UPDATE SET "
            "total_seen = total_seen + excluded.total_seen, "
            "runs_checked = runs_checked + 1",
            (card_name, count),
        )
        conn.commit()


def get_all_sightings() -> dict:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT card_name, total_seen, runs_checked FROM card_sightings"
        ).fetchall()
    return {row[0]: {"total_seen": row[1], "runs_checked": row[2]} for row in rows}
