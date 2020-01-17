""" Ansible commands """

import click

import bwdt.cli.ansible


def test_get_ansible_group():
    """ return a click.core.Group object """
    group = bwdt.cli.ansible.get_ansible_group()
    assert isinstance(group, click.core.Group), 'click group is returned'
