
from beets.dbcore import FieldQuery
from beets.plugins import BeetsPlugin

from beetsplug.audiofilefields import fields as audio_file_fields
from beetsplug.metadata import ExtendedMetaData
from beetsplug.queries.helper import create_query


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

        if audio_file_fields[self.input_field] is not None:
            extended_meta_data = audio_file_fields[self.input_field]
            self.add_media_field(u'' + self.query_field, extended_meta_data)

    def queries(self):
        return {
            '.': ExtendedMetaDataMatchQuery
        }

