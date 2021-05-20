#!/usr/bin/env python3
# TV2Feed
# Copyright (C) 2021 Oscar Benedito <oscar@oscarbenedito.com>
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

# Follow TV shows using web feeds!
#
# How to use: go to https://www.tvmaze.com and search the shows you want to
# follow. Write down their IDs (the show number in the URL) and then run the
# following:
#
#     tv2feed id1 id2 ...
#
# Or run it multiple times to get one feed per TV show.
#
# Note 1: Keep in mind that each show will make two API requests, and there is a
# limit of 20 requests every 10 seconds (for contents that are not cached). If
# you are following many shows, you might want to spread out the API calls so
# you don't hit the rate limit.
#
# Note 2: The feeds are expected to go under:
#
#   - https://<domain>/<path>/feed: if multiple feeds specified
#   - https://<domain>/<path>/show/<show_id>: if only one show specified
#
# Also note that if only one feed is specified, TV2Feed will generate the feed
# assuming there is one feed per show (personalizing the title as well).
#
# All the data generated is gathered from https://www.tvmaze.com and its API.

# TODO allow empty path

import sys
import urllib.request
import json
import datetime


domain = 'oscarbenedito.com'
path = 'tv2feed'            # leave empty for content under https://domain/
entries_per_show = 10
shows = sys.argv[1:]        # alternatively, hardcode them in the script

version = '0.1'             # TV2Feed version
url_base = 'https://{}/{}'.format(domain, path + '/' if path != '' else '')
id_base = 'tag:{},2021-05-19:/{}'.format(domain, path + '/' if path != '' else '')
info_endpoint_tmpl = 'https://api.tvmaze.com/shows/{}'
episodes_endpoint_tmpl = 'https://api.tvmaze.com/shows/{}/episodes?specials=1'


# basic sanitizing (just escaping XML) and convert to string if needed
def san(s):
    return str(s).replace('&', '&amp;').replace('>', '&gt;').replace('<', '&lt;').replace('\'', '&apos;').replace('"', '&quot;')


if len(shows) < 1:
    sys.exit('Usage: tv2feed id1 [id2 [id3 ...]]')

now = datetime.datetime.now(datetime.timezone.utc).isoformat()
feed_data = []
for show in shows:
    response = urllib.request.urlopen(info_endpoint_tmpl.format(show))
    info = json.load(response)
    response = urllib.request.urlopen(episodes_endpoint_tmpl.format(show))
    episodes = json.load(response)

    episodes.sort(reverse=True, key=lambda x : x['airstamp'])

    countdown = entries_per_show
    for episode in filter(lambda x : x['airstamp'] < now, episodes):
        feed_data.append({
            'airstamp': episode['airstamp'],
            'id': episode['id'],
            'name': episode['name'],
            'number': episode['number'],
            'season': episode['season'],
            'show_id': info['id'],
            'show_name': info['name'],
            'summary': episode['summary'],
            'url': episode['url']
        })
        countdown -= 1
        if countdown == 0:
            break

    if info['status'] != 'Running':
        feed_data.append({
            'airstamp': now,
            'id': 'status',
            'name': 'Show status: {}.'.format(info['status']),
            'number': None,
            'season': None,
            'show_id': info['id'],
            'show_name': info['name'],
            'summary': '<p>Show status: {}.</p>'.format(info['status']),
            'url': info['url']
        })

if len(shows) > 1:
    feed_title = 'TV2Feed'
    feed_id = id_base + 'feed'
    feed_url = url_base + 'feed'
else:
    feed_title = san(feed_data[0]['show_name'])
    feed_id = id_base + 'show/' + san(feed_data[0]['show_id'])
    feed_url = url_base + 'show/' + san(feed_data[0]['show_id'])

ret  = '<?xml version="1.0" encoding="utf-8"?>\n'
ret += '<feed xmlns="http://www.w3.org/2005/Atom">'
ret += '<link href="{}" rel="self" />'.format(feed_url)
ret += '<title>{}</title>'.format(feed_title)
ret += '<author><name>TV2Feed</name></author>'
ret += '<updated>{}</updated>'.format(now)
ret += '<id>' + feed_id + '.atom</id>'
ret += '<generator uri="https://oscarbenedito.com/projects/tv2feed/" version="{}">TV2Feed</generator>'.format(version)

for episode in sorted(feed_data, reverse=True, key=lambda x : x['airstamp']):
    season = 'S' + san(episode['season']) if episode['season'] is not None else ''
    number = 'E' + san(episode['number']) if episode['number'] is not None else ''
    sn = season + number + ' ' if season + number != '' else ''
    ret += '<entry>'
    ret += '<title>{} - {}{}</title>'.format(san(episode['show_name']), sn, san(episode['name']))
    ret += '<link rel="alternate" href="{}" />'.format(san(episode['url']))
    ret += '<id>' + id_base + 'show/' + show + '/episode/' + san(episode['id']) + '</id>'
    ret += '<updated>{}</updated>'.format(san(episode['airstamp']))
    ret += '<summary type="html">{}</summary>'.format(san(episode['summary']))
    ret += '</entry>'

ret += '</feed>'
print(ret)
