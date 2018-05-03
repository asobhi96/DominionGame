from communication import read_message, send_input_command, send_print_command, send_end_command
from CardDefinitions.Card import Card
class Remodel(Card):
    def __init__(self):
        super().__init__()
        self.card_name = "Remodel"
        self.card_types = ['action']
        self.cost = 4
        self.text = """
        Trash a card from your hand. Gain a card costing up to $2 more than the trashed card.
        """
    def play(self,player):
        while True:
            send_print_command(player.show_hand(),player.connection)
            send_print_command("Choose a card to trash",player.connection)
            send_input_command(player.connection)
            card_name = read_message(player.connection)
            card = player.find_card_from_hand(card_name)
            if card:
                break
        original_cost = card.cost
        player.trash_from_hand(card)
        potential_buys = player.supply.get_potential_purchases(max_cost=original_cost+2)
        while True:
            send_print_command(potential_buys,player.connection)
            send_print_command("Choose a card to gain up to +2 trashed card cost",player.connection)
            send_input_command(player.connection)
            new_card_name = read_message(player.connection).lower()
            if new_card_name in potential_buys:
                player.gain_card(new_card_name.lower())
                send_print_command("Gaining a {}\n".format(new_card_name),player.connection)
                break
        send_end_command(player.connection)
