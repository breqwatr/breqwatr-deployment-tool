""" Commands to configure BWDT """
from pprint import pprint

import click

import bwdt.lib.auth as auth
import bwdt.lib.configure


def get_configure_group():
    """ return the configure group function """
    @click.group(name='configure')
    def configure_group():
        """ Interact with the BWDT Configuration """
    configure_group.add_command(setup)
    configure_group.add_command(show)
    return configure_group


@click.command()
def setup():
    """ Re-Launch the setup wizard """
    bwdt.lib.configure.configure()


@click.command()
def show():
    """ Print the current config """
    pprint(auth.get())


