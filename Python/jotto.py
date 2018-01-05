from randomn import *
import tensorflow as tf
import numpy as np
import os
import string

class Computer(object):
    def __init__(self):
        alphalist = list(string.ascii_lowercase)
        self.alphabet = {}
        for letter in alphalist:
            self.alphabet[letter] = 0
        self.words = [line.rstrip('\n') for line in open('word_files/words.txt')]
        self.choice = random.choice(self.words)

class Human(object):
    def __init__(self):
        self.alphabet = {}
        for letter in alphalist:
            self.alphabet[letter] = 0
            self.words = [line.rstrip('\n') for line in open('word_files/words.txt')]

class Self_Play(object):
    def __init__(self):
        computer = Computer()
        human = Human()

class Human_Play(object):
    def __init__(self):
        player1 = Computer()
        player2 = Human()

if __name__ == "__main__":
    # Empty for now
