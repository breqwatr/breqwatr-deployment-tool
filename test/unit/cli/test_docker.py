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
    mm_cmd = MagicMock()
    monkeypatch.setattr(bwdt.lib.container.Docker, 'pull', mm_cmd)
    runner = CliRunner()
    result = runner.invoke(bwdt.cli.docker.pull_one, ['repo'])
    assert result.exit_code == 0
    assert mm_cmd.called


def test_pull_all(monkeypatch):
    """ call bwdt.lib.container.Docker().pull_all """
    mm_cmd = MagicMock()
    monkeypatch.setattr(bwdt.lib.container.Docker, 'pull_all', mm_cmd)
    runner = CliRunner()
    result = runner.invoke(bwdt.cli.docker.pull_all)
    assert result.exit_code == 0
    assert mm_cmd.called


@pytest.mark.parametrize('parm_pull', ['pull_true', 'pull_false'])
def test_export_image(monkeypatch, parm_pull):
    """
        - call bwdt.lib.container.Docker.pull() to download the image
          only when --pull is used
        - call bwdt.lib.container.Docker.export_image() to save as file
    """
    mm_pull = MagicMock()
    monkeypatch.setattr(bwdt.lib.container.Docker, 'pull', mm_pull)
    mm_export_image = MagicMock()
    monkeypatch.setattr(bwdt.lib.container.Docker, 'export_image',
                        mm_export_image)
    runner = CliRunner()
    pull = parm_pull == 'pull_true'
    opts = ['repo', '--pull'] if pull else ['repo', '--no-pull']
    result = runner.invoke(bwdt.cli.docker.export_image, opts)
    assert result.exit_code == 0
    assert mm_pull.called == pull
    assert mm_export_image.called


@pytest.mark.parametrize('parm_pull', ['pull_true', 'pull_false'])
def test_export_image_all(monkeypatch, parm_pull):
    """
        - call bwdt.lib.container.Docker.pull_all() to download the image only
          when --pull is used
        - call bwdt.lib.container.Docker.export_image_all() to save as file
    """
    mm_pull_all = MagicMock()
    monkeypatch.setattr(bwdt.lib.container.Docker, 'pull_all', mm_pull_all)
    mm_export_image_all = MagicMock()
    monkeypatch.setattr(bwdt.lib.container.Docker, 'export_image_all',
                        mm_export_image_all)
    runner = CliRunner()
    pull = parm_pull == 'pull_true'
    opts = ['--pull'] if pull else ['--no-pull']
    result = runner.invoke(bwdt.cli.docker.export_image_all, opts)
    assert result.exit_code == 0
    assert mm_pull_all.called == pull
    assert mm_export_image_all.called
