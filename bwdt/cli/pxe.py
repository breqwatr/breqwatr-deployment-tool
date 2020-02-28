""" Commands for operating the PXE service """
import click

import bwdt.services.pxe as pxe


def get_pxe_group():
    """ Return the PXE click group """
    @click.group(name='pxe')
    def pxe_group():
        """ Network boot service - deploys Ubuntu 18.04 """
    pxe_group.add_command(start)
    return pxe_group


@click.option('--interface', required=True,
              help='Name of interface PXE service will listen on')
@click.option('--dhcp-start', required=True, help='DHCP range start IP')
@click.option('--dhcp-end', required=True, help='DHCP range end IP')
@click.option('--dns-ip', required=False, default='8.8.8.8',
              help='Optional alternative DNS IP')
@click.command()
def start(interface, dhcp_start, dhcp_end, dns_ip):
    """Launch the local PXE service"""
    click.echo("Launching container: pxe")
    success = pxe.start(
        interface=interface,
        dhcp_start=dhcp_start,
        dhcp_end=dhcp_end,
        dns_ip=dns_ip)
    if success:
        click.echo('Done')
    else:
        click.echo('Failed to launch - Maybe its already running?')
