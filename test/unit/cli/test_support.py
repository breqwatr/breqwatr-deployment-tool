""" support commands """
import click
import pytest
from click.testing import CliRunner
from mock import MagicMock

import bwdt.cli.support


def test_support_group():
    """ return a click.core.Group object """
    group = bwdt.cli.support.get_support_group()
    assert isinstance(group, click.core.Group), 'click group is returned'


def test_status(monkeypatch):
    """ Run the status command """
    mm_status = MagicMock()
    monkeypatch.setattr(bwdt.lib.support, 'get_connection_status', mm_status)
    runner = CliRunner()
    result = runner.invoke(bwdt.cli.support.status)
    assert result.exit_code == 0
    assert mm_status.called

@pytest.mark.parametrize('status', ['is_online', 'not_online'])
def test_open_tunnel(monkeypatch, status):
    """ run  bwdt.cli.support.open_tunnel """
    is_online = status == 'is_online'
    mm_pub_key = MagicMock()
    mm_start = MagicMock()
    mm_status = MagicMock()
    mm_connect = MagicMock()
    mm_tunnel = MagicMock()
    def start(*args, **kwargs):
        mm_tunnel.return_value['status'] = 'ONLINE'
    mm_start = start
    mm_status.return_value = {'connected': is_online, 'uptime': '0:10:11'}
    mm_tunnel.return_value = {
        'status': 'ONLINE' if is_online else 'BUILDING',
        'error': ''}
    monkeypatch.setattr(bwdt.lib.support, 'gen_ssh_keys', mm_pub_key)
    monkeypatch.setattr(bwdt.lib.support, 'start_tunnel', mm_start)
    monkeypatch.setattr(bwdt.lib.support, 'get_connection_status', mm_status)
    monkeypatch.setattr(bwdt.lib.support, 'get_tunnel', mm_tunnel)
    monkeypatch.setattr(bwdt.lib.support, 'connect', mm_connect)
    runner = CliRunner()
    result = runner.invoke(bwdt.cli.support.open_tunnel)
    assert result.exit_code == 0
    assert mm_pub_key.called
    assert mm_connect.called != is_online, 'already online'


def test_close_tunnel():
    """ close the tunnel """
