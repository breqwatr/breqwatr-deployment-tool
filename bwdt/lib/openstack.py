""" Openstack client and deployment logic """
import os
import pathlib
import requests
import sys

from keystoneauth1 import session
from keystoneauth1.identity import v3
from keystoneclient.v3 import client as keystone

import bwdt.constants as constants
import bwdt.lib.docker as docker


# pylint: disable-all
requests.packages.urllib3.disable_warnings()


def get_absolute_path(file_path):
    """ Return the absolute path of a potentially relative file path"""
    path = pathlib.Path(file_path)
    path = path.expanduser()
    path = path.absolute()
    return str(path)


def assert_file_exists(file_path):
    """ Gracefully exist if a file does not exist """
    path = pathlib.Path(get_absolute_path(file_path))
    if not path.exists():
        err = f'ERROR: Expected file/directory {file_path} not found\n'
        sys.stderr.write(err)
        sys.exit(1)


def kolla_ansible_pull(release, force=True):
    """ Pull the kolla_ansible image """
    docker.assert_valid_release(release)
    if force is False and docker.is_image_pulled('kolla-ansible', release):
        return
    docker.assert_valid_release(release)
    docker.get_image('kolla-ansible', release)


def kolla_ansible_genpwd(release):
    """ Genereate passwords.yml and print to stdout """
    kolla_ansible_pull(release, force=False)
    cwd = os.getcwd()
    path = '/var/repos/kolla-ansible/etc/kolla/passwords.yml'
    cmd = (f'docker run --rm '
           f'-v {cwd}:/etc/kolla '
           f'{constants.IMAGE_PREFIX}/kolla-ansible:{release} '
           f'bash -c "kolla-genpwd --passwords {path} '
           f'&& cp {path} /etc/kolla/passwords.yml"')
    docker.shell(cmd)


def kolla_ansible_inventory(release):
    """ Print the inventory template for the given release """
    kolla_ansible_pull(release, force=False)
    cwd = os.getcwd()
    inventory_file = '/var/repos/kolla-ansible/ansible/inventory/all-in-one'
    cmd = (f'docker run --rm '
           f'-v {cwd}:/etc/kolla '
           f'{constants.IMAGE_PREFIX}/kolla-ansible:{release} '
           f'cp {inventory_file} /etc/kolla/inventory')
    docker.shell(cmd)


def _volume_opt(src, dest):
    """ Return a volume optional argument for docker run commands """
    assert_file_exists(src)
    absolute_path = get_absolute_path(src)
    return f'-v {absolute_path}:{dest} '


def kolla_ansible_generate_certificates(release, passwords_path, globals_path):
    """ Genereate certificates directory """
    kolla_ansible_pull(release, force=False)
    cwd = os.getcwd()
    cmd = (f'docker run --rm '
           + _volume_opt(globals_path, '/etc/kolla/globals.yml')
           + _volume_opt(passwords_path, '/etc/kolla/passwords.yml') +
           f'-v {cwd}/certificates:/etc/kolla/certificates '
           f'{constants.IMAGE_PREFIX}/kolla-ansible:{release} '
           f'kolla-ansible certificates')
    docker.shell(cmd)


def kolla_ansible_get_admin_openrc(release, inventory_path, globals_path,
                                   passwords_path):
    """ Run kolla-ansible post-deploy and get file """
    docker.assert_valid_release(release)
    docker.assert_image_pulled('kolla-ansible', release)
    cwd = os.getcwd()
    cmd = (f'docker run --rm --network host '
           + _volume_opt(inventory_path, '/etc/kolla/inventory')
           + _volume_opt(globals_path, '/etc/kolla/globals.yml')
           + _volume_opt(passwords_path, '/etc/kolla/passwords.yml')
           + f'-v {cwd}:/target '
           f'{constants.IMAGE_PREFIX}/kolla-ansible:{release} '
           f'bash -c "kolla-ansible post-deploy -i /etc/kolla/inventory && '
           f'cp /etc/kolla/admin-openrc.sh /target/"')
    docker.shell(cmd)


def kolla_ansible_exec(release, inventory_path, globals_path, passwords_path,
                       ssh_key_path, certificates_dir, config_dir,
                       command):
    """ Run kolla-ansible pull """
    valid_cmds = ['deploy', 'mariadb_recovery', 'prechecks', 'post-deploy',
                  'pull', 'reconfigure', 'upgrade', 'check', 'stop',
                  'deploy-containers', 'prune-images']
    if command not in valid_cmds:
        err = (f'ERROR: Invalid command "{command}" - '
               f'Valid commands: {valid_cmds}\n')
        sys.stderr.write(err)
        sys.exit(1)
    docker.assert_valid_release(release)
    kolla_ansible_pull(release, force=False)
    config_vol = ' '
    if config_dir is not None:
        config_vol = _volume_opt(config_dir, '/etc/kolla/config')
    cmd = (f'docker run --rm --network host '
           + _volume_opt(inventory_path, '/etc/kolla/inventory')
           + _volume_opt(globals_path, '/etc/kolla/globals.yml')
           + _volume_opt(passwords_path, '/etc/kolla/passwords.yml')
           + _volume_opt(ssh_key_path, '/root/.ssh/id_rsa')
           + _volume_opt(certificates_dir, '/etc/kolla/certificates')
           + config_vol
           + f'{constants.IMAGE_PREFIX}/kolla-ansible:{release} '
           f'kolla-ansible {command} -i /etc/kolla/inventory')
    docker.shell(cmd)


def cli_exec(release, openrc_path, command, volume=None):
    """ Execute <command> using breqwatr/openstack-client:<release>

        Optionally, mount file(s) into the client with the volume arg
    """
    docker.assert_valid_release(release)
    command = 'openstack' if command is None else command
    mount = '-v {volume} ' if volume is not None else ' '
    cmd = (f'docker run -it --rm --network host '
           + _volume_opt(openrc_path, '/admin-openrc.sh')
           + mount +
           f'{constants.IMAGE_PREFIX}/openstack-client:{release} '
           f'bash -c "source /admin-openrc.sh && '
           f'. /var/repos/env/bin/activate && {command}"')
    docker.shell(cmd, print_error=False)


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
