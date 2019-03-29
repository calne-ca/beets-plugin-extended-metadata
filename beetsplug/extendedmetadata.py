import base64
import json
import re
from json import JSONDecodeError

from beets.dbcore import FieldQuery
from beets.plugins import BeetsPlugin

from beetsplug.audiofilefields import fields as audio_file_fields


class ExtendedMetaDataMatchQuery(FieldQuery):

    base64_pattern = '(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?=?'
    metadata_pattern = f'^EMD: ({base64_pattern})$'
    selector_pattern = '^(\\w+):(\\w*)$'
    selector_pattern_regex = '^(\\w+)::(.*)$'

    @classmethod
    def value_match(cls, pattern, val):
        re_result = re.search(cls.metadata_pattern, str(val))

        if re_result is None:
            return False

        encoded_metadata = re_result.group(1)

        if encoded_metadata is None:
            return False

        try:
            meta_data = base64.b64decode(encoded_metadata)
            json_object = json.loads(meta_data)
        except JSONDecodeError:
            return False

        re_result = re.search(cls.selector_pattern, pattern)
        use_regex = False

        if re_result is None:
            re_result = re.search(cls.selector_pattern_regex, pattern)
            use_regex = True

        if re_result is None:
            return False

        field_name = re_result.group(1)
        field_pattern = re_result.group(2)

        if field_pattern is None:
            field_pattern = ''

        try:
            field_value = json_object[field_name]
        except KeyError:
            return False

        if field_value is None:
            return False
        elif len(field_pattern) is 0:
            return True

        if isinstance(field_value, list):
            if use_regex:
                for item in field_value:
                    if re.search(field_pattern, item) is not None:
                        return True
                return False
            else:
                for item in field_value:
                    if field_pattern.lower() == item.lower():
                        return True
                return False
        else:
            if use_regex:
                return re.search(field_pattern, field_value) is not None
            else:
                return field_pattern.lower() == field_value.lower()


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
