#!/usr/bin/python

import sys


class IdBase(object):

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        if other is None:
            return False
        return self.id == other.id

    def __cmp__(self, other):
        if other is None:
            return 1
        return cmp(self.id, other.id)


class RepoOwner(object):

    def __init__(self, name):
        self.name = name
        self.owns = set()


class Repo(IdBase):

    def __init__(self, id):
        self.id = id
        self.watched_by = set()

        self.owner = None
        self.name = None
        self.forked_from = None
        self.forked_by = []
        self.langs = []

    def is_watched_by(self, user):
        self.watched_by.add(user)


class User(IdBase):

    def __init__(self, id):
        self.id = id
        self.watching = set()
        self.similar_users = set()

    def is_watching(self, repo):
        self.watching.add(repo)

    def similar_to(self, similarity):
        self.similar_users.add(similarity)


class UserSimilarity(object):

    def __init__(self, user1, user2):
        self.users = (user1, user2)
        self.common_repos = set()

    def __hash__(self):
        return self.users[0].id ^ self.users[1].id

    def __eq__(self, other):
        return self.users[0] in other.users and self.users[1] in other.users


def find_similar_users(target_user, users):
    similar_users = set()

    for repo in target_user.watching:
        for user in repo.watched_by:
            if user is not target_user and user.id > target_user.id:
                similarity = UserSimilarity(target_user, user)
                # May have already done this user from another common repo
                if similarity not in target_user.similar_users:
                    similarity.common_repos = \
                            target_user.watching.intersection(user.watching)
                    target_user.similar_to(similarity)
                    user.similar_to(similarity)

class Context(object):

    def __init__(self, users, repos, popular_repos):
        self.users = users
        self.repos = repos
        self.popular_repos = popular_repos


def load_data(args):
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

    owners = {}
    print "Reading repo details"
    repo_txt = open(args[1], 'r')
    for line in repo_txt.readlines():
        id, other = line.strip().split(':')
        id = int(id)
        parts = other.split(',')

        repo = repos[id]

        owner, repo.name = parts[0].split('/', 1)
        repo.creation_date = parts[1]

        if owner in owners:
            repo.owner = owners[owner]
        else:
            repo.owner = RepoOwner(owner)
            owners[owner] = repo.owner

        repo.owner.owns.add(repo)

        if len(parts) > 2:
            repo.forked_from = repos[int(parts[2])]
            repo.forked_from.forked_by.append(repo)

    repo_txt.close()

    print "Reading repo language"
    lang = open(args[2], 'r')
    for line in lang.readlines():
        id, other = line.strip().split(':')
        id = int(id)
        
        if id not in repos:
            continue

        parts = other.split(',')

        repo = repos[id]
        for part in parts:
            lang_name, count = part.split(';')
            repo.langs.append((lang_name, int(count)))

    lang.close()

#    print "Matching up similar users"
#    sorted_users = users.values()
#    sorted_users.sort()
#    total = len(sorted_users)
#    cur = 0
#    for user in sorted_users:
#        cur += 1
#        sys.stdout.write("\r%d / %d - %3d%%" % (cur, total, cur/total * 100))
#        sys.stdout.flush()
#
#        find_similar_users(user, users)        

    return users, repos, popular_repos


class Suggestions(object):

    def __init__(self, user):
        self.user = user
        self.suggested_repos = []

    def add(self, repo):
        if repo not in self.user.watching and repo not in self.suggested_repos:
            self.suggested_repos.append(repo)


def suggest_repos(repos, users, target_user):
    suggestions = Suggestions(target_user)
    similar_users = set()

    for repo in target_user.watching:
        if len(suggestions.suggested_repos) > 10:
            break
        for child in repo.forked_by:
            suggestions.add(child)
        if repo.forked_from != None:
            suggestions.add(repo.forked_from)

    watched_users = [x.owner for x in target_user.watching]
    for watched_user in watched_users:
        if len(suggestions.suggested_repos) > 10:
            break
        for users_repo in x.owner.owns:
            suggestions.add(users_repo)

    return suggestions.suggested_repos[:10]
#        for user in repo.watched_by:
#            if user is not target_user:
#                similar_users.add(user)

#    for similar_user in similar_users:
#        if len(target_user.watching.intersection(similar_user.watching)) < 4:
#            continue
#
#       possible_repos = target_user.watching - similar_user.watching
#
#        for repo in possible_repos:
#            if repo not in suggested_repos:
#                suggested_repos[repo] = 0
#
#            suggested_repos[repo] += 1
#
#
#    suggested_repos_sorted = sorted(suggested_repos.items(), key=lambda x: x[1],
#            reverse=True)
#
#    return [x[0] for x in suggested_repos_sorted[:10]]


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

        suggested_repos = suggest_repos(repos, users, user)

        popular = 0
        remaining_slots = 10 - len(suggested_repos)
        while remaining_slots > 0:
            while popular_repos[popular] in suggested_repos:
                popular += 1
            suggested_repos.append(popular_repos[popular])
            remaining_slots -= 1

        results.write(str(user_id))
        results.write(':')

        suggested_repos.sort()

        results.write(','.join([str(x.id) for x in suggested_repos]))
        results.write('\n')

    print "\nDone"
    test.close()
    results.close()


if __name__ == "__main__":
    main(sys.argv[1:])
