""" Entrypoint for breqwatr-deployment-tool cli """
import click

import bwdt.cli.ansible
import bwdt.cli.registry
import bwdt.cli.pxe


@click.group()
def main():
    """ Entrypoint for breqwatr deployment tool cli """


main.add_command(bwdt.cli.registry.registry)
main.add_command(bwdt.cli.pxe.pxe)
main.add_command(bwdt.cli.ansible.ansible)
