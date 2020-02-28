""" Entrypoint for breqwatr-deployment-tool cli """
import sys

import click

# Requires python 3
if sys.version_info[0] != 3:
    sys.stderr.write('ERROR: Python 3 required \n')
    sys.exit(42)

# flake8: noqa=402
# pylint: disable=wrong-import-position
import bwdt.cli.ansible
import bwdt.cli.apt
import bwdt.cli.arcus
import bwdt.cli.configure
import bwdt.cli.docker
import bwdt.cli.download
import bwdt.cli.support
import bwdt.cli.util
import bwdt.cli.registry
import bwdt.cli.pip
import bwdt.cli.pxe
import bwdt.lib.config as config
import bwdt.lib.envvar
import bwdt.lib.license as license


def get_entrypoint():
    """ Return the entrypoint click group """
    @click.group()
    def entrypoint():
        """ Entrypoint for Click """
    entrypoint.add_command(bwdt.cli.configure.get_configure_group())
    entrypoint.add_command(bwdt.cli.ansible.get_ansible_group())
    entrypoint.add_command(bwdt.cli.apt.get_apt_group())
    entrypoint.add_command(bwdt.cli.docker.get_docker_group())
    entrypoint.add_command(bwdt.cli.download.get_download_group())
    entrypoint.add_command(bwdt.cli.util.get_util_group())
    entrypoint.add_command(bwdt.cli.registry.get_registry_group())
    entrypoint.add_command(bwdt.cli.pip.get_pip_group())
    entrypoint.add_command(bwdt.cli.pxe.get_pxe_group())
    if license.is_licensed():
        # These features only work with a valid license
        entrypoint.add_command(bwdt.cli.arcus.get_arcus_group())
    if bwdt.lib.envvar.env()['BWDT_FEATURE_PREVIEW'] == 'yes':
        # These features are not ready for production, but available
        entrypoint.add_command(bwdt.cli.support.get_support_group())
    return entrypoint


def main():
    """ Entrypoint defined int setup.py for bwdt command"""
    try:
        if not config.is_config_found():
            bwdt.cli.configure.config_wizard()
        entrypoint = get_entrypoint()
        entrypoint()
    except KeyboardInterrupt:
        sys.exit(100)

