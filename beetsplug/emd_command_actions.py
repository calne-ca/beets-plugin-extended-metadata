import re
from abc import ABC, abstractmethod

from beetsplug.emd_query import OneOfQuery, EmdQuery


class EmdCommandAction(ABC):

    @abstractmethod
    def add_parser_option(self, parser):
        pass

    @abstractmethod
    def parser_destination(self):
        pass

    @abstractmethod
    def apply_option_values(self, opt_values, beets_lib):
        pass


class EmdCommandItemAction(EmdCommandAction):
    def __init__(self, needs_confirmation):
        self.needs_confirmation = needs_confirmation

    @abstractmethod
    def apply_to_item(self, item, emd):
        pass

    @abstractmethod
    def is_applicable(self):
        pass

    @abstractmethod
    def action_description(self):
        pass


class EmdQueryAction(EmdCommandAction):

    def __init__(self):
        self.items = []
        self.query = ''

    def apply_option_values(self, opt_values, beets_lib):
        self.query = opt_values
        self.items = beets_lib.items(f"'{self.query}'")

    def add_parser_option(self, parser):
        parser.add_option(
            '-q', '--query', dest=self.parser_destination(),
            action="store", type="string",
            help='a beets query that matches the items to which the actions will be applied to.'
        )

    def parser_destination(self):
        return 'query'


class EmdConfirmationAction(EmdCommandAction):

    def __init__(self):
        self.auto_confirm = False

    def apply_option_values(self, opt_values, _):
        self.auto_confirm = opt_values

    def add_parser_option(self, parser):
        parser.add_option(
            '-y', '--yes', dest=self.parser_destination(),
            action="store_true", help='automatically confirms yes/no prompts that require user input'
        )

    def parser_destination(self):
        return 'auto_confirm'

    def is_confirmed(self, items, item_actions):
        confirmation_necessary = len([a for a in item_actions if a.needs_confirmation and a.is_applicable()]) > 0

        if self.auto_confirm or not confirmation_necessary:
            return True

        print("Matching items:")

        for item in items:
            print(item)

        print("\nActions:")

        for item_option in item_actions:
            for line in item_option.action_description().splitlines():
                if line:
                    print(f'=> {line}')

        return self._confirmed_by_user(items)

    def _confirmed_by_user(self, items):
        confirmation = ''

        while confirmation != 'yes' and confirmation != 'no':
            print(f"\nAre you sure you want to apply the listed actions to {len(items)} listed items (yes/no)?", end=' ')
            confirmation = input().lower()

        return confirmation == 'yes'


class EmdShowMetadataAction(EmdCommandItemAction):

    def __init__(self):
        super(EmdShowMetadataAction, self).__init__(needs_confirmation=False)
        self.show_emd = False

    def apply_option_values(self, opt_values, _):
        self.show_emd = opt_values

    def apply_to_item(self, item, emd):
        if self.show_emd:
            print(emd)

    def add_parser_option(self, parser):
        parser.add_option(
            '-s', '--show', dest=self.parser_destination(),
            action="store_true", help='show the extended meta data of the items'
        )

    def parser_destination(self):
        return 'show_emd'

    def action_description(self):
        return 'Show resulting extended meta data' if self.show_emd else ''

    def is_applicable(self):
        return self.show_emd


class EmdAddTagAction(EmdCommandItemAction):

    def __init__(self):
        super(EmdAddTagAction, self).__init__(needs_confirmation=True)
        self.added_tag_values_tuples = []

    def apply_option_values(self, opt_values, _):
        self.added_tag_values_tuples = [self._extract_tag_value_tuple(v) for v in opt_values]

    def apply_to_item(self, item, emd):
        if not self.added_tag_values_tuples:
            return

        for tag, values in self.added_tag_values_tuples:
            if tag in emd:
                tag_values = emd[tag]

                for value in values:
                    if value not in tag_values:
                        tag_values.append(value)
            else:
                emd[tag] = values

    def add_parser_option(self, parser):
        parser.add_option(
            '-a', '--add', dest=self.parser_destination(),
            action="append", type="string", default=[],
            help='add a tag value. Example: "tag1:v1" or "tag1:v1,v2,v3".'
        )

    def parser_destination(self):
        return 'add_expression'

    def action_description(self):
        action_description = ''

        for tag, values in self.added_tag_values_tuples:
            action_description += f"Add values {values} to tag '{tag}'"
            action_description += '\n'

        return action_description.rstrip()

    def is_applicable(self):
        return len(self.added_tag_values_tuples) > 0

    @staticmethod
    def _extract_tag_value_tuple(value):
        query = OneOfQuery._create(value)

        if not query:
            raise Exception(f"Invalid syntax '{value}'.")

        return query.field, query.values


class EmdDeleteTagAction(EmdCommandItemAction):

    def __init__(self):
        super(EmdDeleteTagAction, self).__init__(needs_confirmation=True)
        self.removed_tag_values_tuples = []

    def apply_option_values(self, opt_values, _):
        self.removed_tag_values_tuples = [self._extract_tag_value_tuple(v) for v in opt_values]

    def apply_to_item(self, item, emd):
        if not self.removed_tag_values_tuples:
            return

        for tag, values in self.removed_tag_values_tuples:
            if tag not in emd:
                return

            if len(values) == 0:
                del emd[tag]
            else:
                for value in values:
                    emd[tag].remove(value)

    def add_parser_option(self, parser):
        parser.add_option(
            '-d', '--delete', dest=self.parser_destination(),
            action="append", type="string", default=[],
            help='delete a tag value or tag. Example: "tag1" or "tag1:v1".'
        )

    def parser_destination(self):
        return 'delete_expression'

    def action_description(self):
        action_description = ''

        for tag, values in self.removed_tag_values_tuples:
            action_description += f"Delete tag '{tag}'" if len(values) == 0 else f"Delete values {values} from tag '{tag}'"
            action_description += '\n'

        return action_description.rstrip()

    def is_applicable(self):
        return len(self.removed_tag_values_tuples) > 0

    @staticmethod
    def _extract_tag_value_tuple(value):
        query = OneOfQuery._create(value)

        if not query:
            raise Exception(f"Invalid syntax '{value}'.")

        return query.field, query.values


class EmdRenameTagAction(EmdCommandItemAction):

    def __init__(self):
        super(EmdRenameTagAction, self).__init__(needs_confirmation=True)
        self.renamed_tag_tuples = []

    def apply_option_values(self, opt_values, _):
        self.renamed_tag_tuples = [self._extract_source_destination_tag_tuple(v) for v in opt_values]

    def apply_to_item(self, item, emd):
        for old_tag, new_tag in self.renamed_tag_tuples:
            if old_tag in emd:
                emd[new_tag] = emd[old_tag]
                del emd[old_tag]

    def add_parser_option(self, parser):
        parser.add_option(
            '-r', '--rename', dest=self.parser_destination(),
            action="append", type="string", default=[],
            help='rename a tag. Example: "tag1/tag2".'
        )

    def parser_destination(self):
        return 'rename_expression'

    def action_description(self):
        action_description = ''

        for old_tag, new_tag in self.renamed_tag_tuples:
            action_description += f"Rename tag '{old_tag}' to '{new_tag}'"
            action_description += '\n'

        return action_description.rstrip()

    def is_applicable(self):
        return len(self.renamed_tag_tuples) > 0

    @staticmethod
    def _extract_source_destination_tag_tuple(value):
        re_result = re.search(f'^({EmdQuery._word_pattern})+/({EmdQuery._word_pattern})+$', value)

        if not re_result:
            raise Exception(f"Invalid syntax '{value}'")

        return re_result.group(1), re_result.group(2)


class EmdUpdateTagAction(EmdCommandItemAction):

    def __init__(self):
        super(EmdUpdateTagAction, self).__init__(needs_confirmation=True)
        self.updated_tag_value_tuples = []

    def apply_option_values(self, opt_values, _):
        self.updated_tag_value_tuples = [self._extract_source_destination_tag_value_tuple(v) for v in opt_values]

    def apply_to_item(self, item, emd):
        for src, dst in self.updated_tag_value_tuples:
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

    def add_parser_option(self, parser):
        parser.add_option(
            '-u', '--update', dest=self.parser_destination(),
            action="append", type="string", default=[],
            help='update or move a tag value. Example: "tag1:v1/tag1:v2" or "tag1:v1/tag2:v1" or "tag1:v1/tag2:v2".'
        )

    def parser_destination(self):
        return 'update_expression'

    def action_description(self):
        action_description = ''

        for src, dst in self.updated_tag_value_tuples:
            old_tag = src[0]
            new_tag = dst[0]
            old_value = src[1][0]
            new_value = dst[1][0]

            if old_value != new_value and old_tag == new_tag:
                action_description += f"Change value '{old_value}' from tag '{old_tag}' to '{new_value}'"
            elif old_tag != new_tag and old_value == new_value:
                action_description += f"Move value '{new_value}' from tag '{old_tag}' to tag '{new_tag}'"
            elif old_tag != new_tag and old_value != new_value:
                action_description += f"Change value '{old_value}' from tag '{old_tag}' to '{new_value}' and move it to tag '{new_tag}'"

            action_description += '\n'

        return action_description.rstrip()

    def is_applicable(self):
        return len(self.updated_tag_value_tuples) > 0

    @staticmethod
    def _extract_source_destination_tag_value_tuple(value):
        re_result = re.search(f'^(.+)+/(.+)+$', value)

        if not re_result:
            raise Exception(f"Invalid syntax '{value}'")

        return EmdUpdateTagAction._extract_tag_value_tuple(
            re_result.group(1)), EmdUpdateTagAction._extract_tag_value_tuple(re_result.group(2))

    @staticmethod
    def _extract_tag_value_tuple(value):
        query = OneOfQuery._create(value)

        if not query:
            raise Exception(f"Invalid syntax '{value}'.")

        return query.field, query.values