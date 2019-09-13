"""Common code for bwdt"""
import os


def get_latest_tag(image):
    """ Returns the latest tag for a particular image supported by bwdt """
    tags = {
        'registry': '2',
        'breqwatr/pxe': '7.0'
    }
    return tags[image]


def _env_get(env_name, default_val):
    """ Return an environment variable if defined else default value """
    if env_name in os.environ:
        return os.environ[env_name]
    return default_val


def env():
    """ Dictionary of environment variables or their default value """
    return {
        'auth_file': _env_get('BWDT_AUTH_FILE', '/etc/breqwatr/auth.json'),
        'region': _env_get('BWDT_REGION', 'ca-central-1'),
    }

