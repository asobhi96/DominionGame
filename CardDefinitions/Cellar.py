from CardDefinitions.Card import Card
from communication import read_message, send_input_command, send_print_command, send_end_command

class Cellar(Card):
    def __init__(self):
        super().__init__()
        self.card_name = "Cellar"
        self.card_types = ['action']
        self.cost = 2
        self.text = """
        +1 Action
        Discard any number of cards, then draw that many.
        """
    def play(self,player):
        player.actions += 1
        while True:
            send_print_command("How many cards do you wish to discard?",player.connection)
            send_input_command(player.connection)
            number_of_cards_to_discard =  read_message(player.connection)
            if number_of_cards_to_discard.isdigit() and int(number_of_cards_to_discard) >= 0 and int(number_of_cards_to_discard) <= len(player.hand):
                number_of_cards_to_discard = int(number_of_cards_to_discard)
                break
        for _ in range(number_of_cards_to_discard):
            while True:
                send_print_command(player.show_hand(),player.connection)
                send_print_command("Enter name of card you wish to discard",player.connection)
                send_input_command(player.connection)
                card_name = read_message(player.connection)
                card = player.find_card_from_hand(card_name)
                if card:
                    break
            player.discard_from_hand(card)
        player.draw(number_to_draw=number_of_cards_to_discard)
        send_end_command(player.connection)
