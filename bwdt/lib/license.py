""" BWDT license library """
import bwdt.lib.config as config


def get_keys_from_license(license):
    """ Return tupple: (bool if valid, dict with 'id' and 'secret' keys) """
    if len(license) != 61 or license[20] != '-':
        return (False, {})
    key_id = license[0:19]
    key_secret = license[21:61]
    return True, {'id': key_id, 'secret': key_secret}


def is_valid_license(license):
    """ Check if a license looks valid """
    return get_keys_from_license(license)[0]

def keys():
    """ Return the AWS Key ID and secret from license """
    license = config.get_config()['license']
    return get_keys_from_license(license)


def is_licensed():
    """ Return bool, has this user applied a license """
    return keys()[0]
