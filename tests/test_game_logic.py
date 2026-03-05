import pytest
from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)


def test_get_range_for_difficulty():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 50)
    assert get_range_for_difficulty("Hard") == (1, 100)
    assert get_range_for_difficulty("Unknown") == (1, 50)


def test_parse_guess_valid_int_and_float():
    ok, val, err = parse_guess("42")
    assert ok and val == 42 and err is None

    ok, val, err = parse_guess("3.0")
    assert ok and val == 3 and err is None


def test_parse_guess_empty_and_invalid():
    ok, val, err = parse_guess("")
    assert not ok and err == "Enter a guess."

    ok, val, err = parse_guess(None)
    assert not ok and err == "Enter a guess."

    ok, val, err = parse_guess("abc")
    assert not ok and err == "That is not a number."


def test_check_guess_outcomes():
    assert check_guess(50, 50) == "Win"
    assert check_guess(60, 50) == "Too High"
    assert check_guess(40, 50) == "Too Low"


def test_update_score_win_and_floor():
    assert update_score(0, "Win", 1) == 100
    assert update_score(0, "Win", 2) == 90
    assert update_score(0, "Win", 20) == 10


def test_update_score_wrong_guess_penalty():
    assert update_score(10, "Too Low", 1) == 5
    assert update_score(10, "Too High", 3) == 5
