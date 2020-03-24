""" Openstack client and deployment logic """
import requests
import pathlib
import sys

from keystoneauth1 import session
from keystoneauth1.identity import v3
from keystoneclient.v3 import client as keystone

import bwdt.constants as constants
import bwdt.lib.docker as docker


# pylint: disable-all
requests.packages.urllib3.disable_warnings()


def assert_file_exists(file_path):
    """ Gracefully exist if a file does not exist """
    path = pathlib.Path(file_path)
    if not path.exists():
        err = f'ERROR: Expected file {file_path} not found\n'
        sys.stderr.write(err)
        sys.exit(1)


def get_absolute_path(file_path):
    """ Return the absolute path of a potentially relative file path"""
    path = pathlib.Path(file_path)
    absolute_path = '{}/{}'.format(path.parent.absolute(), path)
    return str(absolute_path)


def kolla_ansible_pull(release):
    """ Pull the kolla_ansible image """
    docker.assert_valid_release(release)
    docker.get_image('kolla-ansible', release)


def kolla_ansible_genpwd(release):
    """ Genereate passwords.yml and print to stdout """
    docker.assert_valid_release(release)
    docker.assert_image_pulled('kolla-ansible', release)
    path = '/var/repos/kolla-ansible/etc/kolla/passwords.yml'
    cmd = (f'docker run --rm {constants.IMAGE_PREFIX}/kolla-ansible:{release} '
           f'bash -c "kolla-genpwd --passwords {path} '
           f'&& cat {path}"')
    docker.shell(cmd)


def kolla_ansible_inventory(release):
    """ Print the inventory template for the given release """
    docker.assert_valid_release(release)
    docker.assert_image_pulled('kolla-ansible', release)
    cmd = (f'docker run --rm {constants.IMAGE_PREFIX}/kolla-ansible:{release} '
           f'cat /var/repos/kolla-ansible/ansible/inventory/all-in-one')
    docker.shell(cmd)


def _volume_opt(src, dest):
    """ Return a volume optional argument for docker run commands """
    assert_file_exists(src)
    absolute_path = get_absolute_path(src)
    return f'-v {absolute_path}:{dest} '


def kolla_ansible_bootstrap(release, inventory_path, globals_path,
                            passwords_path, ssh_key_path):
    """ Run kolla-ansible bootstrap """
    docker.assert_valid_release(release)
    docker.assert_image_pulled('kolla-ansible', release)
    cmd = (f'docker run --rm --network host '
           + _volume_opt(inventory_path, '/etc/kolla/inventory')
           + _volume_opt(globals_path, '/etc/kolla/globals.yml')
           + _volume_opt(passwords_path, '/etc/kolla/passwords.yml')
           + _volume_opt(ssh_key_path, '/root/.ssh/id_rsa')
           + f'{constants.IMAGE_PREFIX}/kolla-ansible:{release} '
           f'kolla-ansible bootstrap-servers -i /etc/kolla/inventory')
    docker.shell(cmd)


def kolla_ansible_pull_images(release, inventory_path, globals_path,
                              passwords_path, ssh_key_path):
    """ Run kolla-ansible pull """
    docker.assert_valid_release(release)
    docker.assert_image_pulled('kolla-ansible', release)
    cmd = (f'docker run --rm --network host'
           + _volume_opt(inventory_path, '/etc/kolla/inventory')
           + _volume_opt(globals_path, '/etc/kolla/globals.yml')
           + _volume_opt(passwords_path, '/etc/kolla/passwords.yml')
           + _volume_opt(ssh_key_path, '/root/.ssh/id_rsa')
           + f'{constants.IMAGE_PREFIX}/kolla-ansible:{release} '
           f'kolla-ansible pull -i /etc/kolla/inventory')
    docker.shell(cmd)


def kolla_ansible_deploy(release, globals_path, inventory_path, passwords_path,
                         ssh_key_path, config_dir=None):
    """ Run kolla-ansible deploy """
    docker.assert_valid_release(release)
    docker.assert_image_pulled('kolla-ansible', release)


class OpenstackClient(object):
    """ Auth'd Openstack Client class with services as properties """
    def __init__(self, fqdn, user, password, project, https=True):
        proto = 'https' if https else 'http'
        auth_url = '{}://{}:5000/v3'.format(proto, fqdn)
        auth_url = '{}://{}:5000/v3'.format(proto, fqdn)
        auth = v3.Password(
            auth_url=auth_url,
            username=user,
            password=password,
            project_name=project,
            user_domain_id='default',
            project_domain_id='default')
        sess = session.Session(auth=auth, verify=False)
        self.keystone = keystone.Client(session=sess)
