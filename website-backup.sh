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

# Script to backup content on the Internet. It gets a list of URLs and
# destination files and puts each document in the corresponding file,
# adding a date to the filename.

FILE_DIR="$(dirname "$(realpath "$0")")"
. "$FILE_DIR/notify.sh"
URL_FILE="$FILE_DIR/urls.txt"
BACKUP_PATH="$HOME/backups"

save() { wget --quiet --output-document "$OUTPUT" "$URL" ; }

error_message () {
  TITLE="Website backup error"
  MESSAGE="Error backing up $OUTPUT"
  notify "$TITLE" "$MESSAGE"
}

while read -r url file
do
  mkdir -p "$BACKUP_PATH/${file}"
  OUTPUT="$BACKUP_PATH/${file}/$(date +"%Y-%m-%d")-${file}"
  URL="${url}"
  save || error_message
done < "$URL_FILE"
