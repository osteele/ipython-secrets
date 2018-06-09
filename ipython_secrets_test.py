import os

import ipython_secrets
import pytest
from unittest.mock import patch
from keyring.errors import PasswordDeleteError
from ipython_secrets import delete_secret, get_secret, set_secret

os.environ['USER'] = 'ipython_secrets_PYTEST_USER'


@pytest.fixture
def keychain():
    for k in ['KEY', 'K1', 'K2']:
        try:
            delete_secret(k)
        except PasswordDeleteError:
            pass


@pytest.fixture
def input():
    with patch('ipython_secrets.input', lambda *x: 'user input'):
        yield


def test_get_secret(keychain, input):
    assert get_secret('KEY') == 'user input'


def test_get_secret_defaults(keychain):
    assert get_secret('KEY', default='default') == 'default'
    set_secret('KEY', 'S1')
    assert get_secret('KEY', default='default') == 'S1'


def test_set_secret(keychain):
    set_secret('K1', 'S1')
    assert get_secret('K1') == 'S1'

    set_secret('K2', 'S2')
    assert get_secret('K1') == 'S1'
    assert get_secret('K2') == 'S2'

    set_secret('K1', 'S3')
    assert get_secret('K1') == 'S3'
    assert get_secret('K2') == 'S2'


def test_delete_secret(keychain):
    set_secret('K1', 'S1')
    set_secret('K2', 'S2')
    delete_secret('K1')
    assert get_secret('K1', default='none') is 'none'
    assert get_secret('K2') == 'S2'
