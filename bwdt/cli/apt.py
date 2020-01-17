""" Commands for operating the Apt service """
import click

import bwdt.services.apt as apt

def get_apt_group():
    """ return the apt_group """
    @click.group(name='apt')
    def apt_group():
        """ Command group for bwdt PXE service """
    apt_group.add_command(start)
    return apt_group


@click.option('--tag', required=False, default=None, help='optional tag')
@click.option('--port', required=False, default=81, help='listen port')
@click.command()
def start(tag, port):
    """Launch the Apt service"""
    click.echo("Launching container: apt")
    success = apt.start(tag=tag, port=port)
    if success:
        click.echo('Done')
    else:
        click.echo('Failed to launch - Maybe its already running?')


