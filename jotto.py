import random
import string
import tools
# import tensorflow as tf
# import numpy as np
# import os


class Computer(object):
    def __init__(self):
        alphalist = list(string.ascii_lowercase)
        self.alphabet = {}
        for letter in alphalist:
            self.alphabet[letter] = 0
        self.words = tools.filegrab('words/words.txt')
        self.norepeat = tools.filegrab('words/words_without_repeats.txt')
        self.repeat = tools.filegrab('words/words_with_repeats.txt')
        self.choice = random.choice(self.norepeat)

    def eval_guess(self, guess):
        common = 0
        for letter in set(guess):
            common += self.choice.count(letter)
        return common


class Human(object):
    def __init__(self):
        self.alphalist = list(string.ascii_lowercase)
        self.alphabet = {}
        for letter in self.alphalist:
            self.alphabet[letter] = 0
        self.words = tools.filegrab('words/words.txt')


class Self_Play(object):
    def __init__(self):
        self.computer = Computer()


if __name__ == "__main__":
    comp = Computer()
    # print(comp.choice)
    common = comp.eval_guess("eeeee")
    print(comp.choice, common)
