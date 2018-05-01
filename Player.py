from random import shuffle
from Supply import Supply
class Player:
    def __init__(self,id,name,game):
        self.id = id
        self.name = name
        self.hand = []
        self.deck = []
        self.discard = []
        self.money = 0
        self.victory_points = 0
        self.actions = 1
        self.buys = 1
        self.is_safe = False #for attacking/reacting
        self.game = game
        self.supply = game.supply
        self.next_hand_size = 5

    def calculate_money(self):
        return self.money + sum([card.value for card in self.hand])

    def draw(self,number_to_draw=1):
        for card_to_draw in range(number_to_draw):
            if len(self.deck) == 0:
                self.repopulate_deck_form_discard()
            card = self.deck.pop()
            self.hand.append(card)

    def repopulate_deck_form_discard(self):
        shuffle(self.discard)
        self.deck.extend(self.discard)
        self.discard = []

    def select_card_from_supply(self,card_type=None,max_cost=100):
        card_name = input("Enter the name of the card you want to select").lower()
        card = self.supply.create_card_from_supply(card_name)
        while card is None or card.cost > max_cost or (card_type and card_type not in card.card_types):
            card_name = input("Enter the name of the card you want to select").lower()
            card = self.game.supply.create_card_from_supply(card_name)
        return card

    def select_card_from_hand(self,card_type=None,max_cost=100):
        card_name = input("Enter the name of the card you want to select").lower()
        card = self.find_card_from_hand(card_name) #could be simpler maybe, do a list lookup
        while card is None or card.cost > max_cost or (card_type and card_type not in card.card_types):
            print("Either card not found or card is not specificed type")
            card_name = input("Enter the name of the card you want to select").lower()
            card = self.find_card_from_hand(card_name)
        return card

    def choose_card_to_discard(self):
        card = self.select_card_from_hand()
        self.discard_from_hand(card)

    def discard_from_hand(self,card):
        self.hand.remove(card)
        self.discard.append(card)

    def play_card(self,card):
        if card.is_playable():
            self.actions -= 1
            self.discard_from_hand(card)
            print(card.text)
            card.play(self)
            return True
        return False

    def buy_card(self):
        if self.buys >= 1:
            total_money = self.calculate_money()
            print("Player has {} dollars\n".format(total_money))
            potential_purchases = self.supply.get_potential_purchases(max_cost=total_money)
            self.show_cards(potential_purchases)
            card = self.select_card_from_supply(max_cost=total_money)
            self.buy(card)
            return True
        else:
            return False
    def buy(self,card_to_buy):
            self.buys -= 1
            self.money -= card_to_buy.cost
            self.gain_card(card_to_buy.card_name.lower())

    def show_cards(self,card_list):
        for card in card_list:
            print(card)

    def show_hand(self,card_type=None,max_cost=100):
        for card in self.hand:
            if (not card_type or card_type in card.card_types) and card.cost <= max_cost:
                print(card)

    def find_card_from_hand(self,card_name):
        for card in self.hand:
            if card == card_name:
                return card
        print("card not in hand")
        return None

    def gain_card(self,card_name):
        self.supply.decrease_stock(card_name,1)
        new_card = self.supply.create_card_from_supply(card_name)
        self.discard.append(new_card)

    def prompt_reaction(self):
        for card in self.hand:
            if 'reaction' in card.card_types:
                prompt = input("Enter yes to react with card: {}".format(card.card_name))
                if prompt == 'yes':
                    card.react()

    def reveal(self,card_name):
        card = self.find_card_from_hand(card_name)
        if card:
            print("{} reveals {}\n".format(self.name,card.card_name))

    def clean_up(self):
        self.discard_entire_hand()
        self.draw(number_to_draw=self.next_hand_size)
        self.buys = 1
        self.money = 0
        self.actions = 1
        self.is_safe = False
        self.next_hand_size = 5

    def discard_entire_hand(self):
        self.discard.extend(self.hand)
        self.hand = []

    def choose_and_play_action(self):
        if self.actions < 1 or not self.action_in_hand():
            print("Cannot play actions")
            return False
        self.show_hand(card_type='action')
        card = self.select_card_from_hand(card_type='action')
        self.play_card(card)

    def add_to_deck(self,card_name,quantity):
        card = self.supply.create_card_from_supply(card_name)
        self.deck.extend(quantity * [card])

    def shuffle_deck(self):
        shuffle(self.deck)

    def trash_from_hand(self,card):
        self.hand.remove(card)

    def examine_card(self):
        card = self.select_card_from_supply()
        print(card)

    def action_in_hand(self):
        for card in self.hand:
            if 'action' in card.card_types:
                return True
        return False
    def  __str__(self):
        return """
        Player ID    :{}
        Money        :{}
        Actions      :{}
        Buys         :{}
        """.format(self.id,self.calculate_money(),self.actions,self.buys)
