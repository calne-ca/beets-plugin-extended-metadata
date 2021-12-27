from beetsplug.emd.command.action import EmdCommandAction


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
