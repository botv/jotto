# AlphaJotto
# Ben Botvinick & Robert May, 2018

import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import string
import sys
import time


class Utils:
    def filearr(filename):
        # Turn a folder into an array
        words = [line.rstrip("\n") for line in open(filename)]
        return(words)

    def color(color, text):
        colors = {
            "red": "\u001b[31m",
            "green": "\u001b[32m",
            "blue": "\u001b[36m"
        }
        color = colors[color]
        return(u"%s%s\u001b[0m" % (color, text))

    def ellipsis(text, seconds):
        print(text, end="")
        period = seconds / 3
        sys.stdout.flush()
        time.sleep(period)
        for i in range(3):
            print(".", end="")
            sys.stdout.flush()
            time.sleep(period)

    def truncate(filename):
        with open(filename, "w") as f:
            f.truncate()

    def parser():
        parser = argparse.ArgumentParser(prog="jotto")
        parser.add_argument("--train", metavar="GAMES", type=int, default=2000,
                            help="train the agent")
        args = parser.parse_args()
        return args

    def graph_training():
        turns = []
        timearr = Utils.filearr("jotto_files/turntime.txt")
        i = 0
        for timea in timearr:
            turns.append(int(timea.split(":")[1]))
            i += 1
        plt.plot(turns)
        plt.axis([0, len(timearr), 0, max(turns) + 5])
        plt.ylabel("Turns in game")
        plt.xlabel("Game")
        plt.title("Turns Taken in Each Game")
        plt.show()


class Player:
    def __init__(self):
        alphalist = list(string.ascii_lowercase)
        self.alphabet = {}
        for letter in alphalist:
            self.alphabet[letter] = [0, 0, []]
        self.words = Utils.filearr("word_files/words.txt")[:]
        self.for_guessing = self.words[:]
        self.norepeat = Utils.filearr("word_files/words_no_repeats.txt")[:]
        self.repeat = Utils.filearr("word_files/words_repeats.txt")[:]
        self.common_words = Utils.filearr("word_files/common_words.txt")[:]
        self.choice = np.random.choice(self.norepeat)
        self.own_guesses = {}
        self.possible = self.norepeat[:]
        self.last_guess = ""
        self.states = []

    def strat1(self):
        # Cover as many letters as possible
        if len(self.own_guesses) is not 0:
            letters = []
            for guess in self.own_guesses:
                for letter in list(guess):
                    letters.append(letter)
            letters = sorted(set(letters))
            if len(letters) > 20:
                guess = np.random.choice(self.for_guessing)
                return(guess)
            run = True
            ind = 0
            while run:
                if len(letters) == 0:
                    guess = np.random.choice(self.for_guessing)
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
            guess = np.random.choice(self.for_guessing)
        if guess:
            return(guess)

    def strat2(self):
        # Make the best possible guess
        return(np.random.choice(self.possible))

    def strat3(self):
        # Make a guess to find information on a letter
        somehowKnownLetters = []
        for lett in self.alphabet:
            if self.alphabet[lett][1] != 0:
                somehowKnownLetters.append(lett)
        if len(somehowKnownLetters) == 0:
            return(np.random.choice(self.for_guessing))
        otherLetsRequired = 1
        ind = 0
        run = True
        while run:
            if ind >= len(self.for_guessing):
                ind = 0
                otherLetsRequired += 1
            if otherLetsRequired == 5:
                return(np.random.choice(self.for_guessing))
                run = False
            word = self.for_guessing[ind]
            otherCount = 0
            for lett in word:
                if lett not in somehowKnownLetters:
                    otherCount += 1
            if otherCount == otherLetsRequired:
                return(word)
                run = False
            ind += 1

    def strat4(self):
        # Make a guess similar to the last guess with unknown letters
        if self.last_guess == "":
            return(np.random.choice(self.norepeat))
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
                return(np.random.choice(self.norepeat))
                run = False

            def eval_flex(lets, guess):
                common = 0
                for letter in set(guess):
                    common += lets.count(letter)
                return(common)
            check = (eval_flex(sorted(set(unknownLetsInLast)),
                               self.norepeat[ind]) == evalGoal
                     and eval_flex(sorted(set(knownLetsInLast)),
                                   self.norepeat[ind]) == 0)
            if check:
                return(self.norepeat[ind])
                run = False
            ind += 1

    def eval_guess(self, guess):
        # Counts common letters between choice and guess
        common = 0
        for letter in set(guess):
            common += self.choice.count(letter)
        return(common)

    def update_lists(self, guess, common, check_break):
        self.update_alphabet(guess, common, check_break)
        if len(sorted(set(guess))) == len(guess):
            self.norepeat.remove(guess)
        else:
            self.repeat.remove(guess)
        self.for_guessing.remove(guess)
        if guess in self.possible:
            self.possible.remove(guess)

    def explore(self):
        # For off-policy learning
        strat_id = np.random.randint(1, 5)
        return(["strat%i" % strat_id, getattr(self, "strat%i" % strat_id)()])

    def exploit(self):
        f = open("./jotto_files/states.txt", "r")
        full = f.readlines()
        finalExclusive = []
        final = {}
        for line in full:
            splitLine = line.split(">")
            finalExclusive.append(splitLine[0])
            exec("final[splitLine[0]] = %s" % (splitLine[1]))
        f.close()
        state = self.get_current_state(" ")[0:-2]
        if state not in finalExclusive:
            stratCount = 4.0
            strat = np.random.choice(["strat1", "strat2", "strat3", "strat4"],
                                     p=[1 / stratCount] * int(stratCount))
            guess = getattr(self, strat)()
        else:
            weightList = final[state]
            strat = self.get_strat(weightList)
            guess = getattr(self, strat)()
        return([strat, guess])

    def get_strat(self, weights):
        maxi = [weights[0]]
        maxInd = [0]
        i = 0
        for weight in weights:
            if weight > maxi[0]:
                maxi = [weight]
                maxInd = [i]
            elif weight == maxi[0]:
                maxInd.append(i)
            i += 1
        # print(weights, )
        # print(maxi, )
        # print(maxInd, )
        choice = np.random.choice(maxInd)
        # print(choice)
        strat = "strat" + str(choice + 1)
        # print(strat)
        return(strat)

    def get_current_state(self, strat):
        state = []
        known = 0
        known_not = 0
        for lett in self.alphabet:
            if self.alphabet[lett][1] == 1:
                known += 1
            elif self.alphabet[lett][1] == -1:
                known_not += 1
        state.append(known)
        state.append(known_not)
        state.append(known + known_not)
        state.append(strat[-1])
        state_str = ""
        for info in state:
            state_str += str(info) + ";"
        state_str = state_str[0:-1]
        return(state_str)

    def update_possible(self):
        # Updates list of possible words
        known = []
        known_not = []
        for lett in self.alphabet:
            if self.alphabet[lett][1] == 1:
                known.append(lett)
            elif self.alphabet[lett][1] == -1:
                known_not.append(lett)
        ind = 0
        changed = False
        while ind < len(self.possible):
            word = self.possible[ind]
            known_ind = 0
            removed = False
            while known_ind < len(known) and not removed:
                let = known[known_ind]
                if let not in word:
                    self.possible.remove(word)
                    ind -= 1
                    removed = True
                    changed = True
                known_ind += 1
            known_not_ind = 0
            while known_not_ind < len(known_not) and not removed:
                let = known_not[known_not_ind]
                if let in word:
                    self.possible.remove(word)
                    ind -= 1
                    removed = True
                    changed = True
                known_not_ind += 1
            ind += 1
        return(changed)

    def eliminate_letter(self, let):
        letter = self.alphabet[let]
        if letter[1] == -1:
            return(False)
        letterInPossible = False
        ind = 0
        knownLets = []
        for lett in self.alphabet:
            if self.alphabet[lett][1] == 1:
                knownLets.append(lett)
        if let in knownLets:
            return(True)
        if len(knownLets) == 5:
            return(False)
        for guess in letter[2]:
            unknownLetsInGuess = self.own_guesses[guess]
            for lett in knownLets:
                if lett in guess:
                    unknownLetsInGuess -= 1
            if unknownLetsInGuess == 0:
                return(False)
        while ind < len(self.possible) and not letterInPossible:
            word = self.possible[ind]
            if let in word:
                letterInPossible = True
            ind += 1
        if not letterInPossible:
            return(False)
        return(True)

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
            return(False)
        else:
            return(knownLets)

    def update_alphabet(self, guess, common, check_break):
        # Super important function that updates the alphabet every turn
        self.last_guess = guess
        self.own_guesses[guess] = common
        for letter in set(guess):
            if not self.eliminate_letter(letter):
                self.alphabet[letter][1] = -1
            self.alphabet[letter][2].append(guess)
            self.alphabet[letter][0] += 1
        finding = True
        eliminating = True
        updating = True
        while finding or eliminating or updating:
            updating = self.update_possible()
            find_known_letters = self.find_known_letters()
            if find_known_letters is False:
                finding = False
            else:
                for letter in find_known_letters:
                    self.alphabet[letter][1] = 1
            eliminating = False
            for letter in self.alphabet:
                if (not self.eliminate_letter(letter) and
                        self.alphabet[letter][1] != -1):
                    self.alphabet[letter][1] = -1
                    eliminating = True
            if len(self.possible) == 0 and check_break:
                os.system("clear")
                print(Utils.color("red",
                                  "There are no remaining possible words."))
                time.sleep(1)
                print(Utils.color("red",
                                  "You either cheated or are just an idiot."))
                time.sleep(1)
                print(Utils.color("red",
                                  "Your evaluations were: \n"))
                for guess, evall in self.own_guesses.items():
                    print("%s: %s" % (guess, evall))
                str(input("\nPress [ENTER] to leave the game."))
                os.system("clear")
                quit()


class Learning:
    def __init__(self):
        self.time_file_path = "jotto_files/turntime.txt"
        self.time_file = open("jotto_files/turntime.txt", "a+")
        self.game_states = ""

    def train(self, games):
        Utils.truncate(self.time_file_path)
        i = 0
        while i < games:
            self.play("explore")
            self.play("exploit", write=True)
            i += 1

    def play(self, style, write=False):
        start_time = time.time()
        p1 = Player()
        p2 = Player()
        winner = None
        turn = 1
        while not winner:
            guess1 = getattr(p1, style)()
            eval1 = p2.eval_guess(guess1[1])
            if guess1[1] != p2.choice:
                p1.update_lists(guess1[1], eval1, True)
                p1.states.append(p1.get_current_state(guess1[0]))
                guess2 = getattr(p2, style)()
                eval2 = p1.eval_guess(guess2[1])
                if guess2[1] == p1.choice:
                    p2.update_lists(guess2[1], eval2, False)
                    p2.states.append(p2.get_current_state(guess2[0]))
                    print("p2 wins")
                    winner = "p2"
                    self.conclude(p2.states, p1.states, 4)
                else:
                    p2.update_lists(guess2[1], eval2, True)
                    p2.states.append(p2.get_current_state(guess2[0]))
            else:
                p1.update_lists(guess1[1], eval1, False)
                p1.states.append(p1.get_current_state(guess1[0]))
                print("p1 wins")
                winner = "p1"
                self.conclude(p1.states, p2.states, 4)
            turn += 1
        elapsed = time.time() - start_time
        if write:
            self.time_file.write(str(round(elapsed, 1.5))
                                 + ":"
                                 + str(turn - 1)
                                 + ":"
                                 + winner
                                 + "\n")

    def get_states(self):
        f = open("./jotto_files/states.txt", "r")
        full = f.readlines()
        finalExclusive = []
        final = {}
        for line in full:
            splitLine = line.split(">")
            finalExclusive.append(splitLine[0])
            exec("final[splitLine[0]] = %s" % (splitLine[1]))
        f.close()
        return(final, finalExclusive)

    def change_weights(self, strat, reward, weights):
        # print(reward, weights[strat])
        weights[strat] += 0.01 * (reward - weights[strat])
        return(weights)

    def conclude(self, winner, loser, strat_count):
        states, states_exclusive = self.get_states()
        players = [loser, winner]
        r = 0
        while r < 2:
            for state in players[r]:
                state_list = state.split(";")
                strat = int(state_list[-1]) - 1
                state_temp = ""
                j = 0
                while j < len(state_list) - 1:
                    state_temp += state_list[r] + ";"
                    j += 1
                state = state_temp[0:-1]
                if state not in states_exclusive:
                    states[state] = [0.5] * strat_count
                else:
                    states[state] = self.change_weights(strat,
                                                        r,
                                                        states[state])
            r += 1
        full_str = ""
        for state in states:
            full_str += state + ">" + str(states[state]) + "\n"
        f = open("./jotto_files/states.txt", "w")
        f.write(full_str)
        f.close()

    def get_average(self, explore, exploit):
        timearr = Utils.filearr(self.time_file_path)
        times = []
        for timea in timearr:
            times.append(int(timea.split(":")[1]))
        first_bit = times[0:explore]
        last_bit = times[-exploit:]
        first_avg = np.average(first_bit)
        last_avg = np.average(last_bit)
        return(str(first_avg) + "::" + str(last_avg))


class Interactive:
    def get_guess(self):
        is_good = False
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        wordlist = Utils.filearr("word_files/words.txt")[:]
        while not is_good:
            catches = []
            word = str(input("Enter a valid guess (5 letters, "
                             + "no non-letter characters): "))
            is_good = True
            word = word.lower()
            if len(word) != 5:
                is_good = False
                catches.append(Utils.color("red",
                                           "-does not meet"
                                           + "length requirement "
                                           + "(5 letters)"))
            for lett in word:
                if lett not in alphabet:
                    is_good = False
                    catches.append(Utils.color("red",
                                               "-non letter character '"
                                               + lett
                                               + "' used"))
            if word not in wordlist:
                is_good = False
                catches.append(Utils.color("red",
                                           "-word does not exist"))
            if not is_good:
                os.system("clear")
                print(Utils.color("red",
                                  "Your guess is invalid. Guess caught at:"))
                for catch in catches:
                    print("    %s" % (catch))
                str(input("Press [ENTER] to go back to guessing."))
                os.system("clear")
        return(word)

    def get_eval(self, guess):
        is_good = False
        nums = ["0", "1", "2", "3", "4", "5"]
        while not is_good:
            print("My guess is: %s" % (guess))
            evaluation = str(input("Evaluate my guess (an integer 0-5): "))
            is_good = True
            catches = []
            if evaluation not in nums:
                if evaluation.lower() == "true":
                    return(-1)
                is_good = False
                if evaluation.isdigit():
                    catches.append(Utils.color("red",
                                               "-evaluation greater "
                                               + "than five"))
                else:
                    catches.append(Utils.color("red",
                                               "-non number "
                                               + "character used"))
            if evaluation.isdigit():
                if int(evaluation) > len(sorted(set(guess))):
                    is_good = False
                    catches.append(Utils.color("red",
                                               "-evaluation greater than "
                                               + "amount of unique letters "
                                               + "in guess")
                                   + "\nTIP: only count "
                                   + "repeated letters once!")
            if not is_good:
                os.system("clear")
                print(Utils.color("red",
                                  "Your evaluation is invalid. "
                                  + "Evaluation caught at:"))
                for catch in catches:
                    print("    %s" % (catch))
                str(input("Press [ENTER] to go back to guess evaluation."))
                os.system("clear")
        return(int(evaluation))

    def play(self):
        try:
            comp = Player()
            game_over = False
            game_results = {
                "winner": str(),
                "my_word": comp.choice,
                "guesses": int(),
                "p1_guesses": {},
                "p2_guesses": {}
            }
            os.system("clear")
            Utils.ellipsis("The game is about to begin. Good luck", 1.5)
            os.system("clear")
            print("First, choose your word.")
            str(input("Press [ENTER] once you have chosen a word."))
            os.system("clear")
            turn = 0
            while not game_over:
                turn += 1
                guess1 = self.get_guess()
                eval1 = comp.eval_guess(guess1)
                game_results["p1_guesses"][str(guess1)] = eval1
                if guess1 != comp.choice:
                    print("My evaluation of your guess: %s" % (eval1))
                    str(input("Press [ENTER] to continue."))
                    os.system("clear")
                    guess2 = comp.exploit()
                    if turn == 1:
                        print("NOTE: When you evaluate a guess, "
                              + "only count repeated "
                              + "letters once. \n      If the guess is"
                              + " the same as "
                              + "your word, reply "
                              + "'true'.")
                        print(Utils.color("red",
                                          "CAUTION: If your evaluation is "
                                          + "incorrect, the program "
                                          + "will break."))
                        str(input("Press [ENTER] to continue."))
                        os.system("clear")
                    eval2 = self.get_eval(guess2[1])
                    game_results["p2_guesses"][str(guess2)] = eval2
                    os.system("clear")
                    if eval2 == -1:
                        os.system("clear")
                        print(Utils.color("green", "I won!"))
                        game_results["winner"] = "Player"
                        print("My word was "
                              + comp.choice
                              + ".")
                        str(input("Press [ENTER] to leave the game."))
                        game_over = True
                        os.system("clear")
                    else:
                        comp.update_lists(guess2[1], eval2, True)
                else:
                    os.system("clear")
                    print(Utils.color("green", "You won!"))
                    game_results["winner"] = "Human"
                    print("I had "
                          + str(len(comp.possible))
                          + " words in my "
                          + "possible word list.")
                    str(input("Press [ENTER] to leave the game."))
                    game_over = True
                    os.system("clear")
            game_results["guesses"] = len(game_results["p1_guesses"])
            showGraph = str(input("Show graph of improvement? [y/n]: "))
            if showGraph[0].lower() == "y":
                Utils.graph_training()
            return(game_results)
        except KeyboardInterrupt:
            os.system("clear")
            Utils.ellipsis("Aborting", 3)
            os.system("clear")


def main():
    args = Utils.parser()
    if args.train:
        agent = Learning()
        agent.train(args.train)
    else:
        agent = Interactive()
        agent.play()


if __name__ == "__main__":
    main()
