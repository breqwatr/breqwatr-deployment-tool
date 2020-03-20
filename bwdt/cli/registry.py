"""Commands for operating the local registry"""
import sys

import click
import requests

import bwdt.services.registry as registry


def get_registry_group():
    """ return the registry group function """
    @click.group(name='registry')
    def registry_group():
        """ Local Docker image registry """
    registry_group.add_command(start)
    registry_group.add_command(sync_image)
    registry_group.add_command(sync_all_images)
    registry_group.add_command(list_images)
    return registry_group


@click.option('--ip', default='0.0.0.0', help='optional bind IP address')
@click.option('--port', default='5000', help='optional bind port')
@click.command()
def start(ip, port):
    """Launch the local registry"""
    click.echo("Launching container: registry")
    registry.start(ip, port)


@click.argument('image_name')
@click.argument('registry_url')
@click.option('--tag', default=None, help='optional image tag')
@click.command(name='sync-image')
def sync_image(image_name, registry_url, tag):
    """ Load image_name and push it to the local registry """
    click.echo('Sync {} to {}...'.format(image_name, registry_url))
    registry.sync_image(image=image_name, registry_url=registry_url, tag=tag)


@click.argument('registry_url')
@click.option('--tag', default=None, help='optional image tag')
@click.command(name='sync-openstack-images')
def sync_all_images(registry_url, tag):
    """ Load all OpenStack images and push them to the local registry """
    click.echo('Pushing all OpenStack images to {}'.format(registry_url))
    registry.sync_all_images(registry_url=registry_url, tag=tag)


@click.argument('registry_url')
@click.command(name='list-images')
def list_images(registry_url):
    """ List the images in a registry """
    if 'http' not in registry_url:
        registry_url = 'http://{}'.format(registry_url)
    catalog_url = '{}/v2/_catalog'.format(registry_url)
    try:
        response = requests.get(url=catalog_url)
    except requests.exceptions.ConnectionError:
        err = f'ERROR: Failed to connect to {registry_url}\n'
        err += '       Is the port correct? Usually it\'s :5000\n'
        sys.stderr.write(err)
        sys.exit(1)
    repositories = response.json()['repositories']
    for repo in repositories:
        click.echo('{}'.format(repo))
        tags_url = '{}/v2/{}/tags/list'.format(registry_url, repo)
        tag_resp = requests.get(url=tags_url)
        tags = tag_resp.json()['tags']
        for tag in tags:
            click.echo('  - {}'.format(tag))
