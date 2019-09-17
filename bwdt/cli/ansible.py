""" Commands for operating the Ansible service """
import click

import bwdt.services as services


@click.group()
def ansible():
    """ Command group for bwdt Ansible service """


@click.option('--ssh-key-path', required=True, help='path to SSH private key')
@click.option('--globals-path', required=True, help='path to globals.yml file')
@click.command()
def start(ssh_key_path, globals_path):
    """Launch the local registry"""
    click.echo("Launching container: breqwatr-pxe")
    success = services.ansible_start(
        ssh_key_path=ssh_key_path,
        globals_path=globals_path)
    if success:
        click.echo('Done')
    else:
        click.echo('Failed to launch - Maybe its already running?')


ansible.add_command(start)
