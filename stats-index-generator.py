#!/usr/bin/env python3
# Copyright (C) 2020 Oscar Benedito <oscar@oscarbenedito.com>
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

# Generate index for GoAccess stats.

import sys
import datetime
import os.path

if len(sys.argv) < 2:
    sys.exit('Usage: stats-index-generator statsDir')

dir = sys.argv[1]

def has_info(link):
    return os.path.isfile(os.path.join(dir, link, 'index.html'))

output = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
    <meta name="description" content="Oscar Benedito's website stats">
    <meta name="author" content="Oscar Benedito">
    <title>Website stats</title>

    <link rel="icon" href="/favicon.min.svg">
    <link rel="shortcut icon" href="/favicon.ico">
    <style>
body {
  font-family: 'sans-serif';
  margin: 3em;
}

a.no-format {
  color: inherit;
  text-decoration: none;
}

a.hover:hover {
    text-decoration: underline;
}

h1,
h2 {
  text-align: center;
}

div.year {
  margin: 5em auto;
}

div.year-cal {
  display: flex;
  flex-flow: row wrap;
  justify-content: flex-start;
  max-width: 1024px;
  margin: 0 auto;
}

div.month {
  width: 17em;
  margin: 0;
  padding: 1em 0;
  flex: 1;
}

div.month ul {
  width: 17em;
  margin: 0 auto;
  padding: 0em 1em 1em 1em;
}

div.month li {
  float: left;
  display: block;
  width: 12.5%;
  text-align: center;
  list-style-type: none;
}

div.month a li:hover {
  border-radius: 5px;
  background-color: #1abc9c;
  color: #ecf0f1 !important;
}

div.month li.today {
  border-radius: 5px;
  background-color: #5759D4;
  color: #ecf0f1;
}

div.month li.week {
  font-weight: 900;
  color: #e67e22;
}
    </style>
  </head>

  <body>
"""

output += '<h1><a class="no-format hover" href="/all">See stats of all time</a></h1>'

for year in [2020]:
    link = 'y/' + str(year)
    if has_info(link):
        output += '<div class="year"><h1><a class="no-format hover" href="/' + link + '">' + str(year) + '</a></h1><div class="year-cal">'
    else:
        output += '<div class="year"><h1>' + str(year) + '</h1><div class="year-cal">'

    for month in range(1, 13):
        date = datetime.datetime(year, month, 1)
        link = date.strftime("m/%Y/%m")
        if has_info(link):
            output += '<div class="month"><h2><a class="no-format hover" href="/' + link + '">' + datetime.datetime(year, month, 1).strftime("%B") + '</a></h2><ul>'
        else:
            output += '<div class="month"><h2>' + datetime.datetime(year, month, 1).strftime("%B") + '</h2><ul>'

        if date.isocalendar()[2] != 1:
            date = datetime.datetime(year, month, 1)
            isoweek = date.strftime("%V")
            link = date.strftime("w/%G/%V")
            if has_info(link):
                output += '<a class="no-format" href="/' + link + '"><li class="week">' + isoweek + '</li></a>'
            else:
                output += '<li class="week">' + isoweek + '</li>'

            for i in range(date.isocalendar()[2] - 1):
                output += '<li style="opacity: 0;">-</li>'

        for day in range(1, 32):
            try:
                date = datetime.datetime(year, month, day)
            except:
                break

            if date.isocalendar()[2] == 1:
                isoweek = date.strftime("%V")
                link = date.strftime("w/%G/%V")
                if has_info(link):
                    output += '<a class="no-format" href="/' + link + '"><li class="week">' + isoweek + '</li></a>'
                else:
                    output += '<li class="week">' + isoweek + '</li>'

            today = ' class="today"' if datetime.datetime.today().date() == date.date() else ''
            link = date.strftime("d/%Y/%m/%d")
            if has_info(link):
                output += '<a class="no-format" href="/' + link + '"><li' + today + '>' + str(day) + '</li></a>'
            else:
                output += '<li' + today + '>' + str(day) + '</li>'

        output += '</ul></div>'

    output += '</div></div>'

output += '</body></html>\n'

with open(os.path.join(dir, 'index.html'), 'wt') as f:
    f.write(output)
