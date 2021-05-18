
from beets.dbcore import FieldQuery
from beets.plugins import BeetsPlugin

from beetsplug.emd_metadata import ExtendedMetaData
from beetsplug.emd_query import create_query
from beetsplug.emd_audiofilefields import fields


class ExtendedMetaDataMatchQuery(FieldQuery):

    @classmethod
    def value_match(cls, pattern, val):
        meta_data = ExtendedMetaData.create(val)

        if meta_data is None:
            return False

        query = create_query(pattern)

        if query is None:
            return False

        return query.matches(meta_data)


class ExtendedMetaDataPlugin(BeetsPlugin):

    def __init__(self):
        super(ExtendedMetaDataPlugin, self).__init__()

        self.input_field = self.config['input_field'].get('comments')
        self.query_field = self.config['query_field'].get('x')

        if fields[self.input_field] is not None:
            extended_meta_data = fields[self.input_field]
            self.add_media_field(u'' + self.query_field, extended_meta_data)

    def queries(self):
        return {
            '.': ExtendedMetaDataMatchQuery
        }

