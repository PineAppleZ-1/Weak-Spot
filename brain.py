# brain.py - the "invisible AI" part of the game
# It watches how you type, works out which letters you struggle with,
# and picks words that make you practise them. It saves to a file so it
# remembers you next time.

import json
import os
import random

LETTERS = "abcdefghijklmnopqrstuvwxyz"
SAVE_FILE = "profile.json"


class TypingBrain:
    def __init__(self):
        self.reset()
        self.load()

    def reset(self):
        # for every letter: how many times you got it right, got it wrong,
        # and how long it took you (so we can work out the average)
        self.stats = {}
        for letter in LETTERS:
            self.stats[letter] = {"hits": 0, "misses": 0, "time": 0.0, "timed": 0}

    # ---------- learning ----------
    def record_hit(self, letter, seconds=None):
        self.stats[letter]["hits"] += 1
        if seconds is not None:
            self.stats[letter]["time"] += seconds
            self.stats[letter]["timed"] += 1

    def record_miss(self, letter):
        self.stats[letter]["misses"] += 1

    def total_keys(self):
        return sum(s["hits"] + s["misses"] for s in self.stats.values())

    def average_time(self):
        total_time = sum(s["time"] for s in self.stats.values())
        total_timed = sum(s["timed"] for s in self.stats.values())
        if total_timed == 0:
            return 0.3
        return total_time / total_timed

    def weakness(self, letter):
        # 0 = fine. Higher = you miss it a lot or you're slow on it.
        s = self.stats[letter]
        tries = s["hits"] + s["misses"]
        if tries < 3:
            return 0  # not enough data yet
        miss_rate = s["misses"] / tries
        slowness = 0
        if s["timed"] > 0:
            letter_time = s["time"] / s["timed"]
            slowness = max(0, letter_time / self.average_time() - 1)
        return miss_rate * 3 + slowness

    def weakest_letters(self, count=5):
        letters = sorted(LETTERS, key=self.weakness, reverse=True)
        return [l for l in letters[:count] if self.weakness(l) > 0.4]

    def reason(self, letter):
        s = self.stats[letter]
        tries = s["hits"] + s["misses"]
        miss_rate = s["misses"] / tries if tries else 0
        if miss_rate > 0.1:
            return f"missed {miss_rate * 100:.0f}%"
        return "slow"

    # ---------- choosing words ----------
    def pick_word(self, words, ai_on=True):
        """Returns (word, letters it is training)."""
        # random word if AI is off, if we don't know you yet,
        # or 25% of the time so it keeps learning about every letter
        if not ai_on or self.total_keys() < 30 or random.random() < 0.25:
            return random.choice(words), []

        weak = {letter: self.weakness(letter) for letter in LETTERS}
        weights = []
        for word in words:
            weights.append(1 + 10 * sum(weak[c] for c in set(word)))
        word = random.choices(words, weights=weights)[0]
        targets = [c for c in set(word) if weak[c] > 0.5]
        return word, targets

    # ---------- saving ----------
    def save(self):
        with open(SAVE_FILE, "w") as f:
            json.dump(self.stats, f)

    def load(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE) as f:
                    saved = json.load(f)
                for letter in LETTERS:
                    if letter in saved:
                        self.stats[letter] = saved[letter]
            except (ValueError, KeyError):
                self.reset()
