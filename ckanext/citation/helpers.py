from six import string_types
from ckan.common import config, json



_helpers = {}


def helper(fn):
    _helpers[f"citation_{fn.__name__}"] = fn
    return fn


def get_helpers():
    return _helpers.copy()


