from six import string_types
from ckan.common import config, json


CKAN_TO_CSL_FIELDS = {
    'title': 'title',
    'author': 'author'
}

_helpers = {}


def helper(fn):
    _helpers[f"citation_{fn.__name__}"] = fn
    return fn


def get_helpers():
    return _helpers.copy()


@helper
def map_ckan_to_csl_field():
    mappings = config.get('ckanext.citation.csl_mappings')
    if mappings:
        if isinstance(mappings, string_types):
            CKAN_TO_CSL_FIELDS.update(json.loads(mappings))
        elif isinstance(mappings, dict):
            CKAN_TO_CSL_FIELDS.update(mappings)
    return CKAN_TO_CSL_FIELDS
