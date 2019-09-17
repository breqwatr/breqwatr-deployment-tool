""" Commands for operating Docker on the host """
import click

from bwdt.container import Docker


@click.group()
def docker():
    """ Command group for local docker commands """


@click.argument('repository')
@click.option('--tag', default='latest',
              help='optional tag to pull, default=latest')
@click.command()
def pull(repository, tag):
    """ Pull an image from the upstream registry """
    click.echo('Pulling {}:{} from upstream registry'.format(repository, tag))
    _docker = Docker()
    _docker.pull(repository=repository, tag=tag)
    click.echo('Done')


docker.add_command(pull)
