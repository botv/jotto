# The Jottobot
# Ben Botvinick & Robert May, 2018

import random
import string
import time
import numpy as np
# import tensorflow as tf
# import os


def filearr(file):
    words = [line.rstrip('\n') for line in open(file)]
    return words


class Computer:
    def __init__(self):
        alphalist = list(string.ascii_lowercase)
        self.alphabet = {}
        for letter in alphalist:
            self.alphabet[letter] = [0, 0, []]
        self.words = filearr('words/words.txt')
        self.for_guessing = self.words
        self.norepeat = filearr('words/words_without_repeats.txt')
        self.repeat = filearr('words/words_with_repeats.txt')
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
        self.own_guesses[guess] = common

    def strat1(self):
        # Cover as many letters as possible
        if len(self.own_guesses) is not 0:
            letters = []
            for guess in self.own_guesses:
                print "in own_guesses"
                print list(guess)
                for letter in list(guess):
                    print "in list(guess)"
                    letters.append(letter)
            letters = set(letters)
            run = True
            ind = 0
            while run:
                print "run = true"
                if len(letters) == 0:
                    return random.choice(self.for_guessing)
                if ind < len(self.for_guessing):
                    word = self.for_guessing[ind]
                    if not any(x in word for x in letters):
                        guess = word
                        run = False
                    else:
                        ind += 1
                else:
                    letters.pop()
            return guess
        else:
            return random.choice(self.for_guessing)

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
        letter = self.alphabet[let]
        if letter[1] == -1:
            return False
        letterInPossible = False
        ind = 0
        knownLets = []
        for lett in self.alphabet:
            if self.alphabet[lett][1] == 1:
                knownLets.append(lett)
        if let in knownLets:
            return True
        for guess in letter[2]:
            unknownLetsInGuess = self.own_guesses[guess]
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

    def find_known_letters(self):
        knownLets = []
        tempKnownLets = []
        knownNotLets = []
        for lett in self.alphabet:
            if self.alphabet[lett][1] == 1:
                knownLets.append(lett)
                tempKnownLets.append(lett)
            elif self.alphabet[lett][1] == -1:
                knownNotLets.append(lett)
        for guess in self.own_guesses:
            commonLetsInGuess = self.own_guesses[guess]
            unknownLetsInGuess = 0
            for lett in guess:
                if lett in knownLets:
                    commonLetsInGuess -= 1
                if self.alphabet[lett][1] == 0:
                    unknownLetsInGuess += 1
            if commonLetsInGuess == unknownLetsInGuess:
                for lett in guess:
                    if self.alphabet[lett][1] == 0:
                        knownLets.append(lett)
                        self.alphabet[lett][1] = 1
        if knownLets == tempKnownLets:
            return False
        else:
            return knownLets

    def update_alphabet(self, guess, common):
        # Super important function that updates the alphabet every turn
        self.own_guesses[guess] = common
        for letter in set(guess):
            if not self.eliminate_letter(letter):
                self.alphabet[letter][1] = -1
            self.alphabet[letter][2].append(guess)
            self.alphabet[letter][0] += 1
        stillFinding = True
        stillEliminating = True
        while stillFinding or stillEliminating:
            find_known_letters = self.find_known_letters()
            if find_known_letters is False:
                stillFinding = False
            else:
                for letter in find_known_letters:
                    self.alphabet[letter][1] = 1
            stillEliminating = False
            for letter in self.alphabet:
                if (not self.eliminate_letter(letter) and
                        self.alphabet[letter][1] != -1):
                    self.alphabet[letter][1] = -1
                    stillEliminating = True
        print self.alphabet


class Learning:
    def __init__(self):
        self.sessions = open('states/sessions.txt', 'r+')
        self.time_file = open('states/turntime.txt', 'a')
        self.states_file = open('states/states.txt', 'r+')
        self.states_list_unparsed = filearr('states/states.txt')
        self.sess_id = int(self.sessions.readline()) + 1
        self.gam = open('states/games/sess' + str(self.sess_id) + '.txt', 'w+')

    def record_p1_state(self, p1, game, strategy, guess, common):
        self.gam.write(str(p1.alphabet) + ';'
                       + strategy + ';'
                       + guess + ';' + str(common) + '\n')

    def record_p2_state(self, p2, game, strategy, guess, common):
        self.gam.write(str(p2.alphabet) + ';'
                       + strategy + ';'
                       + guess + ';' + str(common) + '\n')

    def parser(self, games, winners):
        lines = filearr(self.gam)
        for game in games:
            for line in lines:
                if (list(line.split("")))[:3] is ("--" + winners[game - 1]):
                    print("HEllo")
        print lines

    def play(self, games):
        if games > 9:
            games = 9
        self.sessions.seek(0)
        self.sessions.truncate()
        self.sessions.write(str(self.sess_id))
        game = 1
        start_time = time.time()
        while game <= games:
            p1 = Computer()
            p2 = Computer()
            if game != 1:
                self.gam.write("=")
            game_over = False
            winner = None
            turn = 1
            while not game_over:
                print "Started"
                self.gam.write('--1' + str(turn) + '\n')
                print "before guess"
                guess1 = p1.guess()
                print "before eval guess"
                eval1 = p2.eval_guess(guess1[1])
                print "before 1st update"
                p1.update_alphabet(guess1[1], eval1)
                print "updated 1"
                self.record_p1_state(p1, game, guess1[0], guess1[1], eval1)
                if guess1[1] != p2.choice:
                    print "player 2:"
                    self.gam.write('--2' + str(turn) + '\n')
                    guess2 = p2.guess()
                    eval2 = p1.eval_guess(guess2[1])
                    p2.update_alphabet(guess2[1], eval2)
                    print "Finished Both"
                    self.record_p2_state(p2, game, guess2[0], guess2[1], eval2)
                    print "recorded"
                    if guess2[1] == p1.choice:
                        game_over = True
                        winner = "2"
                else:
                    game_over = True
                    winner = "1"
                turn += 1
            game += 1
            elapsed = time.time() - start_time
            self.time_file.write(str(round(elapsed, 3))
                                 + ":" + str(turn - 1) + ":"
                                 + str(int((turn - 1) / elapsed))
                                 + ":" + winner + "\n")


def main():
    game = Learning()
    game.play(1)


if __name__ == "__main__":
    main()
