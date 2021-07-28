import click 
import os
import inspect
import xml.etree.cElementTree as ET
from collections import OrderedDict
from ckan.common import json

@click.group()
def citation():
    pass

def get_commands():
    return [citation]

m = __import__('ckanext.citation', fromlist=[''])
P = os.path.join(os.path.dirname(inspect.getfile(m)),
                 'public', 'ckanext', 'citation', 'csl')
CSL_P = os.path.join(P, 'styles')

@citation.command('build_styles')
def cmd_build_styles():
     major_styles = [
         'apa',
     #    'modern-language-association',
         'chicago-note-bibliography',
         'chicago-author-date',
     #    'ieee',
     #    'council-of-science-editors',
     #    'american-medical-association',
     #    'american-chemical-society',
     #    'american-institute-of-physics',
     #    'american-society-of-civil-engineers',
     ]
     all_csl = os.listdir(CSL_P)
     major_csl = [s + '.csl' for s in major_styles if s + '.csl' in all_csl]
     # other_csl = [c for c in all_csl if c not in major_csl]
     styles = _build_styles(major_csl, 'major')# + _build_styles(other_csl, 'other')
     styles_json = json.dumps(styles, separators=(',', ':'))
     with open (os.path.join(P, 'csl_styles.json'), 'w') as f:
         f.write(styles_json)

def _build_styles(csl, category=''):
    xmlns = 'http://purl.org/net/xbiblio/csl'
    output = []
    for c in csl:
        if not c.endswith('.csl'): continue
        tree = ET.parse(os.path.join(CSL_P, c))
        root = tree.getroot()
        info = root.find('./{%s}info' % xmlns)
        title = info.find('./{%s}title' % xmlns).text
        title_short = info.find('./{%s}title-short' % xmlns)
        if title_short != None:
            title_short = title_short.text
            title += ' (%s)' % title_short
        output.append(OrderedDict([
                ('id', c.split('.', 1)[0]),
                ('text', title),
                ('href', '/ckanext/citation/csl/styles/' + c),
                ('category', category)])
        )
    return output
