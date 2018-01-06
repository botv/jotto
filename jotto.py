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
        self.norepeat = tools.filegrab('words/words_without_repeats.txt')
        self.repeat = tools.filegrab('words/words_with_repeats.txt')
        self.choice = random.choice(self.norepeat)

    def eval_guess(self, guess):
        common = 0
        for letter in set(guess):
            common += self.choice.count(letter)
        return common

    def choose_strat(self):
        prob1 = 1/3.0
        prob2 = 1/3.0
        prob3 = 1/3.0
        draw = np.random.choice(['strat1', 'strat2', 'strat3'], 1,
                                p=[prob1, prob2, prob3])
        return draw


class Human(object):
    def __init__(self):
        self.alphalist = list(string.ascii_lowercase)
        self.alphabet = {}
        for letter in self.alphalist:
            self.alphabet[letter] = 0
        self.words = tools.filegrab('words/words.txt')


class Self_Play(object):
    def __init__(self):
        self.player1 = Computer()
        self.player2 = Computer()


if __name__ == "__main__":
    comp = Computer()
    draw = comp.choose_strat()
    print(draw)
