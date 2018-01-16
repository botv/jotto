# The Jottobot
# Ben Botvinick & Robert May, 2018

import random
import string
import time
import numpy as np
import ast
import os
# import tensorflow as tf


def filearr(file):
    # Turn a folder into an array
    words = [line.rstrip('\n') for line in open(file)]
    return words


def cleanup():
    os.system("rm states/games/*")


def red(text):
    return (u"\u001b[31m"
            + text
            + u"\u001b[0m")


def green(text):
    return (u"\u001b[32m"
            + text
            + u"\u001b[0m")


class Computer:
    def __init__(self):
        alphalist = list(string.ascii_lowercase)
        self.alphabet = {}
        for letter in alphalist:
            self.alphabet[letter] = [0, 0, []]
        self.words = filearr('words/words.txt')[:]
        self.for_guessing = self.words[:]
        self.norepeat = filearr('words/words_without_repeats.txt')[:]
        self.repeat = filearr('words/words_with_repeats.txt')[:]
        self.common_words = filearr('words/common_words.txt')[:]
        self.choice = random.choice(self.norepeat)
        self.own_guesses = {}
        self.possible = self.norepeat[:]

    def update_lists(self, guess, common, player):
        # Fixes stuff
        if len(sorted(set(guess))) == len(guess):
            self.norepeat.remove(guess)
        else:
            self.repeat.remove(guess)
        self.for_guessing.remove(guess)
        if guess in self.possible:
            self.possible.remove(guess)

    def strat1(self):
        # Cover as many letters as possible
        if len(self.own_guesses) is not 0:
            letters = []
            for guess in self.own_guesses:
                for letter in list(guess):
                    letters.append(letter)
            letters = sorted(set(letters))
            if len(letters) > 20:
                guess = random.choice(self.for_guessing)
                return guess
            run = True
            ind = 0
            while run:
                if len(letters) == 0:
                    guess = random.choice(self.for_guessing)
                if ind < len(self.for_guessing):
                    word = self.for_guessing[ind]
                    if not any(x in word for x in letters):
                        guess = word
                        run = False
                    else:
                        ind += 1
                else:
                    letters.pop()
                    ind = 0
        else:
            guess = random.choice(self.for_guessing)
        if guess:
            return guess

    def strat2(self):
        # Make the best possible guess
        knownLets = []
        for lett in self.alphabet:
            if self.alphabet[lett][1] == 1:
                knownLets.append(lett)
        if len(knownLets) == 0:
            return random.choice(self.possible)
        ind = 0
        run = True
        while run:
            if ind >= len(self.possible):
                ind = 0
                knownLets.pop()
            word = self.possible[ind]
            if all(x in word for x in knownLets):
                guess = word
                run = False
            elif len(knownLets) == 0:
                run = False
            else:
                ind += 1
        if guess:
            return guess

    def strat3(self):
        # Make a guess to find information on a letter
        somehowKnownLetters = []
        for lett in self.alphabet:
            if self.alphabet[lett][1] != 0:
                somehowKnownLetters.append(lett)
        if len(somehowKnownLetters) == 0:
            return random.choice(self.for_guessing)
        otherLetsRequired = 1
        ind = 0
        run = True
        while run:
            if ind >= len(self.for_guessing):
                ind = 0
                otherLetsRequired += 1
            if otherLetsRequired == 5:
                return random.choice(self.for_guessing)
                run = False
            word = self.for_guessing[ind]
            otherCount = 0
            for lett in word:
                if lett not in somehowKnownLetters:
                    otherCount += 1
            if otherCount == otherLetsRequired:
                return word
                run = False
            ind += 1

    def eval_guess(self, guess):
        # Counts common letters between self.choice and guess
        common = 0
        for letter in set(guess):
            common += self.choice.count(letter)
        return common

    def guess(self):
        # Chooses a strategy with weighted probabilities
        prob1 = 1 / 3.0
        prob2 = 1 / 3.0
        prob3 = 1 / 3.0
        strat = np.random.choice(['strat1', 'strat2', 'strat3'], 1,
                                 p=[prob1, prob2, prob3])
        guess = getattr(self, strat[0])()
        return [strat[0], guess]

    def test_guess(self, turn):
        # Temporary guess function for testing
        if turn < 21:
            return ['strat1', self.strat1()]
        else:
            return ['strat2', self.strat2()]

    def get_current_state(self, turn):
        state = []
        state.append(str(turn))
        knownLets = 0
        knownNotLets = 0
        for lett in self.alphabet:
            if self.alphabet[lett][1] == 1:
                knownLets += 1
            elif self.alphabet[lett][1] == -1:
                knownNotLets += 1
        state.append(str(knownLets))
        state.append(str(knownNotLets))
        return state

    def guess_complex(self, current_state, turn):
        # A better guessing function
        if len(self.possible) == 1:
            return ['strat2', self.strat2()]
        states_arr = filearr("states/states.txt")
        weights = []
        current_state = self.get_current_state(turn)
        for state in states_arr:
            state = state.split(";")
            strat_choice = state.pop(-1)
            # scaled_success = state.pop(-2)
            if state == current_state:
                weights.append(strat_choice)
        if len(weights) != 0:
            part_weight = 0.25 / float(len(weights))
            prob1 = 0.25 + (part_weight * (weights.count('strat1')))
            prob2 = 0.25 + (part_weight * (weights.count('strat2')))
            prob3 = 0.25 + (part_weight * (weights.count('strat3')))
        else:
            prob1 = 1 / 3.0
            prob2 = 1 / 3.0
            prob3 = 1 / 3.0
        strat = np.random.choice(['strat1', 'strat2', 'strat3'], 1,
                                 p=[prob1, prob2, prob3])
        guess = getattr(self, strat[0])()
        return [strat[0], guess]

    def update_possible(self):
        # Updates list of possible words
        knownLets = []
        knownNotLets = []
        for lett in self.alphabet:
            if self.alphabet[lett][1] == 1:
                knownLets.append(lett)
            elif self.alphabet[lett][1] == -1:
                knownNotLets.append(lett)
        ind = 0
        changed = False
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
                    changed = True
                knownLetsInd += 1
            knownNotLetsInd = 0
            while knownNotLetsInd < len(knownNotLets) and not wordRemoved:
                let = knownNotLets[knownNotLetsInd]
                if let in word:
                    self.possible.remove(word)
                    ind -= 1
                    wordRemoved = True
                    changed = True
                knownNotLetsInd += 1
            ind += 1
        return changed

    def eliminate_letter(self, let):
        # Returns False if the given letter cannot be in the words
        # Returns True if nothing can be proven about the letter
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
        if len(knownLets) == 5:
            return False
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
        # Returns a list of known letters or simply False
        knownLets = []
        tempKnownLets = []
        knownNotLets = []
        for lett in self.alphabet:
            if self.alphabet[lett][1] == 1:
                knownLets.append(lett)
                tempKnownLets.append(lett)
            elif self.alphabet[lett][1] == -1:
                knownNotLets.append(lett)
        if len(knownNotLets) == 21 and len(knownLets) != 5:
            for lett in self.alphabet:
                if lett not in knownNotLets:
                    self.alphabet[lett][1] = 1
                    knownLets.append(lett)
        for guess in self.own_guesses:
            commonLetsInGuess = self.own_guesses[guess]
            unknownLetsInGuess = 0
            for lett in sorted(set(guess)):
                if lett in knownLets:
                    commonLetsInGuess -= 1
                if self.alphabet[lett][1] == 0:
                    unknownLetsInGuess += 1
            if commonLetsInGuess == unknownLetsInGuess:
                for lett in sorted(set(guess)):
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
        stillUpdatingPossible = True
        while stillFinding or stillEliminating or stillUpdatingPossible:
            stillUpdatingPossible = self.update_possible()
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
            if len(self.possible) == 0:
                os.system("clear")
                print(red("There are no remaining possible words."))
                time.sleep(1)
                print(red("You either cheated or are just an idiot."))
                time.sleep(1)
                raw_input("Press [ENTER] to leave the game.")
                os.system("clear")
                quit()


class Learning:
    def __init__(self):
        self.sessions = open('states/sessions.txt', 'r+')
        self.time_file = open('states/turntime.txt', 'a')
        self.states_file = open('states/states.txt', 'a+')
        self.sess_id = int(self.sessions.readline()) + 1
        self.gam = open('states/games/sess' + str(self.sess_id) + '.txt', 'w+')
        self.gam_string = 'states/games/sess' + str(self.sess_id) + '.txt'
        self.data = 'states/games/sess' + str(self.sess_id) + '.txt'
        self.game_states = ""

    def record_player_state(self, player, game, strategy,
                            guess, common, player_name, turn):
        alphabetStr = str(player.alphabet).replace(':', '=>')
        nowInfo = 0
        for lett in player.alphabet:
            if player.alphabet[lett][1] != 0:
                nowInfo += 1
        if turn != "1":
            noInd = self.game_states.split("\n")
            tempGameStates = noInd[:len(self.game_states.split("\n"))-1]
            tempState = tempGameStates[len(tempGameStates)-2].split(";")
            pastInfo = int(tempState[len(tempState)-3])
            learnedInfo = nowInfo - pastInfo
        else:
            learnedInfo = nowInfo
        self.game_states += (player_name + ";" + turn + ";" +
                             str(alphabetStr) + ';' + strategy + ';' +
                             guess + ';' + str(common) + ';' +
                             str(nowInfo) + ';' + str(learnedInfo) + ';\n')

    def save_game(self):
        os.system("ruby writer.rb \"%s\" \"%s\"" % (self.game_states,
                                                    self.gam_string))

    def bad_parser(self, winner, file):
        data = filearr(self.data)
        for line in data:
            point = list(line.split(";"))
            if point[0] != winner:
                data.remove(line)
        for line in data:
            datap = list(line.split(";"))
            lettersKnown = 0
            lettersNot = 0
            alpha = ast.literal_eval(datap[2])
            for lett in alpha:
                if alpha[lett][1] == -1:
                    lettersNot += 1
                elif alpha[lett][1] == 1:
                    lettersKnown += 1
            self.states_file.write(datap[1] + ";" + str(lettersKnown)
                                   + ";" + str(lettersNot) + ";"
                                   + datap[3] + ";\n")

    def parser(self, winner):
        os.system("ruby parser.rb %s %s" % (winner, self.gam_string))

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
            self.save_game()
            self.game_states = ""
            if game != 1:
                self.gam.write("=")
            game_over = False
            winner = None
            turn = 1
            while not game_over:
                guess1 = p1.guess_complex(p1.get_current_state(turn), turn)
                eval1 = p2.eval_guess(guess1[1])
                p1.update_lists(guess1[1], eval1, 'p1')
                p1.update_alphabet(guess1[1], eval1)
                self.record_player_state(p1, game, guess1[0], guess1[1],
                                         eval1, '1', str(turn))
                if guess1[1] != p2.choice:
                    guess2 = p2.guess_complex(p2.get_current_state(turn),
                                              turn)
                    eval2 = p1.eval_guess(guess2[1])
                    p2.update_lists(guess2[1], eval2, 'p2')
                    p2.update_alphabet(guess2[1], eval2)
                    self.record_player_state(p2, game, guess2[0], guess2[1],
                                             eval2, '2', str(turn))
                    if guess2[1] == p1.choice:
                        print "p2 wins"
                        game_over = True
                        winner = "2"
                else:
                    print "p1 wins"
                    game_over = True
                    winner = "1"
                turn += 1
            self.save_game()
            self.game_states = ""
            game += 1
            elapsed = time.time() - start_time
            self.time_file.write(str(round(elapsed, 3))
                                 + ":" + str(turn - 1) + ":"
                                 + str(int((turn - 1) / elapsed))
                                 + ":" + winner + "\n")
            self.parser(winner)

    def get_average(self):
        timearr = filearr(self.time_file)
        times = []
        for timea in timearr:
            times.append(int(timea.split(":")[1]))
        first_hun = times[0:99]
        last_hun = times[-99:]
        first_avg = np.average(first_hun)
        last_avg = np.average(last_hun)
        print(str(first_avg) + "::" + str(last_avg))

    def get_guess(self):
        isGood = False
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        wordlist = filearr('words/words.txt')[:]
        while not isGood:
            word = raw_input("Enter a valid guess (5 letters, "
                             + "no non-letter characters): ")
            isGood = True
            word = word.lower()
            if len(word) != 5:
                isGood = False
            for lett in word:
                if lett not in alphabet:
                    isGood = False
            if word not in wordlist:
                isGood = False
            if not isGood:
                os.system("clear")
                print(red("Your guess is invalid."))
                raw_input("Press [ENTER] to go back to guessing.")
                os.system("clear")
        return word

    def get_eval(self, guess):
        isGood = False
        nums = ['0', '1', '2', '3', '4', '5']

        while not isGood:
            print("My guess is: %s" % (guess))
            evaluation = raw_input("Evaluate my guess (an integer 0-5): ")
            isGood = True
            if evaluation not in nums:
                if evaluation.lower() == 'true':
                    return "Same"
                isGood = False
                os.system("clear")
                print(red("Your evaluation is invalid."))
                raw_input("Press [ENTER] to go back to guess evaluation.")
                os.system("clear")
            elif int(evaluation) > len(sorted(set(guess))):
                isGood = False
                os.system("clear")
                print(red("Your evaluation is invalid."))
                raw_input("Press [ENTER] to go back to guess evaluation.")
                os.system("clear")
        return int(evaluation)

    def play_human(self):
        # Play against a human
        comp = Computer()
        game_over = False
        os.system("clear")
        print("The game is about to begin. Good luck...")
        time.sleep(1)
        os.system("clear")
        print("First, choose your word. My word is " + comp.choice + ".")
        raw_input("Press [ENTER] once you have chosen a word.")
        os.system("clear")
        turn = 0
        while not game_over:
            turn += 1
            guess1 = self.get_guess()
            eval1 = comp.eval_guess(guess1)
            print "My evaluation of your guess: %s" % (eval1)
            raw_input("Press [ENTER] to continue.")
            os.system("clear")
            if guess1 != comp.choice:
                guess2 = comp.guess()
                if turn == 1:
                    print(red("NOTE: When you evaluate a guess, "
                              + "only count repeated "
                              + "letters once. If the guess is the same as "
                              + "your word, reply 'true'. "))
                    print(red("CAUTION: If your evaluation is incorrect, "
                          + "the program might break."))
                    raw_input("Press [ENTER] to continue.")
                    os.system("clear")
                eval2 = self.get_eval(guess2[1])
                os.system("clear")
                # print comp.possible
                if eval2 == "Same":
                    os.system("clear")
                    print(green("Ha! I beat you!"))
                    print("My word was " + comp.choice + ".")
                    raw_input("Press [ENTER] to leave the game.")
                    game_over = True
                    os.system("clear")
                else:
                    comp.update_lists(guess2[1], eval2, 'comp')
                    comp.update_alphabet(guess2[1], eval2)
            else:
                os.system("clear")
                print(green("You won!"))
                print("I had " + str(len(comp.possible)) + " words in my "
                      + "possible word list.")
                raw_input("Press [ENTER] to leave the game.")
                game_over = True
                os.system("clear")


def check_average():
    timearr = filearr("states/turntime.txt")
    times = []
    for timea in timearr:
        times.append(int(timea.split(":")[1]))
    first_hun = times[0:99]
    last_hun = times[-99:]
    first_avg = np.average(first_hun)
    last_avg = np.average(last_hun)
    print(str(first_avg) + "::" + str(last_avg))


def main():
    game = Learning()
    game.play_human()


def train(games):
    i = 0
    while i < games:
        game = Learning()
        game.play()
        cleanup()
        i += 1


if __name__ == "__main__":
    main()
