#!/bin/sh
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

# Script that notifies through Gotify when a website has changed.


GOTIFY_DOMAIN="gotify.oscarbenedito.com"
API_TOKEN="<redacted>"

check_and_send_message() {
  newhash="$(curl "$URL" 2>/dev/null | sha256sum | cut -f 1 -d " ")"
  [ "$HASH" != "$newhash" ] && \
    curl -X POST "https://$GOTIFY_DOMAIN/message?token=$API_TOKEN" \
      -F "title=$TITLE" \
      -F "message=$URL" \
      -F "priority=5" \
      >/dev/null 2>&1
}


HASH="<hash>"
URL="<url>"
TITLE="<title>"

check_and_send_message
