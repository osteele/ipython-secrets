import os
from itertools import product
from unittest.mock import patch

import pytest
from ipython_secrets import delete_secret, get_secret, set_secret
from keyring.errors import PasswordDeleteError

os.environ['USER'] = 'ipython_secrets_PYTEST_USER'


@pytest.fixture
def keychain():
    # TODO: use a mock keyring backend, instead of mutating the real one
    users = [None, 'u1', 'u2']
    keys = ['KEY', 'K', 'K1', 'K2']
    for user, key in product(users, keys):
        try:
            delete_secret(key, username=user)
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
    assert get_secret('KEY', default=None) is None

    set_secret('KEY', 'S1')
    assert get_secret('KEY', default='default') == 'S1'
    assert get_secret('KEY', default=None) == 'S1'


def test_set_secret(keychain):
    set_secret('K1', 'S1')
    assert get_secret('K1') == 'S1'

    set_secret('K2', 'S2')
    assert get_secret('K1') == 'S1'
    assert get_secret('K2') == 'S2'

    set_secret('K1', 'S3')
    assert get_secret('K1') == 'S3'
    assert get_secret('K2') == 'S2'

    set_secret('K1', 'S4', username='u1')
    set_secret('K1', 'S5', username='u2')
    assert get_secret('K1') == 'S3'
    assert get_secret('K1', username='u1') == 'S4'
    assert get_secret('K1', username='u2') == 'S5'


def test_delete_secret(keychain):
    set_secret('K1', 'S1')
    set_secret('K2', 'S2')
    delete_secret('K1')
    assert get_secret('K1', default='none') is 'none'
    assert get_secret('K2') == 'S2'
