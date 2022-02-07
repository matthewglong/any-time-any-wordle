# %%
import random
import sys
import time

with open("words.txt", "r") as f:
    words = f.read().splitlines()


class Game:
    def __init__(self):
        self.wordle = random.choice(words)
        self.incorrect_letters = []
        self.guesses = []

    def __repr__(self):
        return f"Wordle: {self.wordle}"

    def new_guess(self, guess):
        g = Guess(self, guess)
        self.guesses.append(g)

    def matched_letters(self):
        return self.guesses[-1].matches()

    def fuzzy_letters(self):
        return self.guesses[-1].fuzzies()

    def unused_letters(self):
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        unused = []
        for l in letters:
            if (
                (l not in self.matched_letters()) &
                (l not in self.fuzzy_letters()) &
                (l not in self.incorrect_letters)
            ):
                unused.append(l)
        return list(sorted(unused))



class Guess:
    def __init__(self, game, guess):
        guess = guess.upper()
        if guess not in words:
            raise Exception(f"{guess} is not a valid wordle")
        
        class Position:
            def __repr__(self):
                return str(self.__dict__)
        
        positions = []

        wordle = game.wordle
        for i in range(len(guess)):
            position = Position()
            position.char = guess[i]
            if position.char == wordle[i]:
                position.status = "MATCH"
            elif position.char in wordle:
                position.status = "FUZZY"
            else:
                position.status = "MISS"
                if guess[i] not in game.incorrect_letters:
                    game.incorrect_letters.append(guess[i])
            positions.append(position)

        self.game = game
        self.atts = positions
        self.guess = guess

        self.win = all([p.status == 'MATCH' for p in self.atts])
    
    def __repr__(self):
        return self.display_guess()

    def display_guess(self):
        def color_char(char, status):
            color = {
                'MATCH' : "\u001b[42m\u001b[30m",
                'FUZZY' : "\u001b[43m\u001b[30m",
                'MISS' : "\u001b[47m\u001b[30m"
            }
            return f"{color[status]} {char} \u001b[0m"

        return ''.join([color_char(g.char, g.status) for g in self.atts])

    def word_filter(self, word):
        conditions = [True]
        for i in range(len(self.guess)):
            x = self.atts[i]
            if x.status == 'MATCH':
                conditions.append(x.char == word[i])
            elif x.status == 'FUZZY':
                conditions.append(x.char != word[i])
                conditions.append(x.char in word)
            elif x.status == 'MISS':
                pass
            else:
                raise Exception("Incorrect status passed.")
        for l in self.game.incorrect_letters:
            conditions.append(l not in word)
        return all(conditions)

    def possible_next_words(self):
        return list(filter(self.word_filter, words))

    def matches(self):
        return list(sorted([p.char for p in self.atts if p.status == 'MATCH']))

    def fuzzies(self):
        return list(sorted([p.char for p in self.atts if p.status == 'FUZZY']))

class PlayShellGame(Game):
    def __init__(self):
        super().__init__()

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
            win = False
            turns_remaining = 6
            while True:
                if turns_remaining <= 0:
                    print(f"Sorry, you ran out of guesses!\nThe wordle was {self.wordle}.")
                    break
                if win:
                    print("You won!\n")
                    break

                try:
                    g = Guess(self, input())
                    sys.stdout.write("\033[F")
                    sys.stdout.write("\033[K")
                    print(g.display_guess())
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
            if play:
                self = PlayShellGame()

    
