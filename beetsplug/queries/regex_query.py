import re

from beetsplug.metadata import ExtendedMetaData
from beetsplug.queries.emd_query import EmdQuery


class RegexQuery(EmdQuery):
    REGEX_MATCHER = '::'
    _query_pattern = f'^({EmdQuery._word_pattern}){REGEX_MATCHER}(.*)$'

    def __init__(self, field, regex):
        self.field = field
        self.regex = regex

    def matches(self, metadata: ExtendedMetaData):
        if len(self.regex) is 0:
            return True

        field_value = metadata.value(self.field)

        if field_value is None:
            return False

        if isinstance(field_value, list):
            for item in field_value:
                if re.search(self.regex, item) is not None:
                    return True
            return False
        else:
            return re.search(self.regex, field_value) is not None

    @staticmethod
    def _create(raw_query):
        re_result = re.search(RegexQuery._query_pattern, raw_query)

        if re_result is None:
            return None

        field = re_result.group(1)
        regex = re_result.group(2)

        if field is None or regex is None:
            return None

        try:
            re.compile(regex)
        except re.error:
            return None

        return RegexQuery(field, regex)
