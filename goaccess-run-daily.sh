#!/bin/sh
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

# Runs daily to generate stats with GoAccess.

# directory for html output
[ -z "$OUT_DIR" ] && echo "Error: variable OUT_DIR not set." && exit 1
# directory with all the GoAccess databases
[ -z "$DB_DIR" ] && echo "Error: variable DB_DIR not set." && exit 1
# name of log (the script appends strings ".1", ".2.gz" assuming that logrotate
# is used with delaycompress)
[ -z "$LOGS_PREFIX" ] && echo "Error: variable LOGS_PREFIX not set." && exit 1

# Shortcut to run GoAccess.
# Arguments:
#   1. Log file
#   2. Output file
#   3. (Optional) Database location
#   4. (Optional) Load from disk? Options: 0 (default), 1
#   5. (Optional) Keep DB files? Options: 0 (default), 1
run_goaccess() {
  if [ "$#" -ge 2 ]; then
    cmd="goaccess $1 -o $2"
    cmd="${cmd} --log-format=COMBINED --static-file=.js --static-file=.css --static-file=.ico --static-file=.svg --static-file=.png"
    if [ "$#" -ge 3 ]; then
      cmd="${cmd} --db-path=$3"
    fi
    if [ "$#" -ge 4 ]; then
      if [ "$4" -eq 1 ]; then
        cmd="${cmd} --restore"
      fi
    fi
    if [ "$#" -ge 5 ]; then
      if [ "$5" -eq 1 ]; then
        cmd="${cmd} --persist"
      fi
    fi
    eval $cmd
  else
    exit 1
  fi
}

# Runs GoAccess for on a time interval (year, month, etc.) respects the fact
# that the last day of the week will also be in the following week (because logs
# are created at an hour in the middle of the day, the boundary days are not
# complete).
# Runs GoAccess with a filtered accesses file and without a filter.
run_goaccess_time_interval() {
  if [ "$#" -eq 2 ]; then
    db="$DB_DIR/$1"
    filtered=$(mktemp)
    filter_file "$LOGS_PREFIX.1" > "$filtered"
    if [ -d "$db" ]; then
      mkdir -p "$OUT_DIR/$1"
      run_goaccess "$filtered" "$OUT_DIR/$1/index.html" "$db" 1 1
    else
      mkdir -p "$db"
      mkdir -p "$OUT_DIR/$1"
      run_goaccess "$filtered" "$OUT_DIR/$1/index.html" "$db" 0 1
    fi

    if [ "$1" != "$2" ]; then
      db="$DB_DIR/$2"
      if [ -d "$db" ]; then
        mkdir -p "$OUT_DIR/$2"
        run_goaccess "$filtered" "$OUT_DIR/$2/index.html" "$db" 1 0
        rm -rf "$db"
      fi
    fi
    rm "$filtered"
  else
    exit 1
  fi
}

filter_file() {
  grep -v ".well-known/acme-challenge" "$1"
}

# Day
tmp=$(mktemp)
tmp2=$(mktemp)
log2=$(mktemp)
out_today="$OUT_DIR/$(date --date="yesterday" +"d/%Y/%m/%d")"

cp "$LOGS_PREFIX.2.gz" "$log2.gz"
gunzip -f "$log2.gz"

mkdir -p "$out_today"
cat "$log2" "$LOGS_PREFIX.1" > "$tmp"
filter_file "$tmp" > "$tmp2"
run_goaccess "$tmp2" "$out_today/index.html"
rm "$tmp" "$tmp2" "$log2"

# Week
today="$(date +"w/%G/%V")"
yesterday="$(date --date="yesterday" +"w/%G/%V")"
run_goaccess_time_interval "$today" "$yesterday"

# Month
today="$(date +"m/%Y/%m")"
yesterday="$(date --date="yesterday" +"m/%Y/%m")"
run_goaccess_time_interval "$today" "$yesterday"

# Year
today="$(date +"y/%Y")"
yesterday="$(date --date="yesterday" +"y/%Y")"
run_goaccess_time_interval "$today" "$yesterday"

# All time
today="all"
yesterday="all"
run_goaccess_time_interval "$today" "$yesterday"
