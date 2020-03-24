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
    openstack_group.add_command(deploy)
    openstack_group.add_command(generate_certificates)
    openstack_group.add_command(get_admin_openrc)
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
    click.echo('Creating password file: ./passwords.yml')
    openstack.kolla_ansible_genpwd(release)


@click.option('--release', help='OpenStack release name', required=True)
@click.command(name='get-inventory-template')
def get_inventory_template(release):
    """ Print a template inventory to stdout """
    click.echo('Creating inventory template: ./inventory')
    openstack.kolla_ansible_inventory(release)


@click.option('--release', help='OpenStack release name', required=True)
@click.option('--passwords-file', 'passwords_file', required=True,
              help='Path the the passwords.yml file')
@click.option('--globals-file', 'globals_file', required=True,
              help='Path to the globals.yml file')
@click.command(name='generate-certificates')
def generate_certificates(release, passwords_file, globals_file):
    """ Generate self signed certificates, write to certificates/ """
    click.echo(f'Generating ./certificates/')
    openstack.kolla_ansible_generate_certificates(
        release=release,
        passwords_path=passwords_file,
        globals_path=globals_file)


@click.option('--release', help='OpenStack release name', required=True)
@click.option('--ssh-private-key-file', 'ssh_private_key_file', required=True,
              help='Path the the SSH private key file')
@click.option('--inventory-file', 'inventory_file', required=True,
              help='Path the the Ansible inventory file')
@click.option('--passwords-file', 'passwords_file', required=True,
              help='Path the the passwords.yml file')
@click.option('--globals-file', 'globals_file', required=True,
              help='Path to the globals.yml file')
@click.command(name='bootstrap')
def bootstrap(release, ssh_private_key_file, inventory_file, globals_file,
              passwords_file):
    """ Bootstrap the OpenStack nodes """
    openstack.kolla_ansible_bootstrap(
        release=release,
        ssh_key_path=ssh_private_key_file,
        inventory_path=inventory_file,
        globals_path=globals_file,
        passwords_path=passwords_file)


@click.option('--release', help='OpenStack release name', required=True)
@click.option('--ssh-private-key-file', 'ssh_private_key_file', required=True,
              help='Path the the SSH private key file')
@click.option('--inventory-file', 'inventory_file', required=True,
              help='Path the the Ansible inventory file')
@click.option('--passwords-file', 'passwords_file', required=True,
              help='Path the the passwords.yml file')
@click.option('--globals-file', 'globals_file', required=True,
              help='Path to the globals.yml file')
@click.command(name='pull-images')
def pull_images(release, ssh_private_key_file, inventory_file, globals_file,
                passwords_file):
    """ Pull the Kolla OpenStack images to each node """
    openstack.kolla_ansible_pull_images(
        release=release,
        ssh_key_path=ssh_private_key_file,
        inventory_path=inventory_file,
        globals_path=globals_file,
        passwords_path=passwords_file)


@click.option('--release', help='OpenStack release name', required=True)
@click.option('--ssh-private-key-file', 'ssh_private_key_file', required=True,
              help='Path the the SSH private key file')
@click.option('--inventory-file', 'inventory_file', required=True,
              help='Path the the Ansible inventory file')
@click.option('--passwords-file', 'passwords_file', required=True,
              help='Path the the passwords.yml file')
@click.option('--globals-file', 'globals_file', required=True,
              help='Path to the globals.yml file')
@click.option('--certificates-dir', 'certificates_dir', required=True,
              help='Path to the config/ dir')
@click.option('--config-dir', 'config_dir', required=False, default=None,
              help='Path to the config/ dir')
@click.command(name='deploy')
def deploy(release, ssh_private_key_file, inventory_file, globals_file,
           passwords_file, certificates_dir, config_dir):
    """ Deploy OpenStack  """
    openstack.kolla_ansible_deploy(
        release=release,
        ssh_key_path=ssh_private_key_file,
        inventory_path=inventory_file,
        globals_path=globals_file,
        passwords_path=passwords_file,
        certificates_dir=certificates_dir,
        config_dir=config_dir)


@click.option('--release', help='OpenStack release name', required=True)
@click.option('--inventory-file', 'inventory_file', required=True,
              help='Path the the Ansible inventory file')
@click.option('--passwords-file', 'passwords_file', required=True,
              help='Path the the passwords.yml file')
@click.option('--globals-file', 'globals_file', required=True,
              help='Path to the globals.yml file')
@click.command(name='get-admin-openrc')
def get_admin_openrc(release, inventory_file, globals_file, passwords_file):
    """ Genereate the admin-openrc file"""
    openstack.kolla_ansible_get_admin_openrc(
        release=release,
        inventory_path=inventory_file,
        globals_path=globals_file,
        passwords_path=passwords_file)
