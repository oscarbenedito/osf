#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2021 Oscar Benedito <oscar@oscarbenedito.com>
# License: Affero General Public License version 3 or later

# Convert text/gemini files to HTML.
#
# Usage:
#
#     ./gemini-to-html.py [file.gmi]
#
# If no file is specified, standard input is used.

import sys
import re


css = """
body { margin: 1em auto; max-width: 700px; line-height: 1.5; font-family: sans-serif; padding: 0 1em; }
a { color: #02d; }
a:hover { color: #309; }
.a:before { content: "⇒ "; color: #888; }
pre { background-color: #eee; padding: 1rem; overflow-x: auto; }
blockquote { padding: 0 0 0 1.2rem; border-left: 3px solid; }
"""


if len(sys.argv) == 1:
    data = sys.stdin.readlines()
elif len(sys.argv) == 2:
    try:
        with open(sys.argv[1], 'r') as f:
            data = f.readlines()
    except IOError:
        sys.stderr.write('Error reading file {}.\n'.format(sys.argv[1]))
        sys.exit(1)
else:
    sys.stderr.write('Usage: {} file.gmi.\n'.format(sys.argv[0]))
    sys.exit(1)


print('<!DOCTYPE html>')
print('<html>')
print('<head>')
print('<meta charset="utf-8"/>')
print('<meta name="viewport" content="width=device-width, initial-scale=1"/>')
if data[0][:1] == '#' and data[0][:2] != '##':
    print('<title>{}</title>'.format(data[0][1:].strip()))
if css is not None:
    print('<style>{}</style>'.format(css))
print('</head>')
print('<body>')


state = ''

for line in data:
    line = line[:-1]
    if state == 'ul':
        if line[:2] == '* ':
            print('<li>{}</li>'.format(line[2:]))
            continue
        else:
            print('</ul>')
            state = ''
    elif state[:3] == 'pre':
        if line[:3] == '```':
            print('</code></pre>')
            state = ''
            continue
        else:
            if state == 'pre-first':
                sys.stdout.write('{}'.format(line))
                state = 'pre'
            else:
                sys.stdout.write('\n{}'.format(line))
            continue

    if line[:2] == '=>':
        # re.sub
        m = re.match('^=>[ \t]*(\S+)(?:[ \t]+(.+))?', line)
        if m is None:
            sys.stderr.write('Incorrect syntax on line of type link:\n'
                             '    {}'.format(line))
            print('<p>{}</p>'.format(line))
            continue
        text = m.group(2) if m.group(2) is not None else m.group(1)
        print('<p class="a"><a href="{}">{}</a></p>'.format(m.group(1), text))
    elif line[:3] == '```':
        if len(line) > 3:
            sys.stdout.write('<pre aria-label="{}"><code>'.format(line[3:]))
        else:
            sys.stdout.write('<pre><code>')
        state = 'pre-first'
    elif line[:3] == '###':
        print('<h3>{}</h3>'.format(line[3:]))
    elif line[:2] == '##':
        print('<h2>{}</h2>'.format(line[2:]))
    elif line[:1] == '#':
        print('<h1>{}</h1>'.format(line[1:]))
    elif line[:2] == '* ':
        print('<ul>\n<li>{}</li>'.format(line[2:]))
        state = 'ul'
    elif line[:1] == '>':
        print('<blockquote>{}</blockquote>'.format(line[1:]))
    else:
        print('<p>{}</p>'.format(line))

print('</body>\n</html>')
