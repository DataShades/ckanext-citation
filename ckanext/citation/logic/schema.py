from ckan.logic.schema import validator_args


@validator_args
def format_style(not_empty, one_of, ignore_missing):
    return {
        "style_id": [
            not_empty,
        ],
        "style_dict": [
            not_empty,
        ],
        "style_formatter": [
            ignore_missing,
            one_of(["plain", "html", "rst"]),
        ],
    }
