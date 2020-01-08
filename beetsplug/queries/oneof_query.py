import re

from beetsplug.metadata import ExtendedMetaData
from beetsplug.queries.emd_query import EmdQuery


class OneOfQuery(EmdQuery):
    CONTAINS_MATCHER = ':'
    _query_pattern = f'^({EmdQuery._word_pattern}){CONTAINS_MATCHER}((!?){EmdQuery._word_pattern}(,(!?){EmdQuery._word_pattern})*)*$'

    def __init__(self, field, values, negated_values):
        self.field = field
        self.values = values
        self.negated_values = negated_values

    def matches(self, metadata: ExtendedMetaData):
        if len(self.values) is 0 and len(self.negated_values) is 0:
            return True
        if len(self.values) is 0 and len(self.negated_values) is 1 and len(self.negated_values[0]) is 0:
            return False

        field_value = metadata.value(self.field)

        if field_value is None:
            return len(self.negated_values) is 1 and len(self.values) is 0

        if isinstance(field_value, list):
            for pattern in self.values:
                for item in field_value:
                    if pattern.lower() == item.lower():
                        return True
            for pattern in self.negated_values:
                for item in field_value:
                    if pattern.lower() == item.lower():
                        return False
            return len(self.negated_values) > 0
        else:
            for pattern in self.values:
                if pattern.lower() == field_value.lower():
                    return True
            for pattern in self.negated_values:
                if pattern.lower() == field_value.lower():
                    return False
            return len(self.negated_values) > 0

    @staticmethod
    def _create(raw_query):
        re_result = re.search(OneOfQuery._query_pattern, raw_query)

        if re_result is None:
            return None

        field = re_result.group(1)
        selectors = re_result.group(2)

        if field is None:
            return None

        if selectors is None:
            return OneOfQuery(field, [], [])

        values = [v for v in selectors.split(',') if v]
        negated_values = [x[1:] for x in values if x.startswith('!')]
        values = [x for x in values if not x.startswith('!')]

        return OneOfQuery(field, values, negated_values)
