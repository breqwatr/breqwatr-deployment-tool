""" CLI entrypoint """

import pytest
from mock import MagicMock

import bwdt.cli.main
import bwdt.lib.configure
import bwdt.lib.auth

@pytest.mark.parametrize('parm_auth', ['auth_found', 'auth_not_found'])
def test_main(monkeypatch, parm_auth):
    """
        - configure.configure() should run when auth is false
        - ensure entrypoint runs
    """
    # auth.get() should return whether auth was found. Test true and false.
    mm_auth_get = MagicMock(name='mm_configure')
    auth_found = True if (parm_auth == 'auth_found') else None
    mm_auth_get.return_value = auth_found
    monkeypatch.setattr(bwdt.lib.auth, 'get', mm_auth_get)
    # bwdt.lib.configure.configure() is not being tested here, should be called
    mm_configure = MagicMock(name='mm_configure')
    monkeypatch.setattr(bwdt.lib.configure, 'configure', mm_configure)
    # make sure the return value of get_entrypoint runs
    mm_entrypoint = MagicMock(name='mm_get_entrypoint')
    monkeypatch.setattr(bwdt.cli.main, 'get_entrypoint', mm_entrypoint)
    bwdt.cli.main.main()
    assert mm_auth_get.called, 'called auth.get()'
    if not auth_found:
        assert mm_configure.called, 'called configure() when auth not found'
    assert mm_entrypoint.return_value.called, 'entrypoint ran'

