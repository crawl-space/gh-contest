#!/usr/bin/python

import sys

from ghcontest import load_data, suggest_repos
from ghcontest.models import User

def main(args):
    users, repos, popular_repos = load_data(args)

    print "Processing test users"
    test = open(args[3], 'r')
    results = open(args[4], 'w')

    # cheating again
    total = 4788.0
    cur = 0

    for line in test.readlines():
        cur += 1
        sys.stdout.write("\r%3d%%" % (cur/total * 100))
        sys.stdout.flush()

        user_id = int(line.strip())

        if not user_id in users:
            print "\nuser %d not found. suggesting popular repos" % user_id
            user = User(user_id)
        else:
            user = users[user_id]

        suggested_repos = suggest_repos(repos, popular_repos, users, user)

        results.write(str(user_id))
        results.write(':')

        suggested_repos.sort()

        results.write(','.join([str(x.id) for x in suggested_repos]))
        results.write('\n')
        results.flush()

    print "\nDone"
    test.close()
    results.close()


if __name__ == "__main__":
    main(sys.argv[1:])
