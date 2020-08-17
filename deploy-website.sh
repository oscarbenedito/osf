#!/usr/bin/env sh
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

# Script to deploy a website built with Hugo.

HUGO_PATH="/root/oscarbenedito.com"
WEB_PATH="/srv/oscarbenedito.com"
GOTIFY_DOMAIN="gotify.oscarbenedito.com"
FILE_DIR="$(dirname "$(realpath "$0")")"

# Pull rewritting history if needed, check that commit is PGP signed by a known
# key and if so, rebuild the website
git -C $HUGO_PATH fetch origin master
git -C $HUGO_PATH reset --hard origin/master
git -C $HUGO_PATH verify-commit master || exit 1
rm -rf $HUGO_PATH/public
rm -rf $HUGO_PATH/resources
hugo -s $HUGO_PATH --gc

# Edit Hugo output: delete unwanted files (also from sitemap)
rm -rf "$HUGO_PATH/public/licenses/page/"
rm -f "$HUGO_PATH/public/index.xml" "$HUGO_PATH/public/licenses/index.html" \
    "$HUGO_PATH/public/licenses/index.xml"
path="\\/licenses\\/"
sed -i "/<url>/{:a;N;/<\/url>/!ba};N;/<loc>https:\/\/oscarbenedito\.com${path}<\/loc>/d" \
    "$HUGO_PATH/public/sitemap.xml"
# Explanation of RegEx:
# /<url>/       # find <url>
# {             # start command declaration
#   :a          # create label "a"
#   N           # read next line into pattern space
#   /<\/url>/!  # if not match </url>...
#   ba          # goto "a"
# }             # end command
# N             # read next line into pattern space (the empty line on sitemap.xml)
# /<lo....oc>/  # if pattern matches...
# d             # delete

# Sync new build to production
rsync --perms --recursive --checksum --delete "$HUGO_PATH/public/" "$WEB_PATH"

# Notify
API_TOKEN="$(cat "$FILE_DIR/gotify_token.txt")"
TITLE="Web update triggered"
MESSAGE="Git hooks triggered an update of the website."

curl -X POST "https://$GOTIFY_DOMAIN/message?token=$API_TOKEN" \
  -F "title=$TITLE" \
  -F "message=$MESSAGE" \
  -F "priority=5" \
  >/dev/null 2>&1
