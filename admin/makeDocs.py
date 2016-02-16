#!/usr/bin/env python3

#====================================================================
# Syntax      : makeDocs.py
# Description : Generate documentation based on individual project
#               files. For now only the one README.md file is
#               generated as top level document.
# Author      : AP
# Created     : 08 Jan 2016
#--------------------------------------------------------------------


#====================================================================
# Imports
#--------------------------------------------------------------------
import glob
import re
import os.path


#====================================================================
# Functions
#--------------------------------------------------------------------
def print_static_header(of):
    of.write('''
# Overview
A collection of examples for getting started in the Internet of Things (IoT). This includes code, wiring diagrams and documentation. In the description of each example, we list supported/tested boards. The same code may work on other boards with no or minimal changes. Files are organized in the following manner:

* `admin`: Utilities for maintaining this repo.
* `Arduino`: Projects on Arduino and Energia. Most examples are about Arduino Uno and TI LaunchPadF5529.

Examples using other platforms such as Intel Edison, Broadcom WICED, ARM mbed or Raspberry Pi may be added in future.
''')


def get_project_fields(sketch, images):
    with open(sketch, 'r') as sk:
        content = sk.read()

    # Extract fields from sketch content    
    purpose, boards = re.findall(r'Purpose\s*:\s*(.*?)Date\s*:\s*.*?Boards\s*:\s*(.*?)\n', content, re.S)[0]
    purpose = re.sub(r'\n\s*', r'\n', purpose) # remove leading spaces in each line
    name = os.path.splitext(os.path.basename(sketch))[0]

    # Filter relevant images for this sketch
    prefix = sketch[:-4:]
    skimgs = [x for x in images if prefix in x]

    return dict(zip(('name', 'purpose', 'boards', 'images'), (name, purpose, boards, skimgs)))


def print_project(of, fields):
    of.write('\n## {}\n'.format(fields['name']));
    of.write('<table><tr>\n');
    of.write('<td>\n');
    for img in fields['images']:
        of.write('''<br><img src="{}" width=320px>\n'''.format(img))
    of.write('\n</td>\n');
    of.write('<td>\n');
    of.write('<b>Boards</b><p><pre>{}</pre></p>\n'.format(fields['boards']));
    of.write('<b>Description</b><p><pre>{}</pre></p>\n'.format(fields['purpose']));
    of.write('</td>\n');
    of.write('</tr></table>\n');
    of.write('\n');


#====================================================================
# Main processing
#--------------------------------------------------------------------
with open("README.md", "w") as of:
    print_static_header(of)

    of.write('''# Basic Examples\n''')
    images = glob.glob('**/**/*_bb.png')
    for sketch in sorted(glob.iglob('**/**/*.ino')):
        fields = get_project_fields(sketch, images)
        print_project(of, fields)
