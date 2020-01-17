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


def entrypoint():
    """ Return the entrypoint click group """
    @click.group()
    def entrypoint():
        """ Entrypoint for Click """
        pass
    entrypoint.add_command(bwdt.cli.ansible.ansible_group)
    entrypoint.add_command(bwdt.cli.apt.apt_group)
    entrypoint.add_command(bwdt.cli.arcus.arcus_group)
    entrypoint.add_command(bwdt.cli.configure.configure_group)
    entrypoint.add_command(bwdt.cli.docker.docker_group)
    entrypoint.add_command(bwdt.cli.download.download_group)
    entrypoint.add_command(bwdt.cli.util.util_group)
    entrypoint.add_command(bwdt.cli.registry.registry_group)
    entrypoint.add_command(bwdt.cli.pip.pip_group)
    entrypoint.add_command(bwdt.cli.pxe.pxe_group)
    return entrypoint()


def main():
    """ Entrypoint defined int setup.py for bwdt command"""
    if auth.get() is None:
        bwdt.lib.configure.configure()
    entrypoint()
