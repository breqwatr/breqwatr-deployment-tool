""" Openstack client and deployment logic"""
import requests

from keystoneauth1 import session
from keystoneauth1.identity import v3
from keystoneclient.v3 import client as keystone

import bwdt.constants as constants
import bwdt.lib.docker as docker


# pylint: disable-all
requests.packages.urllib3.disable_warnings()


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
