💭 Reflection: Game Glitch Investigator
Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

1. What was broken when you started?
What did the game look like the first time you ran it?
List at least two concrete bugs you noticed at the start
(for example: "the secret number kept changing" or "the hints were backwards").

- Difficulty inconsistancy beween normal and hard. Normal is makes you guess from 1 to 100 which is harder than hard.
- The hint mechanism is reversed 
- Game message still show after pressing new game (and then game crashes, doesn't let me submit a new guess after resetting)
- Minuses score every guess (I don't know if this is a feature or a bug)
- Game difficulty remained at medium (guessing 1 to 100) despite changing difficulty
- Starting game guesses decreased by one
- Negative attempts left


2. How did you use AI as a teammate?
Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).


I used Copilot for this activity. 
Here is an example of a useful debug from copilot:

Here are some of the issues that I have found.

Difficulty inconsistancy beween normal and hard. Normal is makes you guess from 1 to 100 which is harder than hard.
The hint mechanism is reversed
Game message still show after pressing new game (and then game crashes, doesn't let me submit a new guess after resetting)
Minuses score every guess (I don't know if this is a feature or a bug)
Game difficulty remained at medium (guessing 1 to 100) despite changing difficulty
Starting game guesses decreased by one
Negative attempts left
Could you suggest some potential cause?


Difficulty range wrong: In app.py get_range_for_difficulty maps "Normal" to 1–100 and "Hard" to 1–50. Cause: inverted/incorrect range mapping. Fix: assign ranges so Hard ≥ Normal ≥ Easy (and use the same ranges when starting a new game).

Hints reversed: The hint text is swapped where comparisons happen (e.g., when guess > secret the message says “Go HIGHER”). Fix: make messages match the comparison (if guess > secret → “Go LOWER”).

Type-mixing breaks comparisons: The code converts the secret to str on some attempts (secret = str(...)), then check_guess has a TypeError path that compares strings vs ints lexicographically. Cause: inconsistent secret/guess types. Fix: keep secret as an int always and compare numeric values only.

Secret appears to change / commitment issues: Streamlit reruns recreate values unless stored in st.session_state. The app partly uses st.session_state.secret but also reassigns secret locally and sometimes recreates it on new_game with a hard-coded 1–100 range. Cause: inconsistent initialization and recreating secret with wrong range. Fix: set st.session_state.secret once (or when starting new game) using the current difficulty’s range and do not overwrite it elsewhere.

New game leaves stale state / blocks play: new_game handler resets attempts and secret but does not reset st.session_state.status (still "won"/"lost"), so the UI shows end-of-game messages and st.stop() prevents further plays. Fix: reset status to "playing" (and reset history, score, attempts) when starting a new game.

Off-by-one attempts / negative attempts left: The app initializes attempts to 1 (should start at 0) and computes attempts left as attempt_limit - attempts, causing display and boundary errors. Fix: initialize attempts = 0, increment on submit, and use clear >= checks for failing the game.

Scoring looks like a bug (negative on every guess): update_score intentionally subtracts or adds based on outcome and parity; code subtracts for "Too Low" and sometimes subtracts for "Too High". Cause: scoring rules are unusual (or inverted). Fix: decide desired scoring policy and simplify (e.g., award points only on win, small penalty per wrong guess), then implement deterministically.

Tests vs UI API mismatch: Tests expect check_guess to return a single outcome string, but UI logic uses (outcome, message) pairs. Cause: inconsistent function contract between logic_utils.py and app.py. Fix: move pure logic (range, parse, check returning outcome string) into logic_utils.py, and have app.py map outcomes → messages for display.



Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
3. Debugging and testing your fixes
How did you decide whether a bug was really fixed?
Describe at least one test you ran (manual or using pytest)
and what it showed you about your code.
Did AI help you design or understand any tests? How?
4. What did you learn about Streamlit and state?
In your own words, explain why the secret number kept changing in the original app.
How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
What change did you make that finally gave the game a stable secret number?
5. Looking ahead: your developer habits
What is one habit or strategy from this project that you want to reuse in future labs or projects?
This could be a testing habit, a prompting strategy, or a way you used Git.
What is one thing you would do differently next time you work with AI on a coding task?
In one or two sentences, describe how this project changed the way you think about AI generated code.


