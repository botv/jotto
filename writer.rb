def write(alphabet=ARGV[0], game=ARGV[1], strategy=ARGV[2], guess=ARGV[3], common=ARGV[4], gam_string=ARGV[5])
  file = File.open(gam_string, 'a')
  alphabetStr = "{"
  alphabet = eval(alphabet)
  alphabet.each do |letter|
    alphabetStr += "'#{letter}'=> [#{alphabet[letter][0]}, #{alphabet[letter][1]}]"
    if letter != 'z'
      alphabetStr += ", "
    end
  end
  alphabetStr += "}"
  file.write(alphabetStr.to_s + ";" + guess + ";" + common.to_s + "\n")
end
