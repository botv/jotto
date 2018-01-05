words = File.readlines('words.txt')

words.each_with_index do |word, index|
  words[index] = word.chop
end

File.open("word_files/words_with_repeats.txt", "w+") do |f|
  words.each { |element| f.puts(element) }
end
