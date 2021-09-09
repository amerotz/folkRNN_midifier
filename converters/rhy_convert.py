import sys
import random
import re

filename = sys.argv[1]

# get all data
lines = ''
with open(filename, 'r') as f:
    lines = f.readlines()

# headers to ignore
def ignore(string):
    headers = ['X', 'T', 'M', 'K']
    for h in headers:
        if string.startswith(h):
            return True
    return False

# select music only
data = ''

for line in lines:
    if ignore(line):
        continue
    data += line

# remove non rhythm chars

data = re.sub('[^a-zA-Z0-9/(]', '', data)
data = re.sub('[a-zA-Z]', 'x', data)

# replace x3 rhythm with random group
x3_subs = ['xxx', 'x2x', 'xx2']
x3_count = data.count('x3')
data = data.replace('x3', '{}').format(*(random.choice(x3_subs) for _ in range(x3_count)))

# note tokens
tokens = {
    0: '(3xxx',
    1: 'x/2',
    2: 'x2',
    3: 'x'
}

# tokenize
for tok in tokens:
    data = data.replace(tokens[tok], str(tok))

# clean string
data = re.sub('[^0123]', '', data)

# write to file 
with open(filename + '.dat', 'w') as f:
    f.write(data)
