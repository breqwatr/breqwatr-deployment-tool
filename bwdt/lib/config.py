""" BWDT Config File functions """
import json
from pathlib import Path

import bwdt.lib.envvar


DEFAULTS = {
    'license': '',
    'offline': 'true',
    'offline_path': '',
    'update_images': 'true'}


def get_config():
    """ Return the conf file content.

        Create file if not found.
        Apply defaults when not present from DEFAULTS constant
    """
    path = Path(bwdt.lib.envvar.env()['BWDT_CONF_PATH'])
    data = {}
    if path.exists():
        with open(path, 'r') as conf_file:
            data = json.load(conf_file)
    for key in DEFAULTS:
        if key not in data:
            data[key] = DEFAULTS[key]
    return data


def set_config(config):
    """ Write the config file """
    data = get_config()
    filename = bwdt.lib.envvar.env()['BWDT_CONF_PATH']
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    for key in config:
        data[key] = config[key]
    jdata = json.dumps(data, indent=4, sort_keys=True)
    jdata = jdata.rstrip()
    with open(filename, 'w+') as out_file:
        out_file.write(jdata)


def is_config_found():
    """ Return bool if config file exists """
    filename = bwdt.lib.envvar.env()['BWDT_CONF_PATH']
    path = Path(filename)
    return path.exists()


def is_offline():
    """ Return if ECR should be used, safely handing str values """
    data = get_config()
    return str(data['offline']).lower() == 'false'