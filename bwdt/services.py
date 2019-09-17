""" Controls for the Breqwatr services """

from bwdt.container import Docker
from bwdt.lib import get_latest_tag


def registry_start(ip='0.0.0.0', port=5000):
    """ Start the registry container """
    repo = 'registry'
    tag = get_latest_tag(repo)
    http_addr = "{}:{}".format(ip, port)
    image = '{}:{}'.format(repo, tag)
    docker_kwargs = {
        'environment': {'REGISTRY_HTTP_ADDR': http_addr},
        'ports': {'5000': '5000'}
    }
    docker = Docker()
    docker.pull(repository=repo, tag=tag)
    success = docker.run(image, name='registry', **docker_kwargs)
    return success


def pxe_start(interface, dhcp_start, dhcp_end, dns_ip='8.8.8.8'):
    """ Start the breqwatr-pxe container """
    name = 'breqwatr_pxe'
    repo = "breqwatr/pxe"
    tag = get_latest_tag(repo)
    image = '{}:{}'.format(repo, tag)
    docker_kwargs = {
        'privileged': True,
        'network_mode': 'host',
        'environment': {
            'INTERFACE': interface,
            'DHCP_RANGE_START': dhcp_start,
            'DHCP_RANGE_END': dhcp_end,
            'DNS_IP': dns_ip
        },
        'sysctls': {'net.ipv4.ip_forward': 1}
    }
    docker = Docker()
    docker.pull(repository=repo, tag=tag)
    success = docker.run(image, name=name, **docker_kwargs)
    return success


def ansible_start(ssh_key_path, globals_path):
    """ Start the Ansible container """
    name = 'breqwatr_ansible'
    repo = 'breqwatr/ansible'
    tag = get_latest_tag(repo)
    image = '{}:{}'.format(repo, tag)
    docker_kwargs = {
        'volumes':  {
            ssh_key_path: {'bind': '/root/.ssh/id_rsa', 'mode': 'ro'},
            globals_path: {'bind': '/etc/breqwatr/globals.yml', 'mode': 'rw'}}}
    docker = Docker()
    docker.pull(repository=repo, tag=tag)
    success = docker.run(image, name=name, **docker_kwargs)
    return success


def apt_start(tag=None, passkey=None):
    """ Start the APT container """
    name = 'breqwatr_apt'
    repo = 'breqwatr/apt'
    tag = get_latest_tag(repo)
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


def pip_start(tag=None):
    """ Start the PIP container """
    repo = 'breqwatr/pip'
    if tag is None:
        tag = get_latest_tag(repo)
    docker = Docker()
    docker.pull(repository=repo, tag=tag)
    image = '{}:{}'.format(repo, tag)
    docker = Docker()
    docker.pull(repository=repo, tag=tag)
    docker.run(image, name='bw-pip', network_mode='host')




def dns_start(interface_name, cloud_vip, cloud_fqdn, tag=None):
    """ Start the DNS container """
    repo = 'breqwatr/dns'
    if tag is None:
        tag = get_latest_tag(repo)
    docker = Docker()
    docker.pull(repository=repo, tag=tag)
    image = '{}:{}'.format(repo, tag)
    env = {
        'INTERFACE': interface_name,
        'CLOUD_VIP': cloud_vip,
        'CLOUD_FQDN': cloud_fqdn,
    }
    docker.run(image, name='bw-dns', network_mode='host', environment=env)


def ntp_start(tag=None):
    """ Start the NTP service """
    repo = 'breqwatr/ntp'
    if tag is None:
        tag = get_latest_tag(repo)
    docker = Docker()
    docker.pull(repository=repo, tag=tag)
    image = '{}:{}'.format(repo, tag)
    docker.run(image, name='bw-ntp', network_mode='host', privileged=True)
