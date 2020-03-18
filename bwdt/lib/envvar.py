""" Central place to reference the environment variables used """
import os


def _env_get(env_name, default_val):
    """ Return an environment variable if defined else default value """
    if env_name in os.environ:
        return os.environ[env_name]
    return default_val


# BWDT_CONF_PATH:       Path to the bwdt configuration file
# BWDT_AWS_REGION:      AWS region to use for ECR, S3, etc
# BWDT_FEATURE_PREVIEW: Display unstable in-development features
# BWDT_DHUB_OVERRIDE:   Use docker hub even when licensed
# BWDT_DEBUG:           Enable debug mode
# BWDT_DISABLE_SHELL:   Don't run shell commands (Docker) when enabled

def env():
    """ Dictionary of environment variables or their default value """
    home = os.path.expanduser("~")
    default_conf_path = f'{home}/.breqwatr/config.json'
    return {
        'BWDT_CONF_PATH': _env_get('BWDT_CONF_PATH', default_conf_path),
        'BWDT_AWS_REGION': _env_get('BWDT_AWS_REGION', 'ca-central-1'),
        'BWDT_FEATURE_PREVIEW': _env_get('BWDT_FEATURE_PREVIEW', 'no'),
        'BWDT_DHUB_OVERRIDE': _env_get('BWDT_FEATURE_PREVIEW', 'false'),
        'BWDT_DEBUG': _env_get('BWDT_DEBUG', 'false'),
        'BWDT_DISABLE_SHELL': _env_get('BWDT_DISABLE_SHELL', 'false'),
    }
