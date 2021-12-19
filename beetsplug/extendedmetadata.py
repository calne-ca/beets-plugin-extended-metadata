from beets.plugins import BeetsPlugin
from beetsplug.emd_command import ExtendedMetaDataCommand
from beetsplug.emd_query import ExtendedMetaDataMatchQuery


class ExtendedMetaDataPlugin(BeetsPlugin):

    def __init__(self):
        super(ExtendedMetaDataPlugin, self).__init__()

        self.input_field = self.config['input_field'].get('comments')
        self.query_prefix = self.config['query_prefix'].get('x')

        ExtendedMetaDataMatchQuery.input_field = self.input_field
        self.item_queries = {self.query_prefix: ExtendedMetaDataMatchQuery}

    def commands(self):
        return [ExtendedMetaDataCommand(self.input_field)]
