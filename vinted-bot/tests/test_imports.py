import db
import vinted
import filters
import notifier


def test_all_modules_importable():
    assert db is not None
    assert vinted is not None
    assert filters is not None
    assert notifier is not None
