#! /usr/bin/env python
# Python program to demonstrate
# main() function
import sys, os
import fileinput
from xml.dom.minidom import parse

def find_string_in_files(file_path, search_string):
    #print(file_path)
    try:
        with open(file_path, 'r') as f:
            for line_number, line in enumerate(f, start=1):
                if search_string in line:
                    print("Found in {} on line {}: {}".format(file_path, line_number, line.strip()))
                    return 0
    except (IOError, UnicodeDecodeError):
        # Skip files that cannot be opened or decoded
        exit(-1)


def find_string_in_files(file_path, search_string, stage_string):
    #print(file_path)
    try:
        with open(file_path, 'r') as f:
            for line_number, line in enumerate(f, start=1):
                if search_string in line and stage_string in line:
                    print("Found in {} on line {}: {}".format(file_path, line_number, line.strip()))
                    return 0
    except (IOError, UnicodeDecodeError):
        # Skip files that cannot be opened or decoded
        exit(-1)





def find_string_in_path(path, search_string):
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path[-3:] == 'xml' and ('2024' in file_path or '2025' in file_path):
                #print(file_path)
                try:
                    with open(file_path, 'r') as f:
                        for line_number, line in enumerate(f, start=1):
                            if search_string in line:
                                print("Found in {} on line {}: {}".format(file_path, line_number, line.strip()))
                                return file_path
                except (IOError, UnicodeDecodeError):
                    # Skip files that cannot be opened or decoded
                    continue
    return ""

def find_and_replace_or_add_line(path, search_string, stage_string, new_line):
    file_path = path
    try:
        # Read the file content
        with open(file_path, 'r') as f:
            lines = f.readlines()

        # Search for the string and track if it was found
        found = False
        with open(file_path, 'w') as f:
            for line in lines:
                if search_string in line and stage_string in line:
                    f.write(new_line + '\n')
                    found = True
                else:
                    f.write(line)

            # If the string was not found, add the new line
            if not found:
                f.write(new_line + '\n')

    except (IOError, UnicodeDecodeError):
        # Skip files that cannot be opened or decodeda
        print("failed to email")
        exit(3)
        #continuemport subprocess

def get_input_def_from_xml(xml, stage):
    docs = parse(xml)
    inputdef=''
    for xmlprojoect in docs.getElementsByTagName('project'):
        for xmlstage in xmlprojoect.getElementsByTagName('stage'):
            if xmlstage.getAttribute("name") != stage:
                continue
            for xmlinputdef in xmlstage.getElementsByTagName("inputdef"):
                inputdef=xmlinputdef.firstChild.data
    return inputdef
