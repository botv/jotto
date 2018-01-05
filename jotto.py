import random
# import tensorflow as tf
# import numpy as np
import os
import string

import tools


class Computer(object):
    def __init__(self):
        alphalist = list(string.ascii_lowercase)
        self.alphabet = {}
        for letter in alphalist:
            self.alphabet[letter] = 0
        self.words = tools.filegrab('word_files/words.txt')
        self.norepeat = tools.filegrab('word_files/words_without_repeats.txt')
        self.repeat = tools.filegrab('word_files/words_with_repeats.txt')
        self.choice = random.choice(self.repeat)

    def strat1(self):
        empty = 0

    def strat2(self):
        empty = 0

    def strat3(self):
        empty = 0


class Human(object):
    def __init__(self):
        self.alphalist = list(string.ascii_lowercase)
        self.alphabet = {}
        for letter in self.alphalist:
            self.alphabet[letter] = 0
        self.words = tools.filegrab('word_files/words.txt')


class Self_Play(object):
    def __init__(self):
        computer = Computer()


if __name__ == "__main__":
    os.system('clear')
    comp = Computer()
    print(comp.choice)
