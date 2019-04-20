import base64
import json
import re
from json import JSONDecodeError

from beets.dbcore import FieldQuery
from beets.plugins import BeetsPlugin

from beetsplug.audiofilefields import fields as audio_file_fields


class ExtendedMetaDataMatchQuery(FieldQuery):

    word_pattern = "[a-zA-Z0-9-_]+"
    base64_pattern = '(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?=?'
    metadata_pattern = f'^EMD: ({base64_pattern})$'
    selector_pattern = f'^({word_pattern}):((!?){word_pattern}(,(!?){word_pattern})*)*$'
    selector_pattern_regex = f'^({word_pattern})::(.*)$'

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

        field_patterns = field_pattern.split(',') if not use_regex and ',' in field_pattern else [field_pattern]

        negated_field_patterns = [x[1:] for x in field_patterns if x.startswith('!')]
        field_patterns = [x for x in field_patterns if not x.startswith('!')]

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
                for pattern in field_patterns:
                    for item in field_value:
                        if pattern.lower() == item.lower():
                            return True
                for pattern in negated_field_patterns:
                    for item in field_value:
                        if pattern.lower() == item.lower():
                            return False
                return len(negated_field_patterns) > 0
        else:
            if use_regex:
                return re.search(field_pattern, field_value) is not None
            else:
                for pattern in field_patterns:
                    if pattern.lower() == field_value.lower():
                        return True
                for pattern in negated_field_patterns:
                    if pattern.lower() == field_value.lower():
                        return False
                return len(negated_field_patterns) > 0


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
