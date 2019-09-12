"""Common code for bwdt"""

import json
import os


def _env_get(env_name, default_val):
    """Return an environment variable if defined else default value"""
    if env_name in os.environ:
        return os.environ[env_name]
    return default_val


def env_vars():
    """Returns a dict of env vars or their defaults if not set"""
    return {
        'auth_file': _env_get('BWDT_AUTH_FILE', '/etc/breqwatr/auth.json'),
    }


def get_auth():
    """Returns the dict of data from the auth file"""
    file_path = env_vars()['auth_file']
    with open(file_path, 'r') as auth_file:
        auth = json.load(auth_file)
    return auth
