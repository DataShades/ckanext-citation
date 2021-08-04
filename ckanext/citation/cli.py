import click
import os
import inspect
import xml.etree.cElementTree as ET
from collections import OrderedDict
from ckan.common import config, json

@click.group()
def citation():
    pass

def get_commands():
    return [citation]

m = __import__('ckanext.citation', fromlist=[''])
P = os.path.join(os.path.dirname(inspect.getfile(m)),
                 'public', 'ckanext', 'citation', 'csl')
CSL_P = os.path.join(P, 'styles')


DEFAULT_CSL_MAJOR_STYLES = [
    'apa',
    'modern-language-association',
    'chicago-note-bibliography',
    'chicago-author-date',
    'ieee',
    'council-of-science-editors',
    'american-medical-association',
    'american-chemical-society',
    'american-institute-of-physics',
    'american-society-of-civil-engineers',
]


@citation.command('build_styles')
def cmd_build_styles():
    all_csl = os.listdir(CSL_P)
    major_csl = []
    for style in _csl_styles():
        style = style + '.csl'
        if style not in all_csl:
            click.secho(f'CSL style {style} not found in {CSL_P}', fg='red')
            continue
        major_csl.append(style)

    styles = _build_styles(major_csl, 'major')
    styles_json = json.dumps(styles, separators=(',', ':'))
    with open (os.path.join(P, 'csl_styles.json'), 'w') as f:
        f.write(styles_json)
    click.secho('Build Finished!', fg='yellow', bold=True)


def _csl_styles():
    styles = config.get('ckanext.citation.csl_styles')
    if styles is None:
        styles = DEFAULT_CSL_MAJOR_STYLES
    else:
        styles = styles.split()
    return styles


def _build_styles(csl, category=''):
    xmlns = 'http://purl.org/net/xbiblio/csl'
    output = []
    for style in csl:
        if not style.endswith('.csl'):
            continue
        tree = ET.parse(os.path.join(CSL_P, style))
        root = tree.getroot()
        info = root.find('./{%s}info' % xmlns)
        title = info.find('./{%s}title' % xmlns).text
        title_short = info.find('./{%s}title-short' % xmlns)
        if title_short != None:
            title_short = title_short.text
            title += ' (%s)' % title_short
        output.append(OrderedDict([
            ('id', style.split('.', 1)[0]),
            ('text', title),
            ('href', '/ckanext/citation/csl/styles/' + style),
            ('category', category)])
        )
    return output
