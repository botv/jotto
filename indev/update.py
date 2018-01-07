import string

alphalist = list(string.ascii_lowercase)
alphabet = {}
for letter in alphalist:
    alphabet[letter] = [0, 0, []]
words = tools.filegrab('words/words.txt')
for_guessing = words
norepeat = tools.filegrab('words/words_without_repeats.txt')
repeat = tools.filegrab('words/words_with_repeats.txt')
choice = random.choice(norepeat)
own_guesses = {}
received_guesses = {}
possible = norepeat


def update_possible(alphabet):
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
        knownNotLetsInd = 0
        while knownNotLetsInd < len(knownNotLets) and not wordRemoved:
            let = knownNotLets[knownNotLetsInd]
            if let in word:
                self.possible.remove(word)
                ind -= 1
                wordRemoved = True
