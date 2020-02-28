""" configure commands """

import click
from click.testing import CliRunner
from mock import MagicMock

import bwdt.cli.configure
import bwdt.lib.config
import bwdt.lib.configure


def test_get_configure_group():
    """ return a click.core.Group object """
    group = bwdt.cli.configure.get_configure_group()
    assert isinstance(group, click.core.Group), 'click group is returned'


def test_setup(monkeypatch):
    """ call bwdt.lib.configure.configure() """
    mm_cmd = MagicMock()
    monkeypatch.setattr(bwdt.lib.configure, 'configure', mm_cmd)
    runner = CliRunner()
    result = runner.invoke(bwdt.cli.configure.setup)
    assert result.exit_code == 0
    assert mm_cmd.called


def test_show(monkeypatch):
    """ call bwdt.lib.config.get_config() """
    mm_cmd = MagicMock()
    monkeypatch.setattr(bwdt.lib.config, 'get_config', mm_cmd)
    runner = CliRunner()
    result = runner.invoke(bwdt.cli.configure.show)
    assert result.exit_code == 0
    assert mm_cmd.called
