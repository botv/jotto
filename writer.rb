# def write(alphabet=ARGV[0], game=ARGV[1], strategy=ARGV[2], guess=ARGV[3], common=ARGV[4], gam_string=ARGV[5], player=ARGV[6], turn=ARGV[7])
#   alphabetStr = "{"
#   alphabet = eval(alphabet)
#   alphabet.each do |letter|
#     alphabetStr += "'#{letter[0]}'=> [#{letter[1][0]}, #{letter[1][1]}]"
#     if letter != 'z'
#       alphabetStr += ", "
#     end
#   end
#   alphabetStr += "}"
#   File.open(gam_string, 'a+') {|file| file << (player + ";" + turn + ";" + alphabetStr.to_s + ";" + guess + ";" + common.to_s + "\n")}
# end

def writer(str=ARGV[0], filename=ARGV[1])
  File.open(filename, 'a+') {|file| file << str}
end

writer()
