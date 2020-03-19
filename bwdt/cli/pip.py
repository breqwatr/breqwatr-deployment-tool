""" Commands for operating the Pip service """
import click

import bwdt.services.pip as pip

def get_pip_group():
    """ return the pip group function """
    @click.group(name='pip')
    def pip_group():
        """ Python package hosting service """
    pip_group.add_command(start)
    return pip_group


@click.option('--version', required=False, default=None,
              help='version override')
@click.command()
def start(version):
    """Launch the Pip service"""
    click.echo("Launching container: pip")
    pip.start(tag=version)

