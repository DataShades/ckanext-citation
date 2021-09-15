from __future__ import annotations

import json
from typing import Any

import citeproc
from  dateutil.parser import parse

import ckan.plugins.toolkit as tk
from ckanext.toolbelt.decorators import Collector

helper, get_helpers = Collector("citation").split()

CONFIG_MAPPING = "ckanext.citation.csl_mappings"
DEFAULT_MAPPING = "{}"


@helper
def format_csl(**metadata: Any) -> dict[str, Any]:
    """Format CSL citation from a list of values from CKAN package/resource
    metadata
    https://docs.citationstyles.org/en/stable/specification.html#appendix-iv-variables

    """

    _map_metadata(metadata)
    ordinary_vars = set(citeproc.VARIABLES)
    ordinary_vars |= {v.replace("_", "-") for v in ordinary_vars}

    citation = { var: metadata[var] for var in ordinary_vars if metadata.get(var) }

    _format_dates(citation)
    _format_names(citation)

    return citation

def _map_metadata(metadata: dict[str, Any]):
    mapping = json.loads(tk.config.get(CONFIG_MAPPING, DEFAULT_MAPPING))

    for from_, to_ in mapping.items():
        value = metadata.pop(from_, None)
        if value:
            metadata[to_] = value

    return metadata


def _format_dates(citation):
    for field in citeproc.DATES:
        if field not in citation:
            continue
        date = parse(citation[field])
        citation[field] = citeproc.source.Date(year=date.year, month=date.month, day=date.day)

def _format_names(citation):
    for field in citeproc.NAMES:
        if field not in citation:
            continue
        value = citation[field]
        citation[field] = [citeproc.source.Name(literal=value)]
