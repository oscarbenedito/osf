#!/usr/bin/env python3
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

import os
import sys
import re
import json
import shutil

HUGO_OUT_DIR = '/root/oscarbenedito.com/public'

if len(sys.argv) != 2:
    print("Usage:\n", sys.argv[0], "file.json")
    exit(1)

with open(sys.argv[1], 'r') as f:
    data = json.load(f)

for dir in data['directories']:
    shutil.rmtree(os.path.join(HUGO_OUT_DIR, dir))

for file in data['files']:
    os.remove(os.path.join(HUGO_OUT_DIR, file))

with open(os.path.join(HUGO_OUT_DIR, 'sitemap.xml'), 'r') as f:
    sitemap = f.read()

for line in data['sitemap']:
    block = '\n[ \t]*<url>\n[ \t]*<loc>https://oscarbenedito\.com' + line + '</loc>\n(?:[ \t]*<lastmod>.*</lastmod>\n)?[ \t]*</url>\n[ \t]*'
    sitemap = re.sub(block, '', sitemap)

with open(os.path.join(HUGO_OUT_DIR, 'sitemap.xml'), 'w') as f:
    f.write(sitemap)
