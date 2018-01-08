# Just some cleanup in case the training data is taking up too much space.

import os

time_file = open('states/turntime.txt', 'a')
sessions = open('states/sessions.txt', 'r+')

sessions.seek(0)
sessions.truncate()
sessions.write("0")

time_file.seek(0)
time_file.truncate()

os.system("rm states/games/*")
