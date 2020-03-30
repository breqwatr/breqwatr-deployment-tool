""" Commands for operating the Ansible service """
import os
import sys

import click

import bwdt.lib.openstack as openstack


def get_openstack_group():
    """ Return the OpenStack click group """
    @click.group(name='openstack')
    def openstack_group():
        """ Deploy and manage OpenStack """
    openstack_group.add_command(get_passwords)
    openstack_group.add_command(get_inventory_template)
    openstack_group.add_command(get_certificates)
    openstack_group.add_command(get_admin_openrc)
    openstack_group.add_command(kolla_ansible)
    openstack_group.add_command(cli)
    return openstack_group


@click.option('--release', help='OpenStack release name', required=True)
@click.command(name='pull-kolla-ansible')
def pull_kolla_ansible(release):
    """ Download the Kolla-Ansible Docker image """
    click.echo('Downloading the Kolla-Ansible image')
    openstack.kolla_ansible_pull(release)


@click.option('--release', help='OpenStack release name', required=True)
@click.command(name='get-passwords')
def get_passwords(release):
    """ Generate passwords, save to ./passwords.yml """
    click.echo('Creating password file: ./passwords.yml')
    openstack.kolla_ansible_genpwd(release)


@click.option('--release', help='OpenStack release name', required=True)
@click.command(name='get-inventory-template')
def get_inventory_template(release):
    """ Generate inventory template, save to ./inventory """
    click.echo('Creating inventory template: ./inventory')
    openstack.kolla_ansible_inventory(release)


@click.option('--release', help='OpenStack release name', required=True)
@click.option('--passwords-file', 'passwords_file', required=True,
              help='Path the the passwords.yml file')
@click.option('--globals-file', 'globals_file', required=True,
              help='Path to the globals.yml file')
@click.command(name='get-certificates')
def get_certificates(release, passwords_file, globals_file):
    """ Generate certificates, save to ./certificates/ """
    click.echo(f'Generating ./certificates/')
    openstack.kolla_ansible_generate_certificates(
        release=release,
        passwords_path=passwords_file,
        globals_path=globals_file)


@click.option('--release', help='OpenStack release name', required=True)
@click.option('--inventory-file', 'inventory_file', required=True,
              help='Path the the Ansible inventory file')
@click.option('--passwords-file', 'passwords_file', required=True,
              help='Path the the passwords.yml file')
@click.option('--globals-file', 'globals_file', required=True,
              help='Path to the globals.yml file')
@click.command(name='get-admin-openrc')
def get_admin_openrc(release, inventory_file, globals_file, passwords_file):
    """ Generate & save ./admin-openrc.sh"""
    openstack.kolla_ansible_get_admin_openrc(
        release=release,
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
              help='Path to globals.yml file')
@click.option('--certificates-dir', 'certificates_dir', required=True,
              help='Path to certificates/ directory')
@click.option('--config-dir', 'config_dir', required=False, default=None,
              help='Path to config/ directory  [optional]')
@click.argument('command')
@click.command(name='kolla-ansible')
def kolla_ansible(release, ssh_private_key_file, inventory_file, globals_file,
                  passwords_file, certificates_dir, config_dir, command):
    """ Execute Kolla-Ansible command  """
    openstack.kolla_ansible_exec(
        release=release,
        ssh_key_path=ssh_private_key_file,
        inventory_path=inventory_file,
        globals_path=globals_file,
        passwords_path=passwords_file,
        certificates_dir=certificates_dir,
        config_dir=config_dir,
        command=command)


@click.option('--release', required=False, default=None,
              help='OpenStack release name (OS_RELEASE)')
@click.option('--openrc-path', 'openrc_path', required=False, default=None,
              help='Openrc file path (OS_OPENRC_PATH)')
@click.option('--command', '-c', required=False, default=None,
              help='Execute this command (non-interactive mode)')
@click.option('--volume', '-v', required=False, default=None,
              help='Mount a file to the client container [optional]')
@click.command(name='cli')
def cli(release, openrc_path, command, volume):
    """ Launch then OpenStack client CLI """
    if release is None:
        if 'OS_RELEASE' not in os.environ:
            err = ('ERROR: either --release option must be used or the '
                   'OS_RELEASE environment variable must be set\n')
            sys.stderr.write(err)
            sys.exit(1)
        release = os.environ['OS_RELEASE']
    if openrc_path is None:
        if 'OS_OPENRC_PATH' not in os.environ:
            err = ('ERROR: either --openrc-path option must be used or the '
                   'OS_OPENRC_PATH environment variable must be set\n')
            sys.stderr.write(err)
            sys.exit(1)
        openrc_path = os.environ['OS_OPENRC_PATH']
    openstack.cli_exec(
        release=release,
        openrc_path=openrc_path,
        command=command,
        volume=volume)
