""" Commands to configure BWDT """
import sys
from pprint import pprint

import click

import bwdt.lib.config as config
import bwdt.lib.license as license


# pylint: disable=inconsistent-return-statements
@click.option('--set', 'new_key', default=None, help='Set a new license key')
@click.command(name='license')
def license(new_key):
    """ Set or show the Breqwatr license key """
    if new_key is None:
        if not config.config_exists():
            return
        data = config.get_config()
        click.echo(data['license'])
    else:
        if not license.is_valid_license(new_key):
            err = 'ERROR: License does not appear valid\n'
            sys.exit(1)
        data = config.get_config()
        data['license'] = new_key
        config.set_config(data)
        click.echo(new_key)


def get_configure_group():
    """ return the configure group function """
    @click.group(name='configure')
    def configure_group():
        """ Interact with the BWDT Configuration """
    configure_group.add_command(license)
    return configure_group
