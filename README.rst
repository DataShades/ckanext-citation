================
ckanext-citation
================

This extension provides a snippet in dataset page
to cite a dataset in a specific citation style.

------------
Requirements
------------

This extension is only tested in CKAN 2.7 and later.

------------
Installation
------------

To install ckanext-citation:

1. Activate your CKAN virtual environment, for example::

    . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-citation Python package into your virtual environment::

    pip install 'git+https://github.com/DataShades/ckanext-citation.git#egg=ckanext-citation'

3. Add ``citation`` to the ``ckan.plugins`` setting in your CKAN
   config file.

-------------
Configuration
-------------

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Mapping between CKAN Fields and `CSL Variables`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Currently only title and author fields are supported. ::

    ckanext.citation.csl_mappings = {"title": "title", "author": "author"}


`CSL Variables`:  https://docs.citationstyles.org/en/stable/specification.html#appendix-iv-variables

-----
Usage
-----

^^^^^^^^
Commands
^^^^^^^^

``citation``

1. ``build_styles``: generate a list of citation styles.::

    ckan citation build_styles

* By default, the following styles will be shown as major styles:

    * apa
    * modern-language-association
    * chicago-note-bibliography
    * chicago-author-date
    * ieee
    * council-of-science-editors
    * american-medical-association
    * american-chemical-society
    * american-institute-of-physics
    * american-society-of-civil-engineers
    
* Or the styles list can be configured via options `ckanext.citation.csl_styles` separating by space, or newline characters. Run the command again when you finish adding styles

* You may need to update the citation styles::

    cd ckanext-citation/ckanext/citation/public/ckanext/citation/csl/styles && git pull

