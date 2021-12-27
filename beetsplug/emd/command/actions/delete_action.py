import re

from beetsplug.emd.command.action import EmdCommandItemAction
from beetsplug.emd.query import EmdQuery


class EmdDeleteTagAction(EmdCommandItemAction):

    def __init__(self):
        super(EmdDeleteTagAction, self).__init__(needs_confirmation=True)
        self.delete_expressions = []

    def apply_option_values(self, opt_values, _):
        self.delete_expressions = [DeleteExpression(v) for v in opt_values]

    def apply_to_item(self, item, emd):
        for exp in self.delete_expressions:
            if exp.tag not in emd:
                return

            if len(exp.values) == 0:
                del emd[exp.tag]
            else:
                for value in exp.values:
                    emd[exp.tag].remove(value)

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

        for exp in self.delete_expressions:
            action_description += f"Delete tag '{exp.tag}'" if len(exp.values) == 0 else f"Delete values {exp.values} from tag '{exp.tag}'"
            action_description += '\n'

        return action_description.rstrip()

    def is_applicable(self):
        return len(self.delete_expressions) > 0


class DeleteExpression:
    _expression_pattern = f'^({EmdQuery.TAG_PATTERN})(:({EmdQuery.VALUE_PATTERN}(,{EmdQuery.VALUE_PATTERN})*))?$'

    def __init__(self, value):
        re_result = re.search(self._expression_pattern, value)

        if not re_result:
            raise Exception(f"Invalid syntax '{value}'")

        values = re_result.group(3)

        self.tag = re_result.group(1)
        self.values = [v for v in values.split(',') if v] if values else []