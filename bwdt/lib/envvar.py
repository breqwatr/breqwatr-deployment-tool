""" Central place to reference the environment variables used """
import os


def _env_get(env_name, default_val):
    """ Return an environment variable if defined else default value """
    if env_name in os.environ:
        return os.environ[env_name]
    return default_val


def env():
    """ Dictionary of environment variables or their default value """
    home = os.path.expanduser("~")
    default_conf_path = f'{home}/.breqwatr/config.json'
    return {
        'BWDT_CONF_PATH': _env_get('BWDT_CONF_PATH', default_conf_path),
        'BWDT_AWS_REGION': _env_get('BWDT_AWS_REGION', 'ca-central-1'),
        'BWDT_FEATURE_PREVIEW': _env_get('BWDT_FEATURE_PREVIEW', 'no')
    }
