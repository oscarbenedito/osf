#!/usr/bin/env sh
# Copyright (C) 2020 Oscar Benedito
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

git -C $HUGO_PATH fetch origin master
git -C $HUGO_PATH reset --hard origin/master
git -C $HUGO_PATH verify-commit master || exit 1
rm -rf $HUGO_PATH/public
rm -rf $HUGO_PATH/resources
hugo -s $HUGO_PATH --gc
$FILE_DIR/post-hugo-script.py "$FILE_DIR/post_hugo_script.json"
rsync --perms --recursive --checksum --delete "$HUGO_PATH/public/" "$WEB_PATH"

API_TOKEN="$(cat "$FILE_DIR/website_api_token.txt")"
TITLE="Web update triggered"
MESSAGE="Git hooks triggered an update of the website."

curl -X POST "https://$GOTIFY_DOMAIN/message?token=$API_TOKEN" \
  -F "title=$TITLE" \
  -F "message=$MESSAGE" \
  -F "priority=5" \
  >/dev/null 2>&1
