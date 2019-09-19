""" Commands for operating the PXE service """
import click

import bwdt.services.arcus as arcus


@click.group(name='arcus')
def arcus_group():
    """ Command group for Arcus """


@click.option('--host', required=True, help='MariaDB IP or FQDN')
@click.option('--admin-user', required=True, help='User to create the DB')
@click.option('--admin-pass', required=True, help='Password to create the DB')
@click.option('--arcus-pass', required=True, help='"arcus" DB user password')
@click.command(name='database-init')
def database_init(host, admin_user, admin_pass, arcus_pass):
    """ Initialize the Arcus database """
    result = arcus.init_database(host, admin_user, admin_pass, arcus_pass)
    for key in result:
        click.echo('{}: {}'.format(key, result[key]))


arcus_group.add_command(database_init)
