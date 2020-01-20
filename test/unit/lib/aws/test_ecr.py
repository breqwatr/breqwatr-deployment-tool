""" tests for ecr """
import boto3
import pytest
from mock import MagicMock

import bwdt.lib.aws.ecr
import bwdt.lib.auth


def test__get_ecr_client(monkeypatch):
    """
        - load the auth key and key ID from config file
        - create an ECR session with AWS boto3
    """
    mm_auth_get = MagicMock(name='auth_get')
    monkeypatch.setattr(bwdt.lib.auth, 'get', mm_auth_get())
    mm_session = MagicMock(name='session')
    monkeypatch.setattr(boto3, 'Session', mm_session)
    client = bwdt.lib.aws.ecr._get_ecr_client()
    assert mm_auth_get.called, 'auth.get() called'
    assert mm_session.called, 'boto3 session created'
    assert mm_session.return_value.client.called, 'ecr client made'
    assert client == mm_session.return_value.client.return_value, 'return ok'


def test_get_ecr_token(monkeypatch):
    """
        - get an authorization token
        - exit when token is invalid
    """
    # I actually don't like this logic and think it should just raise instead.
    # ... Let the Click code handle this user interaction.


def test_get_ecr_credentials():
    """
        - return a dict with username, password, registry as strings
    """
    authorizationToken = b'QVdTOmV5SndZWGxzYjJGa0lqb2lVSFkwWXpKeFNEaHZXVkkxVmtwRmVXdFhXamhKUVRGcGNFWk1kelJKZEV0V1UwSk9MMmw1VlUxR1dFUTNjMGR2Vm1sSlZqTllaMVJXT0cwck1FTm5iV3BSVVRsck5tZFdabkp6WkV4V1pqZDBUSFZSZGtwTVEyeGlRMHd3WlNzclJuRlJRMmtyWjBJcmJtVnlabkVyUzNsTGJtSmhLeTlNZFhseVFVMHlabVoyUkhBMlVETXlVVkJMZFhOamNsUlJOR0pGTlhsVU1UbEdiV0Y0WkdkRFZtVkxhbVpDY0V0Q2RFMXhTVVYxWTBWNk5qZ3ZabUpqTDBKYVRVWjVSRVY1Wm5GcFpubFllR2x5VEVsd1MzWlpRVWhWTjBONVNFUnRNbkVyZWtzdlpGQTBiRGRGZHpBMU1IWlRXbFF2VFVwS1FsbHhjMjVNZUd0U0wyd3lUbGsyYW14c1ZHNUdVMnQxTjB0U1JFVndSa1JhWlZvcmRuSjJhemR0UkhKRGRVNVFZWHBVZFdJNFZWQmxXRk5RT0dWQk1XVk1jMmt5VEdFdlNUaEtaemNyUWpkU2VqUnpaRzFsSzJkVFRGZHRjR1pMVTNJM1ltc3dMMnQ0VEVWR1UxbFZiVlZJU0hacFIyVTVhakYxVlZKc1VEQTBVbXQzU1ZFclNGa3hVRVpxTkVodFozQXhVa2h0Ulc4NFpVdEZRbE5LU1Uxb1l6UlJaM3BZTUhGdWIyODFRekpvY0ZsMFMzRlNUbUpvVUZOcVVGSkdNRTFQTjBSM1JsSXpSbFJ4WTJRdmNUQndjRXhRSzFSUVkyaFlVMU55TnpCQlNqSmlSSGszWWsxYVEwSm5OVGh1TkVaRlYwazJlbXhYWkM5NVlUVkhURzVwWTFKcWVGVTFPV3BPZUN0U1JGVmlWelZCV0Raa1dXVTNObkZzVEUxV1ZsZFNNRFpKZDFVclNsRnBZVXR5WlRBeFJXNXhjbVZYY0hWVmVGWnlVMVJXYTJ0RVoyZE1TeXN4ZEZneGVqaERjRlZpUkVKNmR6Rm1Nbk5RV25ReVIybG9lVlZaVDBSSFlqRk9OQ3RqWTBsc1JHUkxOblZGY1VSdFNXOTZiRVowVXpWeFZHTlZOM2syVUZaa1VWQkxVWGhzVm5WQ2NtOXNWRWhCVVRSYVZsSnJZMHhPTm1zMWRWWkxSVWxRVG1sbFIwcHZVR3Q0WVdRMGJtTm9XVEZDZUVoYVR5dFhVMU54UlhnMFYzaFJRWEpqZDBGVVIyY3lXbWw0VFZKc1IzaDBjbVZoV20wNFRXWnZhR0ZFUjNSU05uVk9aa2RGZUZKME1HMTNUM2xqUVM5NFpUUTBNMVZ5YzBOU1NVTXJjbkIyYTFaMWVTOVBPR1ZaVW5SQlp6a3lVRzAxTmt3clRFaE1VbFZQVkRsRGVuSmxOeXQ0YzFaeWJrMXBOMjlxVFVsd05WSjBUVUZuS3pWUlVFbENZMmhVZFhKRlUwUjJSR05rUVZaYWNGUjZZMWc0UVVFMlJsbE9UVFJ5UVdWWFFuazROekYyUjNScmNYZFhjVGRIWlZSUFpIaGhjVEJ2UnlzMFpEVlVXVWRaY1RGVGFsZFpkbmhzWTJ4elFWQlRLelpaZW1wbmVrODJTRlpIU1RSdFEybDFSRkZqYVhSV1ZrNVdiakZhWlhOWFZtdzNLekpqYVUxb2RHeEVhV0ZuZURoWWNFVmpWamxFYTBKV1dtcHpiaTltWkVkTlVrNHpSbTlWT0cxRllWUTNMekUwT0ZKVFkxa3ZjamxHYWt0dFZIY3pjMWxKWVhRMlRVWTFhVVkxWkZFeWJDc3dhMVFyVTFsVk1YcGhUME5YTUV0c2JqSjBPRGR2T1hZMFZHczRaU3MzYTNoUk5YRnlWSFZVUzNKWmRGQk9hWGQxVURCQk5FaHJUbEJKVEZoU1oydzRXRk54TUVWV1MydDRlbWxIWlV0Vk4zRlRiREZXTnpKdFJWaFFUMUZGVldsd1ZsUlZLemc5SWl3aVpHRjBZV3RsZVNJNklrRlJSVUpCU0doaVRUQllVRlZrWlRSeWEwMHpTVzgxZEdNd05EQnRTazlzU0U4eVkzTmlVVzl4Yld0S1ZYcFpRMU5SUVVGQlNEUjNaa0ZaU2t0dldrbG9kbU5PUVZGalIyOUhPSGRpVVVsQ1FVUkNiMEpuYTNGb2EybEhPWGN3UWtKM1JYZElaMWxLV1VsYVNVRlhWVVJDUVVWMVRVSkZSVVJGYlhsWk9VRlhWbGhvZHl0MmEwNVBkMGxDUlVsQk4yNXFUazl2TmtWRVl6WnJORzFGWVZNd1NIbHRhalJrV0c5cU1HY3hMekF4U0hCeU0xUnZPRlZDYzI4MVkxTTJRMG92VjNaUE1saG9abkIzS3poWlZUZDVRVVkyVlRkblFsVmlPRWhDUkdjOUlpd2lkbVZ5YzJsdmJpSTZJaklpTENKMGVYQmxJam9pUkVGVVFWOUxSVmtpTENKbGVIQnBjbUYwYVc5dUlqb3hOVGM1TlRJNU9EUXhmUT09'
    token = {
        'authorizationData': [{
            'authorizationToken': authorizationToken,
            'proxyEndpoint': 'FAKE ENDPOINT'}]}
    cred = bwdt.lib.aws.ecr.get_ecr_credentials(token)
    assert isinstance(cred, dict), 'dictionary returned'
    assert 'username' in cred and isinstance(cred['username'], str)
    assert 'password' in cred and isinstance(cred['password'], str)
    assert 'registry' in cred and isinstance(cred['registry'], str)


@pytest.mark.parametrize('parm_proto', ['', 'http://', 'https://'])
def test_get_registry_url(monkeypatch, parm_proto):
    """
        - accept dict with 'registry' key
        - returns its value without http/https
    """
    expected_url = 'ABC'
    registry = f'{parm_proto}{expected_url}'
    cred = {'registry': registry}
    url = bwdt.lib.aws.ecr.get_registry_url(cred)
    assert url == expected_url
