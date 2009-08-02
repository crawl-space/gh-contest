#!/usr/bin/python

import sys
import time

from ghcontest import load_data, suggest_repos
from ghcontest.models import User


def main(args):
    start_time = time.time()
    users, repos, popular_repos = load_data(args)

    print "Unique users: %d" % len(users)
    print "Unique repos: %d" % len(repos)

    print "Done in %d seconds" % (time.time() - start_time)


if __name__ == "__main__":
    main(sys.argv[1:])
