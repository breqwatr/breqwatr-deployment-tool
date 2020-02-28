""" Commands to configure BWDT """
import sys
from pprint import pprint

import click

import bwdt.lib.config as config


# pylint: disable=inconsistent-return-statements
def query(question, allowed_vals, default):
    """ User input collection query """
    for i in range(1, 4):
        vals_str = '/'.join(allowed_vals)
        q_str = question
        if len(allowed_vals) > 0:
            q_str = f'{question} [{vals_str}] ({default})'
        click.echo(q_str)
        user_input = input().lower()
        if user_input == '':
            user_input = default
        if user_input in allowed_vals or len(allowed_vals) == 0:
            return user_input
        sys.stderr.write(f'Invalid input, try again ({i}/3)\n')
    sys.stderr.write('ERROR: Invalid input entered too many times\n')
    sys.exit(1)
    return


def config_wizard():
    """ Run the configuraiton CLI wizard """
    if config.is_config_found():
        sys.stdout.write('Re-launching configuration wizard\n\n')
        click.echo('')
    else:
        sys.stdout.write('Running first-time configuration wizard\n\n')
    data = config.get_config()
    data['offline'] = query(
        question='Run BWDT in offline mode:',
        allowed_vals=['true', 'false'],
        default=data['offline'])
    data['offline_path'] = query(
        question='(optional) Offline media path:',
        allowed_vals=[],
        default=data['offline_path'])
    data['license'] = query(
        question='(optional) License key:',
        allowed_vals=[],
        default=data['license'])
    config.set_config(data)
    sys.stdout.write('Configuration finished\n\n\n')


def get_configure_group():
    """ return the configure group function """
    @click.group(name='configure')
    def configure_group():
        """ Interact with the BWDT Configuration """
    configure_group.add_command(setup)
    configure_group.add_command(show)
    return configure_group


@click.command()
def setup():
    """ Re-Launch the setup wizard """
    config_wizard()


@click.command()
def show():
    """ Print the current config """
    pprint(config.get_config())
