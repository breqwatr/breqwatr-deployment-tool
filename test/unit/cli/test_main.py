""" CLI entrypoint """

import click
import pytest
from mock import MagicMock

import bwdt.cli.main
import bwdt.lib.config


def test_get_entrypoint():
    """ return a click.core.Group object """
    group = bwdt.cli.main.get_entrypoint()
    assert isinstance(group, click.core.Group), 'click group is returned'


@pytest.mark.parametrize('conf_present', ['present', 'no_conf_file'])
def test_main(monkeypatch, conf_present):
    """
        - ensure entrypoint runs
    """
    # config.get_config() should return whether auth was found.
    mm_conf_get = MagicMock(name='mm_configure')
    conf_found = True if (conf_present == 'present') else None
    mm_conf_get.return_value = conf_found
    monkeypatch.setattr(bwdt.lib.config, 'get_config', mm_conf_get)
    # bwdt.lib.configure.configure() is not being tested here, should be called
    # make sure the return value of entrypoint runs
    mm_get_entrypoint = MagicMock(name='mm_get_entrypoint')
    monkeypatch.setattr(bwdt.cli.main, 'get_entrypoint', mm_get_entrypoint)
    bwdt.cli.main.main()
    assert mm_get_entrypoint.return_value.called, 'entrypoint ran'
