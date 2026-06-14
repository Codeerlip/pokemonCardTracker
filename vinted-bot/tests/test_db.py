import pytest
from pathlib import Path
import db


@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "test.db")


def test_not_seen_initially():
    assert db.is_seen("listing-123") is False


def test_mark_and_check_seen():
    db.mark_seen("listing-456")
    assert db.is_seen("listing-456") is True


def test_mark_seen_idempotent():
    db.mark_seen("listing-789")
    db.mark_seen("listing-789")
    assert db.is_seen("listing-789") is True


def test_different_ids_independent():
    db.mark_seen("listing-aaa")
    assert db.is_seen("listing-bbb") is False
