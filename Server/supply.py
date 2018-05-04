import importlib
class Supply():
    def __init__(self,configure_board=None):
        self.card_dict = {}
        if configure_board:
            for card_name, quantity in configure_board:
                card = self.__create_card_from_supply__(card_name)
                if card:
                    self.card_dict[card_name.lower()] = [card,quantity]

    def decrease_stock(self,card_name,number=1):
        if self.card_availible(card_name):
            self.card_dict[card_name.lower()][1] -= number
            return True
        else:
            return False

    def __create_card_from_supply__(self,card_name):
        card_name = card_name.capitalize()
        try:
            my_class = getattr(importlib.import_module("CardDefinitions.{}".format(card_name)),card_name)
            instance = my_class()
            return instance
        except ModuleNotFoundError:
            return None

    def card_availible(self,card_name):
        if self.get_quantity(card_name) > 0:
            return True
        return False

    def get_quantity(self,card_name):
        card = self.card_dict.get(card_name.lower(),None)
        if card:
            return card[1]
        return None

    def get_card(self,card_name):
        card =self.card_dict.get(card_name.lower(),None)
        if card:
            return card[0]
        return None

    def show_supply(self):
        header = ["Current Supply:"] + ["{:10}{:4}{:4}".format("Name","Cost","Supply")]
        supply_info = ["{:10}{:4}{:4}".format(card_name.capitalize(),card[0].cost,card[1]) for card_name,card in self.card_dict.items() if self.card_availible(card_name)]
        supply_string = '\n'.join(header+supply_info)
        return supply_string

    def show_cards(self,card_type=None,max_cost=100):
        return "\n".join(card_name for card_name,card in self.card_dict.items() if (not card_type or card_type in card[0].card_types) and card[0].cost <= max_cost)

    def get_potential_purchases(self,card_type=None,max_cost=100):
        return "\n".join(card_name for card_name,card in self.card_dict.items() if self.card_availible(card_name) and (not card_type or card_type in card[0].card_types) and card[0].cost <= max_cost)

    def count_empty_piles(self):
        return sum([True for card_name,card in self.card_dict.items() if card[1] == 0])
