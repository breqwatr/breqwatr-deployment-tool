""" Entrypoint for breqwatr-deployment-tool cli """
import click

import bwdt.cli.ansible
import bwdt.cli.apt
import bwdt.cli.arcus
import bwdt.cli.configure
import bwdt.cli.docker
import bwdt.cli.download
import bwdt.cli.util
import bwdt.cli.registry
import bwdt.cli.pip
import bwdt.cli.pxe
import bwdt.lib.auth as auth
import bwdt.lib.configure


@click.group()
def main():
    """ Entrypoint for breqwatr deployment tool cli """
    if auth.get() is None:
        bwdt.lib.configure.configure()


main.add_command(bwdt.cli.ansible.ansible_group)
main.add_command(bwdt.cli.apt.apt_group)
main.add_command(bwdt.cli.arcus.arcus_group)
main.add_command(bwdt.cli.configure.configure_group)
main.add_command(bwdt.cli.docker.docker_group)
main.add_command(bwdt.cli.download.download_group)
main.add_command(bwdt.cli.util.util_group)
main.add_command(bwdt.cli.registry.registry_group)
main.add_command(bwdt.cli.pip.pip_group)
main.add_command(bwdt.cli.pxe.pxe_group)
