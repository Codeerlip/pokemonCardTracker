import notifier

LISTING = {
    "title": "Rayquaza δ Delta Species 13/113",
    "price": 12.50,
    "condition": "Heel goed",
    "url": "https://www.vinted.nl/items/99",
}

WEBHOOK = "https://discord.com/api/webhooks/123/abc"


def test_send_posts_to_discord_webhook(mocker):
    mock_post = mocker.patch("notifier.requests.post")
    mock_post.return_value.raise_for_status = lambda: None

    notifier.send(LISTING, "Rayquaza δ", "EX Delta Species", "english", WEBHOOK)

    mock_post.assert_called_once()
    call_kwargs = mock_post.call_args
    assert call_kwargs.args[0] == WEBHOOK
    payload = call_kwargs.kwargs["json"]
    assert "embeds" in payload
    assert len(payload["embeds"]) == 1


def test_send_embed_contains_card_name(mocker):
    mock_post = mocker.patch("notifier.requests.post")
    mock_post.return_value.raise_for_status = lambda: None

    notifier.send(LISTING, "Rayquaza δ", "EX Delta Species", "english", WEBHOOK)

    embed = mock_post.call_args.kwargs["json"]["embeds"][0]
    assert "Rayquaza" in embed["title"]


def test_send_embed_contains_price(mocker):
    mock_post = mocker.patch("notifier.requests.post")
    mock_post.return_value.raise_for_status = lambda: None

    notifier.send(LISTING, "Rayquaza δ", "EX Delta Species", "english", WEBHOOK)

    embed = mock_post.call_args.kwargs["json"]["embeds"][0]
    field_values = [f["value"] for f in embed["fields"]]
    assert any("12.50" in v for v in field_values)


def test_send_embed_links_to_vinted(mocker):
    mock_post = mocker.patch("notifier.requests.post")
    mock_post.return_value.raise_for_status = lambda: None

    notifier.send(LISTING, "Rayquaza δ", "EX Delta Species", "english", WEBHOOK)

    embed = mock_post.call_args.kwargs["json"]["embeds"][0]
    assert "vinted.nl" in embed["url"]
