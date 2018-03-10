# The Jottobot
# Ben Botvinick & Robert May, 2018

import random
import string
import time
import ast
import os
import Tkinter as tk
import numpy as np


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


def blue(text):
    return (u"\u001b[36m"
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
        self.last_guess = ""

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
        return random.choice(self.possible)

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

    def strat4(self):
        # Make a guess similar to the last guess with unknown letters
        if self.last_guess == "":
            return random.choice(self.norepeat)
        unknownLetsInLast = ""
        for lett in self.last_guess:
            if self.alphabet[lett][1] == 0:
                unknownLetsInLast += lett
        knownLetsInLast = ""
        for lett in self.last_guess:
            if lett not in unknownLetsInLast:
                knownLetsInLast += lett
        ind = 0
        run = True
        evalGoal = 4
        while run:
            if ind >= len(self.norepeat):
                ind = 0
                evalGoal -= 1
            if evalGoal == 0:
                return random.choice(self.norepeat)
                run = False
            check = (self.eval_flex(sorted(set(unknownLetsInLast)),
                     self.norepeat[ind]) == evalGoal
                     and self.eval_flex(sorted(set(knownLetsInLast)),
                     self.norepeat[ind]) == 0)
            if check:
                return self.norepeat[ind]
                run = False
            ind += 1

    def eval_guess(self, guess):
        # Counts common letters between choice and guess
        common = 0
        for letter in set(guess):
            common += self.choice.count(letter)
        return common

    def eval_flex(self, lets, guess):
        common = 0
        for letter in set(guess):
            common += lets.count(letter)
        return common

    def guess(self):
        # Chooses a strategy with simple probability
        # Deprecated since creation of guess_complex()
        prob1 = 1 / 4.0
        prob2 = 1 / 4.0
        prob3 = 1 / 4.0
        prob4 = 1 / 4.0
        strat = np.random.choice(['strat1', 'strat2', 'strat3', 'strat4'],
                                 1,
                                 p=[prob1, prob2, prob3, prob4])
        guess = getattr(self, strat[0])()
        return [strat[0], guess]

    def test_guess(self, turn):
        # Temporary guess function for testing
        if turn < 21:
            return ['strat1', self.strat1()]
        else:
            return ['strat2', self.strat2()]

    def get_current_state(self, turn):
        # Evaluates the current state of the game
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

    def guess_complex(self, turn):
        # A better guessing function with complex probability
        # Deprecated since creation of guess_vs()
        if len(self.possible) < 4:
            return ['strat2', self.strat2()]
        states_arr = filearr("states/states.txt")
        weights = []
        successes = {
                        'strat1': 0,
                        'strat2': 0,
                        'strat3': 0,
                        'strat4': 0
                    }
        total_success = 0.0
        current_state = self.get_current_state(turn)
        for state in states_arr:
            state = state.split(";")
            strat_choice = state.pop(-1)
            scaled_success = state.pop(-2)
            if state == current_state:
                total_success += scaled_success
                successes[strat_choice] += scaled_success
                weights.append(strat_choice)
        if len(weights) != 0:
            part_weight_c = (0.2 / float(len(weights))) / 2
            part_weight_s = (0.2 / float(total_success)) / 2
            prob1 = (0.2 + ((((part_weight_c * (weights.count('strat1'))) * 3)
                     + ((part_weight_s * (successes['strat1'])) * 5)) / 8))
            prob2 = (0.2 + ((((part_weight_c * (weights.count('strat2'))) * 3)
                     + ((part_weight_s * (successes['strat2'])) * 5)) / 8))
            prob3 = (0.2 + ((((part_weight_c * (weights.count('strat3'))) * 3)
                     + ((part_weight_s * (successes['strat3'])) * 5)) / 8))
            prob4 = (0.2 + ((((part_weight_c * (weights.count('strat4'))) * 3)
                     + ((part_weight_s * (successes['strat4'])) * 5)) / 8))
        else:
            prob1 = 1 / 4.0
            prob2 = 1 / 4.0
            prob3 = 1 / 4.0
            prob4 = 1 / 4.0
        strat = np.random.choice(['strat1', 'strat2', 'strat3', 'strat4'], 1,
                                 p=[prob1, prob2, prob3, prob4])
        guess = getattr(self, strat[0])()
        return [strat[0], guess]

    def guess_vs(self, turn):
        # A better guessing function
        if len(self.possible) < 4:
            return ['strat2', self.strat2()]
        states_arr = filearr("states/states.txt")
        weights = []
        successes = {'strat1': 0, 'strat2': 0, 'strat3': 0, 'strat4': 0}
        total_success = 0.0
        current_state = self.get_current_state(turn)
        for state in states_arr:
            state = state.split(";")
            strat_choice = state.pop(-1)
            scaled_success = state.pop(-2)
            if state == current_state:
                total_success += scaled_success
                successes[strat_choice] += scaled_success
                weights.append(strat_choice)
        if len(weights) != 0:
            part_weight_c = (0.2 / float(len(weights))) / 2
            part_weight_s = (0.2 / float(total_success)) / 2
            prob1 = (0.2 + ((((part_weight_c * (weights.count('strat1'))) * 5)
                     + ((part_weight_s * (successes['strat1'])) * 3)) / 8))
            prob2 = (0.2 + ((((part_weight_c * (weights.count('strat2'))) * 5)
                     + ((part_weight_s * (successes['strat2'])) * 3)) / 8))
            prob3 = (0.2 + ((((part_weight_c * (weights.count('strat3'))) * 5)
                     + ((part_weight_s * (successes['strat3'])) * 3)) / 8))
            prob4 = (0.2 + ((((part_weight_c * (weights.count('strat4'))) * 5)
                     + ((part_weight_s * (successes['strat4'])) * 3)) / 8))
            weightDict = {
                            'strat1': prob1,
                            'strat2': prob2,
                            'strat3': prob3,
                            'strat4': prob4
                         }
            weightList = []
            for key, value in sorted(weightDict.iteritems(),
                                     key=lambda (k, v): (v, k)):
                weightList.append("%s:%s" % (key, value))
            strat = weightList.reverse()[0].split(":")[0]
            guess = getattr(self, strat)()
            return [strat, guess]
        else:
            prob1 = 1 / 4.0
            prob2 = 1 / 4.0
            prob3 = 1 / 4.0
            prob4 = 1 / 4.0
            strat = np.random.choice(['strat1', 'strat2', 'strat3', 'strat4'],
                                     1,
                                     p=[prob1, prob2, prob3, prob4])
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

    def update_alphabet(self, guess, common, checkBreak):
        # Super important function that updates the alphabet every turn
        self.last_guess = guess
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
            if len(self.possible) == 0 and checkBreak:
                os.system("clear")
                print(red("There are no remaining possible words."))
                time.sleep(1)
                print(red("You either cheated or are just an idiot."))
                time.sleep(1)
                print(red("Your evaluations were: "))
                for guess, evall in self.own_guesses.iteritems():
                    print(blue("%s: %s" % (guess, evall)))
                raw_input("Press [ENTER] to leave the game.")
                os.system("clear")
                quit()


class Evaluator:
    def load_test1(self):
        # Deprecated since creation of load_test2
        root = tk.Tk()
        root.title("Evaluation Tool")
        root.minsize(400, 400)
        root.maxsize(400, 400)
        root.resizable(width=False, height=False)
        hidden = tk.Entry(root, text="Hidden").grid(row=0, column=0)
        hidden.pack(side='bottom')
        guess = tk.Entry(root, text="Hidden").grid(row=0, column=1)
        guess.pack(side='bottom')
        submit = tk.Button(root, text="Close",
                           command=root.quit).grid(row=0, column=2)
        submit.pack(side='bottom')
        close = tk.Button(root, text="Close",
                          command=root.quit).grid(row=0, column=3)
        close.pack(side='bottom')
        root.mainloop()

    def load_test2(self):
        # Deprecated since creation of load_test3
        r = 0
        hidden = tk.Entry(width=5)
        hidden.pack()
        hidden.focus_set()
        guess = tk.Entry(width=5)
        guess.pack()
        guess.focus_set()

        def submit_data():
            common_val = hidden.get()
            guess_val = guess.get()
            print([common_val, guess_val])
        tk.Button(text='Submit', command=submit_data).grid(row=r,
                                                           column=2)
        tk.Button(text='Close', command=quit).grid(row=r, column=4)
        tk.mainloop()

    def load_test3(self):
        # Optional common letter evaluation tool
        root = tk.Tk()
        root.title("Jotto Evaluation Tool")
        root.resizable(width=False, height=False)
        options = tk.Frame(root)
        options.pack(side='top')
        # output = tk.Frame(root)
        # output.pack(side='bottom')
        hidden_val = tk.StringVar()
        guess_val = tk.StringVar()
        output_label = tk.Label(options, text="Hidden:")
        output_label.pack(side='left')
        hidden = tk.Entry(options, textvariable=guess_val, width=8)
        hidden.pack(side='left')
        hidden.focus_set()
        output_label = tk.Label(options, text="Guess:")
        output_label.pack(side='left')
        guess = tk.Entry(options, textvariable=hidden_val, width=8)
        guess.pack(side='left')
        guess.focus_set()
        common = tk.StringVar()

        def eval_guess():
            common_out = 0
            guess_eval = guess.get()
            choice = hidden.get()
            all_letters = guess_eval.isalpha() and choice.isalpha()
            if len(guess_eval) == 5 and len(choice) == 5 and all_letters:
                for letter in set(guess_eval):
                    common_out += choice.count(letter)
                    if common_out == 1:
                        common.set("There is 1 common letter.")
                    else:
                        common.set("There are " + str(common_out)
                                   + " common letters.")
            else:
                common.set("There's something wrong with your entry.")

        submit_button = tk.Button(options, text="Submit", width=5,
                                  command=eval_guess)
        submit_button.pack(side='left')
        close_button = tk.Button(options, text='Close', command=quit)
        close_button.pack(side='left')
        output_label = tk.Label(root, relief='sunken',
                                textvariable=common)
        output_label.pack(side='bottom', fill='both')
        tk.mainloop()


class JottoBot:
    def __init__(self):
        self.sessions = open('states/sessions.txt', 'r+')
        self.time_file = open('states/turntime.txt', 'a')
        self.states_file = open('states/states.txt', 'a+')
        self.sess_id = int(self.sessions.readline()) + 1
        self.gam = open('states/games/sess' + str(self.sess_id) + '.txt', 'w+')
        self.gam_string = 'states/games/sess' + str(self.sess_id) + '.txt'
        self.data = 'states/games/sess' + str(self.sess_id) + '.txt'
        self.game_states = ""

    def record_player_state(self,
                            player,
                            strategy,
                            guess,
                            common,
                            player_name,
                            turn):
        alphabetStr = str(player.alphabet).replace(':', '=>')
        nowInfo = 0
        for lett in player.alphabet:
            if player.alphabet[lett][1] == -1:
                nowInfo += 1
            elif player.alphabet[lett][1] == 1:
                nowInfo += 5
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
                guess1 = p1.guess_complex(turn)
                eval1 = p2.eval_guess(guess1[1])
                if guess1[1] != p2.choice:
                    p1.update_lists(guess1[1], eval1, 'p1')
                    p1.update_alphabet(guess1[1], eval1, True)
                    self.record_player_state(p1,
                                             guess1[0],
                                             guess1[1],
                                             eval1,
                                             '1',
                                             str(turn))
                    guess2 = p2.guess_complex(turn)
                    eval2 = p1.eval_guess(guess2[1])
                    if guess2[1] == p1.choice:
                        p2.update_lists(guess2[1], eval2, 'p2')
                        p2.update_alphabet(guess2[1], eval2, False)
                        self.record_player_state(p2,
                                                 guess2[0],
                                                 guess2[1],
                                                 eval2,
                                                 '2',
                                                 str(turn))
                        print("p2 wins")
                        game_over = True
                        winner = "2"
                    else:
                        p2.update_lists(guess2[1], eval2, 'p2')
                        p2.update_alphabet(guess2[1], eval2, True)
                        self.record_player_state(p2,
                                                 guess2[0],
                                                 guess2[1],
                                                 eval2,
                                                 '2',
                                                 str(turn))
                else:
                    p1.update_lists(guess1[1],
                                    eval1,
                                    'p1')
                    p1.update_alphabet(guess1[1],
                                       eval1,
                                       False)
                    self.record_player_state(p1,
                                             guess1[0],
                                             guess1[1],
                                             eval1,
                                             '1',
                                             str(turn))
                    print("p1 wins")
                    game_over = True
                    winner = "1"
                turn += 1
            self.save_game()
            self.game_states = ""
            game += 1
            elapsed = time.time() - start_time
            self.time_file.write(str(round(elapsed, 3))
                                 + ":"
                                 + str(turn - 1)
                                 + ":"
                                 + str(int((turn - 1) / elapsed))
                                 + ":"
                                 + winner
                                 + "\n")
            self.parser(winner)

    def play_for_success(self, games):
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
                guess1 = p1.guess_vs(turn)
                eval1 = p2.eval_guess(guess1[1])
                if guess1[1] != p2.choice:
                    p1.update_lists(guess1[1], eval1, 'p1')
                    p1.update_alphabet(guess1[1], eval1, True)
                    self.record_player_state(p1,
                                             guess1[0],
                                             guess1[1],
                                             eval1,
                                             '1',
                                             str(turn))
                    guess2 = p2.guess_vs(turn)
                    eval2 = p1.eval_guess(guess2[1])
                    if guess2[1] == p1.choice:
                        p2.update_lists(guess2[1], eval2, 'p2')
                        p2.update_alphabet(guess2[1], eval2, False)
                        self.record_player_state(p2,
                                                 guess2[0],
                                                 guess2[1],
                                                 eval2,
                                                 '2',
                                                 str(turn))
                        print("p2 wins")
                        game_over = True
                        winner = "2"
                    else:
                        p2.update_lists(guess2[1], eval2, 'p2')
                        p2.update_alphabet(guess2[1], eval2, True)
                        self.record_player_state(p2,
                                                 guess2[0],
                                                 guess2[1],
                                                 eval2,
                                                 '2',
                                                 str(turn))
                else:
                    p1.update_lists(guess1[1], eval1, 'p1')
                    p1.update_alphabet(guess1[1], eval1, False)
                    self.record_player_state(p1,
                                             guess1[0],
                                             guess1[1],
                                             eval1,
                                             '1',
                                             str(turn))
                    print("p1 wins")
                    game_over = True
                    winner = "1"
                turn += 1
            self.save_game()
            self.game_states = ""
            game += 1
            elapsed = time.time() - start_time
            self.time_file.write(str(round(elapsed, 3))
                                 + ":"
                                 + str(turn - 1)
                                 + ":"
                                 + str(int((turn - 1) / elapsed))
                                 + ":"
                                 + winner
                                 + "\n")
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
        is_good = False
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        wordlist = filearr('words/words.txt')[:]
        while not is_good:
            what_happened = []
            word = raw_input("Enter a valid guess (5 letters, "
                             + "no non-letter characters): ")
            is_good = True
            word = word.lower()
            if len(word) != 5:
                is_good = False
                what_happened.append(red("-does not meet length requirement "
                                     + "(5 letters)"))
            for lett in word:
                if lett not in alphabet:
                    is_good = False
                    what_happened.append(red("-non letter character \'"
                                             + lett + "\' used"))
            if word not in wordlist:
                is_good = False
                what_happened.append(red("-word does not exist"))
            if not is_good:
                os.system("clear")
                print(red("Your guess is invalid. Guess caught at:"))
                for catch in what_happened:
                    print("    %s" % (catch))
                raw_input("Press [ENTER] to go back to guessing.")
                os.system("clear")
        return word

    def get_eval(self, guess):
        is_good = False
        nums = ['0', '1', '2', '3', '4', '5']

        while not is_good:
            print("My guess is: %s" % (guess))
            evaluation = raw_input("Evaluate my guess (an integer 0-5): ")
            is_good = True
            what_happened = []
            if evaluation not in nums:
                if evaluation.lower() == 'true':
                    return "Same"
                is_good = False
                if evaluation.isdigit():
                    what_happened.append(red("-evaluation greater than five"))
                else:
                    what_happened.append(red("-non number character used"))
            if evaluation.isdigit():
                if int(evaluation) > len(sorted(set(guess))):
                    is_good = False
                    what_happened.append(blue("-evaluation greater than "
                                              + "amount of unique letters "
                                              + "in guess")
                                         + "\nTIP: only count "
                                         + "repeated letters once!")
            if not is_good:
                os.system("clear")
                print(red("Your evaluation is invalid. Evaluation caught at:"))
                for catch in what_happened:
                    print("    %s" % (catch))
                raw_input("Press [ENTER] to go back to guess evaluation.")
                os.system("clear")
        return int(evaluation)

    def play_human(self):
        # Play against a human
        comp = Computer()
        game_over = False
        os.system("clear")
        print("The game is about to begin. Good luck...")
        time.sleep(3)
        os.system("clear")
        print("First, choose your word.")
        raw_input("Press [ENTER] once you have chosen a word.")
        os.system("clear")
        turn = 0
        while not game_over:
            turn += 1
            guess1 = self.get_guess()
            eval1 = comp.eval_guess(guess1)
            if guess1 != comp.choice:
                print("My evaluation of your guess: %s" % (eval1))
                raw_input("Press [ENTER] to continue.")
                os.system("clear")
                guess2 = comp.guess_vs(turn)
                if turn == 1:
                    print("NOTE: When you evaluate a guess, "
                          + "only count repeated "
                          + "letters once. \n      If the guess is"
                          + " the same as "
                          + "your word, reply "
                          + "'true'.")
                    eval_tool = raw_input("Do you want to open "
                                          + "the evaluator tool in a "
                                          + "separate window? [y/n]: ")
                    continue_program = False
                    while not continue_program:
                        if eval_tool == "y":
                            evaluator = Evaluator()
                            evaluator.load_test3()
                            continue_program = True
                            print("started")
                        elif eval_tool == "n":
                            continue_program = True
                        else:
                            eval_tool = raw_input("\033[F\033[KPlease enter"
                                                  + " 'y' or 'n': ")
                    print(red("CAUTION: If your evaluation is incorrect, "
                              + "the program will break."))
                    raw_input("Press [ENTER] to continue.")
                    os.system("clear")
                eval2 = self.get_eval(guess2[1])
                os.system("clear")
                if eval2 == "Same":
                    os.system("clear")
                    print(green("I won!"))
                    print("My word was "
                          + comp.choice
                          + ".")
                    raw_input("Press [ENTER] to leave the game.")
                    game_over = True
                    os.system("clear")
                else:
                    comp.update_lists(guess2[1], eval2, 'comp')
                    comp.update_alphabet(guess2[1], eval2, True)
            else:
                os.system("clear")
                print(green("You won!"))
                print("I had "
                      + str(len(comp.possible))
                      + " words in my "
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


def play_success():
    game = JottoBot()
    game.play_for_success(1)


def play_normal():
    game = JottoBot()
    game.play(1)


def main():
    for i in range(0, 1000):
        play_normal()
    for i in range(0, 100):
        play_success()
    check_average()


if __name__ == "__main__":
    main()
