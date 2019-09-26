""" Commands for operating Docker on the host """
import os

import click

from bwdt.constants import KOLLA_IMAGE_TAGS, SERVICE_IMAGE_TAGS
from bwdt.container import Docker, get_image_as_filename


@click.group(name='docker')
def docker_group():
    """ Command group for local docker commands """


@click.argument('repository')
@click.option('--tag', default='latest',
              help='optional tag to pull, default=latest')
@click.command(name='pull')
def _pull(repository, tag):
    """ Pull an image from the upstream registry """
    click.echo('Pulling {}:{}'.format(repository, tag))
    Docker().pull(repository=repository, tag=tag)


def _all_images():
    """ Return dict of all images """
    images = {}
    images.update(SERVICE_IMAGE_TAGS)
    images.update(KOLLA_IMAGE_TAGS)
    return images


@click.option('--tag', default=None, required=False,
              help='optional tag to pull. Default=(current stable)')
@click.command(name='pull-all')
def pull_all(tag):
    """ Pull all images """
    images = _all_images()
    for repository in images:
        if tag is None:
            tag = images[repository]
            click.echo('Pulling {}:{}'.format(repository, tag))
            Docker().pull(repository=repository, tag=tag)


@click.option('--repository', required=True, help='Image name')
@click.option('--tag', required=True, help='Image tag')
@click.option('--output', '-o', required=True, help='Output dir  override')
@click.option('--pull/--no-pull', required=False, default=True,
              help='Use --no-pull to keep older image for this export')
@click.option('--force/--keep-old', required=False, default=False,
              help='--force will overwrite files found at the destination')
@click.command(name='export-image')
def export_image(repository, tag, output, pull, force):
    """ Export an image to directory """
    path = get_image_as_filename(repository, tag, output)
    if os.path.exists(path) and not force:
        click.echo('Skipping (already exists): {}'.format(path))
        return
    client = Docker()
    if pull:
        click.echo('Pulling {}:{}'.format(repository, tag))
        client.pull(repository=repository, tag=tag)
    click.echo('Saving {}:{} to {}'.format(repository, tag, output))
    client.export(repository, tag, output)


@click.option('--output', '-o', required=False, help='Output dir override')
@click.option('--pull/--no-pull', required=False, default=True,
              help='Use --no-pull to keep older image for this export')
@click.option('--tag', default=None, required=False,
              help='optional tag to pull. Default=(current stable)')
@click.option('--force/--keep-old', required=False, default=False,
              help='--force will overwrite files found at the destination')
@click.command(name='export-image-all')
def export_image_all(output, pull, tag, force):
    """ Export all images to directory  """
    # Check if the file exists
    # Export the file
    client = Docker()
    images = _all_images()
    for repository in images:
        image_tag = images[repository] if tag is None else tag
        path = get_image_as_filename(repository, image_tag, output)
        if os.path.exists(path) and not force:
            click.echo('Skipping (already exists): {}'.format(path))
            continue
        try:
            if pull:
                click.echo('Pulling {}:{}'.format(repository, image_tag))
                client.pull(repository=repository, tag=image_tag)
            click.echo('Saving: {}'.format(path))
            client.export(repository, image_tag, output)
        except Exception as e:
            click.echo('ERROR: Failed to pull or save {}'.format(repository))
            raise(e)


docker_group.add_command(_pull)
docker_group.add_command(pull_all)
docker_group.add_command(export_image)
docker_group.add_command(export_image_all)
