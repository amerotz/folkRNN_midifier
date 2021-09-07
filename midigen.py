# Take a folkRNN and generate a midi file
# with harmonization and percussion

# Marco Amerotti
# 07/09/2021
# TMH, KTH, Stockholm

import os
import sys

filename = sys.argv[1]
filename_txt = filename + '.txt'
filename_h = filename.replace('.abc', '.h.abc')
filename_mid = filename.replace('.abc', '.mid')

trainfile = 'rhythm/train/trained'
trainfile_npy = trainfile + '.npy'
trainfile_coup = trainfile + '_couples.npy'

melody_w = str(0.75)
rhy_toklen = str(1000)

print('Reading abc file...')
os.system('python3 converters/abc_convert.py ' + filename)

print('Harmonizing...')
args = filename_txt + ' ' + melody_w
os.system('python3 harmony/create_harmony.py ' + args)

print('Generating rhythms...')
args = trainfile_npy + ' ' + trainfile_coup + ' ' + rhy_toklen + ' ' + filename_txt
os.system('python3 rhythm/rhy_sample.py ' + args)

print('Generating abc score...')
args = filename + ' ' + filename_txt + ' ' + filename_h
os.system('python3 score/create_abc.py ' + args)
print('Score saved to ', filename_h)

print('Generating midi file...')
args = filename_h + ' -o ' + filename_mid + ' -BF -quiet'
os.system('abc2midi ' + args)

print('Removing temp files...')
args = filename_txt
os.system('rm -f ' + args)

print('Done.')
