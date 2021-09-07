import sys
import numpy as np
import random

file_npy = sys.argv[1]
file_coup_npy = sys.argv[2]
sequence_len = int(sys.argv[3])
output = sys.argv[4]

# load matrices

matrix = np.load(file_npy)
couples = np.load(file_coup_npy)

tokens = {
    0: '(3AAA',
    1: 'A/2',
    2: 'A2',
    3: 'A'
}

def between_bars(token):
    if token == 0:
        return '(3:2:4AA/2-|-A/2A'
    elif token == 1:
        return 'A/4-|-A/4'
    elif token == 2:
        return 'A-|-A'
    else:
        return 'A/2-|-A/2'

durations = {
    0: 2,
    1: 0.5,
    2: 2,
    3: 1
}

# start generation

start_couple = np.random.choice(range(16), 1, p=couples)[0]
prev = start_couple % 4
prev_prev = (start_couple - prev)//4

data = []
data.append(prev_prev)
data.append(prev)

choices = range(4)

for it in range(sequence_len):

    prob = matrix[prev_prev][prev]

    next_tok = np.random.choice(choices, 1, p=prob)[0]

    next_prob = matrix[prev][next_tok]
    while next_prob.sum() != 1:
        next_tok = np.random.choice(choices, 1, p=prob)[0]
        next_prob = matrix[prev][next_tok]

    data.append(next_tok)

    prev_prev = prev
    prev = next_tok

# create bar division

notes = '|'
bar_duration = 0

for note in data:
    bar_duration += durations[note]

    if bar_duration < 6:
        notes += tokens[note]
    elif bar_duration % 6 == 0:
        notes += tokens[note]
        notes += '|'
    else:
        notes += between_bars(note)

    bar_duration %= 6

notes = notes.split('|')

# remove series of 8th notes
data = [x for x in notes if x != 'AAAAAA' and '-' not in x][:-1]

# create fills for bar duration 1-5
fills = []
for fill_size in range(1,6):

    bar_duration = 0
    tmp = ''

    while bar_duration != fill_size:

        bar_duration = 0
        tmp = ''
        bar = random.choice(data)

        for tok in tokens:
            bar = bar.replace(tokens[tok], str(tok))

        for note in bar:
            bar_duration += durations[int(note)]
            tmp += tokens[int(note)]
            if bar_duration >= fill_size:
                break

    fills.append(tmp)

fills = '|'.join(fills)

# select 4 different rhythms from the set

data_minus_one = data[:-1]
selection = []

for it in range(2):

    sel = random.choice(data_minus_one)

    while sel in selection and sel.startswith('-'):
        sel = random.choice(data_minus_one)

    selection.append(sel)
    selection.append(data[data.index(sel)+1])

selection = '|'.join(selection)

# save to file

content = '\n' + fills + '\n' + selection

with open(output, 'a') as f:
    f.write(content)
