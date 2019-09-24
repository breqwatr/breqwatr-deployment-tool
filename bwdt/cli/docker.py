""" Commands for operating Docker on the host """
import click

from bwdt.constants import KOLLA_IMAGE_TAGS, SERVICE_IMAGE_TAGS
from bwdt.container import Docker


@click.group(name='docker')
def docker_group():
    """ Command group for local docker commands """


@click.argument('repository')
@click.option('--tag', required=False, help='optional, which tag to pull')
@click.command(name='pull')
def _pull(repository, tag):
    """ Pull an image from the upstream registry """
    click.echo('Pulling {}:{} from upstream registry'.format(repository, tag))
    _docker = Docker()
    _docker.pull(repository=repository, tag=tag)
    click.echo('Done')


def _all_images():
    """ Return dict of all images """
    images = {}
    images.update(SERVICE_IMAGE_TAGS)
    images.update(KOLLA_IMAGE_TAGS)
    return images


@click.command(name='pull-all')
def pull_all():
    """ Pull all images """
    images = _all_images()
    for repository in images:
        tag = images[repository]
        _pull(repository, tag)


@click.option('--repository', required=True, help='Image name')
@click.option('--tag', required=True, help='Image tag')
@click.option('--output', '-o', required=True, help='Output (directory)')
@click.option('--pull/--no-pull', required=False, default=True,
              help='Use --no-pull to keep older image for this export')
@click.command(name='export-image')
def export_image(repository, tag, output, pull):
    """ Export an image to directory """
    if pull:
        _pull(repository, tag)
    docker = Docker()
    click.echo('Saving {}:{} to {}'.format(repository, tag, output))
    docker.export(repository, tag, output)


@click.option('--output', '-o', required=True, help='Output directory')
@click.option('--pull/--no-pull', required=False, default=True,
              help='Use --no-pull to keep older image for this export')
@click.command(name='export-image-all')
def export_image_all(output, pull):
    """ Export all images to directory  """
    images = _all_images()
    for repository in images:
        tag = images[repository]
        export_image(repository, tag, output, pull)


docker_group.add_command(_pull)
docker_group.add_command(pull_all)
docker_group.add_command(export_image)
docker_group.add_command(export_image_all)
