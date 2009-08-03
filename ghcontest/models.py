#!/usr/bin/python

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

        self._lang_names = None
        self._popularity = None

    def is_watched_by(self, user):
        self.watched_by.add(user)

    @property
    def popularity(self):
        if not self._popularity:
            self._popularity = len(self.watched_by)
        return self._popularity

    @property
    def lang_names(self):
        if not self._lang_names:
            names = [x[0] for x in self.langs]
            self._lang_names = set(names)

        return self._lang_names


class User(IdBase):

    def __init__(self, id):
        self.id = id
        self.watching = set()
        self.similar_users = set()

        self._favourite_langs = None

    def is_watching(self, repo):
        self.watching.add(repo)

    def similar_to(self, similarity):
        self.similar_users.add(similarity)

    @property
    def favourite_langs(self):
        if not self._favourite_langs:
            langs = {}
            for repo in self.watching:
                for lang in repo.langs:
                    if lang[0] not in langs:
                        langs[lang[0]] = 0
                    langs[lang[0]] = lang[1]

            favs = langs.items()
            favs.sort(reverse=True, key=lambda x: x[1])
            self._favourite_langs = [x[0] for x in favs]

        return self._favourite_langs

    def lang_pref_similarity(self, repo):
        """
        Compare repo language makeup to this users language preferences.
        Return: a value between 0 and 1, representing preference match, or None
        if the user has no pref, or the repo has no known langs
        """
        langs = repo.langs
        if not self.favourite_langs or not langs:
            return None

        similar = 0
        for lang in langs:
            if lang in self.favourite_langs:
                similar += 1
        
        return similar/len(langs)
