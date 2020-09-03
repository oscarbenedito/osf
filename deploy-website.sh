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

# Script to deploy a website built with Hugo.

# File must implement notify funtion
. "$(dirname "$(realpath "$0")")/notify.sh"

HUGO_PATH="/root/.local/share/scripts/deploy-website/oscarbenedito.com"

make -C "$HUGO_PATH" deploy || exit 1

# Notify
TITLE="Web update triggered"
MESSAGE="Git hooks triggered an update of the website."
notify "$TITLE" "$MESSAGE"
