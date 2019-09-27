""" Commands for downloading from s3 """
import os
import sys

import click

from bwdt.aws.s3 import S3
from bwdt.constants import OSTOOLS_KEY, S3_BUCKET


@click.group(name='download')
def download_group():
    """ Download files for offline install """


@click.argument('path')
@click.option('--force/--no-force', default=False,
              help='Use --force to overwrite file if it already exists')
@click.command()
def ostools(path, force):
    """ Download the offline OS Tools Tarball """
    if os.path.isdir(path):
        path = '{}/{}'.format(path, OSTOOLS_KEY)
    else:
        err = 'ERROR: path {} must be a directory and exist\n'.format(path)
        sys.stderr.write(err)
        sys.exit(1)
    if os.path.exists(path) and not force:
        err = 'ERROR: File {} exists. Use --force to overwrite\n'.format(path)
        sys.stderr.write(err)
        sys.exit(1)

    click.echo('Saving {}'.format(path))
    s3 = S3()
    s3.download(path, S3_BUCKET, OSTOOLS_KEY)


download_group.add_command(ostools)
