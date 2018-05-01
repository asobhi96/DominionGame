import importlib
class Supply():
    def __init__(self,configure_board=None):
        self.card_list = []
        self.card_supply_dict = {}
        self.card_cost_dict = {}
        if configure_board:
            for card_name, cost, quantity in configure_board:
                self.card_supply_dict[card_name] = quantity
                self.card_cost_dict[card_name] = cost
                self.card_list.append(card_name)

    def decrease_stock(self,card_name,number=1):
        if self.card_availible(card_name):
            self.card_supply_dict[card_name.lower()] -= number
        else:
            print("Card out of stock")

    def create_card_from_supply(self,card_name):
        card_name = card_name.capitalize()
        try:
            my_class = getattr(importlib.import_module("CardDefinitions.{}".format(card_name)),card_name)
            instance = my_class()
            return instance
        except ModuleNotFoundError:
            print("Card not found in supply")
            return None

    def card_availible(self,card_name):
        if self.card_supply_dict[card_name.lower()] > 0:
            return True
        return False

    def show_supply(self):
        print("Current Supply:\n")
        print("{:10}{:4}{:4}\n".format("Name","Cost","Supply"))
        for card,supply in self.card_supply_dict.items():
            if self.card_availible(card):
                print("{:10}{:4}{:4}".format(card.capitalize(),self.card_cost_dict[card],supply))

    def get_potential_purchases(self,max_cost):
        result = []
        for card,supply in self.card_supply_dict.items():
            if self.card_availible(card) and self.card_cost_dict[card] <= max_cost:
                result.append(card)
        return result

    def count_empty_piles(self):
        return sum([True for card,supply in self.card_supply_dict.items() if supply == 0])
