"""This package provides functions for using secrets in a Jupyter notebook.

These functions are for use in a notebook that needs to make use of secrets,
such as passwords and API keys, to avoid storing the secret in the notebook
source.

.. note:: This package uses Keyring_. See the `Keyring API documentation`_ for
    additional information about where secrets are stored, and how to change the
    default location.

.. _Keyring: https://pypi.python.org/pypi/keyring
.. _Keyring API documentation: http://keyring.readthedocs.io/en/latest/?badge=latest
"""


__version__ = '0.1.1'

import os
import keyring
try:
    from IPython.display import clear_output
except ImportError:
    def clear_output(): pass


def get_secret(service_name, username=None, *,
               default=None, force_prompt=False, prompt=None):
    """Read a secret from the keyring or the user.

    Look for a secret in the keyring. If it's not present, prompt the user,
    clear the cell, and save the secret.

    Parameters
    ----------
    service_name : str
        A keyring service name.

    username : str, optional
        A keyring username. This defaults to the value of the USER environment
        variable. (Note that this can programmatically altered.)

    default : str, optional
        The default value, if the secret is not present in the keyring. If this
        is non-None, the user is never prompted.

    force_prompt : str, optional
        If true, the user is always prompted for a secret.

    prompt : str, optional
        The text displayed to the user as part of the prompt.

    Examples
    --------
    ::

        from jupyter_secrets import *

        TWILIO_API_KEY = get_secret('TWILIO_API_KEY')
        TWILIO_API_KEY = get_secret('TWILIO_API_KEY', 'my-account')
        TWILIO_API_KEY = get_secret('TWILIO_API_KEY', 'my-account', prompt="Enter the API key")
    """
    if username is None:
        username = os.environ.get('USER')
    password = None if force_prompt else keyring.get_password(service_name, username)
    if password is None:
        password = default
    if password is None:
        # uses ternary instead of `prompt or …`, in order to support prompt == ''
        prompt = '{}[{}]'.format(service_name, username) if prompt is None else prompt
        password = input(prompt)
        keyring.set_password(service_name, username, password)
        clear_output()
    return password


def set_secret(service_name, password, *, username=None):
    """Sets a secret value.

    Parameters
    ----------
    service_name : str A keyring service name.

    password : str A keyring service name.

    username : str, optional A keyring username. This defaults to the value of
        the USER environment variable.

    Notes
    -----
    The argument order to `set_secret` is different from
    :func:`keyring.set_password`, and `username` can only be used as keyword
    parameter. This is in order that `username` can be optional, for
    compatibility with the more-frequently-used functions in this package.

    """
    if username is None:
        username = os.environ.get('USER')
    keyring.set_password(service_name, username, password)


def delete_secret(service_name, username=None):
    """Deletes a secret from the keyring.

    Parameters
    ----------
    service_name : str
        A keyring service name.

    username : str, optional
        A keyring username. This defaults to the value of the USER environment
        variable.
    """
    if username is None:
        username = os.environ.get('USER')
    keyring.delete_password(service_name, username)
