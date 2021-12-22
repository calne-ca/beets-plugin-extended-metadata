from beets.ui import Subcommand

from beetsplug.emd_metadata import ExtendedMetaData
from beetsplug.emd_command_actions import EmdAddTagAction, EmdDeleteTagAction, EmdUpdateTagAction, EmdRenameTagAction, \
    EmdShowMetadataAction, EmdConfirmationAction, EmdQueryAction


class ExtendedMetaDataCommand(Subcommand):
    query_action = EmdQueryAction()
    confirmation_action = EmdConfirmationAction()

    update_action = EmdUpdateTagAction()
    rename_action = EmdRenameTagAction()
    add_action = EmdAddTagAction()
    delete_action = EmdDeleteTagAction()
    show_action = EmdShowMetadataAction()

    emd_command_item_actions = [update_action, rename_action, add_action, delete_action, show_action]
    emd_command_actions = [query_action, confirmation_action, *emd_command_item_actions]

    def __init__(self, input_field):
        super(ExtendedMetaDataCommand, self).__init__('emd', help=u'manage extended meta data')

        self.input_field = input_field

        for option in self.emd_command_actions:
            option.add_parser_option(self.parser)

        self.func = self.handle_command

    def handle_command(self, lib, opts, _):
        for option in self.emd_command_actions:
            option.apply_option_values(getattr(opts, option.parser_destination()), lib)

        if not self._actions_are_valid():
            self.parser.print_help()
            return

        items = self.query_action.items

        if len(items) == 0:
            print(f"No items found matching query '{self.query_action.query}'")
            return

        if self.confirmation_action.is_confirmed(items, self.emd_command_item_actions):
            self._apply_actions(items)

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
        if self.query_action.query is None:
            return False

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
