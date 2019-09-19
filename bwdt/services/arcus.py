""" Controls for the Arcus service """
import mysql.connector


def _create_arcus_database(cursor):
    """ Create the database named arcus if it doesn't exist """
    cursor.execute("SHOW DATABASES;")
    databases = cursor.fetchall()
    if ('arcus',) in databases:
        return
    cursor.execute("CREATE DATABASE arcus;")


def _create_arcus_dbuser(cursor, password):
    """ Create the arcus user in the DB """
    cursor.execute('SELECT user FROM mysql.user;')
    users = cursor.fetchall()
    if (bytearray(b'arcus'),) in users:
        return
    create_cmd = 'CREATE USER arcus IDENTIFIED BY "{}"'.format(password)
    cursor.execute(create_cmd)
    grant_cmd = 'GRANT ALL privileges ON arcus.* TO "arcus";'
    cursor.execute(grant_cmd)


def init_database(host, admin_user, admin_passwd, arcus_passwd):
    """ Initialize the Arcus database """
    conn = mysql.connector.connect(host=host, user=admin_user,
                                   passwd=admin_passwd)
    cursor = conn.cursor()
    _create_arcus_database(cursor)
    _create_arcus_dbuser(cursor, arcus_passwd)
