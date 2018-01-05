from randomn import *
import tensorflow as tf
import numpy as np
import os

class Computer(object):
    def __init__(self):
        self.alphabet = {
            'a': 0, 'b': 0,
            'c': 0, 'd': 0,
            'e': 0, 'f': 0,
            'g': 0, 'h': 0,
            'i': 0, 'j': 0,
            'k': 0, 'l': 0,
            'm': 0, 'n': 0,
            'o': 0, 'p': 0,
            'q': 0, 'r': 0,
            's': 0, 't': 0,
            'u': 0, 'v': 0,
            'w': 0, 'x': 0,
            'y': 0, 'z': 0
        }
        self.words = [line.rstrip('\n') for line in open('word_files/words.txt')]
        self.choice = random.choice(self.words)

    def mostLetters(self):


class Human(object):
    def __init__(self):
        self.alphabet = {
            'a': 0, 'b': 0,
            'c': 0, 'd': 0,
            'e': 0, 'f': 0,
            'g': 0, 'h': 0,
            'i': 0, 'j': 0,
            'k': 0, 'l': 0,
            'm': 0, 'n': 0,
            'o': 0, 'p': 0,
            'q': 0, 'r': 0,
            's': 0, 't': 0,
            'u': 0, 'v': 0,
            'w': 0, 'x': 0,
            'y': 0, 'z': 0
        }
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
