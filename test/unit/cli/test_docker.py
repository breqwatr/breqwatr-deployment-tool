""" docker commands """

import click
import pytest
from click.testing import CliRunner
from mock import MagicMock

import bwdt.cli.docker
import bwdt.lib.container


def test_get_docker_group():
    """ return a click.core.Group object """
    group = bwdt.cli.docker.get_docker_group()
    assert isinstance(group, click.core.Group), 'click group is returned'


def test_pull_one(monkeypatch):
    """ call bwdt.lib.container.Docker().pull """
    mm_docker = MagicMock(name='Docker')
    monkeypatch.setattr(bwdt.lib.container, 'Docker', mm_docker)
    runner = CliRunner()
    result = runner.invoke(bwdt.cli.docker.pull_one, ['repo'])
    assert result.exit_code == 0
    assert mm_docker.return_value.pull.called


def test_pull_all(monkeypatch):
    """ call bwdt.lib.container.Docker().pull_all """
    mm_docker = MagicMock(name='Docker')
    monkeypatch.setattr(bwdt.lib.container, 'Docker', mm_docker)
    runner = CliRunner()
    result = runner.invoke(bwdt.cli.docker.pull_all)
    assert result.exit_code == 0
    assert mm_docker.return_value.pull_all.called


@pytest.mark.parametrize('parm_pull', ['pull_true', 'pull_false'])
def test_export_image(monkeypatch, parm_pull):
    """
        - call bwdt.lib.container.Docker.pull() to download the image
          only when --pull is used
        - call bwdt.lib.container.Docker.export_image() to save as file
    """
    mm_docker = MagicMock(name='Docker')
    monkeypatch.setattr(bwdt.lib.container, 'Docker', mm_docker)
    runner = CliRunner()
    pull = parm_pull == 'pull_true'
    opts = ['repo', '--pull'] if pull else ['repo', '--no-pull']
    result = runner.invoke(bwdt.cli.docker.export_image, opts)
    from pprint import pprint
    pprint(vars(result))
    assert result.exit_code == 0
    assert mm_docker.return_value.pull.called == pull
    assert mm_docker.return_value.export_image.called


@pytest.mark.parametrize('parm_pull', ['pull_true', 'pull_false'])
def test_export_image_all(monkeypatch, parm_pull):
    """
        - call bwdt.lib.container.Docker.pull_all() to download the image only
          when --pull is used
        - call bwdt.lib.container.Docker.export_image_all() to save as file
    """
    mm_docker = MagicMock(name='Docker')
    monkeypatch.setattr(bwdt.lib.container, 'Docker', mm_docker)
    runner = CliRunner()
    pull = parm_pull == 'pull_true'
    opts = ['--pull'] if pull else ['--no-pull']
    result = runner.invoke(bwdt.cli.docker.export_image_all, opts)
    assert result.exit_code == 0
    assert mm_docker.return_value.pull_all.called == pull
    assert mm_docker.return_value.export_image_all.called
