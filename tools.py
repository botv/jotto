def filegrab(file):
    words = [line.rstrip('\n') for line in open(file)]
    return words
