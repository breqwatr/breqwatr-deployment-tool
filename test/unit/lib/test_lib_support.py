""" download commands """
import click
import pytest
from click.testing import CliRunner
from mock import MagicMock

import bwdt.lib.support


def test_start_tunnel():
    """ Run start_tunnel """
    bwdt.lib.support.start_tunnel('FAKE KEY')


def test_get_tunnel():
    """ Return tunnel details in a dict """
    tunnel = bwdt.lib.support.get_tunnel()
    assert isinstance(tunnel, dict)


@pytest.mark.parametrize('state', ['connected', 'not_connected', 'no_file'])
def test_get_connection_status(monkeypatch, state):
    """ get the connection status """
    mm_tun = MagicMock(name='read_tunnel_file')
    if state == 'connected' or state == 'not_connected':
        mm_tun.return_value = {'pid': 12345}
    elif state == 'no_file':
        mm_tun.return_value = None
    monkeypatch.setattr(bwdt.lib.support, 'read_tunnel_file', mm_tun)
    status = bwdt.lib.support.get_connection_status()
    assert isinstance(status, dict)
    assert 'connected' in status


def test_open_tunnel(monkeypatch):
    """ Run connect """
    mm_proc = MagicMock(name='subprocess')
    monkeypatch.setattr(bwdt.lib.support, 'subprocess', mm_proc)
    tunnel = {
        'status': 'ONLINE',
        'in_port': 5022,
        'out_port': 5122,
        'service_port': 22,
        'username': 'root',
        'fqdn': 'bastion.devcloud.ca',
        'error': ''}
    mm_tfile = MagicMock(name='tunnel_file')
    monkeypatch.setattr(bwdt.lib.support, 'write_tunnel_file', mm_tfile)
    bwdt.lib.support.connect(tunnel)
    assert mm_proc.Popen.called
    assert mm_tfile.called

