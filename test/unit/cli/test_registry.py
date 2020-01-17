""" registry commands """

import click

import bwdt.cli.registry


def test_get_registry_group():
    """ return a click.core.Group object """
    group = bwdt.cli.registry.get_registry_group()
    assert isinstance(group, click.core.Group), 'click group is returned'
