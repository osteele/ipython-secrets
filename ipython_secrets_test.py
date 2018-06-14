from unittest.mock import patch

from ipython_secrets import delete_secret, get_secret, set_secret


def test_get_secret(keyring_backend):
    with patch('ipython_secrets.input', lambda *x: 'user input'):
        assert get_secret('KEY') == 'user input'


def test_get_secret_defaults(keyring_backend):
    assert get_secret('KEY', default='default') == 'default'
    assert get_secret('KEY', default=None) is None

    set_secret('KEY', 'S1')
    assert get_secret('KEY', default='default') == 'S1'
    assert get_secret('KEY', default=None) == 'S1'


def test_set_secret(keyring_backend):
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


def test_delete_secret(keyring_backend):
    set_secret('K1', 'S1')
    set_secret('K2', 'S2')
    delete_secret('K1')
    assert get_secret('K1', default='none') is 'none'
    assert get_secret('K2') == 'S2'
