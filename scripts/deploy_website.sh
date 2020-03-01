#!/usr/bin/env sh
# Copyright (C) 2020 Oscar Benedito
#
# This file is part of Utilities.
#
# Utilities is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Utilities is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Utilities.  If not, see <https://www.gnu.org/licenses/>.

# Script to deploy a website built with Hugo.

HUGO_PATH="/srv/oscarbenedito.com"

git -C $HUGO_PATH pull
rm -rf $HUGO_PATH/public
rm -rf $HUGO_PATH/resources
hugo -s $HUGO_PATH --minify

DOMAIN=gotify.oscarbenedito.com
API_TOKEN=<redacted>
TITLE="Web update triggered"
MESSAGE="Git hooks triggered an update of the website."

curl -X POST "https://$DOMAIN/message?token=$API_TOKEN" \
  -F "title=$TITLE" \
  -F "message=$MESSAGE" \
  -F "priority=5" \
  >/dev/null 2>&1
