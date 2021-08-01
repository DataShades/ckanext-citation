from datetime import datetime


_helpers = {}


def helper(fn):
    _helpers[f"citation_{fn.__name__}"] = fn
    return fn


def get_helpers():
    return _helpers.copy()


@helper
def format_csl(**metadata):
    # Format CSL citation from a list of values from CKAN package/resource metadata
    # https://docs.citationstyles.org/en/stable/specification.html#appendix-iv-variables
    ordinary_vars = ['type', 'title', 'URL', 'version']
    citation = { var: metadata[var] for var in ordinary_vars if var in metadata }
    if 'author' in metadata:
        # TODO: Handle list of authors, with more information such as lastname, firstname
        citation['author'] = [{'literal': metadata['author']}]
    if 'issued' in metadata:
        # Should be a valid Python ISO format datetime type
        issued = datetime.fromisoformat(metadata['issued'])
        date_parts = citation.setdefault('issued', {'date-parts': []})['date-parts']
        date_parts.append([issued.year, issued.month, issued.day])
    if 'DOI' in metadata:
        citation['DOI'] = metadata['DOI']
    return citation
