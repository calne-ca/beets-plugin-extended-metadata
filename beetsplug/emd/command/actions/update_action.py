import re

from beetsplug.emd.command.action import EmdCommandItemAction
from beetsplug.emd.query import EmdQuery


class EmdUpdateTagAction(EmdCommandItemAction):

    def __init__(self):
        super(EmdUpdateTagAction, self).__init__(needs_confirmation=True)
        self.update_expressions = []

    def apply_option_values(self, opt_values, _):
        self.update_expressions = [UpdateExpression(v) for v in opt_values]

    def apply_to_item(self, item, emd):
        for exp in self.update_expressions:
            old_tag = exp.source_tag
            new_tag = exp.destination_tag
            old_value = exp.source_value
            new_value = exp.destination_value

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

        for exp in self.update_expressions:
            old_tag = exp.source_tag
            new_tag = exp.destination_tag
            old_value = exp.source_value
            new_value = exp.destination_value

            if old_value != new_value and old_tag == new_tag:
                action_description += f"Change value '{old_value}' from tag '{old_tag}' to '{new_value}'"
            elif old_tag != new_tag and old_value == new_value:
                action_description += f"Move value '{new_value}' from tag '{old_tag}' to tag '{new_tag}'"
            elif old_tag != new_tag and old_value != new_value:
                action_description += f"Change value '{old_value}' from tag '{old_tag}' to '{new_value}' and move it to tag '{new_tag}'"

            action_description += '\n'

        return action_description.rstrip()

    def is_applicable(self):
        return len(self.update_expressions) > 0


class UpdateExpression:
    _base_expression_pattern = f'({EmdQuery._word_pattern}):({EmdQuery._word_pattern})'
    _expression_pattern = f'^{_base_expression_pattern}/{_base_expression_pattern}$'

    def __init__(self, value):
        re_result = re.search(self._expression_pattern, value)

        if not re_result:
            raise Exception(f"Invalid syntax '{value}'")

        self.source_tag = re_result.group(1)
        self.source_value = re_result.group(2)

        self.destination_tag = re_result.group(3)
        self.destination_value = re_result.group(4)