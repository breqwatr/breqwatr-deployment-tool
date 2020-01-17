""" Ansible commands """

import click
from click.testing import CliRunner
from mock import MagicMock

import bwdt.cli.ansible


def test_get_ansible_group():
    """ return a click.core.Group object """
    group = bwdt.cli.ansible.get_ansible_group()
    assert isinstance(group, click.core.Group), 'click group is returned'


def test_start(monkeypatch):
    """ run ansible.start """
    mm_cmd = MagicMock()
    monkeypatch.setattr(bwdt.services.ansible, 'start', mm_cmd)
    runner = CliRunner()
    opts = ['--ssh-key-path', 'x', '--cloud-yml-path', 'x']
    result = runner.invoke(bwdt.cli.ansible.start, opts)
    assert result.exit_code == 0
    assert mm_cmd.called


def test_transfer_kolla_dir(monkeypatch):
    """ run ansible.transfer_kolla_dir """
    mm_cmd = MagicMock()
    monkeypatch.setattr(bwdt.services.ansible, 'transfer_kolla_dir', mm_cmd)
    runner = CliRunner()
    opts = ['--server-ip', 'x']
    result = runner.invoke(bwdt.cli.ansible.transfer_kolla_dir, opts)
    assert result.exit_code == 0
    assert mm_cmd.called
