""" Controls for the Arcus service """
import mysql.connector

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
    arcus_user = next((usr for usr in users if usr.name == 'arcus'), False)
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
