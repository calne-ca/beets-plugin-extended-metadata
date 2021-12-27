from optparse import OptionParser, BadOptionError

from beets.ui import Subcommand
from beetsplug.emd.command.actions.add_action import EmdAddTagAction

from beetsplug.emd.metadata import ExtendedMetaData
from beetsplug.emd.command.actions.confirmation_action import EmdConfirmationAction
from beetsplug.emd.command.actions.copy_action import EmdCopyTagAction
from beetsplug.emd.command.actions.delete_action import EmdDeleteTagAction
from beetsplug.emd.command.actions.rename_action import EmdRenameTagAction
from beetsplug.emd.command.actions.show_action import EmdShowMetadataAction
from beetsplug.emd.command.actions.update_action import EmdUpdateTagAction


class CustomOptionParser(OptionParser):
    def __init__(self, **kwargs):
        super(CustomOptionParser, self).__init__(**kwargs)
        self.set_usage('beet emd <query> [options]')

    def _process_args(self, largs, rargs, values):
        try:
            super(CustomOptionParser, self)._process_args(largs, rargs, values)
        except BadOptionError:
            self.print_help()
            self.exit(0)


class ExtendedMetaDataCommand(Subcommand):
    confirmation_action = EmdConfirmationAction()

    update_action = EmdUpdateTagAction()
    rename_action = EmdRenameTagAction()
    add_action = EmdAddTagAction()
    copy_action = EmdCopyTagAction()
    delete_action = EmdDeleteTagAction()
    show_action = EmdShowMetadataAction()

    emd_command_item_actions = [update_action, rename_action, add_action, copy_action, delete_action, show_action]
    emd_command_actions = [confirmation_action, *emd_command_item_actions]

    def __init__(self, input_field):
        super(ExtendedMetaDataCommand, self).__init__('emd', help=u'manage extended meta data', parser=CustomOptionParser())

        self.input_field = input_field

        for option in self.emd_command_actions:
            option.add_parser_option(self.parser)

        self.func = self.handle_command

    def handle_command(self, lib, opts, args):
        for option in self.emd_command_actions:
            option.apply_option_values(getattr(opts, option.parser_destination()), lib)

        query = self._build_query(args)

        if not query or not self._actions_are_valid():
            self.parser.print_help()
            return

        items = lib.items(query)

        if len(items) == 0:
            print(f"No items found matching query '{query}'")
            return

        if self.confirmation_action.is_confirmed(items, self.emd_command_item_actions):
            self._apply_actions(items)

    def _build_query(self, args):
        return ' '.join([f'"{arg}"' for arg in args]).rstrip()

    def _apply_actions(self, items):
        for item in items:
            print(item)

            old_tags = dict(item).copy()
            emd = self._get_emd(item)

            for option in self.emd_command_item_actions:
                option.apply_to_item(item=item, emd=emd)

            self._update_emd(item, emd)
            new_tags = dict(item)

            if old_tags == new_tags:
                continue

            item.write()
            item.store()

    def _actions_are_valid(self):
        return len([a for a in self.emd_command_item_actions if a.is_applicable()])

    def _get_emd(self, item):
        raw_emd = item[self.input_field]
        emd = ExtendedMetaData.decode(raw_emd)

        if not emd:
            emd = ExtendedMetaData()

        return emd

    def _update_emd(self, item, emd):
        updated_emd = emd.encode()
        item[self.input_field] = updated_emd
