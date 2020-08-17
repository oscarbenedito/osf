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

# Script that notifies through Gotify when a website has changed.

# File must implement notify funtion
. "$(dirname "$(realpath "$0")")/notify.sh"

check_and_notify() {
  newhash="$(curl "$URL" 2>/dev/null | sha256sum | cut -f 1 -d " ")"
  [ "$HASH" != "$newhash" ] && notify "$TITLE" "$URL"
}

# Example usage:
HASH="<hash>"
URL="<url>"
TITLE="<title>"
check_and_notify
