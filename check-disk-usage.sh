#!/bin/sh
# 2022 Oscar Benedito <oscar@oscarbenedito.com>
# License: CC0 1.0 Universal License

tmp="$(df -Ph | grep ' /$')"
used="$(echo "$tmp" | awk {'print $5'})"
left="$(echo "$tmp" | awk {'print $4'})"
max=${MAX_THRESHOLD:-80}

if [ "${used%?}" -ge "${max}" ]; then
    notify "Disk usage warning" "$(hostname) has used $used of its disk space. Space left: $left."
fi
