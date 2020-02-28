""" Test the license lib """
import pytest
import bwdt.lib.license as license


@pytest.mark.parametrize('is_valid_license', ['valid', 'invalid'])
def test_get_keys_from_license(is_valid_license):
    """ test get_key """
    is_valid_license = is_valid_license == 'valid'
    good = "Aqqqqqqqqqqqqqqqq111-1111qqqq111qqqq1111qq1q1q1q1q1q1q1q11111"
    bad = "FAKE"
    license_arg = good if is_valid_license else bad
    valid, keys = license.get_keys_from_license(license_arg)
    assert valid == is_valid_license
    if is_valid_license:
        assert 'id' in keys
        assert 'secret' in keys
