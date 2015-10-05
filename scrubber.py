#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import sys
import logging

infected_pattern = re.compile(r"<\?php\s*eval\((.+\()*base64_decode\(.+\)\).+\s*?>")
blacklist_filetypes = ['.gz', '.zip', '.mov']

def get_file_ext(fname):
    base_name, file_ext = os.path.splitext(fname)
    return file_ext

def exclude_file(fname):
    file_ext = get_file_ext(fname)
    if file_ext in blacklist_filetypes:
        logging.debug('SKIP - blacklisted filetype: %s' % fname)
        return True
    if os.path.islink(fname):
        logging.debug('SKIP - symbolic link: %s' % fname)
        return True
    return False

def remove_infected(dir_):
    logging.info('Scanning and replacing infected files ...')
    count = 0

    infections = []
    for root, dirs, files in os.walk(dir_):
        logging.debug('SCAN: %s' % root)
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
                        infections.append(curfile)
                        logging.error('=' * 30)
                        logging.error('INFECTED, FIXING: %s' % curfile)
                except IOError as err:
                    logging.debug('SKIP - IOError: %s: %s' % (err, curfile))
    logging.info('-' * 30)
    logging.info('TOTAL: %s' % count)

    return infections

def find_infected(dir_):
    logging.info('Finding all infected files ...')
    count = 0

    infections = []
    for root, dirs, files in os.walk(dir_):
        logging.debug('SCAN: %s' % root)
        for fname in files:
            curfile = os.path.join(root, fname)
            if exclude_file(curfile):
                continue
            with open(curfile, 'r') as fp:
                contents = fp.read()
                if infected_pattern.search(contents):
                    count += 1
                    infections.append(curfile)
                    logging.error('=' * 30)
                    logging.error('INFECTED: %s' % curfile)
    logging.info('-' * 30)
    logging.info('TOTAL: %s' % count)

    return infections

if __name__ == '__main__':
    args = sys.argv
    if (len(args) < 3):
        raise ValueError('Please supply the action (find or remove) and the directory ex: python scrubber.py find /home/username')

    action = args[1]
    directory = args[2]

    debug = os.getenv("DEBUG", False)

    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if not os.path.isdir(directory):
        raise IOError('Directory does not exist')
    if action == 'find':
        find_infected(directory)
    elif action == 'remove':
        remove_infected(directory)
    else:
        raise ValueError('Action must be either "find" or "remove"')
