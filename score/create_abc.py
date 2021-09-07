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

key = int(lines[0])

bar_durations = lines[1].replace('\n', '').split('|')
bar_durations = [x for x in bar_durations if x != '']

harmony = lines[2].replace('\n', '').split('|')

rhythm_fills = lines[3].replace('\n','').split('|')

rhythms = lines[4].split('|')

# create rhythm and harmony strings

name = lambda x : chr(65 + (x + key + 2)%7)

harmony_data = '|'
rhythm_data = '|'
beat_data = '|'

rhythm_set = [rhythms[:2], rhythms[2:]]
curr_rhy = 0
rhy_index = 0

for (i, note) in enumerate(harmony):

    if bar_durations[i].startswith(':'):
        harmony_data += ':'
        rhythm_data += ':'
        beat_data += ':'

    bar_len = int(re.sub('[^0-9]', '', bar_durations[i]))

    harmony_data += name(int(note)) + ',' + str(bar_len)

    if bar_len < 6:
        rhythm_data += rhythm_fills[bar_len-1]
    else:
        rhythm_data += rhythm_set[curr_rhy][rhy_index]
        rhy_index = 1 - rhy_index

    beat_data += 'A,' + str(bar_len)

    if bar_durations[i].endswith(':'):
        harmony_data += ':'
        rhythm_data += ':'
        beat_data += ':'

    harmony_data += '|'
    rhythm_data += '|'
    beat_data += '|'

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
        content += '\nR:jig'
        content += '\nV:M clef=treble name="Melody" snm="M"\n'
        content += 'V:H clef=bass name="Harmony" snm="H"\n'
        content += 'V:R clef=percussion name="Rhythm" snm="R"\n'
        content += 'V:B clef=percussion name="Beat" snm="B"\n'
        content += lines[3].strip()
        content += '\nV:M\n'
        content += '%%MIDI program 40\n'
        content += ''.join(lines[4:]).strip()
        content += '\nV:H\n'
        content += '%%MIDI program 21\n'
        content += harmony_data
        content += '\nV:R\n'
        content += '%%MIDI program 115\n'
        content += rhythm_data
        content += '\nV:B\n'
        content += '%%MIDI program 116\n'
        content += beat_data
        out.write(content)
