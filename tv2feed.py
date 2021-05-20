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

# Follow TV shows using Atom feeds!
#
# How to use
# ----------
#
# Go to <https://www.tvmaze.com> and search the TV shows you want to follow.
# Write down their IDs (the number in the URL) and then run the following:
#
#     tv2feed id1 id2 ...
#
# Or run it multiple times to get one feed per TV show. The feeds are expected
# to go under:
#
#   - `https://<domain>/<path>/feed`: if multiple shows specified
#   - `https://<domain>/<path>/show/<show_id>`: if only one show specified
#
# That is because the feed URIs will point there. Note that if only one show is
# specified, TV2Feed will generate it assuming there is one feed per show (which
# will make the feed title the same as the show's).
#
# The API where the data is gathered from caches results for one hour, so you
# can add cron jobs to run every hour:
#
#     0 * * * * /usr/local/bin/tv2feed 210 431 > /srv/www/tv2feed/feed
#
# or, alternatively (could also be scripted with just one cronjob):
#
#     0 * * * * /usr/local/bin/tv2feed 210 > /srv/www/tv2feed/show/210
#     0 * * * * /usr/local/bin/tv2feed 431 > /srv/www/tv2feed/show/431
#
# Other notes
# -----------
#
# Each show will make two API requests, and there is a limit of 20 requests
# every 10 seconds (for contents that are not cached). If you are following many
# shows, this script will sleep for 10 seconds and try again if an API call
# returns a 429 error code, if it fails again (or the error code is not 429), it
# will raise an error and exit.
#
# All data generated is gathered from [TVmaze][]'s API.


import sys
import urllib.request
import json
import datetime
import time


# edit these variables
domain = 'oscarbenedito.com'
path = 'projects/tv2feed'   # leave empty for content under https://domain/
entries_per_show = 10
shows = sys.argv[1:]        # alternatively, hardcode them in the script
# until here!

version = '0.2'             # TV2Feed version
url_base = 'https://{}/{}'.format(domain, path + '/' if path != '' else '')
id_base = 'tag:{},2021-05-19:/{}'.format(domain, path + '/' if path != '' else '')
info_endpoint_tmpl = 'https://api.tvmaze.com/shows/{}'
episodes_endpoint_tmpl = 'https://api.tvmaze.com/shows/{}/episodes?specials=1'


# basic sanitizing: convert to string and escape XML
def san(s):
    return str(s).replace('&', '&amp;').replace('>', '&gt;').replace('<', '&lt;').replace('\'', '&apos;').replace('"', '&quot;')


def api_call(url):
    try:
        response = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print('Error 429. Sleeping for 10 seconds and retrying...', file=sys.stderr)
            time.sleep(10)
            response = urllib.request.urlopen(url)
        else:
            raise

    return json.load(response)


if len(shows) < 1:
    sys.exit('Usage: tv2feed id1 [id2 [id3 ...]]')

now = datetime.datetime.now(datetime.timezone.utc).isoformat()
feed_data = []
for show in shows:
    show_info = api_call(info_endpoint_tmpl.format(show))
    episodes = api_call(episodes_endpoint_tmpl.format(show))

    episodes.sort(reverse=True, key=lambda x: x['airstamp'])

    countdown = entries_per_show
    for episode in filter(lambda x: x['airstamp'] < now, episodes):
        feed_data.append({
            'airstamp': episode['airstamp'],
            'id': episode['id'],
            'name': episode['name'],
            'number': episode['number'],
            'season': episode['season'],
            'show_id': show_info['id'],
            'show_name': show_info['name'],
            'summary': episode['summary'],
            'url': episode['url']
        })
        countdown -= 1
        if countdown == 0:
            break

    if show_info['status'] != 'Running':
        feed_data.append({
            'airstamp': now,
            'id': 'status',
            'name': 'Show status: {}'.format(show_info['status']),
            'number': None,
            'season': None,
            'show_id': show_info['id'],
            'show_name': show_info['name'],
            'summary': '<p>Show status: {}.</p>'.format(show_info['status']),
            'url': show_info['url']
        })

if len(shows) > 1:
    feed_title = 'TV2Feed'
    feed_id = id_base + 'feed'
    feed_url = url_base + 'feed'
else:
    feed_title = san(feed_data[0]['show_name'])
    feed_id = id_base + 'show/' + san(feed_data[0]['show_id'])
    feed_url = url_base + 'show/' + san(feed_data[0]['show_id'])

ret = '<?xml version="1.0" encoding="utf-8"?>\n'
ret += '<feed xmlns="http://www.w3.org/2005/Atom">'
ret += '<link href="{}" rel="self" />'.format(feed_url)
ret += '<title>{}</title>'.format(feed_title)
ret += '<author><name>TV2Feed</name></author>'
ret += '<updated>{}</updated>'.format(now)
ret += '<id>' + feed_id + '.atom</id>'
ret += '<generator uri="https://oscarbenedito.com/projects/tv2feed/" version="{}">TV2Feed</generator>'.format(version)

for episode in sorted(feed_data, reverse=True, key=lambda x: x['airstamp']):
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
