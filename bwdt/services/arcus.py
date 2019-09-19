""" Controls for the Arcus service """
import mysql.connector

from bwdt.constants import SERVICE_IMAGE_TAGS
from bwdt.container import Docker
from bwdt.openstack import Openstack


def _create_arcus_database(cursor):
    """ Create the database named arcus if it doesn't exist """
    cursor.execute("SHOW DATABASES;")
    databases = cursor.fetchall()
    if ('arcus',) in databases:
        return False
    cursor.execute("CREATE DATABASE arcus;")
    return True


def _create_arcus_dbuser(cursor, password):
    """ Create the arcus user in the DB """
    cursor.execute('SELECT user FROM mysql.user;')
    users = cursor.fetchall()
    if (bytearray(b'arcus'),) in users:
        return False
    create_cmd = 'CREATE USER arcus IDENTIFIED BY "{}"'.format(password)
    cursor.execute(create_cmd)
    grant_cmd = 'GRANT ALL privileges ON arcus.* TO "arcus";'
    cursor.execute(grant_cmd)
    return True


def init_database(host, admin_user, admin_passwd, arcus_passwd):
    """ Initialize the Arcus database """
    conn = mysql.connector.connect(host=host, user=admin_user,
                                   passwd=admin_passwd)
    cursor = conn.cursor()
    created_db = _create_arcus_database(cursor)
    created_user = _create_arcus_dbuser(cursor, arcus_passwd)
    return {'created_db': created_db, 'created_user': created_user}


def _create_arcusadmin_openstack_user(openstack, password):
    """ Create the arcusadmin service account in OpenStack """
    users = openstack.keystone.users.list()
    arcus_user = next((usr for usr in users if usr.name == 'arcusadmin'),
                      False)
    if arcus_user:
        return False
    openstack.keystone.users.create(
        name='arcusadmin',
        domain='default',
        password=password,
        email='alerts@breqwatr.com',
        description='Arcus service account')
    return True


def _grant_arcusadmin_openstack_admin_roles(openstack):
    """ Grant amdmin roles to the openstack arcusadmin user """
    user = openstack.keystone.users.find(name='arcusadmin')
    role = openstack.keystone.roles.find(name='admin')
    project = openstack.keystone.projects.find(name='admin')
    openstack.keystone.roles.grant(role=role.id, user=user.id,
                                   project=project.id)
    openstack.keystone.roles.grant(role=role.id, user=user.id,
                                   domain='default')


def create_openstack_sa(fqdn, admin_password, arcus_pass, https=True):
    """ Initialize the OpenStack overcloud for the Arcus service """
    openstack = Openstack(fqdn=fqdn, user='admin', password=admin_password,
                          project='admin', https=https)
    created = _create_arcusadmin_openstack_user(openstack, arcus_pass)
    if created:
        _grant_arcusadmin_openstack_admin_roles(openstack)
    return created


# pylint: disable=R0914
def api_start(fqdn, rabbit_pass, rabbit_ips_list, sql_ip,
              sql_password, ceph_enabled=False, https=True):
    """ Start the Arcus API service """
    name = "arcus_api"
    repo = "breqwatr/arcus-api"
    tag = SERVICE_IMAGE_TAGS[repo]
    image = '{}:{}'.format(repo, tag)
    rabbit_ips_csv = ','.join(rabbit_ips_list)
    docker_kwargs = {
        'environment': {
            'OPENSTACK_VIP': fqdn,
            'PUBLIC_ENDPOINT': 'true',
            'HTTPS_OPENSTACK_APIS': str(https).lower(),
            'RABBITMQ_USERNAME': 'openstack',
            'RABBITMQ_PASSWORD': rabbit_pass,
            'RABBIT_IPS_CSV': rabbit_ips_csv,
            'SQL_USERNAME': 'arcus',
            'SQL_PASSWORD': sql_password,
            'SQL_IP': sql_ip,
            'CEPH_ENABLED': str(ceph_enabled).lower()
        },
        'ports': {'1234': ('0.0.0.0', '1234')}
    }
    docker = Docker()
    docker.pull(repository=repo, tag=tag)
    success = docker.run(image, name=name, **docker_kwargs)
    return success
