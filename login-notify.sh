#!/bin/sh
# 2020 Oscar Benedito <oscar@oscarbenedito.com>
# License: CC0 1.0 Universal License

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
