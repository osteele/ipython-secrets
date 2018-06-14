import os
import keyring
import pytest
from keyring.errors import PasswordDeleteError

os.environ['USER'] = 'ipython_secrets_PYTEST_USER'


class MockKeyringBackend(keyring.backend.KeyringBackend):
    _passwords = dict()

    def clear(self):
        self._passwords.clear()

    def get_password(self, servicename, username):
        return self._passwords.get((servicename, username))

    def set_password(self, servicename, username, password):
        self._passwords[(servicename, username)] = password

    def delete_password(self, servicename, username):
        try:
            self._passwords.pop((servicename, username))
        except IndexError:
            raise PasswordDeleteError()


mockKeyringBackend = MockKeyringBackend()
keyring.set_keyring(mockKeyringBackend)


@pytest.fixture
def keyring_backend():
    mockKeyringBackend.clear()
    return mockKeyringBackend
