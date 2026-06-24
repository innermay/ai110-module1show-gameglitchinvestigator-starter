# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

During the glitch hunt, I found several bugs in the game logic:
The hint messages were backwards. A guess that was too high told the player to go higher, and a guess that was too low told the player to go lower.
The attempt counter started at 1 instead of 0, so the player lost an attempt before making a first guess.
The game sometimes converted the secret number into a string on even attempts, which caused wrong comparisons and could stop a correct guess from winning.
The New Game button ignored the selected difficulty range and could choose a secret from 1 to 100 even on Easy mode.
The score logic rewarded a wrong “Too High” guess on even attempts instead of subtracting points.
I repaired these bugs one at a time, tested each fix manually, and then added pytest tests to verify the core game logic.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Start the app using python -m streamlit run app.py.
2. Choose a difficulty from the sidebar, such as Easy, Normal, or Hard.
3. Open the Developer Debug Info section to view the secret number while testing.
4. Enter a guess lower than the secret number and confirm the game says to go higher.
5. Enter a guess higher than the secret number and confirm the game says to go lower.
6. Enter the correct secret number and confirm the game shows the win message.
7. Click New Game and confirm the new secret number stays inside the selected difficulty range.
8. Run the pytest tests to show that the repaired game logic passes automatically.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================
```

...............                                                          [100%]
python3 -m pytest tests/ -q

15 passed in 0.30s


## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
