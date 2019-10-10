""" Commands to configure BWDT """
import sys
import os

from click import echo

import bwdt.lib.auth as auth


def _error(msg):
    """Print an error to stderr and exist with non-zero code"""
    sys.stderr.write('{}\n'.format(msg))
    sys.exit(1)


def configure(key_id=None, key=None, online=None, offline_path=None):
    """ Launch the configuration setup """
    echo('Running BWDT Configuration Wizard')
    made_dir = auth.mkdir()
    if made_dir:
        echo('Created directory {}'.format(auth.get_dir_path()))
    echo('Writing {}'.format(auth.get_file_path()))
    data = auth.get()
    if online is None:
        echo('Do you have an internet connection? [y/n]:')
        user_in = raw_input().lower()
        if user_in != 'y' and user_in != 'n':
            _error('Invalid input. Expected y or n')
        online = (user_in == 'y')
    if online:
        if key_id is None:
            echo('Enter Download Key ID:')
            key_id = raw_input()
        if key is None:
            echo('Enter Download Key:')
            key = raw_input()
    else:
        if offline_path is None:
            echo('Enter offline media path:')
            offline_path = raw_input()
            if not os.path.exists(offline_path):
                _error('Invalid path: {}'.format(offline_path))
    offline = not online
    auth.set(key_id=key_id, key=key, offline=offline,
             offline_path=offline_path)
    data = auth.get()
    echo('Key ID: {}'.format(data['key_id']))
    echo('Offline: {}'.format(data['offline']))
    echo('Offline Path: {}'.format(data['offline_path']))
