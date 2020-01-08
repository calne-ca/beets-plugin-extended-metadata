from beetsplug.queries.emd_query import EmdQuery
from beetsplug.queries.oneof_query import OneOfQuery
from beetsplug.queries.regex_query import RegexQuery


def create_query(raw_query):
    for s in EmdQuery.__subclasses__():
        query = s._create(raw_query)

        if query is not None:
            return query

    return None
