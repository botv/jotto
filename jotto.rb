def pickWord()
  word = nil
  File.foreach("words.txt").each_with_index do |line, index|
    word = line if rand < 1.0/(index+1)
  end
  return word
end

def generateGuesses()
  File.open("words.txt").each do |line|
    if (line.split("").to_a.uniq.length) == 5
      File.open("guesses.txt", "w") do |file|
        file.write("#{line}")
      end
    end
  end
end


def play()
  word = pickWord()
  guesses = nil
end

generateGuesses()
