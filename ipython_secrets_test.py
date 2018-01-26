from ipython_secrets import *
import os

os.environ['USER'] = 'ipython_secrets_PYTEST_USER'

# This doesn't do much more than test if the import succeeds.


def test_get_secret():
    # delete_secret('SECRET')
    assert get_secret('SECRET', default=10) == 10
