""" Controls for the registry service """
from click import echo

import bwdt.lib.docker as docker
from bwdt.constants import IMAGE_PREFIX, KOLLA_IMAGE_REPOS, SERVICE_IMAGE_TAGS


def start(ip='0.0.0.0', port=5000):
    """ Start the registry container """
    repo = 'registry'
    tag = SERVICE_IMAGE_TAGS[repo]
    http_addr = "{}:{}".format(ip, port)
    docker_kwargs = {
        'name': 'registry',
        'restart_policy': {'Name': 'always'},
        'environment': {'REGISTRY_HTTP_ADDR': http_addr},
        'ports': {port: port},
        'daemon': True
    }
    docker.get_image(repo, tag)
    docker.run(repo, tag, **docker_kwargs)


def sync_image(registry_url, repository, tag):
    """ Pull images from upstream or import from media, push to registry """
    docker.get_image(repository, tag)
    old_image = f'{IMAGE_PREFIX}/{repository}:{tag}'
    new_image = f'{registry_url}/{IMAGE_PREFIX}/{repository}:{tag}'
    echo('> Applying new tag')
    docker.apply_tag(old_image, new_image)
    echo(f'> Pushing {new_image}')
    docker.push(new_image)


def sync_openstack_images(registry_url, release):
    """ Sync all images to registry_url """
    i = 0
    repo_list = KOLLA_IMAGE_REPOS[release]
    length = len(repo_list)
    for repository in repo_list:
        echo('Progress: {} / {}'.format(i, length))
        sync_image(registry_url, repository, tag=release)
        i += 1
