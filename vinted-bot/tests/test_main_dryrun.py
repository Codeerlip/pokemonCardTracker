def test_dry_run_suppresses_discord(mocker):
    """--dry-run runs one pass without calling notifier.send."""
    import main

    mocker.patch("vinted.search_multi", return_value=[])
    mocker.patch("time.sleep")

    cfg = {
        "cards": [{"name": "Test", "search_queries": ["Test delta"], "max_price": 10.0}],
        "discord_webhook_url": "https://discord.com/api/webhooks/test",
    }
    mocker.patch("main.load_config", return_value=cfg)
    mocker.patch("sys.argv", ["main.py", "--dry-run"])
    debrief_mock = mocker.patch("notifier.send_debrief")

    main.main()

    debrief_mock.assert_not_called()
