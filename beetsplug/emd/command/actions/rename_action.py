import re

from beetsplug.emd.command.action import EmdCommandItemAction
from beetsplug.emd.query import EmdQuery


class EmdRenameTagAction(EmdCommandItemAction):

    def __init__(self):
        super(EmdRenameTagAction, self).__init__(needs_confirmation=True)
        self.rename_expressions = []

    def apply_option_values(self, opt_values, _):
        self.rename_expressions = [RenameExpression(v) for v in opt_values]

    def apply_to_item(self, item, emd):
        for exp in self.rename_expressions:
            if exp.old_tag in emd:
                emd[exp.new_tag] = emd[exp.old_tag]
                del emd[exp.old_tag]

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

        for exp in self.rename_expressions:
            action_description += f"Rename tag '{exp.old_tag}' to '{exp.new_tag}'"
            action_description += '\n'

        return action_description.rstrip()

    def is_applicable(self):
        return len(self.rename_expressions) > 0


class RenameExpression:
    _expression_pattern = f'^({EmdQuery._word_pattern})/({EmdQuery._word_pattern})$'

    def __init__(self, value):
        re_result = re.search(self._expression_pattern, value)

        if not re_result:
            raise Exception(f"Invalid syntax '{value}'")

        self.old_tag = re_result.group(1)
        self.new_tag = re_result.group(2)