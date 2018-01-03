from random import *
import tensorflow as tf

class Game(object):
    def __init__(self):
        self.alphabet1 = {
            'a': 0, 'b': 0, 'c': 0,
            'd': 0, 'e': 0, 'f': 0,
            'g': 0, 'h': 0, 'i': 0,
            'j': 0, 'k': 0, 'l': 0,
            'm': 0, 'n': 0, 'o': 0,
            'p': 0, 'q': 0, 'r': 0,
            's': 0, 't': 0, 'u': 0,
            'v': 0, 'w': 0, 'x': 0,
            'y': 0, 'z': 0
        }
        self.alphabet2 = self.alphabet1
        self.words = [line.rstrip('\n') for line in open('words.txt')]
        self.choice2 = words[randint(words.length)]
        self.choice2 = words[randint(words.length)]
        print fh.readline(randint(1, 100))
game = Game()
print(game.alphabet1, game.alphabet2)
