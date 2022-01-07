#!/bin/sh
# 2020 Oscar Benedito <oscar@oscarbenedito.com>
# License: CC0 1.0 Universal License

# Gotify notify: notifies user using a Gotify instance.

GOTIFY_DOMAIN="<redacted>"
GOTIFY_TOKEN="<redacted>"

curl -X POST "https://$GOTIFY_DOMAIN/message?token=$GOTIFY_TOKEN" \
  -F "title=$1" -F "message=$2" -F "priority=${3:-5}" \
  >/dev/null 2>&1
