# Markion
Markion is a Python script to allow writing literate programs using Markdown. Markion retrieves the tangled code in a file and written it to the specified files in the output directory. This README file is an example of a file that Markion can process, indeed, this file will give you Markion itself!

## Prerequisites
In order to run the program, you will need `python3`.

## Running the program
To run the program, execute the file `markion.py` followed by the input file.

```
python3 markion.py file
```

There is an addition option `--output-directory` (or `-d`) to specify an output directory and you can also run the program with `--help` (or `-h`) to get help about the program's usage.

## Program explanation
First of all, we will write the license notice and import all the required libraries.
```python file markion.py
[[ include license ]]
import os, sys, re, argparse
```

### Arguments
We will use Python's `argparse` package to deal with our program's arguments. We initialize the parser with a brief description of the program's utility.
```python file markion.py
parser = argparse.ArgumentParser(description='Markion is a simple scripts that retrieves tangled code from Markdown.')
```
One of the arguments is the name of the input file:
```python file markion.py
parser.add_argument('file', metavar='file', type=str, nargs=1, help='Input file.')
```
The other argument is optional and it let's the user specify the output directory.
```python file markion.py
parser.add_argument('-d', '--output-directory', dest='out_dir', type=str, default=os.getcwd(), help='Change the output directory.')
```
Finally we assign the arguments' values to the `args` variable to use it later on.
```python file markion.py
args = parser.parse_args()
```

### Read input
We read the input file and copy the contents to a variable `inp`.
```python file markion.py
with open(args.file[0], 'r') as f:
    inp = f.read()
```

### Extract code
We extract the important pieces of code from the `inp` variable. To do so there are two regular expressions, one that matches the blocks and one that matches the content to output in the files. We get all the snippets and save them into the variables `blocks` and `files`.
```python file markion.py
r_block = '```[\w\-.]*\s+block\s+([\w.-]+).*?\n(.*?)\n```\s*?\n'
r_file = '```[\w\-.]*\s+file\s+([\w.-]+).*?\n(.*?\n)```\s*?\n'
blocks = re.findall(r_block, inp, flags = re.DOTALL)
files = re.findall(r_file, inp, flags = re.DOTALL)
```

### Resolve blocks
For each file specified in the input, we resolve all the blocks that are included (recursively). To do so we use the function `resolve`.
```python file markion.py
[[ include resolve ]]
block_content = { b[0] : [False, b[1]] for b in blocks }
file_content = dict()
for f in files:
    if f[0] not in file_content:
        file_content[f[0]] = ''
    file_content[f[0]] += resolve(f[1], block_content)
```
The following code is the function resolve included in the last code fragment, it won't be directly written on the file, but be included when the `[[ include resolve ]]` is called. As you can see it indents the whole block.
```python block resolve
r_include = re.compile('([ \t]*)\[\[\s*include\s+([\w\-.]+)\s*\]\]', flags = re.DOTALL)
def resolve(content, blocks):
    it = r_include.finditer(content)
    for include in it:
        block_name = include[2]
        if blocks[block_name][0]:
            raise Exception('Circular dependency in block ' + block_name)
        blocks[block_name][0] = True
        s = resolve(blocks[block_name][1], blocks)
        blocks[block_name][0] = False
        blocks[block_name][1] = s
        s = include[1] + s.replace('\n', '\n' + include[1])
        content = r_include.sub(repr(s)[1:-1], content, count = 1)
    return content
```

### Write files
Finally, if there weren't any errors, we write the output code into the respective files. To do so we create the output directory if not already created:
```python file markion.py
if not os.path.exists(args.out_dir):
    os.mkdirs(args.out_dir)
```
And we write the output.
```python file markion.py
for fn, fc in file_content.items():
    with open(args.out_dir + '/' + fn, 'w') as f:
        f.write(fc)
```

## License
The program is licensed under the GPL v3. License is available [here](https://gitlab.com/oscarbenedito/markion/blob/master/COPYING).

In order to make sure there is no missunderstanding, we will include the following license notice on our file.
```python block license
# Copyright (C) 2019 Oscar Benedito
#
# This file is part of Markion.
#
# Markion is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Markion is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Markion.  If not, see <https://www.gnu.org/licenses/>.
```

## Author
 - **Oscar Benedito** - oscar@obenedito.org
