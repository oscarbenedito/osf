#!/usr/bin/env python3
# Atenea Updates Notifications
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


import os
import requests
import json
import time


with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.json'), 'r') as f:
    CONFIG = json.load(f)


NOTIFICATION_DOMAIN = CONFIG['notification_domain']
TIME_INTERVAL = CONFIG['time_interval']
COURSE_IDS = CONFIG['course_ids']
API_TOKEN = CONFIG['api_token']
NOTIFICATION_TOKEN = CONFIG['notification_token']


def get_updates(id):
    parameters = {
        'wstoken': API_TOKEN,
        'moodlewsrestformat': 'json',
        'wsfunction': 'core_course_get_updates_since',
        'courseid': id,
        'since': int(time.time()) - (TIME_INTERVAL + 20)
    }
    response = requests.get('https://atenea.upc.edu/webservice/rest/server.php', params=parameters)
    return response.json()['instances']


def get_course_docs(id):
    parameters = {
        'wstoken': API_TOKEN,
        'moodlewsrestformat': 'json',
        'wsfunction': 'core_course_get_contents',
        'courseid': id,
    }
    return requests.get('https://atenea.upc.edu/webservice/rest/server.php', params=parameters)


def find_document(docs, doc_id):
    for module in docs:
        for doc in module['modules']:
            if doc['id'] == doc_id:
                return doc


def send_notification(doc, course_name):
    if doc['modname'] == 'resource':
        message = 'URL: ' + doc['contents'][0]['fileurl'] + '&token=' + API_TOKEN
    else:
        message = doc['modplural']

    data = {
        'title': course_name + ': ' + doc['name'],
        'message': message,
        'priority': 5
    }
    requests.post('https://' + NOTIFICATION_DOMAIN + '/message?token=' + NOTIFICATION_TOKEN, data = data)

for id, course_name in COURSE_IDS.items():
    updates = get_updates(id)

    if updates != []:
        course_docs = get_course_docs(id)

    for update in updates:
        doc = find_document(course_docs.json(), update['id'])
        send_notification(doc, course_name)
