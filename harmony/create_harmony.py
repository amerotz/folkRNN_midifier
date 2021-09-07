import numpy as np
import random
import sys

filename = sys.argv[1]
melody_w = float(sys.argv[2])

lines = ''
with open(filename, 'r') as f:
    lines = f.readlines()

key = int(lines[0])
melody = ''.join(lines[2:]).split('|')

# build the matrix

note_matrix = np.array([1, 0, 0, 1, 0, 1, 0], dtype=float)

transition_matrix = np.array([
    [0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 1],
    [0, 0, 0, 1, 0, 0, 0],
    [1, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 1, 0, 0],
    [1, 0, 0, 0, 0, 0, 0]
], dtype=float) + np.eye(7)

for line in transition_matrix:
    num = line.sum()
    if num != 0:
        line /= num

# start generation
chords = range(7)

def initState(bar):
    note_state = np.zeros(7)
    for note in bar:
        note = int(note)
        note_state += np.roll(note_matrix, note)
    note_state /= note_state.sum()
    return np.argmax(note_state)


current_state = initState(melody[0])
harmony = []
harmony.append(current_state)

# for each bar generate a chord
for bar in melody[1:]:

    if bar == '':
        continue

    note_state = np.zeros(7)
    for note in bar:
        note = int(note)
        note_state += np.roll(note_matrix, note)

    num = note_state.sum()
    if num != 0:
        note_state /= num

    # random (weighted) choice between the possible chords
    #prob = (1 - melody_w)*transition_matrix[current_state] + melody_w * note_state
    prob = note_state

    current_state = random.choice(np.argwhere(prob == np.amax(prob)).flatten().tolist())

    harmony.append(current_state)


harmony = [str(x) for x in harmony]
data = ''.join(lines[:2]) + '|'.join(harmony)

with open(filename, 'w') as f:
    f.write(data)
