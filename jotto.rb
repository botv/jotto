def rules()
  puts File.read("gameplay.txt")
end

def pickWord()
  word = nil
  File.foreach("words.txt").each_with_index do |line, index|
    word = line if rand < 1.0/(index+1)
  end
  return word
end

rules()
