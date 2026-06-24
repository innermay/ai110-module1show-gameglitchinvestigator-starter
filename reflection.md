# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
When I first ran the game, it looked like a number guessing game, I noticed that some of the game logic was broken. The biggest issue was that the hint messages were backwards: when the guess was too high, the game told the player to go higher, and when the guess was too low, it told the player to go lower. I also noticed that the attempts started at 1 instead of 0, so the game already showed fewer attempts before I even guessed. Another issue was that starting a new game could choose a secret number from 1 to 100 even if the selected difficulty showed a smaller range, such as Easy or Hard.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
- The hint messages were backwards. When the guess was too high, the game displayed “Go HIGHER!” instead of telling the player to go lower. When the guess was too low, it displayed “Go LOWER!” instead of telling the player to go higher.

- The attempt counter started at 1 instead of 0. This made the game show fewer attempts left before the player even made the first guess.

- The New Game button did not respect the selected difficulty range. For example, Easy mode says the range is 1 to 20, but starting a new game could still choose a secret number from 1 to 100.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess higher than the secret number, such as guessing `60` when the secret is lower | The game should say the guess is too high and tell the player to go lower. | The game labels the outcome as too high but displays the message “Go HIGHER!”, which is the opposite of what the player should do. | none |
| Guess lower than the secret number, such as guessing `10` when the secret is higher | The game should say the guess is too low and tell the player to go higher. | The game labels the outcome as too low but displays the message “Go LOWER!”, which is the opposite of what the player should do. | none |
| Start a new game while using Easy difficulty | The new secret number should stay inside the Easy range of 1 to 20. | The New Game button can create a secret number from 1 to 100, even though the Easy range says 1 to 20. | none |
| Open the game on Normal difficulty before making any guess | The game should start with 8 attempts left before the first guess. | The game starts attempts at 1, so it shows only 7 attempts left before the player guesses. | none |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
Claude
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

One AI suggestion that was correct was the explanation of the backwards hint bug. The AI explained that the `check_guess()` function had the correct outcome labels, such as “Too High” and “Too Low,” but the messages were swapped. For example, when the guess was greater than the secret number, the game said “Go HIGHER!” even though the correct advice should be “Go LOWER!” I verified this by checking the `check_guess()` function in `app.py` and testing the game with guesses above and below the secret number.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

**Fix note: the string-conversion bug (even-numbered attempts)**

1. *What the bug was:* On every even-numbered attempt, the game converted the secret number into a string before comparing it to the guess (`secret = str(st.session_state.secret)`). This meant that on roughly half of all turns, the hints and the win check did not work correctly.

2. *Why converting to a string caused wrong comparisons:* The guess was still an integer, so comparing an integer to a string broke the comparison in two ways. First, `guess == secret` could never be true (an int never equals a string), so a correct guess on an even turn would not register as a win. Second, `guess > secret` raised a `TypeError`, which sent the code into a fallback branch that compared the two values as strings. String comparison is alphabetical, not numeric, so `"9" > "50"` is `True` even though 9 is smaller than 50. That produced backwards hints on even turns.

3. *How I fixed it:* I removed the even-attempt conversion and replaced the whole if/else block with a single line, `secret = st.session_state.secret`, so the secret always stays an integer and `check_guess()` always uses the numeric comparison path. I did not change any other code.

4. *How I manually tested it:* I ran the app with `streamlit run app.py` and used the Developer Debug Info panel to see the secret. With a secret of 50, I guessed `9` on my second (even) attempt: before the fix it said "Go LOWER!", and after the fix it correctly said "Go HIGHER!". I also guessed the exact secret on an even attempt and confirmed the win now registers (balloons and the "You won!" message), which it did not do before.

**Fix note: the attempt counter starting at 1**

1. *What the bug was:* The game initialized `attempts` to 1 when the app first loaded, but the New Game button reset it to 0. The two starting points disagreed, so the first game began one turn ahead of every game started afterward.

2. *Why it caused a problem:* The "Attempts left" message is calculated as `attempt_limit - attempts`. Because the counter started at 1 instead of 0, a fresh load on Normal difficulty showed "Attempts left: 7" before the player had guessed at all, when it should have shown 8.

3. *How I fixed it:* I changed the initial value from 1 to 0 so it matches the New Game reset and the real meaning of the counter (guesses made so far). I did not change the increment logic or the display formula.

4. *How I manually tested it:* I started the app fresh on Normal difficulty and confirmed the info box showed "Attempts left: 8" with Debug Info showing Attempts: 0. I clicked New Game and confirmed it showed the same number, then made one guess and confirmed "Attempts left" dropped to 7 and Attempts read 1.

**Fix note: New Game ignored the difficulty range**

1. *What the bug was:* Each difficulty has its own number range (Easy is 1–20, Hard is 1–50), and the first secret of the game respected it. But the New Game button always generated a secret between 1 and 100, ignoring the selected difficulty.

2. *Why it caused a problem:* The sidebar advertised a range like "Range: 1 to 20" on Easy, but after clicking New Game the actual secret could be far outside that range, making the game unwinnable within the stated bounds and contradicting what the player was told.

3. *How I fixed it:* The New Game button used a hardcoded `random.randint(1, 100)`. I changed it to `random.randint(low, high)` so it reuses the same range values the rest of the app already computes from the difficulty. I did not change other code.

4. *How I manually tested it:* I selected Easy difficulty (range 1–20), clicked New Game several times, and used the Developer Debug Info panel to confirm the secret always stayed between 1 and 20. I repeated this on Hard (1–50) and confirmed the secret never went above 50.

**Fix note: score logic rewarded a wrong "Too High" guess**

1. *What the bug was:* When a guess was too high, the score went UP by 5 points on even-numbered attempts and only down by 5 on odd attempts. A guess that was too low always lost 5 points. So being wrong sometimes increased the score.

2. *Why it caused a problem:* Both "too high" and "too low" are equally wrong, so they should cost the same. The "Too High" branch had an extra `if attempt_number % 2 == 0` check that added points on even turns, making the score inconsistent and even exploitable (a player could farm points by guessing too high on even turns).

3. *How I fixed it:* I removed the attempt-parity special case so the "Too High" branch always returns `current_score - 5`, exactly matching the "Too Low" branch. I did not change the Win scoring or any other code.

4. *How I manually tested it:* I watched the Score in the Developer Debug Info panel. I guessed too high on an even-numbered attempt: before the fix the score increased by 5, and after the fix it decreased by 5, the same as a too-low guess. I also confirmed correct guesses still award points.

**Automated testing with pytest**

After fixing the bugs by hand, I wrote pytest tests in `tests/test_game_logic.py` for the four pure logic functions (`get_range_for_difficulty`, `parse_guess`, `check_guess`, and `update_score`), so I would not have to re-test everything manually each time. There are 15 tests covering the difficulty ranges, valid and invalid input parsing, the "Too High"/"Too Low"/"Win" outcomes and their hint messages, and the rule that wrong guesses must subtract points. Running `python3 -m pytest tests/ -q` showed all 15 passing, which confirmed my fixes hold and gave me a safety net against breaking them later. One test in particular, `test_too_high_subtracts_points_on_even_attempt`, would have failed (105 instead of 95) against the old scoring code, so it directly locks in the score-logic fix.

AI helped me design the tests by reminding me that `check_guess` returns a `(outcome, message)` tuple rather than a single string, which is why the original starter tests were written incorrectly and would have failed even against correct code. It also pointed out that the logic functions currently live in `app.py` (not in `logic_utils.py`, which is still stubbed), so the tests import from `app` for now.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit reruns the script from top to bottom whenever the user interacts with something, like clicking a button or submitting input. This means normal variables can reset unless they are stored somewhere that survives reruns. `st.session_state` is Streamlit’s way of remembering values between reruns, like the secret number, score, attempts, status, and guess history. I would explain it to a friend like this: Streamlit keeps rebuilding the page, and session state is the backpack where the app keeps the important things it should not forget.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One strategy I want to reuse in future projects is fixing one bug at a time and testing it before moving to the next one. This made the debugging process less overwhelming because I could focus on one specific problem, prove it was fixed, and then commit that change. I also want to keep using bug reproduction logs because they forced me to explain the expected behavior and the actual behavior clearly.

Next time I work with AI on a coding task, I would ask it to explain the bug before asking it to change the code. In this project, the best AI help came from explanations that pointed to the exact function and reason for the bug. This project changed the way I think about AI-generated code because I saw that AI can produce code that looks correct but still has hidden logic problems. I learned that I should treat AI code as a draft that needs testing, review, and human judgment.
