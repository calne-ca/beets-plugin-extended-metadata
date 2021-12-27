from abc import ABC, abstractmethod


class EmdCommandAction(ABC):

    @abstractmethod
    def add_parser_option(self, parser):
        pass

    @abstractmethod
    def parser_destination(self):
        pass

    @abstractmethod
    def apply_option_values(self, opt_values, beets_lib):
        pass


class EmdCommandItemAction(EmdCommandAction):
    def __init__(self, needs_confirmation):
        self.needs_confirmation = needs_confirmation

    @abstractmethod
    def apply_to_item(self, item, emd):
        pass

    @abstractmethod
    def is_applicable(self):
        pass

    @abstractmethod
    def action_description(self):
        pass
