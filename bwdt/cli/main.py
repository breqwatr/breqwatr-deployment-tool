""" Entrypoint for breqwatr-deployment-tool cli """
import sys

import click

# Requires python 3
if sys.version_info[0] != 3:
    sys.stderr.write('ERROR: Python 3 required \n')
    sys.exit(42)

# flake8: noqa=402
# pylint: disable=wrong-import-position
import bwdt.cli.ceph
import bwdt.cli.configure
import bwdt.cli.download
import bwdt.cli.docker
import bwdt.cli.openstack
import bwdt.cli.service
import bwdt.cli.support
import bwdt.cli.util
import bwdt.lib.config as config
import bwdt.lib.envvar


def get_entrypoint():
    """ Return the entrypoint click group """
    @click.group()
    def entrypoint():
        """ Entrypoint for Click """
    entrypoint.add_command(bwdt.cli.ceph.get_ceph_group())
    entrypoint.add_command(bwdt.cli.configure.get_configure_group())
    entrypoint.add_command(bwdt.cli.download.get_download_group())
    entrypoint.add_command(bwdt.cli.docker.get_docker_group())
    entrypoint.add_command(bwdt.cli.openstack.get_openstack_group())
    entrypoint.add_command(bwdt.cli.service.get_service_group())
    entrypoint.add_command(bwdt.cli.util.get_util_group())
    if bwdt.lib.envvar.env()['BWDT_FEATURE_PREVIEW'] == 'yes':
        # These features are not ready for production, but available
        entrypoint.add_command(bwdt.cli.support.get_support_group())
    return entrypoint


def main():
    """ Entrypoint defined int setup.py for bwdt command"""
    try:
        entrypoint = get_entrypoint()
        entrypoint()
    except KeyboardInterrupt:
        # Handle ctrl+C without dumping a stack-trace
        sys.exit(100)
