"""Entrypoint for breqwatr-deployment-tool cli"""
import click

import bwdt.cli.registry


@click.group()
def main():
    """Entrypoint for breqwatr deployment tool cli"""


main.add_command(bwdt.cli.registry.registry)
