import sys
import string as s
import re

filename = sys.argv[1]
lines = ''
with open(filename, 'r') as file:
    lines = file.readlines()

music = lines[4:]

# create a single string
music = ''.join(music)

# capitalize everything
music = music.translate(str.maketrans(s.ascii_lowercase, s.ascii_uppercase))

#copy music for bar duration analysis
note_lens = music

###################### RHYTHM CONVERSION ##################### 

# duration of each token in 8th notes
durations = {
    0: 2,
    1: 0.5,
    2: 2,
    3: 1
}

# token notation
tokens = {
    0: '(3xxx',
    1: 'x/2',
    2: 'x2',
    3: 'x'
}

# clean string
note_lens = re.sub('[^A-G0-9|:/(]', '', note_lens)
note_lens = re.sub('[A-G]', 'x', note_lens)

# replace x3 rhythm with xxx
note_lens = note_lens.replace('x3', 'xxx')

for tok in tokens:
    note_lens = note_lens.replace(tokens[tok], str(tok))

note_lens = note_lens.split('|')

temp = '|'

for bar in note_lens:
    if bar == '':
        continue
    bar_len = 0
    for d in bar:
        if d == ':':
            continue
        bar_len += durations[int(d)]
    if bar[0] == ':':
        temp += ':'
    temp += str(bar_len)
    if bar[-1] == ':':
        temp += ':'
    temp += '|'

note_lens = temp

###################### MUSIC CONVERSION ######################

# remove all non note chars
music = re.sub('[^A-G|]', '', music)
# divide into bars
music = music.split('|')

# Take the ascii value, subtract 65 ('A')
# A is 0, B is 1 etc
# to make C = 0, shift by 5 and then mod by 7 (note number)
# no accidentals
note_value = lambda x : (ord(x) - 65 + 5)%7

# get key and mode
key = lines[3].replace('K:', '').strip()
mode = re.sub('[A-Z\n]', '', key)
key = key.replace(mode, '')
key = note_value(key)

# Take the note value, subtract the key to get
# its degree and make it fit between 0-6
note_degree = lambda x : (note_value(x) - key + 7)%7

# create the melody string in this new format
data = str(key) + ' ' + mode + '\n' + note_lens + '\n'
for bar in music:
    if bar == '':
        continue
    new_bar = ''
    for note in bar:
        new_bar += str(note_degree(note))
    data += new_bar + '|'

with open(filename + '.txt', 'w') as f:
    f.write(data)
