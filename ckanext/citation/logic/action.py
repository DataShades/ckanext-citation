from __future__ import annotations

import os

from citeproc import (
    Citation,
    CitationItem,
    CitationStylesBibliography,
    CitationStylesStyle,
    formatter,
)
from citeproc.source.json import CiteProcJSON

import ckan.plugins.toolkit as tk
from ckan.logic import validate

from ckanext.toolbelt.decorators import Collector

from ckanext.citation.logic import schema
from ckanext.citation.utils import CSL_P

action, get_actions = Collector("citation").split()


@action
@tk.side_effect_free
@validate(schema.format_style)
def format_style(context, data_dict):
    style_id = data_dict.get("style_id")
    style_dict = data_dict.get("style_dict")
    style_formatter = data_dict.get("style_formatter", "plain")

    bib_style = CitationStylesStyle(os.path.join(CSL_P, style_id), validate=False)

    style_dict["id"] = "citation"
    bib_source = CiteProcJSON([style_dict])

    if style_formatter == "plain":
        bib_formater = formatter.plain
    if style_formatter == "html":
        bib_formater = formatter.html
    if style_formatter == "rst":
        bib_formater = formatter.rst

    bibliography = CitationStylesBibliography(bib_style, bib_source, bib_formater)
    bibliography.register(Citation([CitationItem("citation")]))

    return _format_citation(str(bibliography.bibliography()[0]))


def _format_citation(citation):
    citation = citation.replace("  ", " ")
    citation = citation.replace("..", ".")
    return citation
