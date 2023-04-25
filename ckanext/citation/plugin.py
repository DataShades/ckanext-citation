import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultTranslation

from ckanext.citation.cli import get_commands
from ckanext.citation.helpers import get_helpers
from ckanext.citation.logic.action import get_actions


class CitationPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IClick)
    plugins.implements(plugins.IActions)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "citation")

    # ITemplateHelpers

    def get_helpers(self):
        return get_helpers()

    def get_commands(self):
        return get_commands()

    def get_actions(self):
        return get_actions()
