#!/usr/bin/python

import sys

data = open(sys.argv[1], 'r')
test = open(sys.argv[2], 'r')

to_filter = [x.strip for x in test.readlines()]

for line in data.readlines():
    parts = line.split(':')

    if parts[0] != to_filter:
        sys.stdout.write(line)
