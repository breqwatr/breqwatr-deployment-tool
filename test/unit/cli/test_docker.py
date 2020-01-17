""" docker commands """

import click

import bwdt.cli.docker


def test_get_docker_group():
    """ return a click.core.Group object """
    group = bwdt.cli.docker.get_docker_group()
    assert isinstance(group, click.core.Group), 'click group is returned'
