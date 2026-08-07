import notifier

LISTING = {
    "title": "Rayquaza δ Delta Species 13/113",
    "price": 12.50,
    "condition": "Heel goed",
    "url": "https://www.vinted.nl/items/99",
    "thumbnail": "",
}

MATCH = {"card_name": "Rayquaza δ", "card_set": "EX Delta Species", "listing": LISTING}
WEBHOOK = "https://discord.com/api/webhooks/123/abc"


def test_debrief_posts_to_discord_webhook(mocker):
    mock_post = mocker.patch("notifier.requests.post")
    mock_post.return_value.raise_for_status = lambda: None

    notifier.send_debrief([MATCH], WEBHOOK)

    mock_post.assert_called_once()
    assert mock_post.call_args.args[0] == WEBHOOK
    assert "embeds" in mock_post.call_args.kwargs["json"]


def test_debrief_embed_contains_card_name(mocker):
    mock_post = mocker.patch("notifier.requests.post")
    mock_post.return_value.raise_for_status = lambda: None

    notifier.send_debrief([MATCH], WEBHOOK)

    embeds = mock_post.call_args.kwargs["json"]["embeds"]
    titles = " ".join(e.get("title", "") for e in embeds)
    assert "Rayquaza" in titles


def test_debrief_embed_contains_price(mocker):
    mock_post = mocker.patch("notifier.requests.post")
    mock_post.return_value.raise_for_status = lambda: None

    notifier.send_debrief([MATCH], WEBHOOK)

    embeds = mock_post.call_args.kwargs["json"]["embeds"]
    all_field_values = [f["value"] for e in embeds for f in e.get("fields", [])]
    assert any("12.50" in v for v in all_field_values)


def test_debrief_embed_links_to_vinted(mocker):
    mock_post = mocker.patch("notifier.requests.post")
    mock_post.return_value.raise_for_status = lambda: None

    notifier.send_debrief([MATCH], WEBHOOK)

    embeds = mock_post.call_args.kwargs["json"]["embeds"]
    urls = [e.get("url", "") for e in embeds]
    assert any("vinted.nl" in u for u in urls)


# T-040
def test_debrief_large_batch_caps_summary_and_does_not_raise(mocker):
    mock_post = mocker.patch("notifier.requests.post")
    mock_post.return_value.raise_for_status = lambda: None

    matches = [MATCH] * 50
    notifier.send_debrief(matches, WEBHOOK)

    header = mock_post.call_args.kwargs["json"]["embeds"][0]
    summary_lines = header["description"].split("\n")
    assert len(summary_lines) == 10  # 9 matches + 1 overflow line
    assert "…and 41 more" in summary_lines[-1]


# T-041
def test_debrief_small_batch_summary_has_no_overflow_line(mocker):
    mock_post = mocker.patch("notifier.requests.post")
    mock_post.return_value.raise_for_status = lambda: None

    notifier.send_debrief([MATCH, MATCH], WEBHOOK)

    header = mock_post.call_args.kwargs["json"]["embeds"][0]
    summary_lines = header["description"].split("\n")
    assert len(summary_lines) == 2
    assert not any("more" in line for line in summary_lines)
