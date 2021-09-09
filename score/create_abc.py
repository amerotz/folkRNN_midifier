import sys
import random
import re

filename = sys.argv[1]
filename_txt = sys.argv[2]
output = sys.argv[3]

lines = ''
with open(filename_txt, 'r') as f:
    lines = f.readlines()

# retrieve info from abc file

key_mode = lines[0].split(' ')
key = int(key_mode[0])
mode = key_mode[1].replace('\n', '')

bar_durations = lines[1].replace('\n', '').split('|')
bar_durations = [x for x in bar_durations if x != '']

harmony = lines[2].replace('\n', '').split('|')

rhythm_fills = lines[3].replace('\n', '').split('|')

rhythms = lines[4].split('|')

# create rhythm and harmony strings

'''
# some chords are diminished in some modes
# the fundamental must be substituted with the 3rd
# of the same chord
diminished_chords = {
    'maj': 6, # VII
    'min': 1, # II
    'dor': 5, # VI
    'mix': 2, # III
}
'''

# get name of notes based on degree and key
name = lambda x : chr(65 + (x + key + 2)%7)

'''
def nearestTo(prev_note, fund):
    new_notes = [fund, (fund + 2)%7]
    dist = [abs(x - prev_note) for x in new_notes]
    note = new_notes[dist.index(min(dist))]
    return note
'''

# init parts
harmony_data = '|'
rhythm_data = '|'
beat_data = '|'

# create set of rhythms to alternate
rhythm_set = [rhythms[:2], rhythms[2:]]
curr_rhy = 0
rhy_index = 0

for (i, note) in enumerate(harmony):

    note = int(note)
    '''
    if i != 0:
        note = nearestTo(int(harmony[i-1]), note)

    # if harmony is diminished
    if note == diminished_chords[mode]:
        # substitute fundamental with third
        note += 2
        note %= 7
    '''
    # check for repeats at the start
    if bar_durations[i].startswith(':'):
        harmony_data += ':'
        rhythm_data += ':'
        beat_data += ':'

    # get bar len
    bar_len = int(re.sub('[^0-9]', '', bar_durations[i]))

    # add bass note
    harmony_data += name(note) + ',' + str(bar_len)

    # if bar is shorter than it should
    if bar_len < 6:
        # add a rhythm fill
        rhythm_data += rhythm_fills[bar_len-1]
        beat_data += 'A,' + str(bar_len)
    else:
        # add rhythm
        rhythm_data += rhythm_set[curr_rhy][rhy_index]
        rhy_index = 1 - rhy_index
        # add beat
        beat_data += 'A,3A,3'

    # check for repeats at the end 
    if bar_durations[i].endswith(':'):
        harmony_data += ':'
        rhythm_data += ':'
        beat_data += ':'

    # end bar
    harmony_data += '|'
    rhythm_data += '|'
    beat_data += '|'

    # double bar at end of section
    if i < len(harmony)-1 and bar_durations[i+1].startswith(':'):
        harmony_data += '|'
        rhythm_data += '|'
        curr_rhy += 1
        beat_data += '|'

# write to file

with open(filename, 'r') as src:
    with open(output, 'w') as out:
        lines = src.readlines()
        content = ''.join(lines[:3]).strip()
        content += '\nQ:1/4=' + str(random.randrange(150, 200))
        content += '\nR:double jig'
        content += '\nV:M clef=treble name="Melody" snm="M"\n'
        content += 'V:H clef=bass name="Harmony" snm="H"\n'
        content += 'V:R clef=percussion name="Rhythm" snm="R"\n'
        content += 'V:B clef=percussion name="Beat" snm="B"\n'
        content += lines[3].strip()
        content += '\nV:M\n'
        content += '%%MIDI program 40\n'
        content += ''.join(lines[4:]).strip()
        content += '\nV:H\n'
        content += '%%MIDI program 46\n'
        content += harmony_data
        content += '\nV:R\n'
        content += '%%MIDI program 115\n'
        content += rhythm_data
        content += '\nV:B\n'
        content += '%%MIDI program 116\n'
        content += beat_data
        out.write(content)
