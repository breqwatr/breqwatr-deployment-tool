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
    res = arcus.init_database(
        host=host,
        admin_user=admin_user,
        admin_passwd=admin_pass,
        arcus_passwd=arcus_pass)
    for key in res:
        click.echo('{}: {}'.format(key, res[key]))


@click.option('--cloud-fqdn', required=True, help='FQDN or VIP for OpenStack')
@click.option('--bootstrap-password', required=True,
              help='Bootstrap \'admin\' SA user\'s password')
@click.option('--sa-password', required=True, help='Service account password')
@click.option('--https/--http', default=True, required=False,
              help='Use --http to disable HTTPS')
@click.command('create-service-account')
def create_service_account(cloud_fqdn, bootstrap_password, sa_password, https):
    """ Create the arcusadmin service account """
    created = arcus.create_openstack_sa(
        fqdn=cloud_fqdn,
        admin_password=bootstrap_password,
        arcus_pass=sa_password,
        https=https)
    if created:
        click.echo('Arcus service account created')
    else:
        click.echo('Arcus service account not created - maybe it exists?')


arcus_group.add_command(database_init)
arcus_group.add_command(create_service_account)
