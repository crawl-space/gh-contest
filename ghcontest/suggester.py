#!/usr/bin/python

class Suggestions(object):

    def __init__(self, user):
        self.user = user
        self.suggested_repos = []

    def could_add(self, repo):
        return repo not in self.user.watching and \
                repo not in self.suggested_repos

    def add(self, repo):
        if self.could_add(repo):
            self.suggested_repos.append(repo)


def suggest_repos(repos, popular_repos, users, target_user):
    suggestions = Suggestions(target_user)
    similar_users = set()

    parents = [repo.forked_from for repo in target_user.watching \
            if repo.forked_from != None]
    parents.sort(key=lambda x: x.popularity, reverse=True)
    for parent in parents:
        suggestions.add(parent)
        if len(suggestions.suggested_repos) >= 10:
            return suggestions.suggested_repos

    watched_owners = [x.owner for x in target_user.watching]
    watched_owners = set(watched_owners)
    owned_by_watched_users = set()
    for watched_owner in watched_owners:
        owned_by_watched_users.update(watched_owner.owns)
    owned_by_watched_users = [x for x in owned_by_watched_users]
    owned_by_watched_users.sort(key=lambda x: x.popularity, reverse=True)
    for repo in owned_by_watched_users:
        suggestions.add(repo)
        if len(suggestions.suggested_repos) >= 10:
            return suggestions.suggested_repos

    fav_langs = set(target_user.favourite_langs)
    for popular_repo in popular_repos:
        if not suggestions.could_add(popular_repo):
            continue
        elif len(fav_langs) > 0 and len(popular_repo.lang_names) > 0:
            lang_names = popular_repo.lang_names
            if len(fav_langs.intersection(lang_names)) < 1:
                continue

        suggestions.add(popular_repo)
        if len(suggestions.suggested_repos) >= 10:
            return suggestions.suggested_repos

    # something went wrong
    return []
