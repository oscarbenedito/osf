# Copyright (C) 2019 Oscar Benedito
#
# This file is part of Git Backup.
#
# Git Backup is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Git Backup is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Git Backup.  If not, see <https://www.gnu.org/licenses/>.

import os
import urllib.request
import json
import datetime
import git

backup_data = {}
backup_data['time'] = str(datetime.datetime.now())
backup_data['sites'] = {}

tokens_file = open('tokens.json')
tokens = json.load(tokens_file)
tokens_file.close()


def get_repositories_data(url, page):
    response = urllib.request.urlopen(url + '&page=' + str(page))
    return json.loads(response.read().decode('utf-8'))

# gitlab.com
if 'gitlab.com' in tokens:
    url = 'https://gitlab.com/api/v4/projects?private_token=' + tokens['gitlab.com'] + '&per_page=100&membership=true'
    page = 1
    repositories = get_repositories_data(url, page)

    backup_data['sites']['gitlab.com'] = []
    while len(repositories) != 0:
        for repository in repositories:
            clone_dir = 'repositories/gitlab.com/' + repository['path_with_namespace']
            print('gitlab.com/' + repository['path_with_namespace'])
            if os.path.isdir(clone_dir):
                git.cmd.Git(clone_dir).fetch()
            else:
                os.system('git clone --mirror ' + repository['ssh_url_to_repo'] + ' ' + clone_dir)
            backup_data['sites']['gitlab.com'].append({
                'name': repository['name'],
                'description': repository['description'],
                'path': repository['path_with_namespace'],
                'ssh_url': repository['ssh_url_to_repo']
            })
        page += 1
        repositories = get_repositories_data(url, page)

# github.com
if 'github.com' in tokens:
    url = 'https://api.github.com/user/repos?access_token=' + tokens['github.com']
    page = 1
    repositories = get_repositories_data(url, page)

    backup_data['sites']['github.com'] = []
    while len(repositories) != 0:
        for repository in repositories:
            clone_dir = 'repositories/github.com/' + repository['full_name']
            print('github.com/' + repository['full_name'])
            if os.path.isdir(clone_dir):
                git.cmd.Git(clone_dir).fetch()
            else:
                os.system('git clone --mirror ' + repository['ssh_url'] + ' ' + clone_dir)
            backup_data['sites']['github.com'].append({
                'name': repository['name'],
                'description': repository['description'],
                'path': repository['full_name'],
                'ssh_url': repository['ssh_url']
            })
        page += 1
        repositories = get_repositories_data(url, page)

# custom
if os.path.exists("custom_directories.json"):
    custom_file = open('custom_directories.json', 'r')
    repositories = json.load(custom_file)
    custom_file.close()
    for repository in repositories:
        clone_dir = 'repositories/' + repository['host'] + '/' + repository['path']
        print(repository['host'] + '/' + repository['path'])
        if os.path.isdir(clone_dir):
            git.cmd.Git(clone_dir).fetch()
        else:
            os.system('git clone --mirror ' + repository['ssh_url'] + ' ' + clone_dir)
        if repository['host'] not in backup_data['sites']:
            backup_data['sites'][repository['host']] = []
        backup_data['sites'][repository['host']].append({
            'name': repository['name'],
            'description': repository['description'],
            'path': repository['path'],
            'ssh_url': repository['ssh_url']
        })

with open('backup_data.json', 'w', encoding='utf-8') as output_file:
    json.dump(backup_data, output_file, ensure_ascii=False)
    output_file.close()
