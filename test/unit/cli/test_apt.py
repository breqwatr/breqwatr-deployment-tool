""" apt commands """

import click

import bwdt.cli.apt


def test_get_apt_group():
    """ return a click.core.Group object """
    group = bwdt.cli.apt.get_apt_group()
    assert isinstance(group, click.core.Group), 'click group is returned'
