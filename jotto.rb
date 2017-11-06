def getGuess(myWords) # Pick a word, any word
  guess = words[rand(0..(guesses.length - 1)]
  return guess
end

def getWords()
  arr = Array.new
  File.open("words.txt").each_line do |line|
    arr.push(line)
  end
end

def takeGuess(playerWords, words)
  print "Guess a five letter word "
  guess = gets.chomp
  if playerWords.include?(guess) && words.include?(guess)
    return guess
  elsif playerWords.include?(guess) == false && words.include?(guess)
    print "You guessed that word already. Try again! "
    return takeGuess(playerWords, words)
  elsif playerWords.include?(guess) && words.include?(guess) == false
    print "That is not a word in the English language. Try again! "
    return takeGuess(playerWords, words)
  end
end

def inCommon(secret, playerGuess)
  sum = 0
  playerGuess.split(" ").to_a.each do |i|
    if secret.split(" ").to_a.include?(i)
      sum += 1
    end
  end
  return sum
end

def play()
  words = getWords()
  myWords = getWords()
  playerWords = getWords()
  secret = words[rand(0..(guesses.length - 1)]
  data = Hash.new
  playerGuess = nil
  while playerGuess != secret && answer.between(0..5)
    playerGuess = takeGuess(playerWords, words)
    playerWords.delete(playerGuess)
    if playerGuess == secret
      print "Oh no! You win!"
    else
      print "Your guess and my word have #{inCommon(secret, playerGuess)}"
    end
    myGuess = getGuess()
    myWords.delete(myGuess)
    print "I guess...#{myGuess}. Enter 'true' or a number between 0 and 5 as your response."
    answer = gets.chomp
    answer = answer.to_i
    if answer.between?(0..5)
      data[myGuess] = answer
    else
      print "Yes! I win!"
    end
  end
end

play()
