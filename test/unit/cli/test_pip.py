""" pip commands """

import click

import bwdt.cli.pip


def test_get_pip_group():
    """ return a click.core.Group object """
    group = bwdt.cli.pip.get_pip_group()
    assert isinstance(group, click.core.Group), 'click group is returned'
