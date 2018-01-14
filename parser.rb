def read(file)
  words = []
  File.open(file).each do |line|
    words.push(line[0..line.length()-2])
  end
  return words[0..words.length-2]
end

def parser(winner=ARGV[0])
  data = read(ARGV[1])
  data_ind = 0
  while data_ind < data.length
    lin = data[data_ind]
    point = lin.split(";")
    if point[0] != winner
      data.delete_at(data_ind)
      data_ind -= 1
    end
    data_ind += 1
  end
  data.each do |line|
    datap = line.split(";")
    lettersKnown = 0
    lettersNot = 0
    alpha = eval(datap[2])
    alpha.each do |lett|
      if lett[1][1] == -1
        lettersNot += 1
      elsif lett[1][1] == 1
        lettersKnown += 1
      end
    end
    File.open("states/states.txt", 'a') { |file| file << (datap[1] + ";" + lettersKnown.to_s + ";" + lettersNot.to_s + ";" + datap[3] + ";\n") }
  end
end

parser(ARGV[0])
