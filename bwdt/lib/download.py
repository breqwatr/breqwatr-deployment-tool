""" Commands for downloading from s3 """
import os
import sys

import click

from bwdt.lib.aws.s3 import S3
from bwdt.constants import (APT_TARGZ_KEY, BWDT_TARGZ_KEY, CLOUDYML_KEY,
                            S3_BUCKET)


def _save(path, key, force):
    """ Download the specified file """
    if os.path.isdir(path):
        path = '{}/{}'.format(path, key)
    else:
        err = 'ERROR: path {} must be a directory and exist\n'.format(path)
        sys.stderr.write(err)
        sys.exit(1)
    if os.path.exists(path) and not force:
        err = 'ERROR: File {} exists. Use --force to overwrite\n'.format(path)
        sys.stderr.write(err)
        sys.exit(1)
    click.echo('Saving {}'.format(path))
    full_path = '{}/files/{}'.format(path, APT_TARGZ_KEY)
    S3().download(full_path, S3_BUCKET, APT_TARGZ_KEY)


def offline_apt(path, force):
    """ Download a subset of breqwatr/apt for offline installs """
    _save(path, APT_TARGZ_KEY, force)


def offline_bwdt(path, force):
    """ Download an offline export of this bwdt tool """
    _save(path, BWDT_TARGZ_KEY, force)


def cloud_yml(path, force):
    """ Download a commented cloud.yml template """
    _save(path, CLOUDYML_KEY, force)
