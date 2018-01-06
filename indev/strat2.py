import random
import string
import tools
import numpy as np
# import tensorflow as tf
# import os


class Computer(object):
    def __init__(self):
        alphalist = list(string.ascii_lowercase)
        self.alphabet = {}
        for letter in alphalist:
            self.alphabet[letter] = [0, 0, []]
        self.words = tools.filegrab('words/words.txt')
        self.for_guessing = self.words
        self.norepeat = tools.filegrab('words/words_without_repeats.txt')
        self.repeat = tools.filegrab('words/words_with_repeats.txt')
        self.choice = random.choice(self.norepeat)
        self.own_guesses = {}
        self.received_guesses = {}
        self.possible = self.norepeat

    def eval_guess(self, guess):
        # Counts common letters between self.choice and guess
        common = 0
        for letter in set(guess):
            common += self.choice.count(letter)
        return common

    def update_possible(self):
        knownLets = []
        knownNotLets = []
        for lett in self.alphabet:
            if self.alphabet[lett][1] == 1:
                knownLets.append(lett)
            elif self.alphabet[lett][1] == -1:
                knownNotLets.append(lett)
        ind = 0
        while ind < len(self.possible):
            word = self.possible[ind]
            knownLetsInd = 0
            wordRemoved = False
            while knownLetsInd < len(knownLets) and not wordRemoved:
                let = knownLets[knownLetsInd]
                if let not in word:
                    self.possible.remove(word)
                    ind -= 1
                    wordRemoved = True
            knownNotLetsInd = 0
            while knownNotLetsInd < len(knownNotLets) and not wordRemoved:
                let = knownNotLets[knownNotLetsInd]
                if let in word:
                    self.possible.remove(word)
                    ind -= 1
                    wordRemoved = True
            ind += 1

    def eliminate_letter(self, let):
        letter = self.alphabet[let]
        if letter[1] == -1:
            return False
        letterInPossible = False
        ind = 0
        while ind < len(self.possible) and not letterInPossible:
            word = self.possible[ind]
            if let in word:
                letterInPossible = True
        if not letterInPossible:
            return False


    def find_known_letters(self):
        for letter in alphabet:
            guessInd = 0
            confirmed = False
            while guessInd < len(letter[2]) and not confirmed:
                otherKnownFalse
                for let in letter[2][guessInd]:

    def guess(self):
        # Chooses a strategy with weighted probabilities
        prob1 = 1/3.0
        prob2 = 1/3.0
        prob3 = 1/3.0
        strat = np.random.choice(['strat1', 'strat2', 'strat3'], 1,
                                 p=[prob1, prob2, prob3])
        guess = getattr(self, strat)()
        return guess

    def update_lists(self, guess, common):
        # Removes OWN guess from list and appends it to
        if len(set(guess)) == len(guess):
            self.norepeat.remove(guess)
        else:
            self.repeat.remove(guess)
        self.for_guessing.remove(guess)
        self.ownguesses[guess] = common
