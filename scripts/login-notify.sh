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

# Script that notifies Gotify when someone logs in through SSH to a computer/server.

GOTIFY_DOMAIN="gotify.oscarbenedito.com"

API_TOKEN="$(cat "$(dirname "$(realpath "$0")")/login_api_token.txt")"

if [ "$PAM_TYPE" != "close_session" ]; then
  TITLE="SSH login: ${PAM_USER}@$(hostname)"
  MESSAGE="IP: ${PAM_RHOST}
Date: $(TZ='Europe/Madrid' date)"

  curl -X POST "https://$GOTIFY_DOMAIN/message?token=$API_TOKEN" \
  -F "title=$TITLE" \
  -F "message=$MESSAGE" \
  -F "priority=5" \
  >/dev/null 2>&1
fi
