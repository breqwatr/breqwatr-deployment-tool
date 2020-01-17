""" download commands """

import click
from click.testing import CliRunner
from mock import MagicMock

import bwdt.cli.download
import bwdt.lib.download


def test_get_download_group():
    """ return a click.core.Group object """
    group = bwdt.cli.download.get_download_group()
    assert isinstance(group, click.core.Group), 'click group is returned'


def test_offline_apt(monkeypatch):
    """ run  bwdt.lib.download.offline_apt """
    mm_cmd = MagicMock
    monkeypatch.setattr(bwdt.lib.download, 'offline_apt', mm_cmd)
    runner = CliRunner()
    result = runner.invoke(bwdt.cli.download.offline_apt, ['path'])
    assert result.exit_code == 0
    assert mm_cmd.called


def test_offline_bwdt(monkeypatch):
    """ run bwdt.lib.download.offline_bwdt """
    mm_cmd = MagicMock
    monkeypatch.setattr(bwdt.lib.download, 'offline_bwdt', mm_cmd)
    runner = CliRunner()
    result = runner.invoke(bwdt.cli.download.offline_bwdt, ['path'])
    assert result.exit_code == 0
    assert mm_cmd.called


def test_cloud_yml(monkeypatch):
    """ run bwdt.lib.download.cloud_yml """
    mm_cmd = MagicMock
    monkeypatch.setattr(bwdt.lib.download, 'cloud_yml', mm_cmd)
    runner = CliRunner()
    result = runner.invoke(bwdt.cli.download.cloud_yml, ['path'])
    assert result.exit_code == 0
    assert mm_cmd.called

