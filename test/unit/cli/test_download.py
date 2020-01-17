""" download commands """

import click

import bwdt.cli.download


def test_get_download_group():
    """ return a click.core.Group object """
    group = bwdt.cli.download.get_download_group()
    assert isinstance(group, click.core.Group), 'click group is returned'
