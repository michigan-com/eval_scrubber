#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import sys
import logging

__version__ = '0.0.3'

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
            with open(curfile, 'rb') as fp:
                contents = fp.read().decode('utf-8')
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
            with open(curfile, 'rb') as fp:
                contents = fp.read().decode('utf-8')
                if infected_pattern.search(contents):
                    count += 1
                    infections.append(curfile)
                    logging.error('=' * 30)
                    logging.error('INFECTED: %s' % curfile)
    logging.info('-' * 30)
    logging.info('TOTAL: %s' % count)

    return infections
