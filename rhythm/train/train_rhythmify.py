import sys
import os

filename = sys.argv[1]

print('Analyzing file', filename, '...')
os.system('python3 ../converters/rhy_convert.py ' + filename)

print('Training model...')
os.system('python3 train/rhy_train.py ' + filename + '.dat')

print('Removing temp files...')
os.system('rm -f ' + filename + '.dat ')

print('Done.')
