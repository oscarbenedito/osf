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
FILE_DIR="$(dirname "$(realpath "$0")")"
. "$FILE_DIR/notify.sh"
URLS="${XDG_CONFIG_HOME:-$HOME/.config}/osf/urls-check-changes.txt"

[ ! -f "$URLS" ] && echo "Error: $URLS is not a file." && exit 1

check_and_notify() {
  newhash="$(curl "$1" 2>/dev/null | sha256sum | cut -f 1 -d " ")"
  [ "$2" != "$newhash" ] && notify "$3" "$1"
}

while read -r url hash title
do
  check_and_notify "$url" "$hash" "$title"
done < "$URLS"

# Can also be used by calling check_and_notify directly. Example:
# check_and_notify url hash title
