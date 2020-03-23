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
    openstack_group.add_command(get_inventory_template)
    openstack_group.add_command(bootstrap)
    openstack_group.add_command(pull_images)
    return openstack_group


@click.option('--release', help='OpenStack release name', required=True)
@click.command(name='pull-kolla-ansible')
def pull_kolla_ansible(release):
    """ Download the Kolla-Ansible Docker image """
    click.echo('Downloading the Kolla-Ansible image')
    openstack.kolla_ansible_pull(release)


@click.option('--release', help='OpenStack release name', required=True)
@click.command(name='generate-passwords')
def generate_passwords(release):
    """ Generate passwords.yml and print to stdout """
    openstack.kolla_ansible_genpwd(release)


@click.option('--release', help='OpenStack release name', required=True)
@click.command(name='get-inventory-template')
def get_inventory_template(release):
    """ Print a template inventory to stdout """
    openstack.kolla_ansible_inventory(release)


@click.option('--release', help='OpenStack release name', required=True)
@click.option('--inventory-file', 'inventory_file', required=True,
              help='Path the the Ansible inventory file')
@click.option('--globals-file', 'globals_file', required=True,
              help='Path to the globals.yml file')
@click.command(name='bootstrap')
def bootstrap(release, inventory_file, globals_file):
    """ Bootstrap the OpenStack nodes """
    openstack.kolla_ansible_bootstrap(
        release=release,
        inventory_path=inventory_file,
        globals_path=globals_file)


@click.option('--release', help='OpenStack release name', required=True)
@click.option('--inventory-file', 'inventory_file', required=True,
              help='Path the the Ansible inventory file')
@click.option('--globals-file', 'globals_file', required=True,
              help='Path to the globals.yml file')
@click.command(name='pull-images')
def pull_images(release, inventory_file, globals_file):
    """ Pull the Kolla OpenStack images to each node """
    openstack.kolla_ansible_pull_images(
        release=release,
        inventory_path=inventory_file,
        globals_path=globals_file)
