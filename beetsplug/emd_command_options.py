import re
from abc import ABC, abstractmethod

from beetsplug.emd_query import OneOfQuery, EmdQuery


class EmdCommandOption(ABC):

    @abstractmethod
    def add_parser_option(self, parser):
        pass

    @abstractmethod
    def parser_destination(self):
        pass

    @abstractmethod
    def apply(self, emd, opt_values):
        pass


class EmdShowOption(EmdCommandOption):

    def apply(self, emd, opt_values):
        if opt_values:
            print(emd)

    def add_parser_option(self, parser):
        parser.add_option(
            '-s', '--show', dest=self.parser_destination(),
            action="store_true", help='show the extended meta data of the files'
        )

    def parser_destination(self):
        return 'show_emd'


class EmdAddOption(EmdCommandOption):

    def apply(self, emd, opt_values):
        added_tag_values_tuples = [self._extract_tag_value_tuple(v) for v in opt_values]
        self._add_tag_values(emd, added_tag_values_tuples)

    def add_parser_option(self, parser):
        parser.add_option(
            '-a', '--add', dest=self.parser_destination(),
            action="append", type="string", default=[],
            help='add a tag value. Example: "tag1:v1" or "tag1:v1,v2,v3".'
        )

    def parser_destination(self):
        return 'add_expression'

    @staticmethod
    def _extract_tag_value_tuple(value):
        query = OneOfQuery._create(value)

        if not query:
            raise Exception(f"Invalid syntax '{value}'.")

        return query.field, query.values

    @staticmethod
    def _add_tag_values(emd, value_tuples):
        if not value_tuples:
            return

        for tag, values in value_tuples:
            if tag in emd:
                tag_values = emd[tag]

                for value in values:
                    if value not in tag_values:
                        tag_values.append(value)
            else:
                emd[tag] = values


class EmdDeleteOption(EmdCommandOption):

    def apply(self, emd, opt_values):
        removed_tag_values_tuples = [self._extract_tag_value_tuple(v) for v in opt_values]
        self._remove_tag_values(emd, removed_tag_values_tuples)

    def add_parser_option(self, parser):
        parser.add_option(
            '-d', '--delete', dest=self.parser_destination(),
            action="append", type="string", default=[],
            help='delete a tag value or tag. Example: "tag1" or "tag1:v1".'
        )

    def parser_destination(self):
        return 'delete_expression'

    @staticmethod
    def _extract_tag_value_tuple(value):
        query = OneOfQuery._create(value)

        if not query:
            raise Exception(f"Invalid syntax '{value}'.")

        return query.field, query.values

    @staticmethod
    def _remove_tag_values(emd, value_tuples):
        if not value_tuples:
            return

        for tag, values in value_tuples:
            if tag not in emd:
                return

            if len(values) == 0:
                del emd[tag]
            else:
                for value in values:
                    emd[tag].remove(value)


class EmdRenameTagOption(EmdCommandOption):

    def apply(self, emd, opt_values):
        renamed_tag_tuples = [self._extract_source_destination_tag_tuple(v) for v in opt_values]
        self._rename_tags(emd, renamed_tag_tuples)

    def add_parser_option(self, parser):
        parser.add_option(
            '-r', '--rename', dest=self.parser_destination(),
            action="append", type="string", default=[],
            help='rename a tag. Example: "tag1/tag2".'
        )

    def parser_destination(self):
        return 'rename_expression'

    @staticmethod
    def _rename_tags(emd, tags):
        for old_tag, new_tag in tags:
            if old_tag in emd:
                emd[new_tag] = emd[old_tag]
                del emd[old_tag]

    @staticmethod
    def _extract_source_destination_tag_tuple(value):
        re_result = re.search(f'^({EmdQuery._word_pattern})+/({EmdQuery._word_pattern})+$', value)

        if not re_result:
            raise Exception(f"Invalid syntax '{value}'")

        return re_result.group(1), re_result.group(2)


class EmdUpdateOption(EmdCommandOption):

    def apply(self, emd, opt_values):
        updated_tag_value_tuples = [self._extract_source_destination_tag_value_tuple(v) for v in opt_values]
        self._update_tag_values(emd, updated_tag_value_tuples)

    def add_parser_option(self, parser):
        parser.add_option(
            '-u', '--update', dest=self.parser_destination(),
            action="append", type="string", default=[],
            help='update or move a tag value. Example: "tag1:v1/tag1:v2" or "tag1:v1/tag2:v1" or "tag1:v1/tag2:v2".'
        )

    def parser_destination(self):
        return 'update_expression'

    @staticmethod
    def _update_tag_values(emd, tag_value_tuples):
        for src, dst in tag_value_tuples:
            old_tag = src[0]
            new_tag = dst[0]
            old_value = src[1][0]
            new_value = dst[1][0]

            if old_tag not in emd or old_value not in emd[old_tag]:
                continue

            emd[old_tag].remove(old_value)

            if new_tag in emd:
                emd[new_tag].append(new_value)
            else:
                emd[new_tag] = new_value

    @staticmethod
    def _extract_source_destination_tag_value_tuple(value):
        re_result = re.search(f'^(.+)+/(.+)+$', value)

        if not re_result:
            raise Exception(f"Invalid syntax '{value}'")

        return EmdUpdateOption._extract_tag_value_tuple(
            re_result.group(1)), EmdUpdateOption._extract_tag_value_tuple(re_result.group(2))

    @staticmethod
    def _extract_tag_value_tuple(value):
        query = OneOfQuery._create(value)

        if not query:
            raise Exception(f"Invalid syntax '{value}'.")

        return query.field, query.values