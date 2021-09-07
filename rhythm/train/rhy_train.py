import sys
import numpy as np

filename = sys.argv[1]

lines = ''
with open(filename, 'r') as f:
    lines = ''.join(f.readlines())

toknum = 4
matrix = np.zeros((toknum, toknum, toknum), dtype = float)

couples = np.zeros(toknum*toknum)

index_of = lambda x, y : x*4 + y

prev_prev = int(lines[0])
prev = int(lines[1])

couples[index_of(prev_prev, prev)] += 1

for tok in lines[2:]:
    token = int(tok)

    matrix[prev_prev][prev][token] += 1
    couples[index_of(prev, token)] += 1

    prev_prev = prev
    prev = token

for mat in matrix:
    for line in mat:
        num = line.sum()
        if num != 0:
            line /= num

couples /= couples.sum()

output = 'trained'
np.save(output, matrix)
np.save(output + '_couples', couples)
