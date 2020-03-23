""" Commands for operating the Ansible service """
import click

import bwdt.lib.openstack as openstack


def get_openstack_group():
    """ Return the OpenStack click group """
    @click.group(name='openstack')
    def openstack_group():
        """ Deploy and manage OpenStack """
    openstack_group.add_command(pull_kolla_ansible)
    openstack_group.add_command(generate_passwords)
    return openstack_group


@click.argument('release')
@click.command(name='pull-kolla-ansible')
def pull_kolla_ansible(release):
    """ Download the Kolla-Ansible image for the given release """
    click.echo('Downloading the Kolla-Ansible image')
    openstack.kolla_ansible_pull(release)


@click.argument('release')
@click.command(name='generate-passwords')
def generate_passwords(release):
    """ Generate passwords.yml and print to stdout """
    openstack.kolla_ansible_genpwd(release)
