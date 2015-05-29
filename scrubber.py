#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import re
import sys

infected_pattern = re.compile(r"<\?php\s*eval\((.+\()*base64_decode\(.+\)\).+\s*?>")

def remove_infection(dir_):
    print('Scanning and replacing infected files ...')
    count = 0
    for root, dirs, files in os.walk(dir_):
        for fname in files:
            contents = ''
            with open(os.path.join(root, fname), 'r') as fp:
                contents = fp.read()
            new_str = re.sub(infected_pattern, '', contents)
            if len(contents) != len(new_str):
                with open(os.path.join(root, fname), 'w') as fp:
                    fp.write(new_str)
                    count += 1
                    print(os.path.join(root, fname))
    print('-' * 30)
    print('Total: %s' % count)

def find_infected_files(dir_):
    print('Finding all infected files ...')
    count = 0
    for root, dirs, files in os.walk(dir_):
        for fname in files:
            with open(os.path.join(root, fname), 'r') as fp:
                contents = fp.read()
                if infected_pattern.search(contents):
                    count += 1
                    print(os.path.join(root, fname))
    print('-' * 30)
    print('Total: %s' % count)

if __name__ == '__main__':
    args = sys.argv
    if (len(args) < 3):
        raise ValueError('Please supply the action (find or remove) and the directory ex: python scrubber.py find /home/usrname')
    action = args[1]
    directory = args[2]
    if not os.path.isdir(directory):
        raise IOError('Directory does not exist')
    if action == 'find':
        find_infected_files(directory)
    elif action == 'remove':
        remove_infection(directory)
    else:
        raise ValueError('Action must be either "find" or "remove"')
