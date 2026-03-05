💭 Reflection: Game Glitch Investigator
Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

1. What was broken when you started?
When I first ran the app the secret number kept changing and hints were often the opposite of what they should be. Difficulty ranges were inconsistent ("Normal" used a larger range than "Hard"), and attempts were off-by-one which led to negative "attempts left" values. Starting a new game sometimes left the UI in a terminal state because `status` wasn't reset, so the user couldn't submit new guesses. Scoring felt wrong — points were deducted in confusing ways — and the code mixed types (sometimes converting the secret to a string) which broke comparisons.

2. How did you use AI as a teammate?
I used Copilot as a coding assistant to suggest refactors and small fixes while I explored the code. One correct suggestion was to use `st.session_state` to persist the secret across reruns — I implemented that and the secret stopped changing unexpectedly. One misleading suggestion was an earlier helper that coerced the secret to a string on alternating attempts; that turned out to be the source of type-comparison bugs so I reverted that behavior and kept numeric comparisons only.

3. Debugging and testing your fixes
I decided a bug was fixed when the unit tests for logic functions passed and the manual Streamlit flow behaved correctly (winnable, truthful hints, stable secret). I added pytest cases for `get_range_for_difficulty`, `parse_guess`, `check_guess`, and `update_score` — for example `test_check_guess_outcomes` asserts that 60 vs 50 is "Too High" and 40 vs 50 is "Too Low". Writing those tests made the contract explicit and prevented regressions; the tests exercise pure logic in `logic_utils.py` so they run fast and isolate behavior from the UI. AI helped suggest parsing edge-cases (floats, empty input) which I included in the tests.

4. What did you learn about Streamlit and state?
The secret number kept changing because Streamlit re-runs the script on every interaction and the original code recreated or mutated the secret outside of persistent session state. Streamlit reruns work by re-executing the script from top to bottom on each event; `st.session_state` is the mechanism to store values across reruns so they remain stable. The fix was to initialize `st.session_state.secret` only when it doesn't exist (or when the user explicitly starts a new game) and to avoid creating local shadows or string coercions of that value. After moving pure logic into `logic_utils.py` and relying on `st.session_state` for the secret and `status`, the game became stable and predictable.

5. Looking ahead: your developer habits
One habit I'll keep is extracting pure logic into testable modules and writing small pytest cases before or alongside UI fixes; it made debugging much faster. Next time I’ll ask for smaller, focused code suggestions from AI and validate each change with a unit test immediately, rather than applying a large block of AI-generated code without tests. This project reinforced that AI-generated code can be a great starting point, but it requires careful reading, tests, and incremental fixes to reach reliable behavior.

Files touched: `app.py`, `logic_utils.py`, and new tests under `tests/` (see `tests/test_game_logic.py`).
