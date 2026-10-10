# Weak Spot

A typing game that learns which letters you struggle with and quietly gives you more words with those letters.

## How to run

```
pip install pygame
python game.py
```

## Controls

- Type to shoot words. The first letter locks onto a word.
- Backspace switches to a different word.
- F1 shows what the AI has learned.
- Esc goes back to the menu.
- On the menu, A turns the AI on or off and R resets it.

## How the AI works (brain.py)

1. Every key you press is recorded: right or wrong, and how long it took.
2. Each letter gets a weakness score: `miss rate × 3 + how much slower it is than your average`.
3. When a new word spawns, words with your weak letters are more likely to be picked. 25% of words are still random, so it keeps learning about every letter.
4. Everything is saved to `profile.json`, so it remembers you next time.

We used simple statistics instead of a neural network because it learns from just a few keystrokes, updates instantly, and we can explain every decision it makes.

## Files

- `game.py` is the game: screens, falling words, typing.
- `brain.py` is the AI.
- `words.py` is the word list.
