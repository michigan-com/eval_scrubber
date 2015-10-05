# -*- coding: utf-8 -*-
import os
import sys
import logging

from . import find_infected, remove_infected

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
