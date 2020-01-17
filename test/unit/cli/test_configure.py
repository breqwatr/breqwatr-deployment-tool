""" configure commands """

import click

import bwdt.cli.configure


def test_get_configure_group():
    """ return a click.core.Group object """
    group = bwdt.cli.configure.get_configure_group()
    assert isinstance(group, click.core.Group), 'click group is returned'
