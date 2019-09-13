"""Commands for operating the local registry"""
import click

import bwdt.services as services


@click.group()
def registry():
    """Command group for bwdt registry"""


@click.option('--ip', default='0.0.0.0', help='optional bind IP address')
@click.option('--port', default='5000', help='optional bind port')
@click.command()
def start(ip, port):
    """Launch the local registry"""
    click.echo("Launching container: registry")
    success = services.registry_start(ip, port)
    if success:
        click.echo('Done')
    else:
        click.echo('Failed to launch - Maybe its already running?')


registry.add_command(start)
