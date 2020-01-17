""" arcus commands """

import click

import bwdt.cli.arcus


def test_get_arcus_group():
    """ return a click.core.Group object """
    group = bwdt.cli.arcus.get_arcus_group()
    assert isinstance(group, click.core.Group), 'click group is returned'
