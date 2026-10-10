# Weak Spot - a typing game that learns which letters you struggle with
# Run with: python game.py
#
# Controls:
#   type        - shoot words (first letter locks onto a word)
#   backspace   - switch to a different word
#   F1          - show what the AI has learned
#   esc         - quit to menu

import random
import sys
import time

import pygame

from brain import LETTERS, TypingBrain
from words import WORDS

# ---------------- settings ----------------
WIDTH = 1000
HEIGHT = 650
BOTTOM = HEIGHT - 60          # words that reach this line cost a life
START_LIVES = 3
START_SPEED = 70              # pixels per second
LONG_WORDS = [w for w in WORDS if len(w) >= 5]

NAVY = (15, 25, 60)
DARK_NAVY = (10, 17, 42)
WHITE = (240, 240, 245)
GREY = (140, 150, 185)
YELLOW = (255, 205, 80)
RED = (225, 80, 80)
GREEN = (90, 200, 120)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Weak Spot")
clock = pygame.time.Clock()

title_font = pygame.font.SysFont("arial", 80, bold=True)
big_font = pygame.font.SysFont("arial", 40, bold=True)
font = pygame.font.SysFont("arial", 24)
small_font = pygame.font.SysFont("arial", 18)
word_font = pygame.font.SysFont("consolas,menlo,dejavusansmono,couriernew", 30, bold=True)
CHAR_W = word_font.size("a")[0]   # every letter is the same width in a monospace font


def draw_text(text, fnt, color, x, y, center=False):
    img = fnt.render(text, True, color)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(img, rect)


def weakness_color(value):
    # green (fine) -> yellow -> red (weak)
    t = min(value / 1.5, 1)
    if t < 0.5:
        a, b, t = GREEN, YELLOW, t * 2
    else:
        a, b, t = YELLOW, RED, (t - 0.5) * 2
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


class FallingWord:
    def __init__(self, text, targets):
        self.text = text
        self.targets = targets      # letters the AI chose this word to train
        self.x = random.randint(20, WIDTH - 20 - len(text) * CHAR_W)
        self.y = -30
        self.typed = 0              # how many letters typed so far
        self.last_key_time = None


class Game:
    def __init__(self):
        self.brain = TypingBrain()
        self.ai_on = True
        self.show_ai = False
        self.state = "menu"

    def new_game(self):
        self.words = []
        self.current = None         # the word you're typing right now
        self.lives = START_LIVES
        self.score = 0
        self.speed = START_SPEED
        self.spawn_timer = 0
        self.correct = 0
        self.mistakes = 0
        self.cleared = 0
        self.spawned = 0
        self.targeted = 0
        self.start_time = time.time()
        self.state = "play"

    # ---------------- gameplay ----------------
    def spawn_word(self):
        # don't spawn a word starting with a letter already on screen
        used = [w.text[0] for w in self.words]
        options = [w for w in LONG_WORDS if w[0] not in used]
        text, targets = self.brain.pick_word(options, self.ai_on)
        self.words.append(FallingWord(text, targets))
        self.spawned += 1
        if targets:
            self.targeted += 1

    def type_letter(self, letter):
        now = time.time()

        # not locked onto a word yet: find one starting with this letter
        if self.current is None:
            for word in self.words:
                if word.text[0] == letter:
                    self.current = word
                    word.typed = 1
                    word.last_key_time = now
                    self.brain.record_hit(letter)   # no timing for first letter
                    self.correct += 1
                    return
            self.mistakes += 1
            return

        word = self.current
        expected = word.text[word.typed]
        if letter == expected:
            seconds = now - word.last_key_time
            if seconds > 1.5:
                seconds = None   # you probably paused, so don't count it
            self.brain.record_hit(letter, seconds)
            self.correct += 1
            word.typed += 1
            word.last_key_time = now
            if word.typed == len(word.text):
                self.words.remove(word)
                self.current = None
                self.cleared += 1
                self.score += len(word.text) * 10
                self.speed = min(220, self.speed + 1.5)   # gets a bit faster every word
        else:
            self.brain.record_miss(expected)
            self.mistakes += 1

    def update(self, dt):
        self.spawn_timer -= dt
        if self.spawn_timer <= 0 or not self.words:
            self.spawn_word()
            self.spawn_timer = max(1.2, 2.2 - self.cleared * 0.02)

        for word in self.words[:]:
            word.y += self.speed * dt
            if word.y + 30 >= BOTTOM:
                self.words.remove(word)
                if word is self.current:
                    self.current = None
                    self.brain.record_miss(word.text[word.typed])  # got stuck here
                self.lives -= 1
                self.speed = max(START_SPEED, self.speed - 10)   # ease off a bit
                if self.lives <= 0:
                    self.brain.save()
                    self.state = "game_over"

    def wpm(self):
        minutes = (time.time() - self.start_time) / 60
        if minutes < 0.05:
            return 0
        return (self.correct / 5) / minutes

    def accuracy(self):
        total = self.correct + self.mistakes
        if total == 0:
            return 100
        return self.correct / total * 100

    # ---------------- drawing ----------------
    def draw_menu(self):
        draw_text("Weak Spot", title_font, WHITE, WIDTH // 2, 170, center=True)
        draw_text("A typing game that learns which letters you struggle with",
                  font, GREY, WIDTH // 2, 250, center=True)
        draw_text("Press Enter to start", big_font, YELLOW, WIDTH // 2, 350, center=True)

        ai_text = "on" if self.ai_on else "off"
        draw_text(f"A  -  AI targeting: {ai_text}", font, WHITE, WIDTH // 2, 440, center=True)
        draw_text("R  -  reset what the AI has learned", font, WHITE, WIDTH // 2, 480, center=True)
        draw_text("F1 in game  -  see what the AI is learning", font, WHITE, WIDTH // 2, 520, center=True)

        weak = self.brain.weakest_letters()
        if weak:
            msg = "Your weak letters so far: " + "  ".join(l.upper() for l in weak)
        else:
            msg = "The game will learn your typing as you play."
        draw_text(msg, small_font, GREY, WIDTH // 2, HEIGHT - 40, center=True)

    def draw_play(self):
        # bottom line
        pygame.draw.rect(screen, DARK_NAVY, (0, BOTTOM, WIDTH, HEIGHT - BOTTOM))
        pygame.draw.line(screen, RED, (0, BOTTOM), (WIDTH, BOTTOM), 2)
        draw_text("Backspace: switch word     F1: show AI     Esc: menu",
                  small_font, GREY, WIDTH // 2, BOTTOM + 30, center=True)

        # words
        for word in self.words:
            draw_text(word.text, word_font, WHITE, word.x, word.y)
            if word is self.current:
                # underline the letters you've typed
                pygame.draw.rect(screen, YELLOW, (word.x, word.y + 36, word.typed * CHAR_W, 4))
            if self.show_ai and word.targets:
                draw_text("training: " + " ".join(word.targets), small_font, YELLOW,
                          word.x, word.y + 42)

        # top bar
        pygame.draw.rect(screen, DARK_NAVY, (0, 0, WIDTH, 50))
        draw_text(f"Score: {self.score}", font, WHITE, 20, 12)
        draw_text(f"WPM: {self.wpm():.0f}", font, WHITE, 200, 12)
        draw_text(f"Accuracy: {self.accuracy():.0f}%", font, WHITE, 340, 12)
        draw_text("Lives:", font, WHITE, WIDTH - 190, 12)
        for i in range(START_LIVES):
            color = RED if i < self.lives else GREY
            pygame.draw.circle(screen, color, (WIDTH - 100 + i * 30, 26), 10)

        if self.show_ai:
            self.draw_ai_panel()

    def draw_ai_panel(self):
        x, y = WIDTH - 280, 70
        pygame.draw.rect(screen, DARK_NAVY, (x, y, 260, 330), border_radius=10)
        pygame.draw.rect(screen, YELLOW, (x, y, 260, 330), 2, border_radius=10)
        draw_text("What the AI has learned", font, YELLOW, x + 15, y + 12)

        if self.brain.total_keys() < 30:
            draw_text("Still learning your typing...", small_font, WHITE, x + 15, y + 55)
        else:
            draw_text("Weak letters:", small_font, GREY, x + 15, y + 50)
            weak = self.brain.weakest_letters()
            if not weak:
                draw_text("none yet", small_font, WHITE, x + 15, y + 75)
            for i, letter in enumerate(weak):
                row_y = y + 75 + i * 30
                value = self.brain.weakness(letter)
                draw_text(letter.upper(), font, WHITE, x + 15, row_y)
                pygame.draw.rect(screen, weakness_color(value),
                                 (x + 45, row_y + 8, int(min(value, 2) * 50), 10))
                draw_text(self.brain.reason(letter), small_font, GREY, x + 160, row_y + 3)

        percent = self.targeted / self.spawned * 100 if self.spawned else 0
        draw_text(f"Speed: {self.speed:.0f}", small_font, WHITE, x + 15, y + 250)
        draw_text(f"Words aimed at weak letters: {percent:.0f}%", small_font, WHITE, x + 15, y + 280)

    def draw_game_over(self):
        draw_text("Game Over", big_font, WHITE, WIDTH // 2, 60, center=True)
        draw_text(f"Score: {self.score}     WPM: {self.wpm():.0f}     "
                  f"Accuracy: {self.accuracy():.0f}%     Words: {self.cleared}",
                  font, WHITE, WIDTH // 2, 120, center=True)

        # keyboard heatmap
        draw_text("Your keyboard (red = weak spot)", font, GREY, WIDTH // 2, 185, center=True)
        rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
        size = 50
        for r, row in enumerate(rows):
            start_x = WIDTH // 2 - 275 + r * 25
            for c, letter in enumerate(row):
                x = start_x + c * (size + 5)
                y = 220 + r * (size + 5)
                s = self.brain.stats[letter]
                if s["hits"] + s["misses"] < 3:
                    color = GREY       # not enough data
                else:
                    color = weakness_color(self.brain.weakness(letter))
                pygame.draw.rect(screen, color, (x, y, size, size), border_radius=6)
                draw_text(letter.upper(), font, NAVY, x + size // 2, y + size // 2, center=True)

        weak = self.brain.weakest_letters()
        y = 420
        if weak:
            draw_text("Letters to practise:", font, WHITE, WIDTH // 2, y, center=True)
            for letter in weak:
                y += 32
                draw_text(f"{letter.upper()}  -  {self.brain.reason(letter)}",
                          font, YELLOW, WIDTH // 2, y, center=True)
        else:
            draw_text("No weak letters found yet - play more!", font, WHITE, WIDTH // 2, y, center=True)

        draw_text("Enter: play again     Esc: menu", font, GREY, WIDTH // 2, HEIGHT - 35, center=True)

    # ---------------- main loop ----------------
    def run(self):
        while True:
            dt = clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.brain.save()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.handle_key(event)

            if self.state == "play":
                self.update(dt)

            screen.fill(NAVY)
            if self.state == "menu":
                self.draw_menu()
            elif self.state == "play":
                self.draw_play()
            else:
                self.draw_game_over()
            pygame.display.flip()

    def handle_key(self, event):
        if event.key == pygame.K_F1:
            self.show_ai = not self.show_ai
        elif self.state == "menu":
            if event.key == pygame.K_RETURN:
                self.new_game()
            elif event.key == pygame.K_a:
                self.ai_on = not self.ai_on
            elif event.key == pygame.K_r:
                self.brain.reset()
                self.brain.save()
        elif self.state == "play":
            if event.key == pygame.K_ESCAPE:
                self.brain.save()
                self.state = "menu"
            elif event.key == pygame.K_BACKSPACE:
                self.current = None
            elif len(event.unicode) == 1 and event.unicode.lower() in LETTERS:
                self.type_letter(event.unicode.lower())
        elif self.state == "game_over":
            if event.key == pygame.K_RETURN:
                self.new_game()
            elif event.key == pygame.K_ESCAPE:
                self.state = "menu"


Game().run()
