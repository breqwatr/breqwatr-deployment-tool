""" Controls for the registry service """
from click import echo

import bwdt.lib.docker as docker
from bwdt.constants import IMAGE_PREFIX, KOLLA_IMAGE_TAGS, SERVICE_IMAGE_TAGS


def start(ip='0.0.0.0', port=5000):
    """ Start the registry container """
    repo = 'registry'
    tag = SERVICE_IMAGE_TAGS[repo]
    http_addr = "{}:{}".format(ip, port)
    docker_kwargs = {
        'name': 'registry',
        'environment': {'REGISTRY_HTTP_ADDR': http_addr},
        'ports': {port: port},
        'daemon': True
    }
    docker.get_image(repo, tag)
    docker.run(repo, tag, **docker_kwargs)


def sync_image(registry_url, image, tag=None):
    """ Pull images from upstream or import from media, push to registry """
    if tag is None:
        tag = KOLLA_IMAGE_TAGS[image]
    docker.get_image(image, tag)
    old_image = f'{IMAGE_PREFIX}/{image}:{tag}'
    new_image = f'{registry_url}/{IMAGE_PREFIX}/{image}:{tag}'
    echo('> Applying new tag')
    docker.apply_tag(old_image, new_image)
    echo(f'> Pushing {new_image}')
    docker.push(new_image)


def sync_all_images(registry_url, tag=None):
    """ Sync all images to registry_url """
    i = 0
    length = len(KOLLA_IMAGE_TAGS)
    for image in KOLLA_IMAGE_TAGS:
        echo('Progress: {} / {}'.format(i, length))
        sync_image(registry_url, image, tag)
        i += 1
