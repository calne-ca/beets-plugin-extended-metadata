import base64
import json
import re
from json import JSONDecodeError


class ExtendedMetaData:
    _base64_pattern = '(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?=?'
    _metadata_pattern = f'^EMD: ({_base64_pattern})$'

    def __init__(self, data):
        self._data = data

    def value(self, field):
        try:
            return self._data[field]
        except KeyError:
            return None

    @staticmethod
    def create(raw_value):
        re_result = re.search(ExtendedMetaData._metadata_pattern, str(raw_value))

        if re_result is None:
            return None

        encoded_metadata = re_result.group(1)

        if encoded_metadata is None:
            return None

        try:
            meta_data = json.loads(base64.b64decode(encoded_metadata))
        except JSONDecodeError:
            return None

        return ExtendedMetaData(meta_data)
