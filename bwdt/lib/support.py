""" support commands library """

import json
import os
import pathlib
import shlex
import signal
import socket
import subprocess
import time
from datetime import datetime

import bwdt.lib.aws.apigateway


HOME = os.getenv('HOME')
PATHS = {
    'dir': f'{HOME}/.breqwatr/',
    'rsa_public': f'{HOME}/.breqwatr/id_rsa.pub',
    'rsa_private': f'{HOME}/.breqwatr/id_rsa',
    'tunnel_json': f'{HOME}/.breqwatr/tunnel.json'}


def create_ssh_keys():
    """ Creates the SSH keys and their dir if not present """
    pathlib.Path(PATHS['dir']).mkdir(parents=True, exist_ok=True)
    if not os.path.exists(PATHS['rsa_private']):
        os.system('ssh-keygen -f "{}" -q -N ""'.format(PATHS['rsa_private']))


def gen_ssh_keys():
    """ Cretea SSH public and private keys for this session """
    create_ssh_keys()
    with open(PATHS['rsa_public']) as public_file:
        public_key = public_file.read()
    with open(PATHS['rsa_private']) as private_file:
        private_key = private_file.read()
    return {'public': public_key, 'private': private_key}


def start_tunnel(public_key):
    """ Launch the tunnel for this user """
    # TODO: Implement this
    pass



def get_tunnel():
    """ Check the tunnel status """
    #TODO: Implement this
    return {
        'status': 'ONLINE',
        'in_port': 5022,
        'out_port': 5122,
        'service_port': 22,
        'username': 'root',
        'fqdn': 'bastion.devcloud.ca',
        'error': ''}


def write_tunnel_file(pid, port, fqdn):
    """ Writes a pid file for the conncetion """
    pathlib.Path(PATHS['dir']).mkdir(parents=True, exist_ok=True)
    timestamp = int(time.time())
    data = {'pid': pid, 'port': port, 'fqdn': fqdn, 'timestamp': timestamp}
    with open (PATHS['tunnel_json'], 'w') as tunnel_file:
        tunnel_file.write(json.dumps(data))


def read_tunnel_file():
    """ Return dict of tunnel data, or None """
    if not os.path.exists(PATHS['tunnel_json']):
        return None
    with open(PATHS['tunnel_json']) as tunnel_file:
        tunnel_data = json.loads(tunnel_file.read())
    return tunnel_data


def process_exists(pid):
    """ return bool, check if a pid exists """
    return os.path.exists(f'/proc/{pid}')


def is_tcp_port_open(host, port):
    """ return bool, is a port open """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0


def get_uptime_string(timestamp):
    """ Returns a string denoting uptime given a starting timestamp """
    now = datetime.fromtimestamp(time.time())
    dt_created = datetime.fromtimestamp(timestamp)
    diff = now - dt_created
    return str(diff)


def get_connection_status():
    """ Check the status of the tunnel connection """
    status = {'connected': False, 'uptime': '0:00:00' }
    tunnel_data = read_tunnel_file()
    if (tunnel_data is None
            or not process_exists(tunnel_data['pid'])
            or not is_tcp_port_open(tunnel_data['fqdn'], tunnel_data['port'])):
        return status
    if not process_exists(tunnel_data['pid']):
        return status
    status['uptime'] = get_uptime_string(tunnel_data['timestamp'])
    status['connected'] = True
    return status


def connect(tunnel):
    """ Open a support tunnel """
    ssh = '/usr/bin/ssh'
    rule = f'0.0.0.0:{tunnel["out_port"]}:127.0.0.1:{tunnel["service_port"]}'
    target = f'{tunnel["username"]}@{tunnel["fqdn"]}'
    no_key_check = 'StrictHostKeyChecking=no'
    no_hosts_file = 'UserKnownHostsFile=/dev/null'
    cmd = (f'{ssh} -o {no_key_check} -o {no_hosts_file} -p {tunnel["in_port"]}'
          f' -i {PATHS["rsa_private"]} -N -R {rule} {target}')
    args = shlex.split(cmd)
    process = subprocess.Popen(args, stderr=subprocess.DEVNULL)
    write_tunnel_file(process.pid, tunnel['out_port'], tunnel['fqdn'])


def stop_tunnel_instance(tunnel):
    """ Stop the jump service instance """
    # TODO
    pass


def disconnect(pid):
    """ Disconnect from the tunnel """
    os.kill(pid, signal.SIGTERM)


def close_tunnel():
    """ Close the tunnel and clean up the jump service instance """
    connection_status = get_connection_status()
    if connection_status['connected']:
        tunnel_data = read_tunnel_file()
        disconnect(tunnel_data['pid'])
    tunnel = get_tunnel()
    if tunnel['status'] == 'ONLINE':
        stop_tunnel_instance(tunnel)
