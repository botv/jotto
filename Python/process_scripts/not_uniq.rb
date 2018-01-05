words = File.readlines('../word_files/words.txt')

words.each_with_index do |word, index|
  words[index] = word.chop
end

File.open("../word_files/words_with_repeats.txt", "w+") do |f|
  words.each do |element|
    unless (element.downcase !~ /([a-z]).*\1/)
      f.puts(element)
    end
  end
end
