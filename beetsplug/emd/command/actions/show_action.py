from beetsplug.emd.command.action import EmdCommandItemAction


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
