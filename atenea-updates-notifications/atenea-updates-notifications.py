#!/usr/bin/env python3
# Copyright (C) 2020 Oscar Benedito, Ernesto Lanchares, Ferran López
#
# This file is part of Atenea Updates Notifications (AUN).
#
# AUN is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# AUN is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with AUN.  If not, see <https://www.gnu.org/licenses/>.

import os
import requests
import json
import time


NOTIFICATION_DOMAIN = 'gotify.obenedito.org'
TIME_INTERVAL = 120
COURSE_IDS = {
    55144: "EDOS",
    55145: "TP"
}


with open('api_token.txt', 'r') as f:
    API_TOKEN = f.read().strip()

with open('notification_token.txt', 'r') as f:
    NOTIFICATION_TOKEN = f.read().strip()


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
    data = {
        'title': course_name + ': ' + doc['name'],
        'message': 'URL: ' + doc['contents'][0]['fileurl'] + '&token=' + API_TOKEN,
        'priority': 5
    }
    requests.post('https://' + NOTIFICATION_DOMAIN + '/message?token=' + NOTIFICATION_TOKEN, data = data)


for id, course_name in COURSE_IDS.items():
    updates = get_updates(id)

    if updates != []:
        course_docs = get_course_docs(id)

    for update in updates:
        doc = find_document(course_docs.json(), update['id'])

        if doc['modname'] == 'resource':
            send_notification(doc, course_name)
