#!/bin/sh
# 2020 Oscar Benedito <oscar@oscarbenedito.com>
# License: CC0 1.0 Universal License

# Script that notifies through Gotify when a website has changed.

# This scripts assumes there is an executable called "notify" in your PATH that
# takes two arguments (the first one is the notification title and the second
# one is the message).

URLS_FILE="${URLS_FILE:-${XDG_CONFIG_HOME:-$HOME/.config}/osf/urls-check-changes.txt}"

[ ! -f "$URLS_FILE" ] && echo "Error: $URLS_FILE is not a file." && exit 1

check_and_notify() {
  newhash="$(curl "$1" 2>/dev/null | sha256sum | cut -f 1 -d " ")"
  [ "$2" != "$newhash" ] && notify "$3" "$1"
}

while read -r url hash title
do
  check_and_notify "$url" "$hash" "$title"
done < "$URLS_FILE"

# Can also be used by calling check_and_notify directly. Example:
# check_and_notify url hash title
