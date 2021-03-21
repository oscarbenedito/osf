#!/bin/sh
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

# Script that sends a notification when someone logs in through SSH to a
# computer/server.

# This scripts assumes there is an executable called "notify" in your PATH that
# takes two arguments (the first one is the notification title and the second
# one is the message).

if [ "$PAM_TYPE" != "close_session" ]; then
  TITLE="SSH login: ${PAM_USER}@$(hostname)"
  MESSAGE="IP: ${PAM_RHOST}
Date: $(TZ='Europe/Madrid' date)"

  notify "$TITLE" "$MESSAGE"
fi
