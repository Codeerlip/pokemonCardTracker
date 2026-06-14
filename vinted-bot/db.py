import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "seen_listings.db"


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS seen_listings "
        "(id TEXT PRIMARY KEY, seen_at TEXT DEFAULT (datetime('now')))"
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
