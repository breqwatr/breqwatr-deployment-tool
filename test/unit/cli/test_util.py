""" util commands """

import click

import bwdt.cli.util


def test_get_util_group():
    """ return a click.core.Group object """
    group = bwdt.cli.util.get_util_group()
    assert isinstance(group, click.core.Group), 'click group is returned'
