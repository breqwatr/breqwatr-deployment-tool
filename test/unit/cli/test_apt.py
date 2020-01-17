""" apt commands """

import click
from click.testing import CliRunner
from mock import MagicMock

import bwdt.cli.apt
import bwdt.services.apt


def test_get_apt_group():
    """ return a click.core.Group object """
    group = bwdt.cli.apt.get_apt_group()
    assert isinstance(group, click.core.Group), 'click group is returned'


def test_start(monkeypatch):
    """ run apt.start """
    mm_cmd = MagicMock()
    monkeypatch.setattr(bwdt.services.apt, 'start', mm_cmd)
    runner = CliRunner()
    result = runner.invoke(bwdt.cli.apt.start)
    assert result.exit_code == 0
    assert mm_cmd.called
