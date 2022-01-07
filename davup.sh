#!/bin/sh
# Copyright (C) 2020 Oscar Benedito <oscar@oscarbenedito.com>
# License: Affero General Public License version 3 or later

# DAVup: back up calendars and contacts from a DAV server (CalDAV and CardDAV).

domain="<DAV server address>"       # example: https://dav.mailbox.org (no trailing "/")
user="<username>"
pass="<password>"

get_cal() {
    curl -s -X "PROPFIND" -u "${user}:${pass}" -H "Content-Type: text/xml" -H "Depth: 1" \
        --data "<propfind xmlns='DAV:'><prop><calendar-data xmlns='urn:ietf:params:xml:ns:caldav'/></prop></propfind>" \
        "${domain}/${resource}"
}

get_card() {
    curl -s -X "PROPFIND" -u "${user}:${pass}" -H "Content-Type: text/xml" -H "Depth: 1" \
        --data "<propfind xmlns='DAV:'><prop><address-data xmlns=\"urn:ietf:params:xml:ns:carddav\"/></prop></propfind>" \
        "${domain}/${resource}"
}

process_cal() {
    intro="BEGIN:VCALENDAR"
    preevent="BEGIN:VEVENT"
    postevent="END:VEVENT"
    pretodo="BEGIN:VTODO"
    posttodo="END:VTODO"
    step="0"
    while read -r line; do
        line="${line%}"
        case $step in
            0) echo "${line}" | grep -q "${intro}" && step="1" && echo "${intro}" ;;
            1) echo "${line}"; \
                if [ "${line}" = "${preevent}" ]; then step="2"; \
                elif [ "${line}" = "${pretodo}" ]; then step="3"; fi ;;
            2) echo "${line}" && [ "${line}" = "${postevent}" ] && step="4" ;;
            3) echo "${line}" && [ "${line}" = "${posttodo}" ] && step="4" ;;
            4) if [ "${line}" = "${preevent}" ]; then step="2"; echo "${line}"; \
                elif [ "${line}" = "${pretodo}" ]; then step="3"; echo "${line}"; fi ;;
        esac
    done
    echo "END:VCALENDAR"
}

process_card() {
    pre="BEGIN:VCARD"
    post="END:VCARD"
    step="1"
    while read -r line; do
        line="${line%}"
        case $step in
            1) echo "${line}" | grep -q "${pre}" && step="2" && echo "${pre}" ;;
            2) echo "${line}" | grep -q "${post}" && step="1" && echo "${post}" \
                || echo "${line}" ;;
        esac
    done
}

# examples (resource address will be "${domain}/${resource}"):
#     resource="caldav/mycal" && get_cal | process_cal > calendar_and_todos.ics
#     resource="carddav/mycard" && get_card | process_card > contacts.vcf
