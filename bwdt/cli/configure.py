""" Commands to configure BWDT """
from pprint import pprint

import click

import bwdt.lib.auth as auth
import bwdt.lib.configure


@click.group(name='configure')
def configure_group():
    """ Interact with the BWDT Configuration """


@click.command()
def setup():
    """ Re-Launch the setup wizard """
    bwdt.lib.configure.configure()


@click.command()
def show():
    """ Print the current config """
    pprint(auth.get())


configure_group.add_command(setup)
configure_group.add_command(show)
