""" Entrypoint for breqwatr-deployment-tool cli """
import click

# Requires python 3
import sys
if sys.version_info[0] != 3:
    sys.stdout.write('ERROR: Python 3 required \n')
    sys.exit(42)

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


def get_entrypoint():
    """ Return the entrypoint click group """
    @click.group()
    def entrypoint():
        """ Entrypoint for Click """
        pass
    entrypoint.add_command(bwdt.cli.ansible.get_ansible_group())
    entrypoint.add_command(bwdt.cli.apt.get_apt_group())
    entrypoint.add_command(bwdt.cli.arcus.get_arcus_group())
    entrypoint.add_command(bwdt.cli.configure.get_configure_group())
    entrypoint.add_command(bwdt.cli.docker.get_docker_group())
    entrypoint.add_command(bwdt.cli.download.get_download_group())
    entrypoint.add_command(bwdt.cli.util.get_util_group())
    entrypoint.add_command(bwdt.cli.registry.get_registry_group())
    entrypoint.add_command(bwdt.cli.pip.get_pip_group())
    entrypoint.add_command(bwdt.cli.pxe.get_pxe_group())
    return entrypoint


def main():
    """ Entrypoint defined int setup.py for bwdt command"""
    if auth.get() is None:
        bwdt.lib.configure.configure()
    entrypoint = get_entrypoint()
    entrypoint()
