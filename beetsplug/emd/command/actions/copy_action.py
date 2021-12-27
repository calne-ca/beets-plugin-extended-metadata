import re

from beetsplug.emd.command.action import EmdCommandItemAction
from beetsplug.emd.query import EmdQuery


class EmdCopyTagAction(EmdCommandItemAction):

    def __init__(self):
        super(EmdCopyTagAction, self).__init__(needs_confirmation=True)
        self.copy_expressions = []

    def apply_option_values(self, opt_values, _):
        self.copy_expressions = [CopyExpression(v) for v in opt_values]

    def apply_to_item(self, item, emd):
        for exp in self.copy_expressions:
            if exp.is_source_emd and exp.source_tag not in emd:
                continue

            value = emd[exp.source_tag][0] if exp.is_source_emd else item[exp.source_tag]

            if exp.is_destination_emd:
                if exp.destination_tag in emd:
                    emd[exp.destination_tag].append(value)
                else:
                    emd[exp.destination_tag] = value
            else:
                item[exp.destination_tag] = value

    def add_parser_option(self, parser):
        parser.add_option(
            '-c', '--copy', dest=self.parser_destination(),
            action="append", type="string", default=[],
            help='copy a tag value from/to extended metadata or normal metadata. Tags prefixed with . refer to tags of normal metadata. Examples: "tag1/tag2", ".artist/tag2", "tag1/.artist", ".artist/.album_artist"'
        )

    def parser_destination(self):
        return 'copy_expression'

    def action_description(self):
        action_description = ''

        for exp in self.copy_expressions:
            action_description += f"Copy value from {'' if exp.is_source_emd else 'normal '}tag '{exp.source_tag}' "
            action_description += f"to {'' if exp.is_destination_emd else 'normal '}tag '{exp.destination_tag}'"
            action_description += '\n'

        return action_description.rstrip()

    def is_applicable(self):
        return len(self.copy_expressions) > 0


class CopyExpression:
    _expression_pattern = f'^(\\.?)({EmdQuery._word_pattern})/(\\.?)({EmdQuery._word_pattern})$'

    def __init__(self, value):
        re_result = re.search(self._expression_pattern, value)

        if not re_result:
            raise Exception(f"Invalid syntax '{value}'")

        self.is_source_emd = len(re_result.group(1)) == 0
        self.source_tag = re_result.group(2)

        self.is_destination_emd = len(re_result.group(3)) == 0
        self.destination_tag = re_result.group(4)