#!/usr/bin/python

import sys

class Repo(object):

    def __init__(self, id):
        self.id = id
        self.watched_by = set()

    def is_watched_by(self, user):
        self.watched_by.add(user)


class User(object):

    def __init__(self, id):
        self.id = id
        self.watching = set()

    def is_watching(self, repo):
        self.watching.add(repo)


def suggest_repos(repos, users, target_user):
    suggested_repos = {}
    similar_users = set()

    for repo in target_user.watching:
        for user in repo.watched_by:
            similar_users.add(user)


    similar_users.remove(target_user)

    for similar_user in similar_users:
        possible_repos = target_user.watching - similar_user.watching

        for repo in possible_repos:
            if repo not in suggested_repos:
                suggested_repos[repo] = 0

            suggested_repos[repo] += 1


    suggested_repos_sorted = sorted(suggested_repos.items(), key=lambda x: x[1],
            reverse=True)

    return [x[0].id for x in suggested_repos_sorted[:10]]


def main(args):
    users = {}
    repos = {}
    popular_repos = []

    print "Loading user to repo map"

    data = open(args[0], 'r')

    # cheating on total number here ;)
    total = 440237.0
    cur = 0

    for line in data.readlines():
        cur += 1
        sys.stdout.write("\r%3d%%" % (cur/total * 100))
        sys.stdout.flush()

        user_id, repo_id = line.strip().split(':')

        user_id = int(user_id)
        repo_id = int(repo_id)

        if user_id in users:
            user = users[user_id]
        else:
            user = User(user_id)
            users[user_id] = user

        if repo_id in repos:
            repo = repos[repo_id]
        else:
            repo = Repo(repo_id)
            repos[repo_id] = repo


        repo.is_watched_by(user)
        user.is_watching(repo)

    print "\nDone"
    data.close()

    print "Ordering repos by popularity"
    popular_repos = sorted(repos.values(), reverse=True,
            key=lambda x: len(x.watched_by))

    print "Processing test users"
    test = open(args[1], 'r')
    results = open(args[2], 'w')

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
            suggested_repos = [x.id for x in popular_repos[:10]]
        else:
            user = users[user_id]
            suggested_repos = suggest_repos(repos, users, user)

            popular = 0
            remaining_slots = 10 - len(suggested_repos)
            while remaining_slots > 0:
                while popular_repos[popular].id in suggested_repos:
                    popular += 1
                suggested_repos.append(popular_repos[popular].id)
                remaining_slots -= 1

        results.write(str(user_id))
        results.write(':')

        results.write(','.join([str(repo) for repo in suggested_repos]))
        results.write('\n')

    print "\nDone"
    test.close()
    results.close()


if __name__ == "__main__":
    main(sys.argv[1:])
