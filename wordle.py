# %%
import random

with open("words.txt", "r") as f:
    words = f.read().splitlines()

# %%
class Guess:
    def __init__(self, guess):
        guess = guess.upper()
        if guess not in words:
            raise Exception(f"{guess} is not a valid wordle")
        
        class Position:
            pass
        
        positions = []

        global incorrect_letters
        for i in range(len(guess)):
            position = Position()
            position.char = guess[i]
            if position.char == wordle[i]:
                position.status = "MATCH"
            elif position.char in wordle:
                position.status = "FUZZY"
            else:
                position.status = "MISS"
                if guess[i] not in incorrect_letters:
                    incorrect_letters.append(guess[i])
            positions.append(position)

        self.guess = positions

        self.win = all([p.status == 'MATCH' for p in self.guess])

    def display_guess(self):
        def color_char(char, status):
            color = {
                'MATCH' : "\u001b[42m\u001b[30m",
                'FUZZY' : "\u001b[43m\u001b[30m",
                'MISS' : "\u001b[47m\u001b[30m"
            }
            return f"{color[status]} {char} \u001b[0m"

        print(''.join([color_char(g.char, g.status) for g in self.guess]))

    def word_filter(self, word):
        conditions = [True]
        for i in range(len(self.guess)):
            x = self.guess[i]
            if x.status == 'MATCH':
                conditions.append(x.char == word[i])
            elif x.status == 'FUZZY':
                conditions.append(x.char != word[i])
                conditions.append(x.char in word)
            elif x.status == 'MISS':
                pass
            else:
                raise Exception("Incorrect status passed.")
        for l in incorrect_letters:
            conditions.append(l not in word)
        return all(conditions)

    def possible_next_words(self):
        return list(filter(self.word_filter, words))

                

# # %%
# wordle = random.choice(words)
# incorrect_letters = []
# # %%
# t = Guess('SNIFF')
# t.display_guess()
# print(t.win)
# print(incorrect_letters)
# t.possible_next_words()
# %%
import sys
import time
play = True
print('')
print("Get your wordle fix anytime, many times\r", end='', flush=True)
time.sleep(0.5)
print("Get your wordle fix anytime, many times.\r", end='', flush=True)
time.sleep(0.5)
print("Get your wordle fix anytime, many times..\r", end='', flush=True)
time.sleep(0.5)
print("Get your wordle fix anytime, many times...\n")
while play:
    time.sleep(1)
    print('Enter your starting word (5 letters) to begin the game:\n')
    wordle = random.choice(words)
    incorrect_letters = []
    win = False
    turns_remaining = 6
    while True:
        if turns_remaining <= 0:
            print(f"Sorry, you ran out of guesses!\nThe wordle was {wordle}.")
            break
        if win:
            print("You won!\n")
            break

        try:
            g = Guess(input())
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
            g.display_guess()
            win = g.win
        except Exception as e:
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
            print(e)
            turns_remaining += 1
            time.sleep(1.5)
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")

        turns_remaining -= 1

    play_again = input('Would you like to play again? (y/n):')
    play = play_again.lower() == 'y'
# %%
# %%
