""" Controls for the apt service """
from bwdt.constants import SERVICE_IMAGE_TAGS
from bwdt.container import Docker


def start(tag=None, passkey=None):
    """ Start the APT container """
    name = 'apt'
    repo = 'breqwatr/apt'
    tag = SERVICE_IMAGE_TAGS[repo]
    image = '{}:{}'.format(repo, tag)
    restart_policy = {'Name': 'always'}
    if passkey is None:
        passkey = 'FfMm5s3a'
    env = {
        'GPG_PASSKEY': passkey,
        'GPG_PRIVATE_KEY_FILE': '/keys/breqwatr-private-key.asc',
        'GPG_PUBLIC_KEY_FILE': '/keys/breqwatr-private-key.asc',
    }
    ports = {'80': ('0.0.0.0', '81')}
    docker = Docker()
    docker.pull(repository=repo, tag=tag)
    docker.run(image, name=name, environment=env,
               restart_policy=restart_policy, ports=ports)
