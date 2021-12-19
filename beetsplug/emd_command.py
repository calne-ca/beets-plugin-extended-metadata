from beets.ui import Subcommand

from beetsplug.emd_metadata import ExtendedMetaData
from beetsplug.emd_command_options import EmdAddOption, EmdDeleteOption, EmdUpdateOption, EmdRenameTagOption, \
    EmdShowOption

emd_command_options = [
    EmdUpdateOption(),
    EmdRenameTagOption(),
    EmdAddOption(),
    EmdDeleteOption(),
    EmdShowOption()
]


class ExtendedMetaDataCommand(Subcommand):
    def __init__(self, input_field):
        super(ExtendedMetaDataCommand, self).__init__('emd', help=u'manage extended meta data')

        self.input_field = input_field

        self.parser.add_option(
            '-q', '--query', dest='query',
            action="store", type="string", default=[],
            help='a beets query that matches the items to which the actions will be applied to.'
        )

        for option in emd_command_options:
            option.add_parser_option(self.parser)

        self.func = self.handle_command

    def handle_command(self, lib, opts, _):
        if not self._options_are_valid(opts):
            self.parser.print_help()
            return

        query = opts.query
        items = lib.items(query)

        for item in items:
            print(item)

            old_tags = dict(item).copy()
            emd = self._get_emd(item)

            for option in emd_command_options:
                option.apply(emd, getattr(opts, option.parser_destination()))

            self._update_emd(item, emd)
            new_tags = dict(item)

            if old_tags == new_tags:
                continue

            item.write()
            item.store()

    @staticmethod
    def _options_are_valid(opts):
        if not opts.query:
            return False

        for option in emd_command_options:
            if getattr(opts, option.parser_destination()):
                return True
        return False

    def _get_emd(self, item):
        raw_emd = item[self.input_field]
        emd = ExtendedMetaData.decode(raw_emd)

        if not emd:
            emd = ExtendedMetaData()

        return emd

    def _update_emd(self, item, emd):
        updated_emd = emd.encode()
        item[self.input_field] = updated_emd
