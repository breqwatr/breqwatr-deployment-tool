""" Commands for operating the Pip service """
import click

import bwdt.services.pip as pip

def get_pip_group():
    """ return the pip group function """
    @click.group(name='pip')
    def pip_group():
        """ Command group for bwdt Pip service """
    pip_group.add_command(start)
    return pip_group


@click.option('--tag', required=False, default=None, help='optional tag')
@click.command()
def start(tag):
    """Launch the Pip service"""
    click.echo("Launching container: pip")
    success = pip.start(tag)
    if success:
        click.echo('Done')
    else:
        click.echo('Failed to launch - Maybe its already running?')


