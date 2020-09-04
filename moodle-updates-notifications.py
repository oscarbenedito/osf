#!/usr/bin/env python3
# Moodle Updates Notifications
# Copyright (C) 2020 Oscar Benedito <oscar@oscarbenedito.com>
# Copyright (C) 2020 Ernesto Lanchares <e.lancha98@gmail.com>
# Copyright (C) 2020 Ferran López <flg@tuta.io>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Get notified when new documents are uploaded to a Moodle instance. Makes use
# of a Gotify server.
#
# The script assumes there is a file on the same directory named
# "mun_config.json" with the configuration. Example configuration file:
#
#     {
#       "moodle_domain": "my.moodle.domain",
#       "gotify_domain": "my.gotify.domain",
#       "time_interval": 120,
#       "moodle_api_token": "myMoodleAPIToken",
#       "gotify_token": "myGotifyToken",
#       "course_ids": {
#         "56145": "GD",
#         "56152": "EDPS"
#       }
#     }
#
# Note: the script assumes Moodle's web service is found at
#     https://moodle_domain/webservice
# If that is not the case, change the moodle_domain variable so that it does.


import os
import requests
import json
import time


with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mun_config.json'), 'r') as f:
    cg = json.load(f)


def get_updates(id):
    parameters = {
        'wstoken': cg['moodle_api_token'],
        'moodlewsrestformat': 'json',
        'wsfunction': 'core_course_get_updates_since',
        'courseid': id,
        'since': int(time.time()) - (cg['time_interval'] + 20)
    }
    response = requests.get('https://' + cg['moodle_domain'] + '/webservice/rest/server.php', params=parameters)
    return response.json()['instances']


def get_course_docs(id):
    parameters = {
        'wstoken': cg['moodle_api_token'],
        'moodlewsrestformat': 'json',
        'wsfunction': 'core_course_get_contents',
        'courseid': id,
    }
    return requests.get('https://' + cg['moodle_domain'] + '/webservice/rest/server.php', params=parameters)


def find_document(docs, doc_id):
    for module in docs:
        for doc in module['modules']:
            if doc['id'] == doc_id:
                return doc


def send_notification(doc, course_name):
    if doc['modname'] == 'resource':
        message = 'URL: ' + doc['contents'][0]['fileurl'] + '&token=' + cg['moodle_api_token']
    else:
        message = doc['modplural']

    data = {
        'title': course_name + ': ' + doc['name'],
        'message': message,
        'priority': 5
    }
    requests.post('https://' + cg['gotify_domain'] + '/message?token=' + cg['gotify_token'], data = data)

for id, course_name in cg['course_ids'].items():
    updates = get_updates(id)

    if updates != []:
        course_docs = get_course_docs(id)

    for update in updates:
        doc = find_document(course_docs.json(), update['id'])
        send_notification(doc, course_name)
