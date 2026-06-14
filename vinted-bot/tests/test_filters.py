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


def test_check_price_within_limit():
    assert filters.check_price(12.50, 25.00) is True


def test_check_price_at_limit():
    assert filters.check_price(25.00, 25.00) is True


def test_check_price_exceeds_limit():
    assert filters.check_price(25.01, 25.00) is False


def test_check_price_none_max_always_passes():
    assert filters.check_price(9999.00, None) is True
