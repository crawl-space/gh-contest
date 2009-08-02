#!/usr/bin/python

import sys
import time
import random

from ghcontest import load_data, suggest_repos
from ghcontest.models import User

def load_data(filename):
    data = set()
    file = open(filename, 'r')

    for line in file.readlines():
        user, repos = line.strip().split(":")
        user = int(user)
        for repo in repos.split(','):
            data.add((user, int(repo)))

    file.close()
    return data

def main(args):
    start_time = time.time()
    
    print "Loading results"
    target = load_data(args[0])
    results = load_data(args[1])

    total = len(target)
    missed = target.difference(results)

    guessed = total - len(missed)
    print "%d/%d, %d%%" % (guessed, len(target),
            (guessed * 100.0) / len(target))


    print "Done in %d seconds" % (time.time() - start_time)

if __name__ == "__main__":
    main(sys.argv[1:])
