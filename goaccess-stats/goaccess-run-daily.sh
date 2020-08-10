#!/usr/bin/env sh
# Copyright (C) 2020 Oscar Benedito
#
# This file is part of Utilities.
#
# Utilities is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Utilities is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Utilities.  If not, see <https://www.gnu.org/licenses/>.

OUT_DIR="/srv/stats"
DB_DIR="/srv/goaccess-db"
LOGS_PREFIX="/var/log/apache2/a-website.log"

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
    DB="$DB_DIR/$1"
    FILTERED_FILE=$(mktemp)
    grep -v ".well-known/acme-challenge" "$LOGS_PREFIX.1" > "$FILTERED_FILE"
    if [ -d "$DB" ]; then
      mkdir -p "$OUT_DIR/$1/nf"
      run_goaccess "$FILTERED_FILE" "$OUT_DIR/$1/index.html" "$DB/f" 1 1
      run_goaccess "$LOGS_PREFIX.1" "$OUT_DIR/$1/nf/index.html" "$DB/nf" 1 1
    else
      mkdir -p "$DB/f"
      mkdir -p "$DB/nf"
      mkdir -p "$OUT_DIR/$1/nf"
      run_goaccess "$FILTERED_FILE" "$OUT_DIR/$1/index.html" "$DB/f" 0 1
      run_goaccess "$LOGS_PREFIX.1" "$OUT_DIR/$1/nf/index.html" "$DB/nf" 0 1
    fi

    if [ "$1" != "$2" ]; then
      DB="$DB_DIR/$2"
      if [ -d "$DB" ]; then
        mkdir -p "$OUT_DIR/$2"
        run_goaccess "$FILTERED_FILE" "$OUT_DIR/$2/index.html" "$DB/f" 1 0
        run_goaccess "$LOGS_PREFIX.1" "$OUT_DIR/$2/nf/index.html" "$DB/nf" 1 0
        rm -rf "$DB"
      fi
    fi
    rm "$FILTERED_FILE"
  else
    exit 1
  fi
}

# Day
TMP_FILE=$(mktemp)
LOGS_2=$(mktemp)
OUT_DIR_TODAY="$OUT_DIR/$(date --date="yesterday" +"d/%Y/%m/%d")"

cp "$LOGS_PREFIX.2.gz" "$LOGS_2.gz"
gunzip -f "$LOGS_2.gz"

mkdir -p "$OUT_DIR_TODAY"
cat "$LOGS_2" "$LOGS_PREFIX.1" | grep -v ".well-known/acme-challenge" > "$TMP_FILE"
run_goaccess "$TMP_FILE" "$OUT_DIR_TODAY/index.html"

mkdir -p "$OUT_DIR_TODAY/nf"
cat "$LOGS_2" "$LOGS_PREFIX.1" > "$TMP_FILE"
run_goaccess "$TMP_FILE" "$OUT_DIR_TODAY/nf/index.html"
rm "$TMP_FILE"

# Week
TODAY="$(date +"w/%G/%V")"
YESTERDAY="$(date --date="yesterday" +"w/%G/%V")"
run_goaccess_time_interval "$TODAY" "$YESTERDAY"

# Month
TODAY="$(date +"m/%Y/%m")"
YESTERDAY="$(date --date="yesterday" +"m/%Y/%m")"
run_goaccess_time_interval "$TODAY" "$YESTERDAY"

# Year
TODAY="$(date +"y/%Y")"
YESTERDAY="$(date --date="yesterday" +"y/%Y")"
run_goaccess_time_interval "$TODAY" "$YESTERDAY"

# All time
TODAY="all"
YESTERDAY="all"
run_goaccess_time_interval "$TODAY" "$YESTERDAY"
