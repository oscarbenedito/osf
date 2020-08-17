#!/usr/bin/env sh
# Gotify notify
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

# Implements notify function, that notifies admin through Gotify. This file is
# imported by other scripts, but it could easily be used on its own adding lines
# that call the function.

notify() {
  GOTIFY_DOMAIN="gotify.oscarbenedito.com"
  GOTIFY_TOKEN="$(cat "$(dirname "$(realpath "$0")")/gotify_token.txt")"
  curl -X POST "https://$GOTIFY_DOMAIN/message?token=$GOTIFY_TOKEN" \
    -F "title=$1" -F "message=$2" -F "priority=${3:-5}" \
    >/dev/null 2>&1
}
