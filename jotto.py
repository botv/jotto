# The Jottobot
# Ben Botvinick & Robert May, 2018

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
        self.possible = self.norepeat
        self.last_guess = None

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
        if len(self.own_guesses) is not 0:
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
        prob1 = 1
        prob2 = 0
        prob3 = 0
        strat = np.random.choice(['strat1', 'strat2', 'strat3'], 1,
                                 p=[prob1, prob2, prob3])
        guess = getattr(self, strat[0])()
        self.last_guess = guess
        return [strat[0], guess]

    def update_possible(self):
        # BUGGY
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
                knownLetsInd += 1
            knownNotLetsInd = 0
            while knownNotLetsInd < len(knownNotLets) and not wordRemoved:
                let = knownNotLets[knownNotLetsInd]
                if let in word:
                    self.possible.remove(word)
                    ind -= 1
                    wordRemoved = True
                knownNotLetsInd += 1
            ind += 1

    def eliminate_letter(self, let):
        # Eliminate a letter using fantastic logic
        letter = self.alphabet[let]
        if letter[1] == -1:
            return False
        letterInPossible = False
        ind = 0
        knownLets = []
        for lett in self.alphabet:
            if self.alphabet[lett][1] == 1:
                knownLets.append(lett)
        for guess in letter[2]:
            unknownLetsInGuess = self.own_guesses[guess]
            print unknownLetsInGuess
            for lett in knownLets:
                if lett in guess:
                    unknownLetsInGuess -= 1
            if unknownLetsInGuess == 0:
                return False
        while ind < len(self.possible) and not letterInPossible:
            word = self.possible[ind]
            if let in word:
                letterInPossible = True
            ind += 1
        if not letterInPossible:
            return False
        return True

    def update_alphabet(self, guess, common):
        # Super important function that updates the alphabet every turn
        for letter in guess:
            self.eliminate_letter(letter)


class Learning:
    def __init__(self):
        self.p1 = Computer()
        self.p2 = Computer()
        self.sessions = open('states/sessions.txt', 'r+')
        self.states_file = open('states/states.txt', 'r')
        self.states_list_unparsed = filegrab('states/states.txt')
        self.sess_id = int(self.sessions.readline()) + 1
        self.gam = open('states/games/sess' + str(self.sess_id) + '.txt', 'w+')

    def record_p1_state(self, game, strategy, guess, common):
        self.gam.write(str(self.p1.alphabet) + ':'
                       + strategy + ';'
                       + guess + ':' + str(common))

    def record_p2_state(self, game, strategy, guess, common):
        self.gam.write(str(self.p1.alphabet) + ':'
                       + strategy + ';'
                       + guess + ':' + str(common))

    def play(self, games):
        self.sessions.write(str(self.sess_id))
        game = 1
        while game <= games:
            self.gam.write('-' + str(game))
            game_over = False
            turn = 1
            while not game_over:
                self.gam.write('--2' + str(turn))
                guess1 = self.p1.guess()
                eval1 = self.p2.eval_guess(guess1)
                self.record_p1_state(game, guess1[0], guess1[1], eval1)
                if eval1 != 5:
                    self.gam.write('--2' + str(turn))
                    guess2 = self.p2.guess()
                    eval2 = self.p1.eval_guess(guess2)
                    self.record_p2_state(game, guess2[0], guess2[1], eval2)
                    if eval2 == 5:
                        game_over = True
                else:
                    game_over = True
                turn += 1
            game += 1


def main():
    game = Learning()
    game.play(1)


if __name__ == "__main__":
    main()
