import base64
import pytest
import image_check


def _make_client_mock(mocker, answer_text: str):
    """Return a mock anthropic.Anthropic client whose messages.create returns answer_text."""
    mock_content = mocker.MagicMock()
    mock_content.text = answer_text

    mock_message = mocker.MagicMock()
    mock_message.content = [mock_content]

    mock_messages = mocker.MagicMock()
    mock_messages.create.return_value = mock_message

    mock_client = mocker.MagicMock()
    mock_client.messages = mock_messages
    return mock_client


def _stub_image_fetch(mocker):
    """Stub requests.Session.get to return a tiny valid JPEG response."""
    fake_bytes = b"\xff\xd8\xff\xe0" + b"\x00" * 16  # minimal JPEG header bytes
    mock_resp = mocker.MagicMock()
    mock_resp.content = fake_bytes
    mock_resp.headers = {"Content-Type": "image/jpeg"}
    mock_resp.raise_for_status.return_value = None
    return mock_resp


# T-019
def test_check_card_is_english_returns_true_for_english(mocker):
    mocker.patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"})

    mock_resp = _stub_image_fetch(mocker)
    mock_session = mocker.MagicMock()
    mock_session.get.return_value = mock_resp

    mock_client = _make_client_mock(mocker, "YES")
    mocker.patch("anthropic.Anthropic", return_value=mock_client)

    result = image_check.check_card_is_english("https://example.com/card.jpg", mock_session)
    assert result is True


# T-020
def test_check_card_is_english_returns_false_for_non_english(mocker):
    mocker.patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"})

    mock_resp = _stub_image_fetch(mocker)
    mock_session = mocker.MagicMock()
    mock_session.get.return_value = mock_resp

    mock_client = _make_client_mock(mocker, "NO")
    mocker.patch("anthropic.Anthropic", return_value=mock_client)

    result = image_check.check_card_is_english("https://example.com/card.jpg", mock_session)
    assert result is False


# T-021
def test_check_card_is_english_fail_open_on_fetch_error(mocker):
    mocker.patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"})

    mock_session = mocker.MagicMock()
    mock_session.get.side_effect = ConnectionError("network down")

    result = image_check.check_card_is_english("https://example.com/card.jpg", mock_session)
    assert result is True


# T-022
def test_check_card_is_english_fail_open_when_no_api_key(mocker):
    mocker.patch.dict("os.environ", {}, clear=True)
    # Ensure ANTHROPIC_API_KEY is absent
    import os
    os.environ.pop("ANTHROPIC_API_KEY", None)

    result = image_check.check_card_is_english("https://example.com/card.jpg")
    assert result is True
