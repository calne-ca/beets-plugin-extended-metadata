import re

from beetsplug.emd.command.action import EmdCommandItemAction
from beetsplug.emd.query import EmdQuery


class EmdAddTagAction(EmdCommandItemAction):

    def __init__(self):
        super(EmdAddTagAction, self).__init__(needs_confirmation=True)
        self.add_expressions = []

    def apply_option_values(self, opt_values, _):
        self.add_expressions = [AddExpression(v) for v in opt_values]

    def apply_to_item(self, item, emd):
        for exp in self.add_expressions:
            if exp.tag in emd:
                tag_values = emd[exp.tag]

                for value in exp.values:
                    if value not in tag_values:
                        tag_values.append(value)
            else:
                emd[exp.tag] = exp.values

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

        for exp in self.add_expressions:
            action_description += f"Add values {exp.values} to tag '{exp.tag}'"
            action_description += '\n'

        return action_description.rstrip()

    def is_applicable(self):
        return len(self.add_expressions) > 0


class AddExpression:
    _expression_pattern = f'^({EmdQuery._word_pattern}):({EmdQuery._word_pattern}(,{EmdQuery._word_pattern})*)$'

    def __init__(self, value):
        re_result = re.search(self._expression_pattern, value)

        if not re_result:
            raise Exception(f"Invalid syntax '{value}'")

        self.tag = re_result.group(1)
        self.values = [v for v in re_result.group(2).split(',') if v]