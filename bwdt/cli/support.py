""" Support tunnel commands """
import sys
import time

import click

import bwdt.lib.support as support


def get_support_group():
    """ return the util group function """
    @click.group(name='support')
    def support_group():
        """ Support tunnel commands """
    support_group.add_command(status)
    support_group.add_command(open_tunnel)
    support_group.add_command(close_tunnel)
    return support_group


@click.command()
def status():
    """ Check if the tunnel is open """
    status = support.get_connection_status()
    if status['connected']:
        uptime = status['uptime']
        click.echo(f'Support tunnel is ONLINE - uptime: {uptime}')
    else:
        click.echo('Support tunnel is OFFLINE')


@click.command(name='open-tunnel')
def open_tunnel():
    """ Open a remote support tunnel sesion """
    status = support.get_connection_status()
    # if status['connected']:
    #    click.echo('Support tunnel is already open')
    #    return
    ssh_keys = support.get_ssh_keys()
    click.echo('Starting support tunnel:')
    support.start_tunnel(ssh_keys['public'])
    tunnel_up = False
    backoff_seconds = 30
    max_tries = 10
    tunnel = None
    for tries in range(1,(max_tries + 1)):
        tunnel = support.get_tunnel()
        click.echo('... Tunnel status is "{}"'.format(tunnel['status']))
        if tunnel['status'] == 'ONLINE':
            tunnel_up = True
            break
        click.echo('... Waiting {backoff_seconds}s ({tries}/{max_tries})')
        time.sleep(backoff_seconds)
        if not tunnel_up and tries == max_tries:
            sys.stderr.write('ERROR: Failed to launch the tunnel')
            sys.stderr.write('Status: {} - {}'.format(tunnel['status'],
                                                      tunnel['error']))
            sys.exit(1)
    click.echo('Opening remote support session')
    support.connect(tunnel)
    click.echo('Connection established')


@click.command(name='close-tunnel')
def close_tunnel():
    """ Close the support tunnel session """
    status = support.get_connection_status()
    if not status['connected']:
        click.echo('Support tunnel was already closed')
        return
    support.close_tunnel()
