""" Commands to configure BWDT """
import sys
import os

from click import echo

import bwdt.lib.config


def _error(msg):
    """Print an error to stderr and exist with non-zero code"""
    sys.stderr.write('{}\n'.format(msg))
    sys.exit(1)


def configure(key_id=None, key=None, online=None, offline_path=None):
    """ Launch the configuration setup """
    echo('Running BWDT Configuration Wizard')
    data = bwdt.lib.config.get_config()
    if online is None:
        echo('Do you have an internet connection? [y/n]:')
        user_in = input().lower()
        if user_in not in ('y', 'n'):
            _error('Invalid input. Expected y or n')
        online = (user_in == 'y')
    if online:
        if key_id is None:
            echo('Enter Download Key ID:')
            key_id = input()
        if key is None:
            echo('Enter Download Key:')
            key = input()
    else:
        if offline_path is None:
            echo('Enter offline media path:')
            offline_path = input()
            if not os.path.exists(offline_path):
                _error('Invalid path: {}'.format(offline_path))
    bwdt.lib.config.set_config(data)
    data = bwdt.lib.config.get_config()
    echo('Key ID: {}'.format(data['key_id']))
    echo('Offline: {}'.format(data['offline']))
    echo('Offline Path: {}'.format(data['offline_path']))
