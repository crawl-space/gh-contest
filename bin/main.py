#!/usr/bin/python

import sys
import time

from ghcontest import load_data, suggest_repos
from ghcontest.models import User


def main(args):
    start_time = time.time()
    users, repos, popular_repos, superprojects = load_data(args)

    print "Processing test users"
    test = open(args[3], 'r')
    results = open(args[4], 'w')

    for line in test.readlines():
        user_id = int(line.strip())

        if not user_id in users:
            user = User(user_id)
        else:
            user = users[user_id]

        suggested_repos = suggest_repos(repos, popular_repos, users, user,
                superprojects)
        suggested_repos.sort()

        results.write('%d:' % user.id)
        results.write(','.join([str(x.id) for x in suggested_repos]))
        results.write('\n')

    test.close()
    results.close()
    print "Done in %d seconds" % (time.time() - start_time)


if __name__ == "__main__":
    main(sys.argv[1:])
