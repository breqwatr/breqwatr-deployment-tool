""" Commands for operating the Apt service """
import click

import bwdt.services.apt as apt


def get_apt_group():
    """ return the apt_group """
    @click.group(name='apt')
    def apt_group():
        """ Ubuntu package hosting service """
    apt_group.add_command(start)
    return apt_group


@click.option('--version', required=False, default=None,
              help='version override')
@click.option('--port', required=True, help='TCP listen port for Apt')
@click.command()
def start(version, port):
    """Launch the Apt service"""
    click.echo("Launching container: apt")
    apt.start(tag=version, port=port)
