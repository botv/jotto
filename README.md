# The Jottobot
## Gameplay
1. Each player chooses a five letter word with no repeating letters (keep it a secret!).
2. Players take turns guessing other five letter words. The other player then responds with a number between 1 and 5, indicating the number of common letters between his opponent's guess and his hidden word. For example, if one player's hidden word is 'spine' and his opponent guesses 'spoke', he would say '3'.
3. The game is over when a player guesses his opponent's hidden word.
## Playing the Jottobot
```
git clone https://github.com/biggomega/jotto.git
cd jotto
python jotto.py
```
## Strategies
The Jottobot has four main strategies:
1. Make a guess to get as much *new* information as possible.
2. Make a guess to get information on a particular letter.
3. Make an educated guess on the player's hidden word based on known information.
4. Make a guess that contains the unknown letters of the last guess.
## How it works
The Jottobot uses a number of learning algorithms to play Jotto. First of all, it plays itself to gain knowledge of the game. Once it has played itself a number of times, the guessing algorithm uses the success rates of the strategies in its training games to choose which strategy to choose ([see above](https://github.com/biggomega/jotto/blob/master/README.md#strategies)). After it chooses this strategy and gathers the player's evaluation, it calculates the success of the previous guess and uses that number in it's next turn.
