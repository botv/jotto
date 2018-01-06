import random
import string
import numpy as np
# import tensorflow as tf
# import os


def filegrab(file):
    words = [line.rstrip('\n') for line in open(file)]
    return words


class Computer:
    def __init__(self):
        alphalist = list(string.ascii_lowercase)
        self.alphabet = {}
        for letter in alphalist:
            self.alphabet[letter] = [0, 0, []]
        self.words = filegrab('words/words.txt')
        self.for_guessing = self.words
        self.norepeat = filegrab('words/words_without_repeats.txt')
        self.repeat = filegrab('words/words_with_repeats.txt')
        self.choice = random.choice(self.norepeat)
        self.own_guesses = {}
        self.received_guesses = {}
        self.possible = self.norepeat

    def update_lists(self, guess, common):
        # Removes OWN guess from list and appends it to
        if len(set(guess)) == len(guess):
            self.norepeat.remove(guess)
        else:
            self.repeat.remove(guess)
        self.for_guessing.remove(guess)
        self.ownguesses[guess] = common

    def strat1(self):
        # Cover as many letters as possible
        if self.own_guesses[0]:
            letters = []
            for guess in self.own_guesses:
                for letter in list(guess):
                    letters.push(letter)
            letters = set(letters)
            run = True
            ind = 0
            while run:
                word = self.for_guessing[ind]
                if not any(x in word for x in letters):
                    guess = word
                    run = False
                if not guess:
                    letters.pop()
        else:
            return random.choice(self.norepeat)

    def strat2(self):
        # Make the best possible guess
        print("No code here yet.")

    def strat3(self):
        # What to do here?
        print("No code here yet.")

    def eval_guess(self, guess):
        # Counts common letters between self.choice and guess
        common = 0
        for letter in set(guess):
            common += self.choice.count(letter)
        return common

    def guess(self):
        # Chooses a strategy with weighted probabilities
        prob1 = 1/3.0
        prob2 = 1/3.0
        prob3 = 1/3.0
        strat = np.random.choice(['strat1', 'strat2', 'strat3'], 1,
                                 p=[prob1, prob2, prob3])
        guess = getattr(self, strat[0])()
        return guess


class Human:
    # For playing with humans
    def __init__(self):
        self.alphalist = list(string.ascii_lowercase)
        self.alphabet = {}
        for letter in self.alphalist:
            self.alphabet[letter] = 0
        self.words = filegrab('words/words.txt')


class Self_Play:
    def __init__(self):
        self.player1 = Computer()
        self.player2 = Computer()


def main():
    comp = Computer()


if __name__ == "__main__":
    main()
