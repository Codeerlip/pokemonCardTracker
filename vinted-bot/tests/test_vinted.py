import pytest
import vinted


MOCK_RESPONSE = {
    "items": [
        {
            "id": 99,
            "title": "Rayquaza Delta Species ex",
            "price": {"amount": "12.50", "currency_code": "EUR"},
            "status": "good",
            "description": "nice card",
            "url": "https://www.vinted.nl/items/99",
        }
    ]
}


def test_search_multi_returns_parsed_listings(mocker):
    mocker.patch.object(vinted, "_get_with_backoff", return_value=MOCK_RESPONSE)
    mocker.patch("vinted._init_session")
    mocker.patch("time.sleep")
    results = vinted.search_multi(["Rayquaza Delta Species ex"])
    assert len(results) == 1
    listing = results[0]
    assert listing["id"] == "99"
    assert listing["price"] == 12.50
    assert listing["condition"] == "good"
    assert listing["currency"] == "EUR"


def test_search_multi_deduplicates_across_queries(mocker):
    mocker.patch.object(vinted, "_get_with_backoff", return_value=MOCK_RESPONSE)
    mocker.patch("vinted._init_session")
    mocker.patch("time.sleep")
    results = vinted.search_multi(["Rayquaza ex delta", "Rayquaza 22/97"])
    assert len(results) == 1


def test_search_multi_empty_response(mocker):
    mocker.patch.object(vinted, "_get_with_backoff", return_value={"items": []})
    mocker.patch("vinted._init_session")
    mocker.patch("time.sleep")
    results = vinted.search_multi(["NonexistentCard"])
    assert results == []


def test_parse_handles_missing_fields():
    listing = vinted._parse({})
    assert listing["id"] == ""
    assert listing["price"] == 0.0
    assert listing["currency"] == "EUR"


def test_fetch_description_returns_description(mocker):
    mock_resp = mocker.MagicMock()
    mock_resp.json.return_value = {"item": {"description": "stamped in italiano"}}
    mocker.patch.object(vinted._session, "get", return_value=mock_resp)
    mocker.patch("vinted._init_session")
    result = vinted.fetch_description("12345")
    assert result == "stamped in italiano"


def test_fetch_description_fail_open_on_error(mocker):
    import requests as req
    mocker.patch.object(vinted._session, "get", side_effect=req.RequestException("timeout"))
    mocker.patch("vinted._init_session")
    result = vinted.fetch_description("12345")
    assert result == ""


def test_fetch_description_fail_open_on_missing_field(mocker):
    mock_resp = mocker.MagicMock()
    mock_resp.json.return_value = {}
    mocker.patch.object(vinted._session, "get", return_value=mock_resp)
    mocker.patch("vinted._init_session")
    result = vinted.fetch_description("12345")
    assert result == ""
