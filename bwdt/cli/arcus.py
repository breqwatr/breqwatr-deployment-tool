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


@click.group()
def api():
    """ Command group for Arcus API """


@click.option('--openstack-fqdn', required=True, help='fqdn/VIP of openstack')
@click.option('--rabbit-pass', required=True, help='RabbitMQ password')
@click.option('--rabbit-ip', required=True, multiple=True,
              help='IP(s) of RabbitMQ service. Repeat for each IP.')
@click.option('--sql-ip', required=True, help='IP/VIP of SQL service')
@click.option('--sql-password', required=True, help='password for SQL service')
@click.option('--ceph/--no-ceph', required=False, default=False,
              help='use --ceph to enable Ceph features')
@click.option('--https/--http', default=True, required=False,
              help='Use --http to disable HTTPS')
@click.command(name='start')
def api_start(openstack_fqdn, rabbit_pass, rabbit_ip, sql_ip, sql_password,
              ceph, https):
    """ Start the Arcus API container """
    arcus.api_start(
        fqdn=openstack_fqdn,
        rabbit_pass=rabbit_pass,
        rabbit_ips_list=rabbit_ip,
        sql_ip=sql_ip,
        sql_password=sql_password,
        ceph_enabled=ceph,
        https=https)


arcus_group.add_command(database_init)
arcus_group.add_command(create_service_account)

api.add_command(api_start)
arcus_group.add_command(api)
