"""Commands for operating the local registry"""
import click


@click.group()
def registry():
    """Command group for bwdt registry"""


@click.command()
def start():
    """Launch the local registry"""
    click.echo("Launching the local registry")


registry.add_command(start)
