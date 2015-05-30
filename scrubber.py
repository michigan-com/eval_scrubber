#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import re
import sys

infected_pattern = re.compile(r"<\?php\s*eval\((.+\()*base64_decode\(.+\)\).+\s*?>")
blacklist_filetypes = ['.gz', '.zip']

def get_file_ext(fname):
    base_name, file_ext = os.path.splitext(fname)
    return file_ext

def exclude_file(fname):
    file_ext = get_file_ext(fname)
    if file_ext in blacklist_filetypes:
        print('SKIP - blacklisted filetype: %s' % fname)
        return True
    if os.path.islink(fname):
        print('SKIP - symbolic link: %s' % fname)
        return True
    return False

def remove_infection(dir_):
    print('Scanning and replacing infected files ...')
    count = 0
    for root, dirs, files in os.walk(dir_):
        print('SCAN: %s' % root)
        for fname in files:
            contents = ''
            curfile = os.path.join(root, fname)
            if exclude_file(curfile):
                continue
            with open(curfile, 'r') as fp:
                contents = fp.read()
            new_str = re.sub(infected_pattern, '', contents)
            if len(contents) != len(new_str):
                try:
                    with open(curfile, 'w') as fp:
                        fp.write(new_str)
                        count += 1
                        print('=' * 30)
                        print('INFECTED, FIXING: %s' % curfile)
                except IOError as err:
                    print('SKIP - IOError: %s: %s' % (err, curfile))
    print('-' * 30)
    print('TOTAL: %s' % count)

def find_infected_files(dir_):
    print('Finding all infected files ...')
    count = 0
    for root, dirs, files in os.walk(dir_):
        print('SCAN: %s' % root)
        for fname in files:
            curfile = os.path.join(root, fname)
            if exclude_file(curfile):
                continue
            with open(curfile, 'r') as fp:
                contents = fp.read()
                if infected_pattern.search(contents):
                    count += 1
                    print('=' * 30)
                    print('INFECTED: %s' % curfile)
    print('-' * 30)
    print('TOTAL: %s' % count)

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
