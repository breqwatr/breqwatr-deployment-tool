""" pxe commands """

import click

import bwdt.cli.pxe


def test_get_pxe_group():
    """ return a click.core.Group object """
    group = bwdt.cli.pxe.get_pxe_group()
    assert isinstance(group, click.core.Group), 'click group is returned'
