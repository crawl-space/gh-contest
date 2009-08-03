#!/usr/bin/python

import sys
import time

from models import User, Repo, RepoOwner

def load_data(args):
    start_time = time.time()
    users = {}
    repos = {}
    popular_repos = []
    superprojects = {}

    print "Loading user to repo map"

    data = open(args[0], 'r')

    for line in data.readlines():
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
    
    data.close()

    print "Ordering repos by popularity"
    popular_repos = sorted(repos.values(), reverse=True,
            key=lambda x: x.popularity)

    owners = {}
    print "Reading repo details"
    repo_txt = open(args[1], 'r')
    for line in repo_txt.readlines():
        id, other = line.strip().split(':')
        id = int(id)

        if id not in repos:
            continue

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

        if len(parts) > 2 and int(parts[2]) in repos:
            repo.forked_from = repos[int(parts[2])]
            repo.forked_from.forked_by.append(repo)

    repo_txt.close()

    print "Grouping superprojects" 
    superproject_keys = ['gnome', 'django', 'ruby', 'perl', 'rails']
    for repo in repos.values():
        for key in superproject_keys:
            if key in repo.name.lower():
                if key not in superprojects:
                    superprojects[key] = []
                superprojects[key].append(repo)

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

    print "Data read in %d seconds" % (time.time() - start_time)

    return users, repos, popular_repos, superprojects
