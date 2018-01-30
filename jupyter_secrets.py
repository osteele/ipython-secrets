"""jupyter_secrets has been renamed to ipython-secrets. Use that instead:

pip3 install ipython-secrets
from ipython_secrets import *
"""


__version__ = '0.2.0'

import sys
# import ipython_secrets


def write_deprecation_warning():
    sys.stderr.write("Warning: " + sys.modules[__name__].__doc__)

write_deprecation_warning()


def get_secret(*args, **kwargs):
    write_deprecation_warning()
    return get_secret(*args, **kwargs)


def set_secret(service_name, password, *, username=None):
    write_deprecation_warning()
    return set_secret(*args, **kwargs)


def delete_secret(service_name, username=None):
    write_deprecation_warning()
    return delete_secret(*args, **kwargs)

for method in [get_secret, set_secret, delete_secret]:
    method.__doc__ = ("Warning: jupyter_secrets.{0:} has been deprecated. " +
                      "Use ipython.{0:} instead.").format(method.__name__)
