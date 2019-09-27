""" Commands for operating Docker on the host """
# pylint disable=broad-except,W0703
import sys

import click

import bwdt.auth
from bwdt.constants import KOLLA_IMAGE_TAGS, SERVICE_IMAGE_TAGS
from bwdt.container import Docker, offline_image_exists


def _all_images():
    """ Return dict of all images """
    images = {}
    images.update(SERVICE_IMAGE_TAGS)
    images.update(KOLLA_IMAGE_TAGS)
    return images


@click.group(name='docker')
def docker_group():
    """ Command group for local docker commands """


def _pull(repository, tag):
    """ Reusable pull command """
    if tag is None:
        tag = _all_images()[repository]
    click.echo('Pulling {}:{}'.format(repository, tag))
    Docker().pull(repository=repository, tag=tag)


@click.argument('repository')
@click.option('--tag', default=None,
              help='optional tag to pull, default=(current stable)')
@click.command(name='pull')
def pull_one(repository, tag):
    """ Pull an image from the upstream registry """
    _pull(repository, tag)


@click.option('--tag', default=None, required=False,
              help='optional tag to pull. Default=(current stable)')
@click.command(name='pull-all')
def pull_all(tag):
    """ Pull all images """
    for repository in _all_images():
        _pull(repository, tag)


def _export_image(repository, tag, pull, force):
    """ Re-usable command to export image to directory """
    if offline_image_exists(repository, tag) and not force:
        click.echo('Skipping (already exists): {}'.format(repository))
        return
    client = Docker()
    try:
        if pull:
            click.echo('Pulling {}:{}'.format(repository, tag))
            client.pull(repository=repository, tag=tag)
        offln_path = bwdt.auth.get()['offline_path']
        click.echo('Saving {}:{} to {}'.format(repository, tag, offln_path))
        client.export_image(repository, tag)
    except Exception:
        sys.stderr('ERROR: Failed to pull or save {}\n'.format(repository))
        sys.exit(1)


@click.option('--repository', required=True, help='Image name')
@click.option('--tag', required=True, help='Image tag')
@click.option('--pull/--no-pull', required=False, default=True,
              help='Use --no-pull to keep older image for this export')
@click.option('--force/--keep-old', required=False, default=False,
              help='--force will overwrite files found at the destination')
@click.command(name='export-image')
def export_image(repository, tag, pull, force):
    """ Export an image to directory """
    _export_image(repository, tag, pull, force)

@click.option('--pull/--no-pull', required=False, default=True,
              help='Use --no-pull to keep older image for this export')
@click.option('--tag', default=None, required=False,
              help='optional tag to pull. Default=(current stable)')
@click.option('--force/--keep-old', required=False, default=False,
              help='--force will overwrite files found at the destination')
@click.command(name='export-image-all')
def export_image_all(pull, tag, force):
    """ Export all images to directory  """
    for repository in all_images():
        _export_image(repository, tag, pull, force)


docker_group.add_command(pull_one)
docker_group.add_command(pull_all)
docker_group.add_command(export_image)
docker_group.add_command(export_image_all)
