""" Commands to configure BWDT """
import os
import subprocess
import sys

import click

import bwdt.lib.download as download
from bwdt.lib.container import Docker


@click.group(name='util')
def util_group():
    """ Deployment utility commands """


@click.argument('path')
@click.option('--force/--no-force', default=False,
              help='Use --force to overwrite files if they already exists')
@click.option('--tag', required=False, default=None,
              help='Optional tag override to build media for older versions')
@click.command(name='export-offline-media')
def export_offline_media(path, force, tag):
    """ Create an offline installer USB/Disk at specified path """
    click.echo('Exporting offline install files to {}'.format(path))
    download.cloud_yml(path, force)
    download.offline_bwdt(path, force)
    download.offline_apt(path, force)
    client = Docker()
    client.pull_all(tag=tag)
    client.export_image_all(tag=tag, force=force)


@click.argument('disk')
@click.option('--force/--ask', required=False, default=False,
              help='Skip the prompt asking you to type the drive name')
@click.command(name='zap-disk')
def zap_disk(disk, force):
    """ Completely delete everything from a disk to prepare it for ceph """
    if not os.path.exists(disk):
        sys.stderr.write('ERROR: {} not found\n'.format(disk))
        sys.exit(1)
    click.echo('WARNING: This will wip {}'.format(disk))
    if not force:
        click.echo('Type the drive name again to continue:')
        user_in = raw_input()
        if user_in != disk:
            sys.stderr.write('ERROR: Confirm does not match {}\n'.format(disk))
            sys.exit(1)
    subprocess.call(['wipefs', '-a', disk])
    dd_cmd = 'dd if=/dev/zero of={} bs=4096k count=100'.format(disk).split(' ')
    subprocess.call(dd_cmd)
    click.echo('Done')


util_group.add_command(export_offline_media)
util_group.add_command(zap_disk)
