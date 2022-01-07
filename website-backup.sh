#!/bin/sh
# 2020 Oscar Benedito <oscar@oscarbenedito.com>
# License: CC0 1.0 Universal License

# Script to backup content on the Internet. It gets a list of URLs and
# destination files and puts each document in the corresponding file,
# adding a date to the filename.

# This scripts assumes there is an executable called "notify" in your PATH that
# takes two arguments (the first one is the notification title and the second
# one is the message).

URLS="${XDG_CONFIG_HOME:-$HOME/.config}/osf/urls-backup.txt"
BACKUPS="${XDG_DATA_HOME:-$HOME/.local/share}/osf/website-backup"

[ ! -f "$URLS" ] && echo "Error: $URLS is not a file." && exit 1

backup() {
  mkdir -p "$BACKUPS/$2"
  output="$BACKUPS/$2/$(date +"%Y-%m-%d")-$2"
  last="$BACKUPS/$2/$(date --date="yesterday" +"%Y-%m-%d")-$2"
  # save new copy
  curl -s -X GET -H "X-Auth-Token: $3" "$1" > "$output" \
    || notify "Website backup error" "Error backing up $2"
  # delete last if duplicated
  cmp -s "$output" "$last" && rm "$last"
}

while read -r url file token
do
  backup "$url" "$file" "$token"
done < "$URLS"

# Can also be used by calling backup directly. Example:
# backup url file [token]
