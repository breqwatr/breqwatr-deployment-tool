"""Commands for operating the local registry"""
import sys

import click

import bwdt.lib as lib


@click.group()
@click.pass_context
def registry(ctx):
    """Command group for bwdt registry"""
    try:
        ctx.auth = lib.get_auth()
    except IOError:
        auth_file = lib.env_vars()['auth_file']
        err_msg = "ERROR: Failed to open file {}".format(auth_file)
        click.echo(err_msg, err=True)
        sys.exit(1)
    except ValueError:
        auth_file = lib.env_vars()['auth_file']
        err_msg = "ERROR: Failed to parse {}".format(auth_file)
        click.echo(err_msg, err=True)
        sys.exit(1)


@click.command()
@click.pass_context
def start(ctx):
    """Launch the local registry"""
    click.echo("Launching the local registry")


registry.add_command(start)
