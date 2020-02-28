""" Entrypoint for breqwatr-deployment-tool cli """
import click

import bwdt.cli.apt
import bwdt.cli.arcus
import bwdt.cli.registry
import bwdt.cli.pip
import bwdt.cli.pxe
import bwdt.lib.license as license


def get_service_group():
    """ Return the entrypoint click group """
    @click.group()
    def service():
        """ Manage Breqwatr's containerized services """
    service.add_command(bwdt.cli.apt.get_apt_group())
    service.add_command(bwdt.cli.registry.get_registry_group())
    service.add_command(bwdt.cli.pip.get_pip_group())
    service.add_command(bwdt.cli.pxe.get_pxe_group())
    if license.is_licensed():
        # These features only work with a valid license
        service.add_command(bwdt.cli.arcus.get_arcus_group())
    return service
