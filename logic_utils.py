def get_range_for_difficulty(difficulty: str):
    # Fix: define ranges so Hard >= Normal >= Easy.
    # Collaboration: Copilot suggested range options; I chose these and verified with tests.
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 50


def parse_guess(raw: str):
    # Fix: robust parsing (empty, floats, invalid input).
    # Collaboration: Copilot gave parsing ideas; I implemented and added tests to confirm edge cases.
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    s = str(raw).strip()
    try:
        if "." in s:
            value = int(float(s))
        else:
            value = int(s)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    # Fix: always compare numeric values and return a simple outcome string (matches tests).
    # Collaboration: I extracted this pure logic from the UI with Copilot's help and validated the contract with pytest.
    try:
        g = int(guess)
        s = int(secret)
    except Exception:
        return "Too Low"

    if g == s:
        return "Win"
    if g > s:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    # Fix: deterministic scoring — win awards points (floor 10), wrong guesses apply a small penalty.
    # Collaboration: Copilot suggested score formulas; I adjusted values and confirmed behavior with unit tests.
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    return current_score - 5
