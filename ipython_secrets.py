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


__version__ = '1.1.1'

import os
import keyring
try:
    from IPython.display import clear_output
except ImportError:
    def clear_output():
        pass

__all__ = ["get_secret", "set_secret", "delete_secret"]

DEFAULT = object()


def _iter_usernames():
    """Yield username candidates.

    Try a few heuristics for determining the username:

    1. The value of the USER environment variable.
    2. If the keyring backend has a `credentials` property
       (:class:`gsheet_keyring:GoogleSheetKeyring` does):

      1. The value of ``credentials.id_token['email']`, if this is defined.
      2. The user info email returned by the Google OAuth2 service.

    3. If the oauth2 library is available, get the application default
       credentials, and repeat 2.1–2.2 with these credentials.
    """
    yield os.environ.get('USER')

    def iter_credential_usernames(credentials):
        try:
            if credentials.id_token:
                yield credentials.id_token['email']
        except (AttributeError, KeyError):
            pass

        try:
            from googleapiclient.discovery import build
            service = build(serviceName='oauth2', version='v2', credentials=credentials)
            info = service.userinfo().get().execute()
            yield info['email']
        except (AttributeError, ImportError):
            pass

    def iter_credentials():
        try:
            yield keyring.get_keyring().credentials
        except AttributeError:
            pass

        try:
            from oauth2client.client import (ApplicationDefaultCredentialsError,
                                             GoogleCredentials)
            yield GoogleCredentials.get_application_default()
        except (ApplicationDefaultCredentialsError, ImportError):
            pass

    for credentials in iter_credentials():
        yield from iter_credential_usernames(credentials)


def get_username():
    """Return a default username, using a few heuristics.

    Returns the first username from the ``USER`` environment variable , the
    current keyring backend's OAuth2 ``credentials``, and (if
    :mod:`oauth2client` is installed) the current environnment's `Application
    Default Credentials`_.

    .. _Application Default Credentials:
    https://cloud.google.com/docs/authentication/production
    """
    return next(filter(None, _iter_usernames()), 'ipython-secrets')


def get_secret(servicename, *, username=None,
               default=DEFAULT, force_prompt=False, prompt=None):
    """Read a stored secret, or prompt the user for its value.

    Look for a secret in the keyring. If it's not present, prompt the user,
    clear the cell, and save the secret.

    Parameters
    ----------
    servicename: str
        A keyring service name.

    username: str, optional
        A keyring username. This defaults to the value of the USER environment
        variable. (Note that this can programmatically altered.)

    default: str, optional
        The default value, if the secret is not present in the keyring. If this
        is supplied, the user is never prompted.

    force_prompt: str, optional
        If true, the user is always prompted for a secret.

    prompt: str, optional
        The text displayed to the user as part of the prompt.

    Examples
    --------
    ::

        from ipython_secrets import *

        TWILIO_API_KEY = get_secret('TWILIO_API_KEY')
        TWILIO_API_KEY = get_secret('TWILIO_API_KEY', 'my-account')
        TWILIO_API_KEY = get_secret('TWILIO_API_KEY', 'my-account',
                                    prompt="Enter the API key")
    """
    if username is None:
        username = get_username()
    password = None
    if not force_prompt:
        password = keyring.get_password(servicename, username)
    if password is not None:
        return password
    if default is not DEFAULT:
        return default
    prompt = '{}[{}]'.format(servicename, username) if prompt is None else prompt
    password = input(prompt)
    keyring.set_password(servicename, username, password)
    clear_output()
    return password


def set_secret(servicename, password, *, username=None):
    """Set a secret value.

    Parameters
    ----------
    servicename: str
        A keyring service name.

    password: str
        A keyring service name.

    username: str, optional
        A keyring username. This defaults to the value of the USER environment
        variable.

    Notes
    -----
    The argument order to `set_secret` is different from
    :func:`keyring.set_password`, and `username` can only be used as keyword
    parameter. This is in order that `username` can be optional, for
    compatibility with the more-frequently-used functions in this package.

    """
    keyring.set_password(servicename, username or get_username(), password)


def delete_secret(servicename, username=None):
    """Delete a secret from the keyring.

    Parameters
    ----------
    servicename: str
        A keyring service name.

    username: str, optional
        A keyring username. This defaults to the value of the USER environment
        variable.
    """
    keyring.delete_password(servicename, username or get_username())
