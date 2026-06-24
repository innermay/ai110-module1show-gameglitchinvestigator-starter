"""Pytest tests for the repaired pure game-logic functions.

These import from app.py, where the working logic currently lives.
(logic_utils.py still holds NotImplementedError stubs; once the functions
are refactored there, switch the import below to `from logic_utils import ...`.)

We test only the pure functions here, not the Streamlit UI.
"""

from app import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)


# 1. Each difficulty returns the correct (low, high) range.
def test_easy_range():
    assert get_range_for_difficulty("Easy") == (1, 20)


def test_normal_range():
    assert get_range_for_difficulty("Normal") == (1, 100)


def test_hard_range():
    assert get_range_for_difficulty("Hard") == (1, 50)


# 2. Valid number input parses correctly.
def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_decimal_input_truncates_to_int():
    ok, value, err = parse_guess("42.9")
    assert ok is True
    assert value == 42
    assert err is None


# 3. Invalid input returns an error instead of crashing.
def test_parse_non_numeric_returns_error():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


def test_parse_empty_input_returns_error():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."


# 4. A guess above the secret is "Too High" and tells the player to go LOWER.
def test_guess_too_high_says_go_lower():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message.upper()


# 5. A guess below the secret is "Too Low" and tells the player to go HIGHER.
def test_guess_too_low_says_go_higher():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message.upper()


# 6. A correct guess returns "Win".
def test_correct_guess_wins():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


# 7. Wrong guesses subtract points instead of adding them.
def test_too_high_subtracts_points_on_even_attempt():
    # Even attempt number used to (wrongly) ADD points; it must now subtract.
    assert update_score(100, "Too High", 2) == 95


def test_too_high_subtracts_points_on_odd_attempt():
    assert update_score(100, "Too High", 1) == 95


def test_too_low_subtracts_points():
    assert update_score(100, "Too Low", 2) == 95


def test_too_high_and_too_low_penalize_equally():
    score = 100
    assert update_score(score, "Too High", 2) == update_score(score, "Too Low", 2)


def test_win_adds_points():
    assert update_score(0, "Win", 1) > 0
