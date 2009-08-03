#!/usr/bin/python

class Suggestions(object):

    def __init__(self, user):
        self.user = user
        self.suggested_repos = {}

    def could_add(self, repo):
        return repo not in self.user.watching

    def add(self, repo, weight):
        if self.could_add(repo):
            if repo not in self.suggested_repos:
                self.suggested_repos[repo] = weight
            else:
                self.suggested_repos[repo] += weight

    def top_ten(self):

        def cmp_repos(r1, r2):
            if r1[1] == r2[1]:
                return cmp(r1[0].popularity, r2[0].popularity)
            else:
                return cmp(r1[1], r2[1])

        suggested_repos = self.suggested_repos.items()
        suggested_repos.sort(reverse=True, cmp=cmp_repos)
        top_ten = [x[0] for x in suggested_repos]

        return top_ten[:10]

    def __len__(self):
        return len(self.suggested_repos)

PARENT = 4
USER = 3
CHILD = 2

# just padding if we don't have enough
POPULAR = 0


def add_parents(suggestions, target_user):
    parents = [repo.forked_from for repo in target_user.watching \
            if repo.forked_from != None]
    for parent in parents:
        suggestions.add(parent, PARENT)

def add_watched_owners(suggestions, target_user):
    watched_owners = [x.owner for x in target_user.watching]
    watched_owners = set(watched_owners)
    owned_by_watched_users = set()
    for watched_owner in watched_owners:
        owned_by_watched_users.update(watched_owner.owns)
    owned_by_watched_users = [x for x in owned_by_watched_users]
    for repo in owned_by_watched_users:
        suggestions.add(repo, USER)

def add_children(suggestions, target_user):
    for parent_repo in target_user.watching:
        for repo in parent_repo.forked_by:
            suggestions.add(repo, CHILD)

def suggest_repos(repos, popular_repos, users, target_user):
    suggestions = Suggestions(target_user)

    add_parents(suggestions, target_user)
    add_watched_owners(suggestions, target_user)
    add_children(suggestions, target_user)

    # pad with popular repos if we don't have 10 already
    if len(suggestions) < 10:
        fav_langs = set(target_user.favourite_langs)
        for popular_repo in popular_repos:
            if not suggestions.could_add(popular_repo):
                continue
            elif len(fav_langs) > 0 and len(popular_repo.lang_names) > 0:
                lang_names = popular_repo.lang_names
                if len(fav_langs.intersection(lang_names)) < 1:
                    continue

            suggestions.add(popular_repo, POPULAR)
            if len(suggestions) >= 10:
                break

    return suggestions.top_ten()
