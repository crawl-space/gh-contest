#!/usr/bin/python

import sys
import time
import random

from ghcontest import load_data, suggest_repos
from ghcontest.models import User


def remove_target_data(users):
    num_users = len(users)
    # about 7% of the users seems to be what github is using
    to_remove = num_users / 100 * 7

    target_users = random.sample(users.values(), to_remove)

    target_data = []
    for user in target_users:
        repos_to_remove = random.sample(user.watching,
                random.randint(1, len(user.watching)))

        target_data.append((user.id, [x.id for x in repos_to_remove]))
        for repo in repos_to_remove:
            user.watching.remove(repo)

    return target_data

def output_sample(filename, users):
    file = open(filename, 'w')
    
    for user in users.values():
        for repo in user.watching:
            file.write("%d:%d\n" % (user.id, repo.id))

    file.close()

def output_test(filename, target_data):
    file = open(filename, 'w')

    for row in target_data:
        file.write("%d\n" % row[0])

    file.close()

def output_target(filename, target_data):
    file = open(filename, 'w')

    for row in target_data:
        file.write("%d:" % row[0])
        file.write (','.join([str(x) for x in row[1]]))
        file.write("\n")

    file.close()

def main(args):
    start_time = time.time()
    users, repos, popular_repos = load_data(args)

    target_data = remove_target_data(users)

    print "Writing test data"
    # XXX create directory
    output_sample("%s/data.txt" % args[3], users)
    output_test("%s/test.txt" % args[3], target_data)
    output_target("%s/target.txt" % args[3], target_data)

    print "Done in %d seconds" % (time.time() - start_time)

if __name__ == "__main__":
    main(sys.argv[1:])
