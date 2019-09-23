""" Entrypoint for breqwatr-deployment-tool cli """
import click

import bwdt.cli.ansible
import bwdt.cli.arcus
import bwdt.cli.configure
import bwdt.cli.docker
import bwdt.cli.registry
import bwdt.cli.pxe


@click.group()
def main():
    """ Entrypoint for breqwatr deployment tool cli """


main.add_command(bwdt.cli.ansible.ansible_group)
main.add_command(bwdt.cli.arcus.arcus_group)
main.add_command(bwdt.cli.configure.configure)
main.add_command(bwdt.cli.docker.docker)
main.add_command(bwdt.cli.registry.registry_group)
main.add_command(bwdt.cli.pxe.pxe_group)
