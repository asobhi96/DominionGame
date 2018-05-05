from random import shuffle
from supply import Supply
class Player:
    def __init__(self,id,name,game,connection):
        self.id = id
        self.name = name
        self.connection = connection
        self.hand = []
        self.deck = []
        self.discard = []
        self.play_area = []
        self.money = 0
        self.victory_points = 0
        self.actions = 1
        self.buys = 1
        self.is_safe = False #for attacking/reacting
        self.game = game
        self.supply = game.supply
        self.next_hand_size = 5

    def calculate_money(self):
        return self.money

    def draw(self,number_to_draw=1):
        for card_to_draw in range(number_to_draw):
            if len(self.deck) == 0:
                self.repopulate_deck_form_discard()
            card = self.deck.pop()
            self.hand.append(card)

    def shuffle_deck(self):
        shuffle(self.deck)

    def repopulate_deck_form_discard(self):
        self.deck.extend(self.discard)
        self.discard.clear()
        self.shuffle_deck()

    def discard_from_hand(self,card):
        self.hand.remove(card)
        self.discard.append(card)

    def move_card_to_play_area(self,card):
        self.hand.remove(card)
        self.play_area.append(card)

    def play_card(self,card):
        if card.is_playable():
            if 'action' in card.card_types:
                self.actions -= 1
            self.move_card_to_play_area(card)
            card.play(self)
            return True
        return False

    def buy(self,card_to_buy):
            self.buys -= 1
            self.money -= card_to_buy.cost
            self.gain_card(card_to_buy.card_name.lower())

    def show_cards(self,card_list,card_type=None,max_cost = 100):
        return "\n".join([card for card in card_list if (not card_type or card_type in card.card_types) and card.cost <= max_cost])

    def show_card_names(self,card_list):
        return "\n".join([card.card_name for card in card_list])

    def show_hand(self,card_type=None,max_cost=100):
        return '\n'.join([card.card_name for card in self.hand if (not card_type or card_type in card.card_types) and card.cost <= max_cost])

    def find_card_from_hand(self,card_name):
        for card in self.hand:
            if card == card_name:
                return card
        return None

    def gain_card(self,card_name):
        self.supply.decrease_stock(card_name,1)
        new_card = self.supply.get_card(card_name)
        self.discard.append(new_card)

    def reveal(self,card_name):
        card = self.find_card_from_hand(card_name)
        if card:
            return "{} reveals {}\n".format(self.name,card.card_name)

    def clean_up(self):
        self.discard_entire_play_area()
        self.discard_entire_hand()
        self.draw(number_to_draw=self.next_hand_size)
        self.buys = 1
        self.money = 0
        self.actions = 1
        self.is_safe = False
        self.next_hand_size = 5

    def discard_entire_hand(self):
        self.discard.extend(self.hand)
        self.hand .clear()

    def discard_entire_play_area(self):
        self.discard.extend(self.play_area)
        self.play_area.clear()

    def add_to_deck(self,card_name,quantity):
        card = self.supply.get_card(card_name)
        self.deck.extend(quantity * [card])

    def trash_from_hand(self,card):
        self.hand.remove(card)

    def type_in_hand(self,card_type):
        for card in self.hand:
            if card_type in card.card_types:
                return True
        return False

    def  __str__(self):
        return """
        Player ID    :{}
        Money        :{}
        Actions      :{}
        Buys         :{}
        """.format(self.id,self.money,self.actions,self.buys)
