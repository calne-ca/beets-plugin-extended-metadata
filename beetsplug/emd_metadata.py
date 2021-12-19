import base64
import json
import re
from json import JSONDecodeError


class ExtendedMetaData:
    _base64_pattern = '(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?=?'
    _metadata_pattern = f'^EMD: ({_base64_pattern})$'

    def __init__(self, data=None):
        self._data = data if data else {}

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value if isinstance(value, list) else [value]

    def __delitem__(self, key):
        del self._data[key]

    def __contains__(self, key):
        return key in self._data

    def __str__(self):
        return str(self._json_data())

    @staticmethod
    def decode(raw_value):
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

        for tag in meta_data:
            value = meta_data[tag]
            if not isinstance(value, list):
                meta_data[tag] = [value]

        return ExtendedMetaData(meta_data)

    def encode(self):
        encoded_data = base64.b64encode(self._json_data().encode('utf-8')).decode('utf-8')
        return f'EMD: {encoded_data}'

    def _json_data(self):
        meta_data = self._data.copy()

        for tag in meta_data.copy():
            value = meta_data[tag]
            if isinstance(value, list):
                if len(value) == 1:
                    meta_data[tag] = value[0]
                elif len(value) == 0:
                    del meta_data[tag]

        return json.dumps(meta_data)
