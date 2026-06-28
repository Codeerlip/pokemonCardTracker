import filters


def test_detect_language_dutch():
    assert filters.detect_language("nieuw kaart verzenden", "") == "dutch"


def test_detect_language_english():
    assert filters.detect_language("mint condition shipping", "") == "english"


def test_detect_language_unknown():
    result = filters.detect_language("Rayquaza Delta Species", "")
    assert result == "unknown"


def test_check_condition_allows_good():
    assert filters.check_condition("good") is True


def test_check_condition_allows_new():
    assert filters.check_condition("new") is True


def test_check_condition_allows_like_new():
    assert filters.check_condition("like_new") is True


def test_check_condition_rejects_satisfactory():
    assert filters.check_condition("satisfactory") is False


def test_check_condition_rejects_poor():
    assert filters.check_condition("poor") is False


def test_check_condition_dutch_goed():
    assert filters.check_condition("Goed") is True


def test_check_condition_dutch_heel_goed():
    assert filters.check_condition("Heel goed") is True


def test_check_condition_dutch_nieuw_met_prijskaartje():
    assert filters.check_condition("Nieuw met prijskaartje") is True


def test_check_condition_dutch_nieuw_zonder_prijskaartje():
    assert filters.check_condition("Nieuw zonder prijskaartje") is True


def test_check_condition_dutch_veelgebruikt_rejected():
    assert filters.check_condition("Veelgebruikt") is False


def test_check_title_relevance_match_via_set_number():
    assert filters.check_title_relevance("Rayquaza 13/113", "Rayquaza δ", "13/113") is True


def test_check_title_relevance_match_via_delta_keyword():
    assert filters.check_title_relevance("Rayquaza delta species holo", "Rayquaza δ", "13/113") is True


def test_check_title_relevance_no_name_match():
    assert filters.check_title_relevance("Umbreon ex 069/131", "Rayquaza δ", "13/113") is False


def test_check_title_relevance_wrong_set_number_and_no_keyword():
    assert filters.check_title_relevance("Rayquaza VMAX 102/159", "Rayquaza δ", "13/113") is False


def test_check_title_relevance_ds_abbreviation_via_set_number():
    assert filters.check_title_relevance("Rayquaza DS 13/113", "Rayquaza δ", "13/113") is True


def test_check_title_relevance_ex_card_requires_ex_in_title():
    # Salamence 14/113 (wrong card, no "ex") must not match Salamence ex δ 98/101
    assert filters.check_title_relevance("Salamence Delta Species 14/113", "Salamence ex δ", "98/101") is False


def test_check_title_relevance_ex_card_passes_with_ex():
    assert filters.check_title_relevance("Salamence ex Dragon Frontiers 98/101", "Salamence ex δ", "98/101") is True


def test_check_title_relevance_conflicting_set_number_rejected():
    # Rayquaza 26/110 listing must NOT match the 13/113 delta species card,
    # even when "delta" appears in the title.
    assert filters.check_title_relevance("Rayquaza 26/110 delta species", "Rayquaza δ", "13/113") is False


def test_check_title_relevance_conflicting_set_number_rejected_for_hp():
    # Same for Holon Phantoms 16/110 — a 26/110 listing must not match it.
    assert filters.check_title_relevance("Rayquaza 26/110 delta species", "Rayquaza δ", "16/110") is False


def test_check_title_relevance_no_set_number_in_title_passes_via_delta():
    # A listing with no set number but with "delta species" must still pass.
    assert filters.check_title_relevance("Rayquaza delta species holo", "Rayquaza δ", "13/113") is True


def test_check_title_relevance_single_set_number_no_delta_keyword_passes():
    # Single-component set numbers: bare number present in title is sufficient —
    # no delta keyword required (mirrors 2-part set number behaviour).
    # "Pikachu (EVO 35) Evoluties" now passes — both name and number are present.
    assert filters.check_title_relevance("Pikachu (EVO 35) Evoluties", "Pikachu δ", "35") is True


def test_check_title_relevance_single_set_number_black_star_promo_passes():
    # T-033: "Pikachu 035 – Black Star Nintendo Promo" must match the promo Pikachu
    # whose set_number is "35" — no delta keyword should be required.
    assert filters.check_title_relevance("Pikachu 035 – Black Star Nintendo Promo", "Pikachu δ", "35") is True


def test_check_title_relevance_single_set_number_passes_with_delta_keyword():
    # A listing that explicitly says "delta" must still match even with a
    # single-component set_number.
    assert filters.check_title_relevance("Pikachu delta promo 35", "Pikachu δ", "35") is True


def test_check_title_relevance_single_set_number_delta_without_number_rejected():
    # B-004: δ keyword present but "35" absent — must be rejected.
    assert filters.check_title_relevance("Pikachu δ Nintendo promo", "Pikachu δ", "35") is False


def test_check_title_relevance_single_set_number_both_number_and_delta_passes():
    # B-004: listing mentions both "35" and δ → passes.
    assert filters.check_title_relevance("Pikachu δ Nintendo promo 35", "Pikachu δ", "35") is True


def test_check_price_within_limit():
    assert filters.check_price(12.50, 25.00) is True


def test_check_price_at_limit():
    assert filters.check_price(25.00, 25.00) is True


def test_check_price_exceeds_limit():
    assert filters.check_price(25.01, 25.00) is False


def test_check_price_none_max_always_passes():
    assert filters.check_price(9999.00, None) is True


def test_check_recency_recent_passes():
    import time
    ts = int(time.time()) - 3600  # 1 hour ago
    assert filters.check_recency(ts, max_days=30) is True


def test_check_recency_old_fails():
    import time
    ts = int(time.time()) - (40 * 24 * 3600)  # 40 days ago
    assert filters.check_recency(ts, max_days=30) is False


def test_check_recency_none_ts_passes():
    # Vinted API no longer returns timestamps; unknown age must not block alerts
    assert filters.check_recency(None, max_days=30) is True


# T-025
def test_check_no_foreign_language_tag_rejects_ita():
    assert filters.check_no_foreign_language_tag("Rayquaza δ Specie Delta Holo 13/113 EX Delta Species ITA Rara Vintage") is False


# T-026
def test_check_no_foreign_language_tag_rejects_fr():
    assert filters.check_no_foreign_language_tag("Carte Pokémon Pikachu 35/108 XY Évolutions FR") is False


# T-027
def test_check_no_foreign_language_tag_rejects_francais():
    assert filters.check_no_foreign_language_tag("Rayquaza delta espèces delta holo français") is False


# T-028
def test_check_no_foreign_language_tag_passes_clean_title():
    assert filters.check_no_foreign_language_tag("Rayquaza delta species holo 13/113 EX Delta Species") is True


# T-029
def test_check_no_foreign_language_tag_passes_anglaise():
    # "anglaise" = French word for English — must not be blocked
    assert filters.check_no_foreign_language_tag("Eevee Delta spieces 68/113 anglaise en très bon état") is True


# T-030
def test_check_no_foreign_language_tag_rejects_italian_in_description():
    # B-006: clean title but description says "Language: Italian"
    assert filters.check_no_foreign_language_tag(
        "Pokémon - Latias 21/110 - Rare Non Holo",
        "Condition: Near Mint\nLanguage: Italian\nYear: 2006",
    ) is False


# T-031
def test_check_no_foreign_language_tag_rejects_french_in_description():
    assert filters.check_no_foreign_language_tag(
        "Rayquaza delta holo 13/113",
        "Language: French",
    ) is False


# T-032
def test_check_no_foreign_language_tag_passes_english_in_description():
    assert filters.check_no_foreign_language_tag(
        "Rayquaza delta holo 13/113",
        "Language: English\nCondition: Near Mint",
    ) is True
