def writer(str=ARGV[0], filename=ARGV[1])
  File.open(filename, 'a+') {|file| file << str}
end

writer()
