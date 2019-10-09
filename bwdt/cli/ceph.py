""" Commands for setting up ceph """

import click


@click.group(name='ceph')
def ceph_group():
    """ Command group for ceph """


@click.command(name='gen-config')
def gen_config():
    """ Generates ceph configs in ansible container """
    click.echo("Generating ceph config files")


ceph_group.add_command(gen_config)
